import { defineConfig } from "vitepress";

export default defineConfig({
  title: "Dashboard",
  description: "Documentación técnica del proyecto",
  themeConfig: {
    nav: [
      { text: "Inicio", link: "/" },
      { text: "Infraestructura", link: "/infrastructure/orchestration" },
    ],
    sidebar: [
      {
        text: "Infraestructura",
        items: [
          { text: "Orquestación", link: "/infrastructure/orchestration" },
        ],
      },
    ],
  },
});
