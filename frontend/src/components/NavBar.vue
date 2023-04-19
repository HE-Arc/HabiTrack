<script setup>
import { ref, onMounted } from "vue";
import { Notify } from "quasar";
import { logout } from "@/utils/auth.js";
import { getCurrentUsername } from "@/utils/auth.js";
import router from "@/router";

const logoutReturn = ref(null);
const username = ref(null);

const submit = async () => {
  logoutReturn.value = await logout();
  if (logoutReturn.value.success) {
    Notify.create({
      message: "Logged out",
      color: "negative",
      position: "top",
    });
    setTimeout(() => {
      router.push({ name: "templates" });
    }, 1000);
  }
};

onMounted(() => {
  // Call a function everytime the router changes
  router.afterEach(async (to, from) => {
    username.value = await getCurrentUsername();
  });
});
</script>

<template>
  <q-header reveal elevated class="bg-grey-10 text-white" height-hint="98">
    <q-toolbar>
      <q-toolbar-title> HabiTrack </q-toolbar-title>
    </q-toolbar>

    <q-tabs align="left">
      <q-route-tab :to="{ name: 'home' }" label="Home" />
      <q-route-tab :to="{ name: 'templates' }" label="All Templates" />
      <q-route-tab
        v-if="username"
        :to="{ name: 'subscriptions' }"
        label="Subscriptions"
      />
      <q-route-tab
        v-if="username"
        :to="{ name: 'edits' }"
        label="My Templates"
      />

      <q-route-tab v-if="username" :to="{ name: 'my-profile' }">
        {{ username }}
      </q-route-tab>

      <q-route-tab v-if="!username" :to="{ name: 'login' }" label="Login" />

      <q-tab v-if="username" :to="{ name: 'logout' }" @click="submit">
        Logout
      </q-tab>
    </q-tabs>
  </q-header>
</template>

<style scoped></style>
