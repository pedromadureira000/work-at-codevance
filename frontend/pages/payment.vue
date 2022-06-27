<template>
  <p v-if="$fetchState.pending">{{$t('Fetching_data')}}</p>
  <p v-else-if="$fetchState.error">{{$t('Error_fetching_data')}}</p>
  <div v-else>
    <div class="ma-3">
      <v-expansion-panels v-if="hasCreatePaymentPermission">
      <!-- <v-expansion-panels> -->
        <v-expansion-panel>
          <v-expansion-panel-header>
            <h3>Create Payment</h3>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <form @submit.prevent="createPayment">
              <!-- Supplier Company -->
              <v-row align="center">
                <v-col
                  class="d-flex"
                  cols="12"
                  sm="3"
                >
                  <v-select
                    v-model="supplier_company"
                    label="Supplier Company"
                    :items="supplier_companies"
                    :item-text="(x) => x.company_name + ' (' + x.cnpj +')'"
                    return-object
                  ></v-select>
                </v-col>
              </v-row>
              <!-- Due date -->
              <v-row>
                <v-col 
                  class="ml-3"
                  cols="12"
                  sm="3"
                >
                  <v-text-field
                    label="Due date"
                    v-model.trim="due_date"
                    class="mr-2"
                    outlined
                    dense
                    persistent-placeholder
                    type="tel"
                    placeholder="mm/dd/yyyy"
                    v-mask="'##/##/####'"
                  />
                </v-col>
              </v-row>
              <!-- Original value -->
              <v-row>
                <v-col 
                  class="ml-3"
                  cols="12"
                  sm="3"
                >
                  <v-text-field
                    label="Original value"
                    v-model="original_value"
                    @blur="$v.original_value.$touch()"
                    :error-messages="originalValueErrors"
                    type="number"
                    step="0.01"
                    min="0.01"
                    max="999999999.99"
                  ></v-text-field>
                </v-col>
              </v-row>
              <!-- Submit Button -->
              <v-btn
                class="mt-4"
                color="primary"
                type="submit"
                :loading="loading"
                :disabled="loading"
                >Submit</v-btn
              >
            </form>

          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>

      <h3 class="mt-6">View payments</h3>
      <div>
        <!-- Search bar -->
        <v-card-text class="mt-3">
          <v-container fluid>
            <v-row no-gutters>
              <!-- Anticipation status -->
              <v-col
                class="d-flex"
                cols="2"
              >
                <v-select
                  v-model="anticipation_status_filter"
                  label="Status"
                  :items="status_options"
                  :item-text="(x) => x.description"
                  :item-value="(x) => x.value"
                ></v-select>
              </v-col>
              <!-- Submit -->
              <v-col cols="2" style="display: flex; justify-content: center;">
                <v-btn
                  class="mt-3 mr-0 ml-0"
                  color="primary"
                  :loading="loading_items"
                  :disabled="loading_items"
                  @click="searchPayments()"
                >Search</v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-data-table
          :headers="headers"
          :items="payments"
          :items-per-page="10"
          item-key="id"
          class="elevation-1 mt-3"
        >
          <template v-slot:item.supplier_company="{ item }">
            <p>{{supplier_companies.find(el=>el.id===item.supplier_company).company_name}}</p>
          </template>
          <template v-slot:item.issuance_date="{ item }">
            <p>{{getLocaleDate(item.issuance_date)}}</p> 
          </template>
          <template v-slot:item.due_date="{ item }">
            <p>{{getLocaleDate(item.due_date)}}</p> 
          </template>
          <template v-slot:item.original_value="{ item }">
            <p>{{getRealMask(Number(item.original_value))}}</p>
          </template>
          <template v-slot:item.new_value="{ item }">
            <p>{{item.new_value ? getRealMask(Number(item.new_value)) : ''}}</p>
          </template>
          <template v-slot:item.anticipation_status="{ item }">
            <p>{{status_options.find(el=>el.value === item.anticipation_status).description}}</p>
          </template>
          <template v-slot:item.actions="{ item }">
            <payment-actions-menu
              :payment="item" 
            />
          </template>
        </v-data-table>
      </div>
    </div>
  </div>
</template>

<script>
import {
  minValue,
  maxValue,
} from "vuelidate/lib/validators";
import { validationMixin } from "vuelidate";
import {mask} from 'vue-the-mask'

export default {
  middleware: ["authenticated"],
  components: {
    "payment-actions-menu": require("@/components/payment/payment-actions-menu.vue").default,
  },
  mixins: [validationMixin],
  directives: {mask},

  data() {
    return {
      // Fields
      supplier_company: null,
      due_date: "",
      original_value: 0,
      supplier_companies: [],
      //
      status_options: [
        {description: 'All', value: null},
        {description: 'Available', value: 1},
        {description: 'Waiting confirmation', value: 2},
        {description: 'Anticipated', value: 3},
        {description: 'Unavailable', value: 4},
        {description: 'Denied', value: 5},
      ],
      anticipation_status_filter: null,
      payments: [],
      loading: false,
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Supplier company', value: 'supplier_company' },
        { text: 'Issuance date', value: 'issuance_date' },
        { text: 'Due date', value: 'due_date' },
        { text: 'Original value', value: 'original_value' },
        { text: 'Anticipated value', value: 'new_value' },
        { text: 'Anticipation status', value: 'anticipation_status' },
        { text: 'Actions', value: 'actions' },
      ],
      loading_items: false
    };
  },

  async fetch() {
    let supplier_companies = await this.$store.dispatch("organization/fetchSupplierCompanies");
    if (supplier_companies){
      this.supplier_companies.push(...supplier_companies)
      this.supplier_company = supplier_companies[0]
    }
  },

  validations: {
    original_value: {
      minValue: minValue(0.01),
      maxValue: maxValue(999999999.99)
    },

    paymentInfoGroup: [
      "original_value",
    ],
  },

  computed: {
    originalValueErrors() {
      const errors = [];
      if (!this.$v.original_value.$dirty) return errors;
      !this.$v.original_value.minValue && errors.push(this.$formatStr(this.$t("This_value_must_be_greater_than_X"),  'R$ 0,00'));
      !this.$v.original_value.maxValue && errors.push(this.$formatStr(this.$t("This_value_must_be_less_than_X"), 'R$ 999.999.999,99'));
      return errors;
    },

    // Permissions
    hasCreatePaymentPermission(){
      let user = this.$store.state.user.currentUser;
      return user.permissions.includes("create_payment")
    },
  },

  methods: {
    async createPayment() {
      this.$v.paymentInfoGroup.$touch();
      if (this.$v.paymentInfoGroup.$invalid) {
        this.$store.dispatch("setAlert", { message: this.$t("Please_fill_the_form_correctly"), alertType: "error" }, { root: true })
      } else {
        this.loading = true;
        let data = await this.$store.dispatch("payment/createPayment", {
          supplier_company: this.supplier_company.id, 
          due_date: this.fixDate(this.due_date), 
          original_value: this.original_value, 
        });
        if (data) {
          this.payments.push(data) 
          this.$v.$reset()
          this.due_date = ""
          this.original_value = 0
        }
        this.loading = false;
      }
    },

    async searchPayments() {
        this.loading_items = true;
        let query_strings = ''
        query_strings += this.anticipation_status_filter ? `anticipation_status=${this.anticipation_status_filter}&` : ''
        if (query_strings !== "") { // remove the last '&' character
          query_strings = query_strings.slice(0, -1) 
        }
        let data = await this.$store.dispatch("payment/fetchPayments", query_strings);
        if (data) {
          /** console.log(">>>>>>> payments", data) */
          this.payments = data
        }
        this.loading_items = false;
    },

    getRealMask(value){
      /** return value.toLocaleString'pt-br',{style: 'currency', currency: 'BRL'}) */
      return value.toLocaleString()
    },

    getLocaleDate(value){
      if (value){
        return new Date(value).toLocaleDateString('en')
      }
      else {
        return ""
      }
    }, 

    fixDate(value){
      let splited_date = value.split('/')
      let fixed_date = splited_date[2] + '-' + splited_date[0] + '-' + splited_date[1]
      return fixed_date
    },
  },

};
</script>
<style scoped>
.v-application .mb-3 {
  margin-bottom: 0px !important;
}
</style>
