import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "../views/LoginPage.vue";
import RankingsPage from "../views/RankingsPage.vue";
import RankingPage from "../views/RankingPage.vue";
import ComparePage from "../views/ComparePage.vue";
import { REST } from "../rest.js";

const routes = [
  {
    path: "/login",
    name: "Login",
    component: LoginPage
  },
  {
    path: "/rankings",
    alias: "/",
    name: "Rankings",
    component: RankingsPage
  },
  {
    path: "/ranking/:id",
    name: "Ranking",
    component: RankingPage
  },
  {
    path: "/compare/:id",
    name: "Comparing",
    component: ComparePage
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
