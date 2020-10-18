export const state = () => ({
  username: "",
  sortBy: "new",
  savedPatterns: 0,
})

export const mutations = {
  setUsername(state, username) {
    state.username = username;
    state.savedPatterns = 0;
  },
  setSort(state, sort) {
    state.sortBy = sort;
  },
  savePattern(state) {
    state.savedPatterns++;
  }
}
