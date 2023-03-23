<template>
  <div v-show="!isResult">
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
  </div>
  <div v-show="isResult">
    <v-card>
      <v-col cols="12">
        <v-card-item>
          <v-card-title>Search Result</v-card-title>

          <template #append>
            <a href="javascript:void(0)" class="text-sm font-weight-medium" @click="isResult = false">Back</a>
          </template>
        </v-card-item>

        <v-card-text>
          <div v-for="paper in searchResults" :key="paper.url">
            <v-spacer></v-spacer>
            <br />
            <h3>
              <a target="_blank" :href="paper.url">{{ paper.title }}</a>
            </h3>
            <p>
              {{ paper.authors.join() }}, {{ paper.year }}
            </p>
            <p>
              Subjects: {{ paper.subjects.join() }}
            </p>
            <p>
              Abstract: {{ paper.abstract }}
            </p>
            <!-- <p>
                Tags:
                <v-chip 
                  class="ma-1" 
                  color="primary" 
                  variant="outlined" 
                  density="compact"
                  :ripple="false" 
                  link 
                  small
                  v-for = "tag in paper.tags">
                    {{ tag }}
                </v-chip>
              </p> -->
            <v-spacer></v-spacer>
            
            <a href="javascript:void(0)" @click="dialog1 = true; exportBib(paper.url)">
              Export BibTex
            </a>
            
            <v-spacer></v-spacer>

            <a v-bind="props" href="javascript:void(0)" @click="dialog2 = true; currentitemurl = paper.url">
              Add this paper to library
            </a>

            <v-spacer></v-spacer>

            <a v-bind="props" href="javascript:void(0)" @click="dialog3 = true; currentitemurl = paper.url">
              View this paper in Paper View
            </a>

            <v-spacer></v-spacer>
            <br />
            <v-divider></v-divider>
          </div>
          
          <v-dialog v-model="dialog1">
            <v-card>
              <v-card-title>
                <span class="text-h5">Export BibTex</span>
              </v-card-title>
              <v-card-text>
                  {{ bibTex }}
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" variant="text" @click="dialog1 = false">
                  Cancel
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

          <v-dialog v-model="dialog2">
            <v-card>
              <v-card-title>
                <span class="text-h5">Add Paper</span>
              </v-card-title>
              <v-card-text>
                Do you want to add this paper to library?
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" variant="text" @click="dialog2 = false">
                  Cancel
                </v-btn>
                <v-btn color="primary" variant="text" @click="dialog2 = false; addPaper(currentitemurl)">
                  Confirm
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

          <v-dialog v-model="dialog3">
            <v-card>
              <v-card-title>
                <span class="text-h5">View Paper</span>
              </v-card-title>
              <v-card-text>
                Here is the paper url: {{ currentitemurl }}. Open and view it in Paper View.
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" variant="text" @click="dialog3 = false">
                  Cancel
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-card-text>
      </v-col>
    </v-card>
  </div>
</template>
  
<script>
import axios from "axios";
export default {
  data() {
    return {
      formSearch: {
        url: "",
      },
      searchResults: [],
      dialog1: false,
      dialog2: false,
      dialog3: false,
      bibTex: null,
      isResult: false,
      currentitemurl: null,
    };
  },
  methods: {
    search() {
      const path = "search";
      this.isResult = true;
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
      this.currentitemurl = url;
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

    addPaper(url) {
      console.log("start addPaper");
      const payload = {
        url: url,
      };
      // can also add book by non-pdf url
      // url = "https://arxiv.org/abs/2104.08678"
      // 'https://arxiv.org/pdf/2210.12257.pdf'
      if (url.substring(url.length - 3) !== "pdf") {
        axios
          .post("get-pdf", payload)
          .then((res) => {
            payload.url = res.data.url;
          })
          .catch((error) => {
            console.log(error);
          });
      };
      axios
        .post("add-paper", payload)
        .catch((error) => {
          console.log(error);
        });
    },
  },
}
</script>

<!-- <style lang="scss" scoped>
.card-list {
  --v-card-list-gap: 1.5rem;
}
</style> -->