<template>
  <form novalidate class="md-layout" @submit.prevent="submitPost" :disabled="loading" v-blur="loading">
    <div class="md-title">Create Post</div>

    <md-field :class="getValidationClass('subject')">
      <label>Your awesome idea</label>
      <md-input id="subject" v-model="form.subject" :disabled="loading"></md-input>
      <span class="md-helper-text">Title</span>
      <span class="md-error" v-if="!$v.form.subject.required">This is required</span>
    </md-field>
    <md-field :class="getValidationClass('body')">
      <label>Body</label>
      <md-textarea id="body" v-model="form.body" :disabled="loading"></md-textarea>
      <span class="md-error" v-if="!$v.form.body.required">This is required</span>
      <span class="md-error" v-else="!$v.form.body.typingDNAValid">Keep typing</span>

    </md-field>
    <md-dialog-actions>
      <md-button @click="hideCreatePost()">Cancel</md-button>
      <md-button @click="submitPost()">Post</md-button>
    </md-dialog-actions>

  </form>
</template>


<style lang="scss" scoped>
  .md-card {
    width: 100%;
    margin: 2rem;
  }
  .md-layout  {
    margin: 2rem;
  }

</style>

<script>
import { mapMutations } from 'vuex'
import { validationMixin } from 'vuelidate'

import {
  required,
} from 'vuelidate/lib/validators'

const typingDNAValid = function() {
  let tp = this.$store.state.tdna.getTypingPattern({type: 0});
  let quality = this.$store.state.tdna.getQuality(tp);
  console.log(quality);
  return quality > this.$store.state.minQuality;
}

  export default {
    name: 'CreatePost',
    data: () => ({
      form: {
        username: "",
        subject: "",
        body: "",
        tp: "",
      },
      loading: false,
      buttonEnabled: false,
    }),
    validations: {
      form: {
        username: {
          required
        },
        subject: {
          required
        },
        body: {
          required,
          typingDNAValid,
        }
      }
    },
    computed: {
      getTypingDNA() {
        let length = this.form.subject.length + this.form.body.length;
        console.log("length:", length);
        let tp = this.$store.state.tdna.getTypingPattern({type: 0, length: length});
        console.log("score:", this.$store.state.tdna.getQuality(tp));
        return tp;
      }
    },
    created() {
      this.$store.commit('startTypingDNA', ["body", "subject"]);
    },
    methods: {
      hideCreatePost() {
        this.$store.commit('hideCreatePost')
      },
      getValidationClass(fieldName) {
        const field = this.$v.form[fieldName]

        if (field) {
          return {
            'md-invalid': field.$invalid && field.$dirty
          }
        }
      },
      stopRecording() {
        this.$store.commit('stopRecording');
      },
      submitPost() {
        this.form.username = this.$store.state.user.username;
        this.form.tp = "" + this.getTypingDNA;
        this.$v.$touch();
        console.log("posting");
        if (!this.$v.$invalid) {
          this.post();
        } else if (this.$v.form.username.$invalid) {
          this.$bus.$emit("toast", "Pick a valid username first");
        } else {
          this.$bus.$emit("toast", "Fix errors first");
        }
      },
      async post() {
        this.loading = true;
        console.log("posting...");
        try {
          let url = "/api/posts";
          let post = await this.$axios.$post(url, this.form)
          this.hideCreatePost();
          this.stopRecording();
          this.$bus.$emit('addPost', post);
          this.$bus.$emit('toast', "Post created");
          this.$store.commit('user/savePattern');
          this.$checkPatterns();
        } catch (error) {
          this.loading = false;
          this.$bus.$emit('toast', "That didn't work");
          this.$handleError(error);
          this.$store.commit('startTypingDNA', ["body", "subject"]);
        }
        this.loading = false;
      }
    }
  }

</script>
