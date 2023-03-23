<template>
  <v-row>
    <v-col>
      <v-expand-transition>
        <v-alert v-show="alert" type="error" closable="true">
          Import paper failed! Paper URL not exists!
        </v-alert>
      </v-expand-transition>
    </v-col>
  </v-row>
  <v-container>
    <v-form>
      <v-row>
        <v-col cols="12" md="1">
          <v-btn @click="import_dialog = true" color="primary">
              Import
          </v-btn>
        </v-col>
        <v-col cols="12" md="2">
          <v-combobox v-model="form.category" label="Category" :items="['Year', 'Author', 'Title', 'Subject', 'Tag']"
            density="compact" variant="solo" single-line hide-details></v-combobox>
        </v-col>
        <v-col cols="12" md="9">
          <v-text-field v-model="form.search" label="Search Paper by Author, Title, and more" density="compact" variant="solo"
            append-inner-icon="mdi-magnify" single-line hide-details @click:append-inner="search"
            required></v-text-field>
        </v-col>
      </v-row>
    </v-form>
    <v-row>
      <v-col>
        <EasyDataTable show-index :headers="headers" :items="items" buttons-pagination alternating
          table-class-name="customize-table">
          <template #item-url="{ url }">
            <a target="_blank" :href="url">{{ url }}</a>
          </template>
          <template #expand="item">
            <div style="padding: 15px">
              Abstract: {{ item.abstract }}
            </div>
          </template>
          <template #item-operation="item">
            <div class="operation-wrapper">
              <img src="../images/delete.png" class="operation-icon" @click="deletePaper(item)" />
              <img src="../images/edit.png" class="operation-icon" @click="editPaper(item)"
                v-if="item.url !== editingitemurl || !isediting" />
              <img src="../images/confirm.png" class="operation-icon" @click="editPaper(item)" v-else />
              <img src="../images/export.png" class="operation-icon" @click="dialog = true; exportBib(item)" />
              <!-- <img src="../images/view.png" class="operation-icon" @click="viewPaper(item)" /> -->
            </div>
          </template>
          <template #item-tags="item">
            <div class="text-left">
              <v-chip class="ma-1" color="primary" variant="outlined" density="compact" :ripple="false" link small
                closable v-if="item.url === editingitemurl && isediting" v-for="tag in item.tags"
                @click:close="removeTag(item, tag)">
                {{ tag }}
              </v-chip>
              <v-chip class="ma-1" color="primary" variant="outlined" density="compact" :ripple="false" link small
                v-else v-for="tag in item.tags">
                {{ tag }}
              </v-chip>
              <v-chip class="ma-1" color="primary" variant="outlined" density="compact" :ripple="false" link small
                @click="addTag_dialog = true; addTag_item = item">
                +
              </v-chip>
            </div>
          </template>
        </EasyDataTable>
      </v-col>
    </v-row>
    <v-dialog v-model="dialog">
      <v-card>
        <v-card-title>
          <span class="text-h5">Export BibTex</span>
        </v-card-title>
        <v-card-text>
            {{ bibTex }}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="dialog = false">
            Cancel
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="addTag_dialog">
      <v-card>
        <v-card-title>
          <span class="text-h5">Add Tag</span>
        </v-card-title>
        <v-card-text>  
          <v-text-field v-model="form.editingTag" label="Type tag here! click +" density="compact" variant="solo" single-line
            hide-details required>
          </v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" variant="text" @click="addTag(addTag_item); addTag_dialog = false; form.editingTag = null">
            Confirm
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="addTag_dialog = false">
            Cancel
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="import_dialog">
      <v-card>
        <v-card-title>
          <span class="text-h5">Import Paper By URL</span>
        </v-card-title>
        <v-card-text>  
          <v-text-field v-model="form.url" label="Add Paper by URL" density="compact" variant="solo"
            append-inner-icon="mdi-plus-circle-outline" single-line hide-details>
          </v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" variant="text" @click="addBook(form.url); import_dialog = false; form.url = null">
            Confirm
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="import_dialog = false">
            Cancel
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import axios from "axios";

export default {
  name: "Library",

  components: {
    // EasyDataTable: window["vue3-easy-data-table"],
  },

  data() {
    return {
      form: {
        url: null,
        search: null,
        category: null,
        editingTag: null,
      },
      headers: [
        { text: "Title", value: "title", sortable: true },
        { text: "Authors", value: "authors" },
        { text: "URL", value: "url", sortable: true },
        { text: "Year", value: "year", sortable: true },
        { text: "Subjects", value: "subjects" },
        { text: "Tags", value: "tags" },
        { text: "Operation", value: "operation" },
      ],
      items: [],
      isediting: false,
      editingitemurl: null,
      dialog: false,
      bibTex: null,
      addTag_dialog: false,
      addTag_item: null,
      import_dialog: false,
      alert: false,
    };
  },
  methods: {
    addBook(url) {
      this.alert = false;
      console.log("start addBook");
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
        .then((res) => {
          if (res.data.code !== 200) {
            this.alert = true;
          }
          this.getPapers();
        })
        .catch((error) => {
          console.log(error);
        });
    },

    getPapers() {
      console.log("start getPapers");
      const path = "library";
      axios
        .get(path)
        .then((res) => {
          this.items = res.data;
          console.log(this.items);
        })
        .catch((error) => {
          console.error(error);
        });
    },

    search(event) {
      console.log("start search")
      console.log(this.form.search)
      if (this.form.search == "") {
        this.getPapers();
      }
      else if (this.form.category == "Year") {
        console.log("start search year")
        const path = "get-paper-by-year";
        const payload = {
          year: this.form.search,
        };
        axios
          .post(path, payload)
          .then((res) => {
            this.items = res.data;
            console.log(res.data);
          })
          .catch((error) => {
            console.error(error);
          });
      } else if (this.form.category == "Author") {
        const path = "get-paper-by-author";
        const payload = {
          author: this.form.search,
        };
        axios
          .post(path, payload)
          .then((res) => {
            this.items = res.data;
            console.log(res.data);
          })
          .catch((error) => {
            console.error(error);
          });
      } else if (this.form.category == "Title") {
        const path = "get-paper-by-title";
        const payload = {
          title: this.form.search,
        };
        axios
          .post(path, payload)
          .then((res) => {
            this.items = res.data;
            console.log(res.data);
          })
          .catch((error) => {
            console.error(error);
          });
      } else if (this.form.category == "Subject") {
        const path = "get-paper-by-subject";
        const payload = {
          subject: this.form.search,
        };
        axios
          .post(path, payload)
          .then((res) => {
            this.items = res.data;
            console.log(res.data);
          })
          .catch((error) => {
            console.error(error);
          });
      } else if (this.form.category == "Tag") {
        const path = "get-paper-by-tag";
        const payload = {
          tag: this.form.search,
        };
        axios
          .post(path, payload)
          .then((res) => {
            this.items = res.data;
            console.log(res.data);
          })
          .catch((error) => {
            console.error(error);
          });
      }
    },

    deletePaper(item) {
      console.log("start remove paper");
      console.log(item);
      const path = "remove-paper";
      console.log(item)
      axios
        .post(path, item)
        .then((res) => {
          this.getPapers();
          console.log(res.data);
        })
        .catch((error) => {
          console.error(error);
        });
    },

    editPaper(item) {
      this.editingitemurl = item.url;
      if (this.isediting) {
        this.isediting = false;
      } else {
        this.isediting = true;
      }

    },

    addTag(item) {
      // layover
      console.log("start addTag")
      console.log(item)
      const path = "attach-tag";
      const payload = {
        tag: this.form.editingTag,
        url: item.url,
      };
      console.log(payload)
      axios
        .post(path, payload)
        .then((res) => {
          this.getPapers();
          console.log(this.items);
        })
        .catch((error) => {
          console.error(error);
        });
    },

    removeTag(item, tag) {
      console.log("start removeTag");
      console.log(item);
      console.log(tag);
      const path = "remove-tag";
      const payload = {
        url: item.url,
        tagname: tag,
      };
      console.log(payload);
      axios
        .post(path, payload)
        .then(() => {
          this.getPapers();
          console.log(this.items);
        })
        .catch((error) => {
          console.error(error);
        });
    },

    exportBib(item) {
      console.log("start exportBib");
      console.log(item);
      const path = "bib";
      const payload = {
        url: item.url,
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

    viewPaper(item) {

    },
  },

  created() {
    this.getPapers();
  },
};
</script>

<style>
.operation-wrapper .operation-icon {
  width: 20px;
  cursor: pointer;
}

.customize-table {
  --easy-table-header-font-size: 16px;
  --easy-table-body-row-font-size: 16px;
}
</style>