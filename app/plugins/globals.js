import Vue from 'vue'
import Vuelidate from 'vuelidate'
const marked = require("marked");
const insane = require("insane");
const eventBus = {};

eventBus.install = function (Vue) {
  Vue.prototype.$bus = new Vue()
}

Vue.use(eventBus);
Vue.use(Vuelidate);

var authErrorCount = 0;

export default (context, inject) => {
  const formatDate = function(date) {
    let duration = this.$moment().diff(this.$moment(date)) / 1000;
    if (duration / 60 >= 2) {
      if (duration / 3600 >= 2) {
        if (duration / (3600 * 24) >= 2) {
          if (duration / (3600 * 24 * 30) >= 2) {
            if (duration / (3600 *24 * 365) >= 2) {
              return "This post old af";
            }
            return `${Math.round(duration / (3600 * 24 * 30))} months ago`;
          }
          return `${Math.round(duration / (3600 * 24))} days ago`;
        }
        return `${Math.round(duration / 3600)} hours ago`;
      }
      return `${Math.round(duration / 60)} minutes ago`;
    }
    return `${Math.round(duration)} seconds ago`;
  };
  inject('formatDate', formatDate);


  const handle401 = function(self, error) {
    authErrorCount++;

    if (authErrorCount > 3) {
      self.$store.commit('user/reset');
      self.$store.commit("nextResetText");
      setTimeout(() => { self.$bus.$emit('usernameReset') }, 4000);
    }
    console.log("Handling error");
    if (error.response.data.detail) {
      self.$bus.$emit('toast', error.response.data.detail);
    } else {
      self.$bus.$emit('toast', self.$store.state.resetText);
    }


  }
  //inject('handle401', handle401);

  const handleError = function(error) {
    console.log("Handling error");
    if (error.response) {
      if (error.response.status == 401) {
        handle401(this, error);
      }
    }

  }
  inject('handleError', handleError);

  const getQuality = function() {
    return this.$store.tdna.getQuality(this.$store.getTypingPattern({type: 0}));
  }
  inject("getQuality", getQuality);

  const username = function() {
    return this.$store.state.user.username;
  }
  inject("username", username);

  const markup = function(text) {
    return insane(marked(text));
  }
  inject("markup", markup);

  const checkPatterns = async function() {
    if (this.$store.state.user.savedPatterns < this.$store.state.minSavedPatterns) {
      await new Promise(r => setTimeout(r, 2000));
      this.$bus.$emit('showDemo');
    }
  }
  inject("checkPatterns", checkPatterns);
}
