<template>
  <div class="APIIntro">
    <div v-if="user == null" class="p-formgroup-inline">
        <div class="p-field">
            <label for="email" class="p-sr-only">Email</label>
            <InputText v-model="email" id="email" type="text" placeholder="Email" />
        </div>
        <div class="p-field">
            <label for="password" class="p-sr-only">Password</label>
            <InputText v-model="password" id="password" type="text" placeholder="Password" />
        </div>
        <Button @click="login" type="submit" label="Login" class="p-mr-2 p-mb-2" />
        <Button @click="register" type="submit" label="Register" class="p-mr-2 p-mb-2" />
    </div>

    <div v-if="user !== null">
      <h2>Logged in: {{ user.identity.email }}</h2>
      <Button @click="refresh" type="submit" label="Refresh token" class="p-mr-2 p-mb-2" />
      <Button @click="logout" type="submit" label="Logout" class="p-mr-2 p-mb-2" />

      <p><b>User id:</b> {{ user.identity.id }}</p>
      <p><b>Access token:</b> {{ user.accessToken }}</p>
      <p><b>Refresh token:</b> {{ user.refreshToken }}</p>
    </div>
  </div>
</template>

<script>
import { REST } from "../rest.js";
export default {
  data: function() {
    return {
      user: null,
      email: "ezo.dev@gmail.com",
      password: "pass"
    };
  },
  methods: {
    async login() {
      await REST.login(this.email, this.password);
      //const respAsJSON = await resp.json();
      this.user = REST.userIdentity();
    },
    async register() {
      const res = await REST.post("/auth/user", {
        email: this.email,
        password: this.password
      });
      const resJSON = await res.json();
      console.log(resJSON);
    },
    async refresh() {
      await REST.refreshToken();
      this.user = REST.userIdentity();
    },
    async logout() {
      REST.logout();
      this.user = null;
    }
  },
  created: async function() {
    this.user = REST.userIdentity();
  }
};
</script>
