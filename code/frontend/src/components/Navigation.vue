<template>
  <v-app-bar color="primary">
    <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
    <v-toolbar-title>YarXiver</v-toolbar-title>
  </v-app-bar>
  <v-navigation-drawer v-model="drawer">
    <v-list density="default" nav>
      <v-list-item v-for="page in pages" :prepend-icon="page.prepend_icon" :title="page.title" :value="page.value"
        :to="page.value" color="primary">
      </v-list-item>
    </v-list>
    <template v-slot:append>
      <v-row justify="center">
        <v-btn v-show="current_user !== null" @click="logout">
          Log out
        </v-btn>
      </v-row>
      <v-row justify="center">
        <v-col align-self="center" cols="2">
          <v-icon icon="mdi-white-balance-sunny"></v-icon>
        </v-col>
        <v-col align-self="center" cols="3">
          <v-switch color="orange darken-3" hide-details="true" @click="toggleTheme"></v-switch>
        </v-col>
        <v-col align-self="center" cols="2">
          <v-icon icon="mdi-weather-night"></v-icon>
        </v-col>
      </v-row>
    </template>
  </v-navigation-drawer>
</template>

<script>
import { useTheme } from "vuetify";
import axios from "axios";

export default {
  name: "Navigation",
  data: () => ({
    drawer: true,
    pages: [
      { prepend_icon: "mdi-home", title: "Home", value: "home" },
      { prepend_icon: "mdi-web", title: "Recommendation", value: "index" },
      { prepend_icon: "mdi-bookshelf", title: "Library", value: "library" },
      // { prepend_icon: "mdi-cog", title: "Settings", value: "settings" },
      { prepend_icon: "mdi-magnify", title: "Search", value: "search" },
      { prepend_icon: "mdi-book-open", title: "Paper View", value: "paperview" },
    ],
    current_user: null,
  }),
  setup() {
    const theme = useTheme();

    return {
      theme,
      toggleTheme: () =>
        (theme.global.name.value = theme.global.current.value.dark ? "light" : "dark"),
    };
  },

  created() {
    axios.get("check-status").then((res) => {
      this.current_user = res.data.username;
      console.log("current user is", this.current_user);
    });
  },

  methods: {
    logout() {
      axios.get("logout").then((res) => {
        console.log(res.data);
        this.$router.go();
      });
    },
  }
};
</script>

<style>
.switch-center {
  display: flex;
  justify-content: center;
}
</style>
