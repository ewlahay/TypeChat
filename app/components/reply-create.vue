<template>
  <div>
    <div v-if="replyVisible" >
        <md-divider></md-divider>
    </div>
    <div v-if="replyVisible" style="margin: auto; width: 80%">
      <md-progress-bar class="md-accent" md-mode="indeterminate" v-if="loading"></md-progress-bar>
      <md-field>
        <label>Type here!</label>
        <md-textarea :id="'body' + post.id" v-model="form.body" md-autogrow></md-textarea>
        <span class="md-helper-text">What do you think?</span>
      </md-field>
    </div>

    <md-card-actions>
      <md-button v-if="replyVisible" @click="cancel()">Cancel</md-button>
      <md-button v-if="showReplyButton || replyVisible" @click="reply()">Reply</md-button>
    </md-card-actions>
  </div>
</template>


<script>
import { mapMutations } from 'vuex'

export default {
  props: {
    post: Object,
    showReplyButton: {
      type: Boolean,
      default: false
    },
    show: false,
  },
  watch: {
    show(newVal, oldVal) {
      if (!newVal && this.replyVisible) {
        this.cancel();
      } else if (newVal && !this.replyVisible) {
        this.start();
      }
    }
  },
  name: 'CreateReply',
  data: () => ({
    form: {
      username: "",
      subject: "",
      body: "",
      tp: "",
    },
    replyVisible: false,
    loading: false,
  }),
  computed: {
    getTypingDNA() {
      let length = this.form.body.length;
      console.log("length:", length);
      let tp = this.$store.state.tdna.getTypingPattern({type: 0, length: length});
      console.log("score:", this.$store.state.tdna.getQuality(tp));
      return tp;
    }
  },
  methods: {
    stopRecording() {
      this.$store.commit('stopRecording')
    },
    async submitPost() {
      let url = "/api/posts/" + this.post.id + "/reply";
      this.form.username = this.$store.state.user.username;
      this.form.tp = "" + this.getTypingDNA;
      //console.log("Typing pattern:", this.form.tp);
      let self = this;
      if (this.$store.state.tdna.getQuality(this.form.tp) == 0) {
        console.warn("quality is low!");
      }
      this.$axios.$post(url, this.form).then(function(r) {
        self.$emit('reply', r);
      });
    },
    async reply() {
      if (this.replyVisible) {
        this.loading = true;
        try {
          await this.submitPost();
        } catch(error) {
          this.loading = false;
          return;
        }
        this.loading = false;
        this.cancel();
      } else {
        this.start();
      }
    },
    cancel() {
      //console.log("Stopping recording");
      this.replyVisible = false;
      this.$store.commit('stopRecording');
      this.form.body = "";
      this.form.tp = "";
      this.$emit('reply-close');

    },
    start() {
      //console.log("Starting recording");
      this.form.tp = "";
      this.replyVisible = true;
      this.$store.commit('startTypingDNA', ["body" + this.post.id, "body"]);
    }

  }
}
</script>
