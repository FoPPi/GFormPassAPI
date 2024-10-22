import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "GFormPassAPI",
  description: "This project is a api for Google Form Assistant designed to process AI functionalities.",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    logo: '/logo.png',
    nav: [
      { text: 'Home', link: '/' },
    ],

    sidebar: [
      {
        text: 'Getting Started',
        items: [
          { text: 'Quickstart', link: '/quickstart' },
          { text: 'Endpoints', link: '/endpoints' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/FoPPi/GFormPassAPI' }
    ],

    footer: {
      message: 'Released under the Reciprocal Public License 1.5 (RPL1.5).',
      copyright: 'Copyright © 2001-2024 Technical Pursuit Inc., All Rights Reserved.'
    }

  }
})
