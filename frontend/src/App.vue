<script setup>
import NavBar from "./components/NavBar.vue";
import { useQuasar } from "quasar";

const $q = useQuasar();
$q.dark.set(true);
</script>

<template>
  <q-layout view="lHh lpr lFf">
    <NavBar />
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<style scoped></style>
