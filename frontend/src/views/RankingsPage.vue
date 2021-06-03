<template>
  <div class="APIIntro">
    <Dialog header="Create ranking" v-model:visible="displayCreateRankingModal" :style="{width: '50vw'}" :modal="true">
      <div class="p-fluid">
        <div class="p-field p-grid">
          <div class="p-col-12 p-md-10">
            <InputText v-model="name" id="name" type="text" placeholder="Name" />
          </div>
        </div>
        <div class="p-field p-grid">
            <div class="p-col-12 p-md-10">
              <Dropdown v-model="datasource" :options="datasourceOptions" optionLabel="label" optionValue="value" placeholder="Datasource"/>
            </div>
        </div>
      </div>

      <template #footer>
        <Button label="Submit" icon="pi pi-check" @click="createRanking" autofocus />
      </template>
    </Dialog>

    <Dialog header="Modify ranking" v-model:visible="displayModifyRankingModal" :style="{width: '50vw'}" :modal="true">
      <div class="p-formgroup-inline">
        <div class="p-field">
          <label for="name" class="p-sr-only">Name</label>
          <InputText v-model="name" id="name" type="text" placeholder="Name" />
        </div>
      </div>

      <template #footer>
        <Button label="Submit" icon="pi pi-check" @click="modifyRanking" autofocus />
      </template>
    </Dialog>
        
    <div class="card">
      <DataView :value="rankings" :layout="layout" :paginator="true" :rows="9" :sortOrder="sortOrder" :sortField="sortField">
        <template #header>
          <div class="p-grid p-nogutter">
            <div class="p-col-2" style="text-align: left">
              <Dropdown v-model="sortKey" :options="sortOptions" optionLabel="label" placeholder="Sort by" @change="onSortChange($event)"/>
            </div>
            <div class="p-col-8" style="text-align: center">
              <Button @click="showCreateRanking" type="submit" icon="pi pi-plus" label="Create new" />
            </div>
            <div class="p-col-2" style="text-align: right">
              <DataViewLayoutOptions v-model="layout" />
            </div>
          </div>
        </template>

        <template #list="slotProps">
          <div class="p-col-12">
            <div class="product-list-item">
              <img :src="`${baseURL}${slotProps.data.datasource}.png`" :alt="slotProps.data.datasource"/>
              <div class="product-list-detail">
                <i class="pi pi-tag product-category-icon"></i><span class="product-category">{{slotProps.data.datasource}}</span>
                <div class="product-name">{{slotProps.data.name}}</div>
                <div class="product-description">{{slotProps.data.id}}</div>
                <div><span :class="'product-badge status-'+slotProps.data.datasource.toLowerCase()">{{slotProps.data.item_count}} items</span></div>
              </div>
              <div class="product-list-action">
                <Button class="" @click="$router.push(`/ranking/${slotProps.data.id}`)" type="submit" icon="pi pi-bars" label="Items" />
                <Button class="p-button-warning" @click="showModifyRanking(slotProps.data)" type="submit" icon="pi pi-pencil" label="Edit"/>
                <Button class="p-button-danger" icon="pi pi-trash" label="Delete" @click="deleteRanking(slotProps.data.id)" />
              </div>
            </div>
          </div>
        </template>

        <template #grid="slotProps">
          <div class="p-col-12 p-md-4">
            <div class="product-grid-item card">
              <div class="product-grid-item-top">
                <div>
                  <i class="pi pi-tag product-category-icon"></i>
                  <span class="product-category">{{slotProps.data.datasource}}</span>
                </div>
                <span :class="'product-badge status-'+slotProps.data.datasource.toLowerCase()">{{slotProps.data.item_count}} items</span>
              </div>
              <div class="product-grid-item-content">
                <img :src="`${baseURL}${slotProps.data.datasource}.png`" :alt="slotProps.data.datasource"/>
                <div class="product-name">{{slotProps.data.name}}</div>
                <div class="product-description">{{slotProps.data.id}}</div>
              </div>
              <div class="product-grid-item-bottom">
                <Button class="" @click="$router.push(`/ranking/${slotProps.data.id}`)" type="submit" icon="pi pi-bars" />
                <Button class="p-button-warning" @click="showModifyRanking(slotProps.data)" type="submit" icon="pi pi-pencil" />
                <Button class="p-button-danger" icon="pi pi-trash" @click="deleteRanking(slotProps.data.id)" />
              </div>
            </div>
          </div>
        </template>
      </DataView>
    </div>

  </div>
</template>

<script>
import { REST } from "../rest.js";
export default {
  data: function() {
    return {
      rankings: null,
      baseURL: process.env.BASE_URL,
      
      displayCreateRankingModal: false,
      displayModifyRankingModal: false,
      rankingId: "",
      name: "",
      datasourceOptions: [
          {label: 'Steam', value: 'steam'},
          {label: 'Anilist', value: 'anilist'}
      ],
      datasource: "steam",

      layout: 'grid',
      sortKey: null,
      sortOrder: null,
      sortField: null,
      sortOptions: [
          {label: 'Item count High to Low', value: '!item_count'},
          {label: 'Item count Low to High', value: 'item_count'},
          {label: 'Name High to Low', value: '!name'},
          {label: 'Name Low to High', value: 'name'},
          {label: 'ID High to Low', value: '!id'},
          {label: 'ID Low to High', value: 'id'},
      ]
    };
  },
  methods: {
    async refreshRankings() {
      const resp = await REST.get("/ranking");
      const respJSON = await resp.json();
      this.rankings = respJSON.rankings;
    },

    showCreateRanking() {
      this.name = "";
      this.datasource = "";
      this.displayCreateRankingModal = true;
    },
    showModifyRanking(ranking) {
      this.rankingId = ranking.id;
      this.name = ranking.name;
      this.displayModifyRankingModal = true;
    },

    async createRanking() {
      const res = await REST.post("/ranking", {
        name: this.name,
        source: this.datasource 
      });
      const resJSON = await res.json();
      this.resp = resJSON;

      this.displayCreateRankingModal = false;
      this.refreshRankings();
    },

    async modifyRanking() {
      const res = await REST.put("/ranking/" + this.rankingId, {
        name: this.name,
      });
      const resJSON = await res.json();
      this.resp = resJSON;

      this.displayModifyRankingModal = false;
      this.refreshRankings();
    },

    async deleteRanking(rankingID) {
      console.log("Delete ranking: " + rankingID);

      const res = await REST.del("/ranking/" + rankingID);
      const resJSON = await res.json();
      this.resp = resJSON;

      this.refreshRankings();
    },

    onSortChange(event){
        const value = event.value.value;
        const sortValue = event.value;

        if (value.indexOf('!') === 0) {
            this.sortOrder = -1;
            this.sortField = value.substring(1, value.length);
            this.sortKey = sortValue;
        }
        else {
            this.sortOrder = 1;
            this.sortField = value;
            this.sortKey = sortValue;
        }
    }
  },
  created: async function() {
    this.refreshRankings();
  }
};
</script>

<style lang="scss" scoped>

.p-button {
    margin: 0.3rem .5rem;
    min-width: 10rem;
}

p {
    margin: 0;
}

.confirmation-content {
    display: flex;
    align-items: center;
    justify-content: center;
}

.p-dialog .p-button {
    min-width: 6rem;
}

.card {
    padding: 2rem;
    box-shadow: 0 2px 1px -1px rgba(0,0,0,.2), 0 1px 1px 0 rgba(0,0,0,.14), 0 1px 3px 0 rgba(0,0,0,.12);
    border-radius: 4px;
    margin-bottom: 2rem;
}
.p-dropdown {
    width: 18rem;
    font-weight: normal;
}

.product-name {
	font-size: 2rem;
	font-weight: 700;
}

.product-description {
	margin: 0 0 1rem 0;
}

.product-category-icon {
	vertical-align: middle;
	margin-right: .5rem;
}

.product-category {
	font-weight: 600;
	vertical-align: middle;
}

::v-deep(.product-list-item) {
	display: flex;
	align-items: center;
	padding: 1rem;
	width: 100%;

	img {
		width: 50px;
		box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
		margin-right: 2rem;
	}

	.product-list-detail {
		flex: 1 1 0;
	}

	.p-rating {
		margin: 0 0 .5rem 0;
	}

	.product-price {
		font-size: 1.5rem;
		font-weight: 600;
		margin-bottom: .5rem;
		align-self: flex-end;
	}

	.product-list-action {
		display: flex;
		flex-direction: column;
	}

	.p-button {
		margin-bottom: .5rem;
	}
}

::v-deep(.product-grid-item) {
	margin: .5rem;
	border: 1px solid #dee2e6;

	.product-grid-item-top {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
	.product-grid-item-bottom {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	img {
		box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
		margin: 2rem 0;
	}

	.product-grid-item-content {
		text-align: center;
	}

	.product-price {
		font-size: 1.5rem;
		font-weight: 600;
	}
}

@media screen and (max-width: 576px) {
	.product-list-item {
		flex-direction: column;
		align-items: center;

		img {
			margin: 2rem 0;
		}

		.product-list-detail {
			text-align: center;
		}

		.product-price {
			align-self: center;
		}

		.product-list-action {
			display: flex;
			flex-direction: column;
		}

		.product-list-action {
			margin-top: 2rem;
			flex-direction: row;
			justify-content: space-between;
			align-items: center;
			width: 100%;
		}
	}
}
</style>
