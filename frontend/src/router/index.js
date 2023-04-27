import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/register",
      name: "register",
      component: () => import("../views/AuthView.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/AuthView.vue"),
    },
    {
      path: "/my-profile",
      name: "my-profile",
      component: () => import("../views/UserProfileView.vue"),
    },
    {
      path: "/change-password",
      name: "change-password",
      component: () => import("../views/ChangePasswordView.vue"),
    },
    {
      path: "/templates",
      name: "templates",
      component: () => import("../views/TemplatesView.vue"),
    },
    {
      path: "/templates/create",
      name: "templates.create",
      component: () => import("../views/CreateTemplateView.vue"),
    },
    {
      path: "/subscriptions",
      name: "subscriptions",
      component: () => import("../views/SubscriptionsView.vue"),
    },
    {
      path: "/edits",
      name: "edits",
      component: () => import("../views/EditsView.vue"),
    },
    {
      path: "/about",
      name: "about",
      component: () => import("../views/AboutView.vue"),
    },
  ],
});

export default router;
