<template>
  <v-app>
    <v-main>
      <v-table>
        <thead>
          <tr>
            <th class="text-left">Options</th>
            <v-switch color="orange darken-3" @click="toggleTheme"> </v-switch>
          </tr>
        </thead>
      </v-table>
    </v-main>
  </v-app>
</template>

<script>
import Navigation from "../components/Navigation.vue";
import axios from "axios";
import { useTheme } from "vuetify";
export default {
  name: "App",
  theme: { dark: false },
  components: {
    Navigation,
  },

  data() {
    return {
      papers: null,
      value: true,
      form: {
        url: null,
        title: null,
      },
    };
  },
  methods: {
    addBook(event) {
      const payload = {
        url: this.form.url,
        title: this.form.title,
      };
      const path = "add-paper";
      axios
        .post(path, payload)
        .then(() => {
          this.getPapers();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getPapers() {
      console.log(this.switch1);
      const path = "library";
      axios
        .get(path)
        .then((res) => {
          this.papers = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  setup() {
    const theme = useTheme();

    return {
      theme,
      toggleTheme: () =>
        (theme.global.name.value = theme.global.current.value.dark ? "light" : "dark"),
    };
  },
  created() {
    this.getPapers();
  },
};
</script>
