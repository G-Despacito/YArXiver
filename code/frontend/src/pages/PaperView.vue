<template>
  <div v-show="!isResult">
    <v-card>
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
              <v-text-field v-model="form.url" label="Paper URL" required hide-details>
              </v-text-field>
            </v-col>
          </v-row>
          <v-row justify="center">
            <v-col cols="12">
              <v-btn block color="primary" type="submit" @click="openPaper">
                Open Paper
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </div>
  <div v-show="isResult">
    <v-row>
      <v-col cols="12" sm="12" md="9" class="my-4">
        <v-card>
          <v-card-item>
            <v-card-title>
              PDF View
            </v-card-title>
            <template #append>
              <a href="javascript:void(0)" class="text-sm font-weight-medium" @click="isResult = false">Back</a>
            </template>
          </v-card-item>
          <v-row justify="center">
            <v-col cols="12">
              <v-btn block color="primary" type="submit" @click="addPaper">
                Add to Library
              </v-btn>
            </v-col>
          </v-row>
          <div v-if="pdfSource !== null">
            <vue-pdf-embed :source="pdfSource" />
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" sm="12" md="3" class="my-4">
        <v-card>
          <v-card-item class="justify-center">
              <v-card-title class="font-weight-semibold text-2xl">
                  Similar Paper Found for You
              </v-card-title>
          </v-card-item>
          <v-card-text>
            <div v-for="paper in recommendPapers" :key="paper.url">
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
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import Navigation from '../components/Navigation.vue'
import VuePdfEmbed from 'vue-pdf-embed'
import axios from "axios";

export default {
  name: "PaperView",
  components: {
    Navigation,
    VuePdfEmbed,
  },

  data() {
    return {
      papers: null,
      value: true,
      pdfSource: null,
      recommendPapers: null,
      form: {
        url: null,
      },
      isResult: false,
      dialog1: false,
      dialog2: false,
      dialog3: false,
      bibTex: null,
      currentitemurl: null,
    };
  },
  methods: {

    openPaper() {
      // can also add book by non-pdf url
      // url = "https://arxiv.org/abs/2104.08678"
      // 'https://arxiv.org/pdf/2210.12257.pdf'
      if (this.form.url.substring(this.form.url.length - 3) !== "pdf") {
        axios
          .post("get-pdf", this.form)
          .then((res) => {
            this.pdfSource = res.data.url;
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        this.pdfSource = this.form.url;
      }
      this.isResult = true;
      console.log(this.pdfSource);
      this.getRecommendPapers(this.pdfSource);
    },

    addPaper(event) {
      console.log("start addPaper");
      const payload = {
        url: this.form.url,
      };
      // can also add book by non-pdf url
      // url = "https://arxiv.org/abs/2104.08678"
      // 'https://arxiv.org/pdf/2210.12257.pdf'
      if (this.form.url.substring(this.form.url.length - 3) !== "pdf") {
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

    getRecommendPapers(url) {
      console.log("start getRecommendPapers");
      const path = "get-recommend-papers";
      const payload = {
        url: url,
      };
      axios
        .post(path, payload)
        .then((res) => {
          this.recommendPapers = res.data;
          console.log(res.data);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
}
</script>

<style>

</style>
