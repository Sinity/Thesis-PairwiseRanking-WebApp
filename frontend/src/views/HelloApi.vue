<template>
  <div class="APIIntro">
    <h1>{{ vueGreeting }}</h1>
    <h1>{{ flaskGreeting }}</h1>

    <InputText type="text" v-model="text"/>
    <Button type="submit" label="Submit"/>

    <div class="p-d-flex p-flex-column">
        <div class="p-mb-2">Row 1</div>
        <div class="p-mb-2">Row 2</div>
        <div>Row 3</div>
    </div>
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
