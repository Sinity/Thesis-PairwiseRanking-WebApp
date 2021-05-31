import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../views/HomePage.vue";
import LoginPage from "../views/LoginPage.vue";
import MedialistsPage from "../views/MedialistsPage.vue";
import { REST } from "../rest.js";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomePage
  },
  {
    path: "/login",
    name: "Login",
    component: LoginPage
  },
  {
    path: "/lists",
    name: "Medialists",
    component: MedialistsPage
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  const publicPages = ['/login'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = (REST.userIdentity() !== null);

  if (authRequired && !loggedIn) {
    return next('/login');
  }

  next();
})

export default router;
