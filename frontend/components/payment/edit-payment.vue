<template>
  <div>
    <!-- ========= Edit Order Dialog ============ -->
    <v-dialog :retain-focus="false" v-model="show_edit_dialog" max-width="35%" persistent>
      <v-card>
        <!-- Close Butto -->
        <div style="text-align: right;"> 
          <v-icon @click="$emit('close-edit-dialog')" large class="pt-2 mr-2">mdi-window-close</v-icon >
        </div>
        <v-card-title style="display: flex; justify-content: center; padding-top: 0px" class="mb-2">Edit Payment</v-card-title>
        <form @submit.prevent="updatePayment" class="ml-3">
          <div style="display: flex; justify-content: center;">
            <div style="width: 80%">
              <v-row >
                <v-col>
                    <!-- Current Due date -->
                    <v-row>
                      <v-col 
                        class="ml-3"
                        cols="12"
                        sm="7"
                      >
                        <v-text-field
                          disabled
                          label="Current due date"
                          :value="getLocaleDate(payment.due_date)"
                          class="mr-2"
                          outlined
                          dense
                        />
                      </v-col>
                    </v-row>
                    <!-- New Due date requested -->
                    <v-row v-if="payment.anticipation_due_date && payment.anticipation_status === 2">
                      <v-col 
                        class="ml-3"
                        cols="12"
                        sm="7"
                      >
                        <v-text-field
                          disabled
                          label="Requested due date"
                          :value="getLocaleDate(payment.anticipation_due_date)"
                          class="mr-2"
                          outlined
                          dense
                        />
                      </v-col>
                    </v-row>
                    <!-- Payment original value -->
                    <v-row>
                      <v-col 
                        class="ml-3"
                        cols="12"
                        sm="7"
                      >
                        <v-text-field
                          disabled
                          label="Original value"
                          :value="payment.original_value"
                          class="mr-2"
                          outlined
                          dense
                        />
                      </v-col>
                    </v-row>
                    <!-- Payment new value -->
                    <v-row v-if="payment.anticipation_due_date">
                      <v-col 
                        class="ml-3"
                        cols="12"
                        sm="7"
                      >
                        <v-text-field
                          disabled
                          label="New value"
                          :value="payment.new_value ? payment.new_value : calculated_value"
                          class="mr-2"
                          outlined
                          dense
                        />
                      </v-col>
                    </v-row>
                    <!-- Payment anticipation status -->
                    <div>
                      <v-select
                        v-model="anticipation_status"
                        label="Anticipation status"
                        :items="status_options"
                        :item-text="(x) => x.description"
                        return-object
                      ></v-select>
                    </div>

                </v-col>
              </v-row>
            </div>
          </div>
          <!-- Submit Form -->
          <v-card-actions>
            <!-- Submit -->
            <v-spacer />
            <v-btn
              class="blue--text darken-1"
              type="submit"
              text
              :loading="loading"
              :disabled="loading"
            >Save</v-btn>
            <v-btn 
              class="black--text darken-1" 
              text 
              @click="$emit('close-edit-dialog')"
            >Close</v-btn>
          </v-card-actions>
        </form>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  props: ['payment', 'show_edit_dialog'],
  data() {
    return {
      loading: false,
      status_options: [
        {description: 'Available', value: 1},
        {description: 'Waiting confirmation', value: 2},
        {description: 'Anticipated', value: 3},
        {description: 'Unavailable', value: 4},
        {description: 'Denied', value: 5},
      ],
      anticipation_status: null,
      calculated_value: 0,
    }
  },

  methods: {
    // Save Orders
    async updatePayment(){
      this.loading = true
      let payload = {
        id: this.payment.id,
        anticipation_status: this.anticipation_status.value,
      }
      let response = await this.$store.dispatch("payment/updatePayment", payload)
      if (response == 'ok') {
        if (this.payment.anticipation_status === 2 && this.anticipation_status.value === 3){
          this.payment.due_date = this.payment.anticipation_due_date
          this.payment.new_value = this.calculated_value
        }
        this.payment.anticipation_status = this.anticipation_status.value
        this.$emit('close-edit-dialog')
      }
      this.loading = false;
    },

    getLocaleDate(value){
      if (value){
        return new Date(value).toLocaleDateString('en')
      }
      else {
        return ""
      }
    }, 
    
    calculateAnticipatedValue(){
      let [year, month, day] = this.payment.due_date.split('-');
      let current_date = new Date(month + '/' + day.substr(0,2) + '/' + year)  //this.payment.due_date
      let [year2, month2, day2] = this.payment.anticipation_due_date.split('-');
      let anticipated_date =  new Date(month2 + '/' + day2.substr(0,2) + '/' + year2)

      const diffTime = Math.abs(current_date - anticipated_date);
      const days_difference = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 

      let original_value = this.payment.original_value
      console.log(">>>>>>> anticipated_date: ", anticipated_date)
      console.log(">>>>>>> current_date: ", current_date)
      console.log(">>>>>>> new_value: ", this.payment.new_value)
      this.calculated_value = (original_value - (original_value * ( (0.03/30) * (days_difference)))).toFixed(2)
    }
  },

  /** computed:{ */
    /** showNewDueDate(){ */
      /** return this.payment.anticipation_due_date && this.payment.anticipation_status === 2 */
    /** } */
  /** }, */

  mounted(){
    this.anticipation_status = this.status_options.find(el=>el.value === this.payment.anticipation_status)
    if (this.payment.anticipation_due_date){
      this.calculateAnticipatedValue()
    }
  },

	watch: {
		show_edit_dialog(newvalue, oldValue) {
			if (newvalue === true){
        if (this.payment.anticipation_status != this.anticipation_status){
          this.anticipation_status = this.status_options.find(el=>el.value === this.payment.anticipation_status)
        }
        if (this.payment.anticipation_due_date){
          this.calculateAnticipatedValue()
        }
			}

		}
	},

}
</script>
