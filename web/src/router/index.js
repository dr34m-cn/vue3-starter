import { createRouter, createWebHashHistory } from "vue-router";
import layout from "@/views/layout.vue";
const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: "/",
      component: () => import("@/views/index.vue"),
    },
    {
      path: "/login",
      component: () => import("@/views/login.vue"),
    },
    {
      path: "/home",
      component: layout,
      children: [
        {
          path: "",
          component: () => import("@/views/pages/home/index.vue"),
          meta: {
            leftIndex: "/home",
          },
        },
      ],
    },
    {
      path: "/users",
      component: layout,
      children: [
        {
          path: "",
          component: () => import("@/views/pages/users/index.vue"),
          meta: {
            leftIndex: "/users",
          },
        },
      ],
    },
  ],
});

export default router;
