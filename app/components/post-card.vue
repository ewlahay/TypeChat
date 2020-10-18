<template>
  <md-card md-with-hover>
      <md-ripple>
        <md-card-header v-on:click.native="openPost()">
          <div class="md-title">{{post.subject}}</div>
          <div class="md-subhead">{{post.username}}, {{$formatDate(post.posted)}}</div>
        </md-card-header>

        <md-card-content v-on:click.native="openPost()" v-html="$markup(post.body)" class="post-content">
        </md-card-content>

        <md-card-actions>
          <md-button :to="'/' + post.id + '?reply=true'">Reply</md-button>
        </md-card-actions>
      </md-ripple>
    </md-card>
</template>
<style>
  .md-card-content.post-content a {
    color: blue;
  }
</style>
<script>
  export default {
    props: ['post'],
    data: () => ({

    }),
    methods: {
      openPost() {
        console.log("pushing link");
        this.$router.push('/' + this.post.id);
      }
    }
  }
</script>
