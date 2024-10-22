---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "GFormPassAPI"
  text: 
  tagline: "This project is a api for Google Form Assistant designed to process AI functionalities."
  actions:
    - theme: brand
      text: Get Started
      link: /quickstart
    - theme: alt
      text: Endpoints
      link: /endpoints

features:
  - title: User Key Management
    details: Generate and activate user keys for secure API access.
  - title: Donation Handling
    details: Process and manage user donations with customizable amounts and currencies.
  - title: GPT Question Handling
    details: Send questions to GPT for automated processing and response.
  - title: Admin Controls
    details: Update user limits and manage expired questions efficiently.
---

<script setup>
import { VPTeamMembers } from 'vitepress/theme'

const members = [
  {
    avatar: 'https://avatars.githubusercontent.com/u/67471841?v=4',
    name: 'Mike',
    title: 'Developer',
    links: [
      { icon: 'github', link: 'https://github.com/FoPPi' },
      { icon: 'linkedin', link: 'https://www.linkedin.com/in/foppi' },
    ]
  },
  {
    avatar: 'https://avatars.githubusercontent.com/u/81939899?v=4',
    name: 'Denis',
    title: 'Developer',
    links: [
      { icon: 'github', link: 'https://github.com/DenisGas' },
      { icon: 'linkedin', link: 'www.linkedin.com/in/denis-gasilo' },
    ]
  },
]
</script>

---
# Our Team

Say hello to our awesome team.

<VPTeamMembers size="small" :members="members" />

