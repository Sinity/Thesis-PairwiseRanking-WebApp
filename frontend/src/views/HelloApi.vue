<template>
  <div class="APIIntro">
    <h1>{{ vueGreeting }}</h1>
    <h1>{{ flaskGreeting }}</h1>

    <InputText type="text" v-model="text"/>
    <Button type="submit" label="Submit"/>
  </div>
</template>

<script>
  export default {
    data: function() {
      return {
        vueGreeting: 'Vue says hi!',
        flaskGreeting: "<Flask didn't respond yet>"
      }
    },
    created: async function() {
      const gResponse = await fetch("http://localhost:5000/greeting");
      const gObject = await gResponse.json();
      this.flaskGreeting = gObject.greeting;
    }
  }
</script>
