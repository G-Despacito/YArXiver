<template>
  <v-card>
    <v-col cols="12">
      <v-card-item class="justify-center">
        <template #prepend>
          <div class="d-flex">
            <img src="../images/logo.png" class="logo" />
          </div>
        </template>
      </v-card-item>

      <v-card-text>
        <v-form>
          <v-row justify="center">
            <v-col cols="12">
              <v-text-field v-model="formSearch.url" label="Online search" required hide-details>
              </v-text-field>
            </v-col>
          </v-row>
          <v-row justify="center">
            <v-col cols="12">
              <v-btn block color="primary" type="submit" @click="search">
                Search
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-col>
  </v-card>
</template>
  
<script>
import axios from "axios";
export default {
  data() {
    return {
      searchResults: [],
      formSearch: {
        url: null,
      },
      dialog: false,
      bibTex: null,
    };
  },
  methods: {
    search() {
      const path = "search";
      const payload = {
        url: this.formSearch.url,
      };
      axios
        .post(path, payload)
        .then((res) => {
          this.searchResults = res.data;
          console.log("search" + this.searchResults);
          console.log(res.data);
        })
        .catch((error) => {
          console.error(error);
        });
    },

    exportBib(url) {
      console.log("start exportBib");
      console.log(url);
      const path = "bib";
      const payload = {
        url: url,
      };
      console.log(payload);
      axios
        .post(path, payload)
        .then((res) => {
          this.bibTex = res.data.bib;
          console.log(this.bibTex);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  }
}
</script>
