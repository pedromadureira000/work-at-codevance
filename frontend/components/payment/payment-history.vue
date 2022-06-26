<template>
  <div v-if="payment_history_fetched">
    <v-dialog :retain-focus="false" :value="show_payment_history_dialog" max-width="90%" persistent>
      <v-card class="pa-3">
        <!-- Close Butto -->
        <div style="text-align: right;"> 
          <v-icon @click="$emit('close-history-dialog')" large class="pt-2 mr-2">mdi-window-close</v-icon >
        </div>
          <!-- Payment History -->
        <h1>Payment History</h1>
        <div v-if="payment_history.length > 0">
          <v-data-table
            :headers="headers"
            :items="payment_history"
            class="elevation-1"
            sort-by="date"
            item-key="id"
            :items-per-page='-1'
          >
            <template v-slot:item.date="{ item }">
              <p>{{getLocaleDateAndTime(item.date)}}</p>
            </template>
            <template v-slot:item.user="{ item }">
              <p>{{item.user}}</p>
            </template>
            <template v-slot:item.history_type="{ item }">
              <p>{{history_type_options.find(el=>el.value===item.history_type).description}}</p>
            </template>
            <template v-slot:item.history_description="{ item }">
              <p
                v-for="(text, index) in parseHistoryDescription(item.history_description)"  
                :key="index"
                style="margin-bottom: 3px;"
              >
                <span v-if="text">{{text}}</span>
              </p>
            </template>
          </v-data-table>
        </div>
        </v-row>
        <v-card-actions>
          <v-spacer />
          <v-btn class="black--text darken-1" text @click="$emit('close-history-dialog')">Close</v-btn>
        </v-card-actions>
      </v-card>

    </v-dialog>
  </div>
</template>

<script>
import { validationMixin } from "vuelidate"

export default {
  mixins: [validationMixin],
  props: ['payment', 'show_payment_history_dialog'],
  data() {
    return {
      loading: false,
      payment_history: [],
      payment_history_fetched: false,
      history_type_options: [
        {description: 'Inclusion', value: 'I'},
        {description: 'Alteration', value: 'A'},
      ],
      headers: [
        { text: 'Date', value: 'date', sortable: true },
        { text: 'User', value: 'user', sortable: true },
        { text: 'History type', value: 'history_type', sortable: true },
        { text: 'History description', value: 'history_description', sortable: true },
      ],
    }
  },

  methods: {
    // Fetch payment history
    async fetchPaymentHistory(){
      let payment_history = await this.$store.dispatch("payment/fetchPaymentHistory", this.payment.id);
      if (payment_history){
        this.payment_history = payment_history
        this.payment_history_fetched = true
      }
    },

    parseHistoryDescription(text){
      let parsed_text = text.split('\n') 
      /** console.log(">>>>>>> parsed_text>>>>: ", parsed_text) */
      return parsed_text
    },

    getLocaleDateAndTime(value){
      if (value){
        return new Date(value).toLocaleDateString('en') + ' - ' + new Date(value).toLocaleTimeString('en') 
      }else{
        return ''
      }
    },
  },
 
  watch: {
    show_payment_history_dialog(newValue){
      if (newValue === true && this.payment_history.length === 0) {
        this.fetchPaymentHistory()
      } 
    }	
  },

}
</script>
