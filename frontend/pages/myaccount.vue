<template>
  <div class="ma-6">
    <div class="ma-3">
      <h3>Update Account Information</h3>
      <form @submit.prevent="updateCurrentUserProfile">
        <div class="mb-3">
          <v-text-field
            label="Email"
            v-model.trim="email"
            :error-messages="emailErrors"
            required
            @blur="$v.email.$touch()"
          />
        </div>
        <v-btn 
          color="primary"
          type="submit"
          :loading="loading_profile"
          :disabled="loading_profile"
        >{{$t('Save')}}</v-btn>
      </form>
    </div>
  </div>
</template>

<script>
import {
  required,
  email
} from "vuelidate/lib/validators";
import { validationMixin } from "vuelidate";

export default {
	middleware: ['authenticated'],
  mixins: [validationMixin],

  data() {
    return {
			email: this.$store.state.user.currentUser.email,
      loading_profile: false,
    };
  },

  validations: {
    email: {
      required,
      email,
    },
    profileGroup: ["email"],
  },

  methods: {
    async updateCurrentUserProfile() {
      this.$v.profileGroup.$touch();
      if (this.$v.profileGroup.$invalid) {
        this.$store.dispatch("setAlert", { message: this.$t("Please_fill_the_form_correctly"), alertType: "error" }, { root: true })
      } else {
        if (
          this.email === this.$store.state.user.currentUser.email
        ){ this.$store.dispatch('setAlert', {message: this.$t('You_have_not_changed_any_fields'), alertType: 'warning'}, { root: true }) }
        else {
          this.loading_profile = true;
          await this.$store.dispatch('user/updateCurrentUserEmail', this.email)
          this.loading_profile = false;
        }	
      }
    },
  },
  computed: {
    emailErrors() {
      const errors = [];
      if (!this.$v.email.$dirty) return errors;
      !this.$v.email.email && errors.push(this.$t("Must be valid e-mail"));
      !this.$v.email.required && errors.push(this.$t("This_field_is_required"));      
      return errors;
    },
  }
}
</script>
<style scoped>
.v-application .mb-3 {
    margin-bottom: 0px !important;
}
</style>
