<template>
 <div>
    <md-empty-state
      md-label="Create the first post"
      md-description="Welcome to TypeChat, a hassle free platform for posting"
      v-if="posts.length == 0 && loaded">
      <md-button class="md-primary md-raised" @click="showCreatePost()">Create first post</md-button>
    </md-empty-state>
   <transition-group :name="transition">
    <div v-for="post in posts" class="md-layout md-gutter md-size-70 " :key="post.id" style="margin: 1rem auto auto auto; width: 80%">
       <post-card  :post="post" v-bind:key="post.id"  class="md-layout-item" style=""></post-card>
     </div>
   </transition-group>

  </div>

</template>

<script>
export default {
  data: () => ({
    posts: [],
    loaded: false,
    transition: "list",
  }),
  name: 'index',
  created() {
    this.getPosts();
    this.$bus.$on("reload", this.reload);
    this.$bus.$on("addPost", (post) => this.addPost(post));
  },
  beforeDestroy() {
    this.$bus.$off('reload',this.reload);
    this.$bus.$off("addPost");
  },
  methods: {
    showCreatePost() {
      this.$store.commit('showCreatePost');
    },
    async getPosts() {
      let url = `/api/posts?sort=${this.$store.state.user.sortBy}`;
      let data = await this.$axios.$get(url);
      this.posts = [];
      for (var i = 0; i < data.length; i++) {
        this.posts.push(data[i]);
        await new Promise(r => setTimeout(r, this.$store.state.loadDelay));
      }
      this.loaded = true;
    },
    addPost(post) {
      this.posts.unshift(post);
    },
    async reload() {
      this.transition = "flip-list";
      let url = `/api/posts?sort=${this.$store.state.user.sortBy}`;
      this.posts = await this.$axios.$get(url);

    }
  }
}
</script>

