<template>
  <div v-if="current_user === null">
    <Login />
  </div>
  <div v-else>
    <!-- <v-row class="match-height">
      <v-col cols="20">
        <OnlineSearch />
      </v-col>
    </v-row> -->
    <v-row class="match-height">
      <v-col cols="12">
        <RecentHistory />
      </v-col>
    </v-row>
    <v-row class="match-height">
      <v-col cols="12">
        <Index />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import Login from "./Login.vue";
// import OnlineSearch from "../components/OnlineSearch.vue";
import axios from "axios";
import RecentHistory from "../components/RecentHistory.vue";
import Index from "./Index.vue";

export default {
  name: "Home",
  components: {
    Login,
    // OnlineSearch,
    RecentHistory,
    Index,
},
  data() {
    return {
      current_user: null
    }
  },
  created() {
    axios.get("check-status").then((res) => {
      this.current_user = res.data.username;
      console.log("current user is", this.current_user);
    })
  }
}

</script>