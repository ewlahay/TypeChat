<template>
  <div>
    <div class="page-container md-layout-column">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

    <md-toolbar class="md-primary">
      <md-button class="md-icon-button" @click="showNavigation = true">
        <md-icon class="fa fa-bars"></md-icon>
      </md-button>
      <span class="md-title" @click="$router.push('/')">TypeChat</span>

      <div class="md-toolbar-section-end">
        <md-field class="md-small-size-50 md-xsmall-hide" style="max-width: 10rem; margin-right: 1rem;">
            <label for="sortBy">Sort by</label>
            <md-select name="sortBy" id="sortBy" v-on:md-selected="changeSort" v-model="sortBy">
              <md-option v-if="sortBy != 'hot'" value="hot">hot</md-option>
              <md-option v-if="sortBy != 'new'" value="new">new</md-option>
              <md-option v-if="sortBy != 'oldest'" value="oldest">old</md-option>
            </md-select>
          </md-field>


        <username></username>
        <md-button class="md-icon-button" @click="showCreatePost()">
            <md-icon class="fa fa-paper-plane"></md-icon>
          </md-button>

      </div>
    </md-toolbar>

    <md-drawer :md-active.sync="showNavigation" md-swipeable>
      <md-toolbar class="md-transparent" md-elevation="0">
        <span class="md-title">TypeChat</span>
      </md-toolbar>

      <md-list>

        <md-list-item :to="`/users/${username}`" @click="showNavigation = false">
          <md-icon class="fa fa-inbox"></md-icon>
          <span class="md-list-item-text">Profile</span>
        </md-list-item>

        <md-list-item :to="`/users/${username}/replies`" @click="showNavigation = false">
          <md-icon class="fa fa-paper-plane"></md-icon>
          <span class="md-list-item-text">Replies</span>
        </md-list-item>

        <md-list-item @click="trash(); showNavigation = false">
          <md-icon class="fa fa-trash"></md-icon>
          <span class="md-list-item-text">Trash</span>
        </md-list-item>
      </md-list>
    </md-drawer>
    <md-dialog id="create-post" :md-active="createPost">
      <create-post></create-post>
    </md-dialog>
      <md-dialog id="delete-post" :md-active="showDelete">
      <delete-post :post="postToDelete"></delete-post>
    </md-dialog>
      <md-dialog id="demo-markdown" :md-active="showDemo">
      <demo-markdown></demo-markdown>
    </md-dialog>

    <div>
      <Nuxt />
    </div>
      <md-snackbar :md-active.sync="showToast" :md-duration="duration" md-persistent>
      <span>{{errorMessage}}</span>
    </md-snackbar>
  </div>
</div>
</template>
<style>
  #create-post {
    width: 50%;
    margin: 0 auto;
  }
</style>
<script>
import { mapMutations } from 'vuex'

export default {
    data: () => ({
      showNavigation: false,
      showSidePanel: false,
      showToast: false,
      showDelete: false,
      showDemo: false,
      postToDelete: null,
      errorMessage: '',
      duration: 3000,
      sortOptions: [
        {text: "new", value: "new"},
         {text: "hot", value: "hot"},
         {text: "old", value: "oldest"}
       ],
       sortBy: "new"
    }),
    created() {
      this.$bus.$on("toast", (message) => this.toast(message));
      this.$bus.$on("showDelete", (post) => this.showDeletePost(post));
      this.$bus.$on("hideDelete", () => this.hideDelete());
      this.$bus.$on("hideDemo", () => this.hideDemo());
      this.$bus.$on("showDemo", () => this.showDemoDialog());
      this.sortBy = this.$store.state.user.sortBy;
    },
    computed: {
      createPost() {
        return this.$store.state.showCreatePost;
      },
      username() {
        return this.$store.state.user.username;
      }
    },
    methods: {
      toast(message) {
        this.errorMessage = message;
        this.showToast = true;
      },
      hideCreatePost() {
        this.$store.commit('hideCreatePost');
        this.$store.commit('stopRecording');
      },
      showCreatePost() {
        this.$store.commit('showCreatePost');
        this.$store.commit('startTypingDNA');
      },
      showDeletePost(post) {
        this.postToDelete = post;
        this.showDelete = true;
      },
      hideDelete() {
        this.showDelete = false;
      },
      showDemoDialog() {
        this.showDemo = true;
      },
      hideDemo() {
        this.showDemo = false;
      },
      changeSort(value) {
        this.$store.commit('user/setSort', value);
        this.$bus.$emit("reload");
      },
      trash() {
        this.toast("trash");
      }

    }
  }
</script>
