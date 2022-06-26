import axios from 'axios'

export default axios.create({
	xsrfHeaderName: 'X-CSRFToken',
	xsrfCookieName: 'csrftoken',
	baseURL: process.env.BASE_URL,
	withCredentials: true,
  timeout: 15000
})
