<template>
  <div class="APIIntro">
    <h3>{{ vueGreeting }}</h3>
    <h3>{{ flaskGreeting }}</h3>
    <Button @click="greetingRequest" type="submit" label="Hail" />
  </div>
</template>

<script>
import { REST } from "../rest.js";
export default {
  data: function() {
    return {
      vueGreeting: "Vue says hi!",
      flaskGreeting: "<Flask didn't respond yet>",
    };
  },
  methods: {
    async greetingRequest() {
      const resp = await REST.get("/greeting");
      const respJSON = await resp.json();
      this.flaskGreeting = respJSON.message;
    }
  },
  created: async function() {}
};
</script>
