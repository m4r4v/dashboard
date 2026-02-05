import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "Dashboard Docs",
  description: "Documentación técnica del proyecto",
  themeConfig: {
    nav: [
      { text: 'Inicio', link: '/' },
      { text: 'Infraestructura', link: '/infrastructure/orchestration' }
    ],
    sidebar: [
      {
        text: 'Arquitectura',
        items: [
          { text: 'Orquestación', link: '/infrastructure/orchestration' }
        ]
      },
      {
        text: 'Reglas de Desarrollo',
        items: [
          { text: 'Frontend Governance', link: '/frontend/governance' },
          { text: 'Backend Governance', link: '/backend/governance' }
        ]
      }
    ]
  }
})