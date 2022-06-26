<template>
  <div>
    <v-dialog :retain-focus="false" v-model="show_request_anticipation_dialog" max-width="50%" persistent>
      <v-card>
        <!-- Close Butto -->
        <div style="text-align: right;"> 
          <v-icon @click="$emit('close-request-anticipation-dialog')" large class="pt-2 mr-2">mdi-window-close</v-icon >
        </div>
        <v-card-title style="display: flex; justify-content: center; padding-top: 0px" class="mb-2">Request anticipation</v-card-title>
        <form @submit.prevent="requestAnticipation" class="ml-3">
          <div style="display: flex; justify-content: center;">
            <div style="width: 80%">
              <v-row >
                <v-col>
                  <div >
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
                            :value="current_due_date"
                            class="mr-2"
                            outlined
                            dense
                          />
                        </v-col>
                      </v-row>
                      <!-- New Due date -->
                      <v-row>
                        <v-col 
                          class="ml-3"
                          cols="12"
                          sm="7"
                        >
                          <v-text-field
                            required
                            label="New due date"
                            v-model.trim="due_date"
                            class="mr-2"
                            outlined
                            dense
                            persistent-placeholder
                            type="tel"
                            placeholder="mm/dd/yyyy"
                            v-mask="'##/##/####'"
                            @blur="calculateAnticipatedValue"
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
                      <v-row>
                        <v-col 
                          class="ml-3"
                          cols="12"
                          sm="7"
                        >
                          <v-text-field
                            disabled
                            label="New value"
                            :value="calculated_value"
                            class="mr-2"
                            outlined
                            dense
                          />
                        </v-col>
                      </v-row>
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
              @click="$emit('close-request-anticipation-dialog')"
            >Close</v-btn>
          </v-card-actions>
        </form>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import {mask} from 'vue-the-mask'
export default {
  props: ['payment', 'show_request_anticipation_dialog'],
  directives: {mask},
  data() {
    return {
      loading: false,
      due_date: null,
      current_due_date: "",
      calculated_value: 0,
    }
  },

  methods: {
    async requestAnticipation(){
      let data = await this.$store.dispatch("payment/requestAnticipation", {payment_id: this.payment.id, 
        new_due_date: this.fixDate(this.due_date)});
      if (data){
      /** return this.payment.anticipation_due_date && this.payment.anticipation_status === 2 */
        this.payment.anticipation_due_date = data.anticipation_due_date
        this.payment.anticipation_status = 2
        this.$emit('close-request-anticipation-dialog')
      }
    },

    fixDate(value){
      let splited_date = value.split('/')
      let fixed_date = splited_date[2] + '-' + splited_date[0] + '-' + splited_date[1]
      return fixed_date
    },

    getLocaleDate(value){
      if (value){
        return new Date(value).toLocaleDateString('en')
      }
      else {
        return ""
      }
    }, 

    dateIsValid(value){
      if (value){
        if (value.length == 10) return true 
        else return false
      }
      else return false
    },

    calculateAnticipatedValue(){
      if (this.dateIsValid(this.due_date)){
        let [year, month, day] = this.payment.due_date.split('-');
        let current_date = new Date(month + '/' + day.substr(0,2) + '/' + year)  //this.payment.due_date
        let anticipated_date =  new Date(this.due_date) //

        const diffTime = Math.abs(current_date - anticipated_date);
        const days_difference = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 

        let original_value = this.payment.original_value
        console.log(">>>>>>> anticipated_date: ", anticipated_date)
        console.log(">>>>>>> current_date: ", current_date)
        console.log(">>>>>>> new_value: ", this.payment.new_value)
        this.calculated_value = (original_value - (original_value * ( (0.03/30) * (days_difference)))).toFixed(2)
      }
      else {
        this.calculated_value = 0
      }
    }
  },

  computed: {
  },

  mounted(){
    this.current_due_date = this.getLocaleDate(this.payment.due_date)
  }

}
</script>
