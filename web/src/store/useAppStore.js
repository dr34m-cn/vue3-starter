import { defineStore } from "pinia";

export const useAppStore = defineStore("app", {
  state: () => ({
    user: null,
    login: null,
    leftIndex: "/home",
  }),

  actions: {
    set(key, value) {
      this[key] = value;
    },
  },

  // 持久化配置
  persist: {
    storage: localStorage,
    pick: ["user", "login"],
  },
});
