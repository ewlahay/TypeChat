function sleep(ms) {
  var start = new Date().getTime(), expire = start + ms;
  while (new Date().getTime() < expire) { }
  return;
}

function waitForLoad() {

}

export const state = () => ({
  showCreatePost: false,
  //tdna: null,
  minQuality: 0.3,
  loadDelay: 50,
  minSavedPatterns: 3,
})

export const mutations = {
  setDelay(state, value) {
    state.loadDelay = value;
  },
  showCreatePost(state) {
    state.showCreatePost = true;
  },
  startTypingDNA(state, targets) {
    if (TypingDNA.instance != null) {
      TypingDNA.instance.stop();
      //state.tdna.stop();
      state.tdna.reset();
      state.tdna.targetIds = [];
      state.tdna.start();
    } else {
      state.tdna = new TypingDNA();
    }

    console.log("Starting recording", state.tdna)


    if (targets) {
      for (let i = 0; i < targets.length; i++) {
        console.log("adding", targets[i])
        state.tdna.addTarget(targets[i]);
      }
    } else {
      state.tdna.addTarget("subject");
      state.tdna.addTarget("body");
    }

  },
  hideCreatePost(state) {
    state.showCreatePost = false;
  },

  stopRecording(state) {
    state.tdna.stop();
    state.tdna.reset();
  },
}
