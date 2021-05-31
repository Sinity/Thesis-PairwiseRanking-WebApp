<template>
  <div class="APIIntro">
    <h3>{{ vueGreeting }}</h3>
    <h3>{{ flaskGreeting }}</h3>
    <p>{{ resp }}</p>
    <Button @click="greetingRequest" type="submit" label="Hail" />
    <Button @click="rankingRequest" type="submit" label="Ranking?" />
    <Button @click="createRanking" type="submit" label="Create" />

    <div class="card">
        <DataView :value="rankings" :layout="layout" :paginator="true" :rows="9" :sortOrder="sortOrder" :sortField="sortField">
			<template #header>
                <div class="p-grid p-nogutter">
                    <div class="p-col-6" style="text-align: left">
                        <Dropdown v-model="sortKey" :options="sortOptions" optionLabel="label" placeholder="Sort By Price" @change="onSortChange($event)"/>
                    </div>
                    <div class="p-col-6" style="text-align: right">
                        <DataViewLayoutOptions v-model="layout" />
                    </div>
                </div>
			</template>

			<template #list="slotProps">
				<div class="p-col-12">
					<div class="product-list-item">
						<img src="https://www.primefaces.org/wp-content/uploads/2020/05/placeholder.png" :alt="slotProps.data.name"/>
						<div class="product-list-detail">
							<div class="product-name">{{slotProps.data.name}}</div>
							<div class="product-description">{{slotProps.data.datasource}}</div>
							<!-- <Rating :modelValue="slotProps.data.rating" :readonly="true" :cancel="false"></Rating> -->
							<!-- <i class="pi pi-tag product-category-icon"></i><span class="product-category">{{slotProps.data.category}}</span> -->
						</div>
						<div class="product-list-action">
							<!-- <span class="product-price">${{slotProps.data.price}}</span> -->
							<Button icon="pi pi-shopping-cart" label="Add to Cart" :disabled="slotProps.data.inventoryStatus === 'OUTOFSTOCK'"></Button>
							<span :class="'product-badge status-'+slotProps.data.inventoryStatus.toLowerCase()">{{slotProps.data.inventoryStatus}}</span>
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
							<!-- <span :class="'product-badge status-'+slotProps.data.inventoryStatus.toLowerCase()">{{slotProps.data.inventoryStatus}}</span> -->
						</div>
						<div class="product-grid-item-content">
							<img src="https://www.primefaces.org/wp-content/uploads/2020/05/placeholder.png" :alt="slotProps.data.name"/>
							<div class="product-name">{{slotProps.data.name}}</div>
							<!-- <div class="product-description">{{slotProps.data.description}}</div> -->
							<Rating :modelValue="slotProps.data.rating" :readonly="true" :cancel="false"></Rating>
						</div>
						<div class="product-grid-item-bottom">
							<!-- <span class="product-price">${{slotProps.data.price}}</span> -->
							<Button icon="pi pi-shopping-cart" :disabled="slotProps.data.inventoryStatus === 'OUTOFSTOCK'"></Button>
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
      vueGreeting: "Vue says hi!",
      flaskGreeting: "<Flask didn't respond yet>",
      resp: "",

      rankings: null,
      layout: 'grid',
      sortKey: null,
      sortOrder: null,
      sortField: null,
      sortOptions: [
          {label: 'Price High to Low', value: '!price'},
          {label: 'Price Low to High', value: 'price'},
      ]
    };
  },
  methods: {
    async greetingRequest() {
      const resp = await REST.get("/greeting");
      const respJSON = await resp.json();
      this.flaskGreeting = respJSON.message;
    },
    async rankingRequest() {
      const resp = await REST.get("/ranking");
      const respJSON = await resp.json();
      this.resp = respJSON;
      this.rankings = respJSON.rankings;
    },
    async createRanking() {
      const res = await REST.post("/ranking", {
        name: "sumname",
        source: "animu" 
      });
      const resJSON = await res.json();
      this.resp = resJSON;
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
  created: async function() {}
};
</script>

<style lang="scss" scoped>
.card {
    background: #ffffff;
    padding: 2rem;
    box-shadow: 0 2px 1px -1px rgba(0,0,0,.2), 0 1px 1px 0 rgba(0,0,0,.14), 0 1px 3px 0 rgba(0,0,0,.12);
    border-radius: 4px;
    margin-bottom: 2rem;
}
.p-dropdown {
    width: 14rem;
    font-weight: normal;
}

.product-name {
	font-size: 1.5rem;
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

	.product-grid-item-top,
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
