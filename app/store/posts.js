export const state = () => ({
  posts: [],
})

export const mutations = {
  set(state, posts) {
    state.posts = posts;
  },
  add(state, post) {
    state.posts.unshift(post);
  },

}

export const getters = {
  posts(state) {
    return state.posts
  },
  post(state, id) {

  }
}
