<template>
  <v-app>
		<v-navigation-drawer v-model="drawer" app> 
      <v-list two-line v-if="logged_user">
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>{{logged_user.username}}</v-list-item-title>
            <v-list-item-subtitle>Role: {{logged_user.roles[0]}}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>

			<v-divider style="margin-top: -8px; margin-bottom: 8px;" />

      <!-- MenuItems composition -->
      <v-list nav dense>
        <v-list-item
          v-for="item in currentMenuItems"
          :key="item.to"
          :to="item.to"
          link
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{item.title}}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <!-- Test Button -->
      <!-- <v-card class="pa-3" color="blue-grey darken-4" tile> -->
        <!-- <nuxt-link :to="switchLocalePath('en')">English</nuxt-link> -->
        <!-- <nuxt-link :to="switchLocalePath('pt-BR')">Português</nuxt-link> -->
        <!-- <nuxt-link :to="admin-organization-company">TEST</nuxt-link> -->
        <!-- <v-btn label="testFF" @click="testFF"/> -->
      <!-- </v-card> -->
      <!-- Test Button -->

    </v-navigation-drawer>
    <!-- App bar -->
    <v-app-bar color="blue-grey darken-4" dark app>
      <v-app-bar-nav-icon
        @click="drawer = !drawer"
      ></v-app-bar-nav-icon>

      <v-toolbar-title>Codevance challenge</v-toolbar-title>

      <v-spacer></v-spacer>
      <h5 v-if="logged_user">{{logged_user.username}}</h5>

			<v-btn 
				v-if="!logged_user"
				text
				dark
				ripple
				class="ma-0 ml-5"
				depressed
				@click="open_login_dialog($event)"
			>Login</v-btn>

			<v-menu v-else offset-y>
				<template v-slot:activator="{ on }">
					<v-btn icon v-on="on" class="ma-0 ml-5">
						<v-avatar size="45px">
							<img src="~assets/images/default_user.jpg">
						</v-avatar>
					</v-btn>
				</template>
				<v-card class="no-padding">					
					<v-list>
            <v-list-item to="/myaccount">
              <v-list-item-title>My Account</v-list-item-title>
            </v-list-item>
            <v-list-item @click="logout">
              <v-list-item-title>Logout</v-list-item-title>
            </v-list-item>
					</v-list>
				</v-card>
			</v-menu>
    </v-app-bar>

    <v-main>
      <nuxt/>
    </v-main>

    <login-dialog ref="login_dialog"/>

    <!-- Alert -->
    <div>
        <!-- dismissible -->
      <v-alert
        :value="$store.state.alert.showAlert"
        :type='$store.state.alert.alertType' 
        style="width: 50%;" 
        class="alert_message" 
        dismissible
      >
        {{$store.state.alert.alertMessage}}
      </v-alert>
    </div>
		<le-footer/>
  </v-app>
</template>

<script>
import footer from '~/components/Footer.vue';
import loginDialog from '~/components/login-dialog.vue'
import {operator, supplier_user} from '~/helpers/permissions'
let payment_permissions = operator.concat(supplier_user)

export default {
	name: "default",
	middleware: ['fwdcookies', 'check_auth'],
  components: {
    loginDialog,
    leFooter: footer
  },

  data() {
    return {
      drawer: null,
      defaultMenuItems: [
        { title: "Home", icon: "mdi-home", to: "/" },
        { title: "About the system", icon: "mdi-help-box", to: "about" },
      ],
      allMenuItems: [
        { permissions: payment_permissions, title: "Payment", icon: "mdi-clipboard-check-multiple", to: "/payment"},
        /** {permissions: operator, title: "Organizations", icon: "mdi-clipboard-check-multiple", to: "admin-organization"}, */
        /** {permissions: usersMenuPermissions , title: "Users", icon: "mdi-account-group", to: "admin-user"}, */
      ],
    }
  },

  methods: {
    open_login_dialog(evt) {
      this.$refs.login_dialog.open()
      evt.stopPropagation()
    },
    logout() {
			this.$store.dispatch('user/logout')
    },

    /** async testFF(){ */
      /** console.log(">>>>>>> process.env.XX: ", process.env.DEV) */
      /** this.$store.dispatch("testFF") */
      
      /** this.$store.dispatch("setAlert", {message: "erro rah rr erro rah rr erro rah rr erro rah rrerro rah rr erro rah rrerro rah rr erro rah rrerro rah rr erro rah rr erro rah rr erro rah rr erro rah rr erro rah rr erro rah rr erro rah rr erro rah rr erro rah rrerro rah rr erro rah rrerro rah rr erro rah rrerro rah rr erro rah rr erro rah rr erro rah rr erro rah rr erro rah rr", alertType: "error"}, { root: true }) */
    /** }, */

  },

  computed: {
		logged_user(){
			return this.$store.state.user.currentUser
		},
    currentUserIsSupplierUser(){
      return this.$store.state.user.currentUser.roles.includes('supplier_user')
    },
    /** Calculates which Menus the CurrentUser has access and return it concatenated with defaultMenuItems (between Home and About_the_system page). */
		currentMenuItems() {
			let user = this.$store.state.user.currentUser;
			if (user) {
        // console.log(">>>>>>> ", user)
				return this.defaultMenuItems
					.slice(0, 1)
          .concat(this.allMenuItems.filter(MenuItem => {
            return MenuItem.permissions.some(permission => {
              return this.$store.state.user.currentUser.permissions.includes(permission)
            })
          }))
					.concat(this.defaultMenuItems.slice(1, 2));
			} else {
				return this.defaultMenuItems;
			}
		},
  },

};
</script>

<style scoped>
.alert_message{
  position: fixed;
  left: 50%;
  bottom: 0px;
  transform: translate(-50%, -50%);
  z-index: 999;
}

.v-application .pa-3 {
	padding: 14px !important;
}
</style>
