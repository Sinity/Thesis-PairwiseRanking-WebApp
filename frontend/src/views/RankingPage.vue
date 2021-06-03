<template>
  <div class="APIIntro">
    <h3>Ranking: {{ rankingId }}</h3>

    <Button class="p-mr-2 p-mb-2" @click="showSyncItems" type="submit" icon="pi pi-plus" label="Sync" />
    <Dialog v-if="ranking != null" :header="'Sync items from ' + ranking.datasource" v-model:visible="displaySyncModal" :style="{width: '50vw'}" :modal="true">
      <div v-if="ranking.datasource == 'anilist'" class="p-fluid">
        <div class="p-field p-grid">
          <label for="anilist_username" class="p-col-12 p-mb-2 p-md-2 p-mb-md-0">Username</label>
          <div class="p-col-12 p-md-10">
            <InputText v-model="anilist_username" id="anilist_username" type="text" placeholder="Username" />
          </div>
        </div>
        <div class="p-field p-grid">
            <label for="anilist_status" class="p-col-12 p-mb-2 p-md-2 p-mb-md-0">Status</label>
            <div class="p-col-12 p-md-10">
              <MultiSelect v-model="anilist_selected_statuses" :options="anilist_statusOptions" optionLabel="label" optionValue="value" placeholder="status" display="chip" />
            </div>
        </div>
      </div>

      <div v-if="ranking.datasource == 'steam'" class="p-fluid">
        <div class="p-field p-grid">
          <label for="steam_id" class="p-col-12 p-mb-2 p-md-2 p-mb-md-0">Steam ID</label>
          <div class="p-col-12 p-md-10">
            <InputText v-model="steam_id" id="steam_id" type="text" placeholder="Steam ID" />
          </div>
        </div>
      </div>

      <template #footer>
        <Button label="Submit" icon="pi pi-check" @click="syncItems" autofocus />
      </template>
    </Dialog>

    <Button class="p-mr-2 p-mb-2" @click="$router.push(`/compare/${rankingId}`)" type="submit" icon="pi pi-arrow-right" label="Compare" />

    <DataTable :value="items">
        <Column field="img_url" header="Image">
          <template #body="slotProps">
              <img :src="slotProps.data.img_url" :alt="slotProps.data.img_url" width="80"/>
          </template>
        </Column>
        <Column :sortable="true" field="label" header="Label"></Column>
        <Column :sortable="true" field="curr_rating" header="Current rating"></Column>
        <Column :sortable="true" field="init_rating" header="Initial rating"></Column>
        <Column :sortable="true" field="stderr" header="Standard error"></Column>
    </DataTable>
  </div>
</template>

<script>
import { REST } from "../rest.js";
export default {
  data: function() {
    return {
      ranking: null,
      rankingId: "",
      
      displaySyncModal: false,
      steam_id: "",
      anilist_username: "",
      anilist_selected_statuses: null,
      anilist_statusOptions: [
          {label: 'Current', value: 'CURRENT'},
          {label: 'Planning', value: 'PLANNING'},
          {label: 'Paused', value: 'PAUSED'},
          {label: 'Completed', value: 'COMPLETED'},
          {label: 'Dropped', value: 'DROPPED'},
          {label: 'Repeating', value: 'REPEATING'}
      ],

      items: [
      ]
    };
  },
  methods: {
    async refreshList() {
      const resp = await REST.get("/ranking/" + this.rankingId);
      const respJSON = await resp.json();
      this.ranking = respJSON.ranking;
      this.items = respJSON.ranking.items;
    },

    showSyncItems() {
      this.username = "";
      this.anilist_selected_statuses = null;
      this.displaySyncModal = true;
    },
    async syncItems() {
      let params = {};
      params['anilist_username'] = this.anilist_username;
      if (this.anilist_selected_statuses != null)
        params['anilist_statuses'] = Array.from(this.anilist_selected_statuses);
      params['steam_id'] = this.steam_id

      await REST.post("/ranking/" + this.rankingId, params);
      this.refreshList();
      this.displaySyncModal = false;
    }
  },
  created: async function() {
    this.rankingId = this.$route.params.id;
    this.refreshList();
  }
};
</script>

<style lang="scss" scoped>

</style>
