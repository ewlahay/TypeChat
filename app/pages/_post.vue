<template>
  <div class="md-layout" style="width: 80%; margin: auto">
    <div style="margin: 1rem auto auto auto; width: 100%">
     <post :post="post" :showTitle="true" :showReplyButton="true" v-if="loaded"></post>
    </div>

  </div>
</template>


<script>
export default {
  data: () => ({
    post: {},
    replies: [],
    loaded: false,
  }),
  created() {
    this.getPost();
    this.$bus.$on('postUpdated', (item) => this.update(item));
  },
  methods: {
    async getPost() {
      let url = `/api/posts/${this.$route.params.post}`;
      let data = await this.$axios.$get(url);
      this.post = data;
      this.loaded = true;
    },
    update(item) {
      if (item.id == this.post.id) {
        this.post = item;
      }
    }
  }
}
</script>
