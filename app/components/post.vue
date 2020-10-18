<template>
  <div class="post">
    <md-list class="md-layout-item md-double-line md-card md-with-hover" style="margin: auto auto auto auto;">
      <md-list-item v-if="showTitle" v-on:click="showReplies = !showReplies" :mdRipple="false">
        <h2><span class="md-list-item-text">{{post.subject}}</span></h2>
      </md-list-item>
      <md-subheader v-on:click.native="showReplies = !showReplies">
        <md-button :to="`/users/${post.username}`" v-on:mouseenter.native="showDelete = !showDelete">{{post.username}}</md-button>
        <md-button class="md-icon-button" v-if="showDelete && $username() == post.username" @click="showDeletePost">
          <md-icon class="fa fa-trash"></md-icon>
        </md-button>
        {{$formatDate(post.posted)}}
      </md-subheader >

      <md-divider></md-divider>
      <md-progress-bar v-if="loading && showEdit" class="md-accent" md-mode="indeterminate"></md-progress-bar>
      <md-list-item v-on:click="toggleReply()" :mdRipple="!showEdit">
        <div v-if="!showEdit" :source="post.body" class="md-list-item-text post-content" v-html="$markup(post.body)" style="white-space: normal;"></div>
        <md-field v-if="showEdit" :class="getValidationClass()">
          <md-textarea v-model="form.body" :id="'bodyEdit' + post.id" md-autogrow></md-textarea>
          <span class="md-error" v-if="!$v.form.body.typingDNAValid">Keep editing</span>
        </md-field>
      </md-list-item>

      <div :id="'reply-' + post.id">
        <div v-if="showReply" >
          <md-divider></md-divider>
          <md-progress-bar v-if="loading" class="md-accent" md-mode="indeterminate"></md-progress-bar>
        </div>
        <div v-if="showReply" style="margin: auto; width: 80%">
          <md-field :class="getValidationClass()">
            <md-textarea :id="'bodyReply' + post.id" v-model="form.body" md-autogrow></md-textarea>
            <span class="md-helper-text">What do you think?</span>
            <span class="md-error" v-if="!$v.form.body.typingDNAValid">Keep typing</span>
          </md-field>
        </div>

        <md-card-actions>
          <md-button v-if="showReply || showEdit" @click="cancel()">Cancel</md-button>
          <md-button v-if="$username() == post.username && !showEdit && !showReply" @click="edit()">Edit</md-button>
          <md-button v-if="(showReplyButton || showReply) && !showEdit" @click="reply()">Reply</md-button>
          <md-button v-if="showEdit" @click="save()">Save</md-button>
        </md-card-actions>
      </div>

    </md-list>
    <div v-for="item in replies" v-bind:key="item.id" style="margin-left: auto; width: 98%" v-show="showReplies">
       <post :post="item" :depth="depth + 1"></post>
   </div>
  </div>
</template>
<style>
  .md-list-item-text.post-content a {
    color: blue;
  }
  .md-list-item-text img {
    width: unset;
  }
</style>
<script>
import { validationMixin } from 'vuelidate'

import {
  required,
} from 'vuelidate/lib/validators'

const typingDNAValid = function() {
  //let tp = this.$store.getters.pattern //.getTypingPattern({type: 0});
  let tp = this.$store.state.tdna.getTypingPattern({type: 0});
  let quality = this.$store.state.tdna.getQuality(tp);
  console.log(quality);
  return quality > this.$store.state.minQuality;
}

  export default {
    name: 'post',
    mixins: [validationMixin],
    props: {
      post: Object,
      showTitle: {
        type: Boolean,
        default: false
      },
      showReplyButton: {
        type: Boolean,
        default: false
      },
      depth: {
        type: Number,
        default: 0
      }
    },
    data: () => ({
      replies: [],
      showReplies: true,
      showReply: false,
      showEdit: false,
      form: {
        username: '',
        subject: '',
        body: '',
        tp: '',
      },
      loading: false,
      showDelete: false,
    }),
    validations: {
      form: {
        username: {
          required
        },
        body: {
          required,
          typingDNAValid,
        }
      }
    },
    created() {
      this.getReplies();
      this.form.username = this.post.username;
      this.form.subject = this.post.subject;
      if (this.depth < 1) {
        if (this.$route.query.reply == "true" ? true : false) {
          this.reply();
        }
      }
      this.$bus.$on("reload", this.getReplies);
      this.$bus.$on('postUpdated', (item) => this.updateReply(item));
      this.$bus.$on('replyCreated', (item) => this.addReply(item));
    },
    beforeDestroy() {
      this.$bus.$off('reload', this.getReplies);
      this.$bus.$off('postUpdated', (item) => this.updateReply(item));
      this.$bus.$off('replyCreated', (item) => this.addReply(item));
    },
    methods: {
      async getReplies() {
        if (this.$route.params.post) {
          let url = `/api/posts/${this.post.id}/replies?sort=${this.$store.state.user.sortBy}`;
          let data = await this.$axios.$get(url);
          this.replies = data;
        }
      },
      getValidationClass () {
        return {
          'md-invalid': this.$v.$invalid
        }
      },
      updateReply(reply) {
        if (this.replies.length > 0) {
          for (let i = 0; i < this.replies.length; i++) {
            if (this.replies[i].id == reply.id) {
              this.replies.splice(i, 1, reply);
              break;
            }
          }
          this.$bus.$emit("toast", "post updated");
        }

      },
      addReply(reply) {
        if (reply.reply == this.post.id) {
          this.replies.push(reply);
        }

        this.showReply = false;
      },
      toggleReply() {
        if (!this.showEdit) {
          if (this.showReply) {
            this.cancel();
          } else {
            this.reply();
          }
        }
      },
      openPost() {
        this.$router.push('/' + this.post.id);
      },
      go(postId) {
        this.$router.push('/' + postId);
      },
      reply() {
        if (!this.showReply) {
          this.start();
          this.showReply = true;
          setTimeout(() => { document.getElementById("bodyReply" + this.post.id).focus() }, 200);
        } else {
          this.save();
        }
      },
      edit() {
        this.start();
        this.form.body = this.post.body;
        this.showEdit = true;
        setTimeout(() => { document.getElementById("bodyEdit" + this.post.id).focus() }, 200);
      },
      async save() {
        //submit post
        this.form.username = this.$store.state.user.username;
        this.form.tp = this.$store.state.tdna.getTypingPattern({type: 0});
        this.$v.$touch();
        if (!this.$v.$invalid) {
          if (this.showEdit) {
            await this.submitEdit();
          } else {
            await this.submitReply();
          }
        } else if (this.$v.form.username.$invalid) {
          this.$bus.$emit("toast", "Pick a valid username first");
        } else {
          this.$bus.$emit("toast", "Fix errors first");
        }

      },
      async submitEdit() {
        let url = `/api/posts/${this.post.id}`;
        this.loading = true;
        try {
          let post = await this.$axios.put(url, this.form);
          this.$bus.$emit("postUpdated", post.data);
          this.cancel();
          this.$checkPatterns();
        } catch (error) {
          console.log(error);
          this.$handleError(error);
        }
        this.loading = false;
      },
      async submitReply() {
        let url = `/api/posts/${this.post.id}/reply`;
        this.loading = true;
        try {
          let post = await this.$axios.post(url, this.form);
          this.$bus.$emit("replyCreated", post.data);
          this.$bus.$emit("toast", "Reply created");
          this.cancel();
          this.$checkPatterns();
        } catch (error) {
          console.log(error);
          this.$handleError(error);
        }
        this.loading = false;

      },
      start() {
        this.$store.commit("startTypingDNA", ['bodyEdit' + this.post.id, 'bodyReply' + this.post.id]);
      },
      cancel() {
        this.showReply = false;
        this.showEdit = false;
        this.form.body = '';
      },
      showDeletePost() {
        this.$bus.$emit('showDelete', this.post);
      }
    }
  }
</script>
