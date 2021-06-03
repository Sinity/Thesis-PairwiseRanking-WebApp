<template>
  <div class="APIIntro">
    <Button class="p-mr-2 p-mb-2" @click="$router.push(`/ranking/${rankingId}`)" type="submit" icon="pi pi-arrow-left" label="Ranking info" />

    <div class="p-grid" v-if="item1 != null && item2 != null && !disabled">
      <div class="p-col">
        <Panel @click="sendComparison(item1.id, item2.id)">
          <template #header>
            <h2>{{ item1.label }}</h2>
          </template>
          <img :src="item1.img_url" :alt="item1.label" />
        </Panel>
      </div>
      <div class="p-col">
        <Panel @click="sendComparison(item2.id, item1.id)">
          <template #header>
            <h2>{{ item2.label }}</h2>
          </template>
          <img :src="item2.img_url" :alt="item2.label" />
        </Panel>
      </div>
    </div>
  </div>
</template>

<script>
import { REST } from "../rest.js";
export default {
  data: function() {
    return {
      disabled: false,
      rankingId: "",
      item1: null,
      item2: null
    };
  },
  methods: {
    async refreshData() {
      const resp = await REST.get("/compare/" + this.rankingId);
      const respJSON = await resp.json();
      this.item1 = respJSON.comparison[0];
      this.item2 = respJSON.comparison[1];
    },
    async sendComparison(winitemId, loseitemId) {
      this.disabled = true;
      const res = await REST.post("/compare/" + this.rankingId, {
        winitem: winitemId,
        loseitem: loseitemId
      });
      await res.json();
      await this.refreshData();
      this.disabled = false;
    }
  },
  created: async function() {
    this.rankingId = this.$route.params.id;
    this.refreshData();
  }
};
</script>

<style lang="scss" scoped>

</style>
