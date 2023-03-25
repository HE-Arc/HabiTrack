<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

const username = ref(null);
const id = ref(null);

const fetchCurrentUser = async () => {
  axios
    .get("current_user/", {
      withCredentials: true,
    })
    .then((response) => {
      console.log(response.data);
      if (response.data.success) {
        username.value = response.data.username;
        id.value = response.data.id;
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

onMounted(() => {
  fetchCurrentUser();
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
        v-if="username"
        :to="{ name: 'profile', params: { id: id } }"
        :label="username"
      />
      <q-route-tab v-if="username" :to="{ name: 'logout' }" label="Logout" />
      <q-route-tab v-else :to="{ name: 'login' }" label="Login" />
    </q-tabs>
  </q-header>
</template>

<style scoped></style>
