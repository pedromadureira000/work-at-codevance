import axios from '~/plugins/axios'

export default {
  // --------------------------------------/ Auth APIs /----------------------------------------
	async checkAuthenticated(){
    return await axios.get("/api/user/own_profile").then((data)=> {return data.data})
	},

	async getCsrf(){
		return await axios.get("/api/user/getcsrf").then(() => {})
	},

	async login(payload){ 
		return await axios({
			method: "post",
			url: "/api/user/login",
			data: { username: payload.username, contracting_code: payload.contracting_code, password: payload.password },
			headers: { "X-CSRFToken": payload.csrftoken },
		})
			.then((response) => {
				return response.data
			})
		},	

	async logout(){
		return await axios({
				method: "post",
				url: "/api/user/logout",
			})
				.then(() => {})
		},

	async updateCurrentUserEmail(new_email){ 
		return await axios({
			method: "put",
			url: "/api/user/own_profile",
			data: { email: new_email },
		})
			.then((response) => {
				return response.data
			})
		},	

  // --------------------------------------/ CRUD Payment APIs /----------------------------------------
  async createPayment(payload){
    let data_body = {
      supplier_company: payload.supplier_company,
      due_date: payload.due_date,
      original_value: payload.original_value,
    }
    return await axios({ 
    method: "post",
    url: "/api/payment/payment",
    data: data_body}).then((request) => {
          return request.data 
        })
  },

  async fetchPayments(query_strings){
    let url =  query_strings ? `/api/payment/payment?${query_strings}` : "/api/payment/payment"
    return await axios({ 
    method: "get",
    url: url,
      }).then((request) => {
          return request.data 
        })
  },

  async updatePayment(payload){
    return await axios({ 
    method: "put",
    url: `/api/payment/payment/${payload.id}`,
    data:{
      anticipation_status: payload.anticipation_status,
    }
      }).then((request) => {
          return request.data 
        })
  },
  
  // async deleteSupplierCompany(payload){
    // return await axios({ 
    // method: "delete",
    // url: `/api/payment/contracting/${payload.contracting_code}`,
      // }).then((request) => {
          // return request.data 
        // })
  // },

  async fetchPaymentHistory(payment_id){
    return await axios({ 
    method: "get",
    url: `/api/payment/payment_history/${payment_id}`,
      }).then((request) => {
          return request.data 
        })
  },

  async requestAnticipation(payload){
    return await axios({ 
    method: "post",
    url: `/api/payment/request_anticipation/${payload.payment_id}`,
    data:{
      anticipation_due_date: payload.new_due_date,
    }
      }).then((request) => {
          return request.data 
        })
  },

 
  // --------------------------------------/ CRUD Organization APIs /----------------------------------------
  
	// async createSupplierCompany(payload){
    // let data_body = {
      // name: payload.name,
      // contracting_code: payload.contracting_code,
      // active_users_limit: payload.active_users_limit,
      // status: payload.status,
      // note: payload.note,
		// }
		// return await axios({ 
		// method: "post",
		// url: "/api/organization/contracting",
		// data: data_body}).then((request) => {
					// return request.data 
				// })
	// },

  async fetchSupplierCompanies(){
    return await axios({ 
    method: "get",
    url: "/api/organization/supplier_company",
      }).then((request) => {
          return request.data 
        })
  },

	// async updateSupplierCompany(payload){
		// return await axios({ 
		// method: "put",
		// url: `/api/organization/contracting/${payload.contracting_code}`,
		// data:{
      // name: payload.name,
      // active_users_limit: payload.active_users_limit,
      // status: payload.status,
      // note: payload.note,
		// }
			// }).then((request) => {
					// return request.data 
				// })
	// },
  
	// async deleteSupplierCompany(payload){
		// return await axios({ 
		// method: "delete",
		// url: `/api/organization/contracting/${payload.contracting_code}`,
			// }).then((request) => {
					// return request.data 
				// })
	// },

  // -----/Supplier user

	// async createSupplierUser(payload){
    // let data_body = {
      // contracting: payload.contracting,
      // username: payload.username,
			// first_name: payload.first_name,
			// last_name: payload.last_name,
			// email: payload.email,
			// note: payload.note,
			// password: payload.password,
		// }
		// return await axios({ 
		// method: "post",
		// url: "/api/user/erp_user",
		// data: data_body}).then((request) => {
					// return request.data 
				// })
	// },

	// async fetchSupplierUsers(){
		// return await axios({ 
		// method: "get",
		// url: "/api/user/erp_user",
			// }).then((request) => {
					// return request.data 
				// })
	// },

	// async updateSupplierUser(payload){
    // let data_body = {
			// first_name: payload.first_name,
			// last_name: payload.last_name,
			// email: payload.email,
			// note: payload.note,
      // status: payload.status,  
		// }
		// return await axios({ 
		// method: "put",
		// url: `/api/user/erp_user/${payload.contracting_code}/${payload.username}`,
		// data: data_body}).then((request) => {
					// return request.data 
				// })
	// },

	// async deleteSupplierUser(payload){
		// return await axios({ 
		// method: "delete",
		// url: `/api/user/erp_user/${payload.contracting_code}/${payload.username}`,
			// }).then((request) => {
					// return request.data 
				// })
	// },
}

