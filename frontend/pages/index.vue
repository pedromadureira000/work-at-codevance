<template>
	<div class="ma-4"><p class="ma-2">{{message}}</p></div>
</template>

<script>
export default {
    name: 'Home',
    data() {
      return {
        message: "" 
      }
    },
		computed: {
			user() {
				return this.$store.state.user.currentUser
			},
		},
		watch: {
			user(newValue, oldValue){
        /** console.log(`old value = ${oldValue}. New value = ${newValue}`  ) */
				if (newValue) {
          this.message = "Welcome " + newValue.username + "!";
				} else {
					this.message = "See you later" 
				}
			}	
		},
		created() {
			if (this.$store.state.user.currentUser){
				this.message = "Welcome " + this.$store.state.user.currentUser.username + "!";
			} else {
				this.message = "Please log in"
			}
		}	
	}
</script>

<style>

</style>

