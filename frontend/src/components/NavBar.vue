<script setup>
import { ref, onMounted } from "vue";
import { getCurrentUser } from "@/utils/auth.js";

const user = ref(null);

onMounted(async () => {
  user.value = await getCurrentUser();
});
</script>

<template>
  <q-header reveal elevated class="bg-grey-10 text-white" height-hint="98">
    <q-toolbar>
      <q-toolbar-title> HabiTrack </q-toolbar-title>
    </q-toolbar>

    <q-tabs align="left">
      <q-route-tab :to="{ name: 'home' }" label="Home" />
      <q-route-tab :to="{ name: 'templates' }" label="Templates" />
      <q-route-tab :to="{ name: 'subscriptions' }" label="Subscriptions" />
      <q-route-tab
        v-if="user"
        :to="{ name: 'my-profile', params: { id: user.id } }"
        :label="user.username"
      />
      <q-route-tab v-if="user" :to="{ name: 'logout' }" label="Logout" />
      <q-route-tab v-else :to="{ name: 'login' }" label="Login" />
    </q-tabs>
  </q-header>
</template>

<style scoped></style>
