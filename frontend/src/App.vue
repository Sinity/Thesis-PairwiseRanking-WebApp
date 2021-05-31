<template>
  <div id="nav">
    <Menubar :model="items" />
  </div>
  <div id="page">
    <router-view />
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      items: [
        { label: 'Home', to: '/' },
        { label: 'Medialists', to: '/lists' },
        { label: 'Account', to: '/login' }
      ]
    };
  },
  methods: {},
  created: async function() {}
};
</script>

<style>
body {
    max-width: 1200px;
    margin: 0 auto !important;
    float: none !important;
    height: 100%;
    overflow-x: hidden;
    overflow-y: auto;
    background-color: var(--surface-f);
    font-family: var(--font-family);
    font-weight: 400;
    color: var(--text-color);
    word-break: break-all;
    white-space: normal;
}

#nav {
  padding: 30px;
  text-align: center;
  background-color: var(--surface-a);
}

#page {
  background-color: var(--surface-b);
  padding:30px;
}

#nav a {
  font-weight: bold;
  font-size: 24px;
  color: var(--secondary-color);

}

#nav a.router-link-exact-active {
  /*color: #42b983;*/
  color: var(--primary-color);
}
</style>
