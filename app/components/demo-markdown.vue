<template>
  <div>
    <md-progress-bar class="md-accent" md-mode="indeterminate" v-if="loading"></md-progress-bar>
    <div class="md-layout md-size-70" v-blur="loading">
    <div class="md-layout-item">
      <div class="md-title" style="width: 100%">Did you know?</div>


      <div class="md-content">
         TypeChat lets you use markup in posts! Try it out with the following examples
      </div>
      <br>
        <div class="md-content">
          <pre class="markdown-body">{{markdownText}}</pre>
          <div v-html="$markup(markdownModel)"></div>
        </div>
        <md-field :class="getValidationClass()">
          <md-textarea id="markdown1" v-model="markdownModel" @paste.prevent></md-textarea>
          <span class="md-error">Type out the exact phrase</span>
        </md-field>
      </div>



    </div>
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
import { required, helpers } from 'vuelidate/lib/validators'
var self = this;

const typingDNAValid = function() {
  /*
  if (self.loading) {
    console.log("Not loaded");
    return false;
  }
  if (!self.$store.tdna) {
    self.$store.commit('startTypingDNA', ["markdown1"]);
  }
  */
  let tp = self.$store.state.tdna.getTypingPattern({type: 0});
  let quality = self.$store.state.tdna.getQuality(tp);
  console.log(quality);
  return quality > self.$store.state.minQuality;
}


const equals = (value, vm) => (vm.markdownText === value);
const autoloadNext = function(value, vm) {
  if (vm.$v.markdownModel.equals && vm.markdownModel.length > 0) {
    vm.next();
  }
  return true;
}

  export default {
    name: 'demoMarkup',
    mixins: [validationMixin],
    data: () => ({
      form: {
        tp: "",
      },
      markdownText: "",
      markdownModel: "",
      loading: true,
      markdownExamples: [],
    }),
    validations: {
      markdownModel: {
        equals,
        autoloadNext
      }
    },
    async created() {
      this.$store.commit('startTypingDNA', ["markdown1"]);
      for (var i = 0; i < 12; i++) {
        this.markdownExamples.push(i);
      }
      this.markdownExamples = this.shuffle(this.markdownExamples);
      self = this;
      await this.getMarkdownExample();
      setTimeout(() => { document.getElementById("markdown1").focus() }, 200);
    },
    computed: {
      getTypingDNA() {
        let tp = this.$store.state.tdna.getTypingPattern({type: 0});
        return tp;
      },
    },
    methods: {
      getValidationClass(fieldName) {
         return {
          'md-invalid': this.$v.$invalid && this.markdownModel.length > 5
        }
      },
      shuffle(a) {
          for (let i = a.length - 1; i > 0; i--) {
              const j = Math.floor(Math.random() * (i + 1));
              [a[i], a[j]] = [a[j], a[i]];
          }
          return a;
      },
      typingDNAValid() {
        let tp = this.$store.state.tdna.getTypingPattern({type: 0});
        let quality = this.$store.state.tdna.getQuality(tp);
        console.log(quality);
        return quality > this.$store.state.minQuality;
      },
      async getMarkdownExample() {
        this.markdownModel = "";
        this.loading = true;
        this.markdownText = await this.$axios.$get(`api/markdown/${this.markdownExamples.pop()}`);
        this.loading = false;

      },
      async next() {
        if (typingDNAValid()) {
          this.savePattern();
          let tp = this.$store.state.tdna.getTypingPattern({type: 0});
          this.$store.commit('startTypingDNA', ["markdown1"]);
          if (tp === this.$store.state.tdna.getTypingPattern({type: 0})) {
            throw 'TypingDNA not reset!'
          }
        }
        await new Promise(r => setTimeout(r, 2000));
        if (this.$store.state.user.savedPatterns < this.$store.state.minSavedPatterns) {
          this.getMarkdownExample();
        } else {
          this.$bus.$emit('hideDemo');
        }
      },
      async savePattern() {
        //this.loading = true;
        let url = `/api/users/${this.$store.state.user.username}`;
        this.form.tp = this.$store.state.tdna.getTypingPattern({type: 0});
        try {
          let data = await this.$axios.post(url, this.form);
          this.$store.commit('user/savePattern');
        } catch(error) {
          this.$handleError(error);
        };
        //this.loading = false;


      },
    }
  }
</script>
