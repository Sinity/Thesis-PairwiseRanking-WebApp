<template>
  <div class="APIIntro">
    <Toast />
    <div v-if="user == null" class="p-formgroup-inline">
        <div class="p-field">
            <label for="email" class="p-sr-only">User</label>
            <InputText v-model="email" id="email" type="text" placeholder="User" />
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
      email: "",
      password: ""
    };
  },
  methods: {
    async login() {
      const resp = await REST.login(this.email, this.password);
      console.log('werehere', resp);
      if (resp != '')
        this.$toast.add({severity:'error', summary: 'Login failed', detail: resp, life: 2000});
      else
        this.$toast.add({severity:'success', summary: 'Logged in!', detail: '', life: 2000});
      this.user = REST.userIdentity();
    },
    async register() {
      const res = await REST.post("/auth/user", {
        email: this.email,
        password: this.password
      });
      const resJSON = await res.json();
      if (res.ok)
        this.$toast.add({severity:'success', summary: 'Registered new account', detail: resJSON['message'], life: 4000});
      else
        this.$toast.add({severity:'error', summary: 'Registration failed', detail: resJSON['message'], life: 3000});
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
