<script>
import axios from "axios";
export default {
  name: "RecentHistory",
  components: {
  },

  data() {
    return {
      papers: null,
      headers: 
        [
          { text: "Title", value: "title", sortable: true },
          { text: "Authors", value: "authors" },
          { text: "URL", value: "url", sortable: true },
          { text: "Year", value: "year", sortable: true },
          { text: "Subjects", value: "subjects" },
        ],
    };
  },
  methods: {
    getRecentHistory() {
      console.log("start getRecentHistory");
      const path = "recent-papers";
      axios
        .get(path)
        .then((res) => {
          this.papers = res.data;
          console.log(res.data);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },

  created() {
    this.getRecentHistory();
  }
}
</script>


<template>
  <v-card>
    <v-card-title>
      Recent History
    </v-card-title>
    <v-table :headers="headers" :items="papers" item-key="url" class="table-rounded" hide-default-footer disable-sort>
      <thead>
        <tr>
          <th v-for="header in headers" :key="header">
            {{ header.text }}
          </th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="paper in papers" :key="paper.url">

          <td>
            <div class="d-flex flex-column">
              <span class="d-block font-weight-semibold text--primary text-truncate">{{ paper.title }}</span>
            </div>
          </td>

          <td v-text="paper.authors.join()" />
          <td v-text="paper.url"></td>
          <td v-text="paper.year" />
          <td v-text="paper.subjects.join()" />
        </tr>
      </tbody>
    </v-table>
  </v-card>
</template>
