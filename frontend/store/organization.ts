import {ErrorHandler} from "~/helpers/functions";
import {ActionTree, Commit, Dispatch} from "vuex"
import {RootState} from "@/store/index"
 // @ts-ignore: This module is dynamically added in nuxt.config.js
import api from "~api"

// ------------------------------------------/ACTIONS/-------------------------------------------

interface OrganizationState {
  test: boolean
}

export const state = (): OrganizationState => ({
  test: true
})  
export const actions: ActionTree<OrganizationState, RootState> = {

  async fetchSupplierCompanies({commit, dispatch}: {commit: Commit, dispatch: Dispatch}){
    try{
      let supplier_companies = await api.fetchSupplierCompanies()
      return supplier_companies
    }
    catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("fetchSupplierCompanies_error_msg"))
    }
  },

}
