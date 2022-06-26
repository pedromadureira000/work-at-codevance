<template>
  <div>
    <dots-menu :menu_items="menu_items" :handleClick="handleClick"/>
    <edit-payment 
      :payment="payment" 
      :show_edit_dialog="show_edit_dialog"
      @close-edit-dialog="show_edit_dialog = false"
    />
    <payment-history 
      :payment="payment" 
      :show_payment_history_dialog="show_payment_history_dialog"
      @close-history-dialog="show_payment_history_dialog = false"
    />
    <request-anticipation
      :payment="payment" 
      :show_request_anticipation_dialog="show_request_anticipation_dialog"
      @close-request-anticipation-dialog="show_request_anticipation_dialog = false"
    />

  </div>
</template>

<script>
export default {
  components: {
    "dots-menu": require("@/components/dots-menu.vue").default,
    "edit-payment": require("@/components/payment/edit-payment.vue").default,
    "payment-history": require("@/components/payment/payment-history.vue").default,
    "request-anticipation": require("@/components/payment/request-anticipation.vue").default,
  },
  props: ['payment'],
  data() {
    return {
      show_payment_history_dialog: false,
      show_edit_dialog: false,
      show_request_anticipation_dialog: false,
      loading: false,
    }
  },

    methods: {
      handleClick(index){
        //this.menu_items[id].click()  #will get errors because the function click will not access properties with its own 'this'
        this.menu_items[index].click.call(this) // will call the function but the function will use the vue instance 'this' context.
      },

      // Permission Functions
      hasUpdatePaymentPermission(){
        let user = this.$store.state.user.currentUser;
        return user.permissions.includes("update_payment")
      },
    },

    computed:{
      menu_items(){
        return [
        ...(this.hasUpdatePaymentPermission() ? [{ 
            title: 'Edit',
            icon: 'mdi-pencil',
            async click(){
              this.show_edit_dialog = true
            }
          }] : [] ),
        ...([{ 
            title: 'Payment History',
            icon: 'mdi-clipboard-text-clock',
            async click(){
              this.show_payment_history_dialog = true
            }
          }]),
        ...(this.requestAnticipationEnabled ? [{
            title: 'Request Anticipation',
            /** icon: 'mdi-cash-clock', TODO why this icon is not working?*/
            icon: 'mdi-cash',
            async click(){
              this.show_request_anticipation_dialog = true
            }
          }] : [] ),
        ]
      }, 

      requestAnticipationEnabled(){
        let user = this.$store.state.user.currentUser;
        return user.permissions.includes("request_payment_anticipation") && this.payment.anticipation_status === 1
      },
    },
}
</script>
