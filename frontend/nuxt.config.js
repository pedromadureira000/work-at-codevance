import colors from 'vuetify/es5/util/colors'
import {messages} from './messages'

const _isdev = process.env.DEV
const _LANG = 'en'
import pt from 'vuetify/es5/locale/pt'

export default {

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: 'Codevance Challenge',
    title: 'Codevance challenge',
    htmlAttrs: {
      lang: _LANG == 'pt' ? 'pt-BR' : 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.jpg' }
    ]
  },

  loading: { color: '#fff' },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
		'@/plugins/vuetify',
		'~/plugins/myFunctions',
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    '@nuxtjs/i18n',
    '@nuxtjs/proxy',
  ],

  i18n: {
    locale: _LANG == 'pt' ? 'pt-BR' : 'en',
    locales: [_LANG == 'pt' ? 'pt-BR' : 'en'],
    strategy: 'prefix_except_default',
    defaultLocale: 'en',
    parsePages: false,   // Disable babel parsing. To use custom pages
    vueI18n: {
      fallbackLocale: 'en',
      messages: messages
    }
  },

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
	// axios: {
	// },

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      // dark: true,
      dark: false,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        }
      }
    },
    lang: _LANG == 'pt' ? {
      locales: { pt },
      current: 'pt'
    } : {},
  },

	// Build Configuration: https://go.nuxtjs.dev/config-build
	build: {
		//You can extend webpack config here
		// loaders: {
			// sass: {
				// implementation: require('sass'),
			// },
		// },
		extend (config, ctx) {
			const home = config.resolve.alias['~']
			config.resolve.alias['~api'] = home + '/helpers/api'
		}
	},

	proxy: _isdev  ? {
		'/api': 'http://127.0.0.1:8000/',
	} : null,

	transpileDependencies: [
		'vuetify'
	],

  publicRuntimeConfig: {
    email: process.env.EMAIL,
    phone_number: process.env.PHONE_NUMBER,
    company_name: process.env.COMPANY_NAME
  },
	
  // router: {
    // middleware: ['fwdcookies', 'auth']
  // },
}
