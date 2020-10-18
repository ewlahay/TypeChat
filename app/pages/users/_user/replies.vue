<template>
  <div>
    <div class="md-layout md-gutter md-size-70 " style="margin: 1rem auto auto auto; width: 80%">
      <h1>{{this.$route.params.user}}</h1>
      <div class="md-layout-item">
        <h2>{{replies.length}} Replies:</h2>
        <transition-group :name="transition">
          <div v-for="post in replies" :key="post.id" style="margin: 1rem auto auto auto;">
            <post-card :post="post" class="md-layout-item" style=""></post-card>
          </div>
        </transition-group>
      </div>
    </div>

  </div>

</template>


<script>
export default {
  data: () => ({
    replies: [],
    transition: "list"
  }),
  created() {
    this.getReplies();
    this.$bus.$on("reload", this.update);
  },
  beforeDestroy() {
    this.$bus.$off('reload',this.update);
  },
  methods: {
    async getReplies() {
      let url = `/api/users/${this.$route.params.user}/replies?sort=${this.$store.state.user.sortBy}`;
      let data = await this.$axios.$get(url);
      this.replies = [];
      for (var i = 0; i < data.length; i++) {
        this.replies.push(data[i]);
        await new Promise(r => setTimeout(r, this.$store.state.loadDelay));
      }

    },
    async update() {
      this.transition = "flip-list";
      let url = `/api/users/${this.$route.params.user}/replies?sort=${this.$store.state.user.sortBy}`;
      this.replies = await this.$axios.$get(url);
    }
  }
}

</script>
