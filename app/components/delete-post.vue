<template>
  <div>
      <md-progress-bar class="md-accent" md-mode="indeterminate" v-if="loading"></md-progress-bar>
    <div class="md-layout md-size-70" v-blur="loading" >
       <div class="md-title" style="width: 100%">Delete Post</div>


      <div class="md-content">
        Please Type the following: "<i>{{validationText}}</i>"
      </div>

      <md-field :class="getValidationClass()">
        <md-input id="body-delete" v-model="form.body"></md-input>
        <span class="md-error" v-if="!$v.form.body.required">This is required</span>
        <span class="md-error" v-else-if="$v.form.username.$invalid">You're not {{post.username}}!</span>
        <span class="md-error" v-else-if="!$v.form.body.equal">Type out the exact phrase</span>

      </md-field>
      <md-dialog-actions>
        <md-button @click="$bus.$emit('hideDelete')">Cancel</md-button>
        <md-button @click="validate()">Post</md-button>
      </md-dialog-actions>
    </div>
    <md-progress-bar v-if="loading"></md-progress-bar>
  </div>
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

const equals = function() {
  return this.form.body == this.validationText;
}

  export default {
    name: 'DeletePost',
    mixins: [validationMixin],
    props: {
      post: {
        type: Object,
        required: true
      }
    },
    data: () => ({
      form: {
        username: "",
        subject: "",
        body: "",
        tp: "",
      },
      loading: true,
      postSaved: true,
      validationText: ""
    }),
    validations: {
      form: {
        username: {
          required
        },
        body: {
          required,
          equals,
        }
      }
    },
    created() {
      this.$store.commit('startTypingDNA', ["body-delete"]);
      this.form.username = this.$store.state.user.username;
      this.getValidationText();
      setTimeout(() => { document.getElementById("body-delete").focus() }, 200);
    },
    computed: {
      getTypingDNA() {
        let tp = this.$store.state.tdna.getTypingPattern({type: 0});
        return tp;
      },
    },
    methods: {
      getValidationClass () {
        return {
          'md-invalid': this.$v.$invalid
        }
      },
      typingDNAValid() {
        let tp = this.$store.state.tdna.getTypingPattern({type: 0});
        let quality = this.$store.state.tdna.getQuality(tp);
        console.log(quality);
        return quality > this.$store.state.minQuality;
      },
      async getValidationText() {
        this.loading = true;
        let data = await this.$axios.$get("api/text");
        this.validationText = data;
        this.loading = false;
      },
      validate () {
        console.log("validating");
        this.form.username = this.$store.state.user.username;
        this.$v.$touch();

        if (!this.$v.$invalid) {
          if (this.typingDNAValid()) {
            this.submitPost();
          } else {
            this.form.body = "";
            this.getValidationText();
            console.log("Not good enough");
          }
        } else {
          console.log("Didn't pass validation", this.$v);
        }
      },
      async submitPost() {
        this.loading = true;
        let url = "/api/posts/" + this.post.id;
        this.form.tp = "" + this.getTypingDNA;
        try {
          let result = await this.$axios({method: "delete", url: url,  data:this.form});
          this.$bus.$emit('deletedPost', this.post);
          this.$bus.$emit('hideDelete');
          this.$bus.$emit('toast', "Post deleted");
          if (this.$route.params.post == this.post.id) {
            this.$router.push("/");
          }

        } catch(error) {
          console.log(error);
        };
        this.loading = false;

      },
    }
  }
</script>
