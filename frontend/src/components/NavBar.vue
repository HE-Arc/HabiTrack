<script setup></script>

<template>
  <q-header reveal elevated class="bg-grey-10 text-white" height-hint="98">
    <q-toolbar>
      <q-toolbar-title> HabiTrack </q-toolbar-title>
    </q-toolbar>

    <q-tabs align="left">
      <q-route-tab :to="{ name: 'home' }" label="Home" />
      <q-route-tab :to="{ name: 'templates' }" label="Templates" />
    </q-tabs>
  </q-header>
</template>

<style scoped></style>
