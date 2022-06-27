import {Commit, Dispatch} from "vuex"
//Organization
let supplier_company = ['company_name', 'cnpj']

// User
let user_fields = ['username', 'email', 'password', 'supplier_company']

// Payment
let payment_fields = ['id', 'operator', 'anticipation_due_date', 'anticipation_status','issuance_date','due_date', 'original_value', 'new_value']
let payment_history_fields = ['payment', 'user', 'history_type', 'history_description', 'date' ]

// field_list
let field_list = supplier_company.concat(user_fields, payment_fields, payment_history_fields)

export const doesHttpOnlyCookieExist = (cookiename: string): boolean => {
	var d = new Date();
	d.setTime(d.getTime() + (1000));
	var expires = "expires=" + d.toUTCString();
	document.cookie = cookiename + "=new_value;path=/;" + expires;
	return document.cookie.indexOf(cookiename + '=') == -1;
}

export const setCookie = (name: string, value: string, days: number) => {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

export const getCookie = (name: string) => {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

export const eraseCookie = (name: string) => {   
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

export const ErrorHandler = (error: any, commit: Commit, dispatch: Dispatch, i18n: any, 
                            default_error_msg: any = i18n.t('Something_went_wrong')  ) => { 
  // error.response.data = null  // <<- this line is for test some errors
  // -----------/ Time-out Error
  if (error.message == 'timeout of 15000ms exceeded'){
    dispatch("setAlert", {message: i18n.t("Request_Time_out"), alertType: "error"}, { root: true })
  } 
  else if (error.response && error.response.data){
    let response = error.response
    let first_key = Object.keys(error.response.data)[0]
    // 500 Server Error
    if (response.status === 500){
        dispatch("setAlert", {message: i18n.t("Server_error"), alertType: "error"}, { root: true })
    }
    // -- DRF Fields
    else if (first_key){
      // 'detail' DRF Errors
      if (first_key == 'detail'){
        let errorMessage = response.data[first_key]
        dispatch("setAlert", {message: errorMessage , alertType: "error"}, { root: true })
      }
      // 'non_field_errors' and 'error'
      else if (first_key == 'non_field_errors' || first_key == 'error') {
        let errorMessage = response.data[first_key][0]
        dispatch("setAlert", {message: errorMessage , alertType: "error"}, { root: true })
      }
      // DRF Normal Field Errors
      else if (field_list.includes(first_key)){
        let errorMessage = response.data[first_key][0]
        // Translation Workaround (XXX Gambiarra)
        if (errorMessage.includes('is not valid cnpj')){
          errorMessage = errorMessage.replace('is not valid cnpj', 'não é um CNPJ valido')
        } 
        //
        dispatch("setAlert", {message: i18n.t(first_key.substring(0,1).toUpperCase() + first_key.substring(1)) + ": " + errorMessage , 
                 alertType: "error"}, { root: true })
      }
      else {
        dispatch("setAlert", {message: default_error_msg, alertType: "error"}, { root: true })
      }
    }
    // Default Error
    else {
      dispatch("setAlert", {message: default_error_msg, alertType: "error"}, { root: true })
    }
  } 
  else {
    dispatch("setAlert", {message: default_error_msg, alertType: "error"}, { root: true })
  }
}
