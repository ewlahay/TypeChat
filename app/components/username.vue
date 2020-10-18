<template>
  <md-field style="max-width: 15rem">
    <label>Username</label>
    <md-input v-model="username" @input="validate"></md-input>
    <span class="md-error" v-if="!$v.username.required">Username is required</span>
    <span class="md-error" v-else-if="!$v.username.minLength">Must be at least 4 characters</span>
  </md-field>
</template>


<script>
import { mapMutations } from 'vuex'
import { validationMixin } from 'vuelidate'
import {
  required, minLength
} from 'vuelidate/lib/validators'


const typingDNAValid = function(value) {
  return this.typingDNAValid();
}

  export default {
    name: 'username',
    mixins: [validationMixin],
    data: () => ({
      username: ''
    }),
    created() {
      this.username = this.$store.state.user.username;
      this.$bus.$on('usernameReset', () => this.username = this.$store.state.user.username);
    },
    validations: {
      username: {
        required,
        minLength: minLength(4)
      }
    },
    computed: {
      errorMessage() {
        if (!this.$v.username.required) {
          return "Username is required";
        } else if (!this.$v.username.minLength) {
          return "Must be at least 4 characters";
        }
      }
    },
    methods: {
      setUsername(username) {
        this.$store.commit('user/setUsername', username);
      },
      validate () {
        this.$v.$touch()
        if (!this.$v.$invalid) {
          this.setUsername(this.username)
        } else {
          this.$bus.$emit('toast', this.errorMessage);
        }
      },
    }
  }
</script>
