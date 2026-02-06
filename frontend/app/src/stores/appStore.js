import { defineStore } from "pinia";
import { useTheme } from "vuetify";
import i18n from "@/plugins/i18n";

export const useAppStore = defineStore("app", {
  state: () => ({
    // Global States
    currentLanguage: localStorage.getItem("app_lang") || "en",
    isDarkMode: localStorage.getItem("app_theme") === "dark",
    isAuthenticated: !!localStorage.getItem("user_token"),
  }),

  actions: {
    /**
     * Toggles between Light and Dark themes.
     * Updates Vuetify instance and persistence.
     */
    toggleTheme(vuetifyTheme) {
      this.isDarkMode = !this.isDarkMode;
      const themeValue = this.isDarkMode ? "dark" : "light";
      vuetifyTheme.global.name.value = themeValue;
      localStorage.setItem("app_theme", themeValue);
    },

    /**
     * Sets global language for i18n and persistence.
     */
    setLanguage(lang) {
      this.currentLanguage = lang;
      i18n.global.locale.value = lang;
      localStorage.setItem("app_lang", lang);
    },

    setAuth(status) {
      this.isAuthenticated = status;
    },
  },
});
