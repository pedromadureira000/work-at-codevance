import {ErrorHandler} from "~/helpers/functions";
import {ActionTree, Commit, Dispatch} from "vuex"
import {RootState} from "@/store/index"
 // @ts-ignore: This module is dynamically added in nuxt.config.js
import api from "~api"

// ------------------------------------------/ACTIONS/-------------------------------------------
interface PaymentState {
  test: boolean
}

export const state = (): PaymentState => ({
  test: true
})  

export const actions: ActionTree<PaymentState, RootState> = {

	async createPayment({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, payload: any){
		try {
			let data = await api.createPayment(payload)
			dispatch("setAlert", {message: this.app.i18n.t('createPayment_success_msg'), alertType: "success"}, { root: true })
			return data
		}
		catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("createPayment_error_msg"))
		}
	},

  async fetchPayments({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, query_strings: string){
    try{
      let payments = await api.fetchPayments(query_strings)
      return payments
    }
    catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("fetchPayments_error_msg"))
    }
  },

  async updatePayment({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, payload: any){
    try {
    await api.updatePayment(payload)
    dispatch("setAlert", {message: this.app.i18n.t('updatePayment_success_msg') , alertType: "success"}, { root: true })
    return 'ok'
    }
    catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t('updatePayment_error_msg'))
		}
  },

	// async deletePayment({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, payload: any){
		// try {
			// await api.deletePayment(payload)
			// dispatch("setAlert", {message: this.app.i18n.t('deletePayment_success_msg'), alertType: "success"}, { root: true })
			// return "ok"
		// }
    // catch(error){
      // ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t('deletePayment_error_msg'))
		// }
	// },

  async requestAnticipation({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, payload: any){
    try {
    let data = await api.requestAnticipation(payload)
    dispatch("setAlert", {message: this.app.i18n.t('requestAnticipation_success_msg') , alertType: "success"}, { root: true })
    return data
    }
    catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t('requestAnticipation_error_msg'))
		}
  },

  async fetchPaymentHistory({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, payment_id: string){
    try{
      let payment_history = await api.fetchPaymentHistory(payment_id)
      return payment_history
    }
    catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("fetchPaymentHistory_error_msg"))
    }
  },

}
