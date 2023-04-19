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
      <transition name="fade">
        <router-view />
      </transition>
    </q-page-container>
  </q-layout>
</template>

<style scoped>
.fade-enter-active {
  transition: opacity 0.5s;
}
.fade-leave-active {
  transition: opacity 0.5s;
  opacity: 0;
}
</style>
