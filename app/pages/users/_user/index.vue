<template>
  <div>
    <div class="md-layout md-gutter md-size-70" style="margin: 1rem auto auto auto; width: 80%">
      <h1>{{this.$route.params.user}}</h1>
      <div class="md-layout-item">
        <h2>{{posts.length}} Posts:</h2>
        <transition-group :name="transition">
          <div v-for="post in posts" :key="post.id" style="margin: 1rem auto auto auto;">
            <post-card :post="post" v-bind:key="post.id" class="md-layout-item" style=""></post-card>
          </div>
        </transition-group>

      </div>
      <div class="md-layout-item">
        <h2>{{replies.length}} Replies:</h2>
        <transition-group :name="transition">
          <div v-for="post in replies" :key="post.id" style="margin: 1rem auto auto auto;">
            <post-card :post="post" v-bind:key="post.id" class="md-layout-item" style=""></post-card>
          </div>
        </transition-group>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data: () => ({
    posts: [],
    replies: [],
    transition: "list",
  }),
  created() {
    this.getUser();
    this.$bus.$on("reload", this.reload);
    this.$bus.$on("addPost", (post) => this.addPost(post));
  },
  beforeDestroy() {
    this.$bus.$off('reload', this.reload);
    this.$bus.$off('addPost',this.addPost);
  },
  methods: {
    async getUser() {
      let url = `/api/users/${this.$route.params.user}?sort=${this.$store.state.user.sortBy}`;
      let data = await this.$axios.$get(url);
      this.posts = [];
      this.replies = [];
      for (let i = 0; i < data.length; i++) {
        if (data[i].reply == null) {
          this.posts.push(data[i]);
        } else {
          this.replies.push(data[i]);
        }
        await new Promise(r => setTimeout(r, this.$store.state.loadDelay));
      }
    },
    addPost(post) {
      if (post.username == this.$route.params.user) {
        this.posts.unshift(post);
      }
    },
    async reload() {
      this.transition = "flip-list";
      let url = `/api/users/${this.$route.params.user}?sort=${this.$store.state.user.sortBy}`;
      let data = await this.$axios.$get(url);
      let posts = [];
      let replies = [];
      for (let i = 0; i < data.length; i++) {
        if (data[i].reply == null) {
          posts.push(data[i]);
        } else {
          replies.push(data[i]);
        }
      }
      this.posts = posts;
      this.replies = replies;
    }
  }
}

</script>
