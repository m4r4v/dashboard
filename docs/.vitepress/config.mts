import { defineConfig } from "vitepress";

export default defineConfig({
  title: "Dashboard Docs",
  description: "Documentación técnica del proyecto",
  themeConfig: {
    nav: [
      { text: "Inicio", link: "/" },
      { text: "Guías Operativas", link: "/guides/troubleshooting" },
    ],
    sidebar: [
      {
        text: "Arquitectura",
        items: [
          { text: "Integración", link: "/architecture/integration" },
          { text: "Orquestación", link: "/infrastructure/orchestration" },
        ],
      },
      {
        text: "Backend",
        items: [
          { text: "Primeros Pasos", link: "/backend/getting-started" },
          { text: "Gobernanza", link: "/backend/governance" },
        ],
      },
      {
        text: "Frontend",
        items: [{ text: "Gobernanza", link: "/frontend/governance" }],
      },
      {
        text: "Guías y Soporte",
        items: [{ text: "Troubleshooting", link: "/guides/troubleshooting" }],
      },
    ],
  },
});
