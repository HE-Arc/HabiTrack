<script setup>
import TemplatesViewComponent from "../components/TemplatesViewComponent.vue";
import { getCurrentUsername } from "../utils/auth";
import { ref, onMounted } from "vue";
import router from "@/router";

const username = ref({});

const createClicked = async () => {
  username.value = await getCurrentUsername();
  if (username.value) {
    router.push({ name: "templates.create" });
  } else {
    router.push({ name: "login" });
  }
};

onMounted(async () => {
  username.value = await getCurrentUsername();
});
</script>
<template>
  <div v-if="username" class="q-pa-md">
    <q-btn class="q-ma-auto" color="primary" v-on:click="createClicked">
      <q-icon left name="mdi-plus-box" />
      <q-label for="add_template">Create a new template</q-label>
    </q-btn>
  </div>
  <div v-else class="q-pa-md">
    <q-btn class="q-ma-auto" color="primary" :to="{ name: 'login' }">
      <q-icon left name="mdi-login" />
      <q-label for="login">Login to create a template</q-label>
    </q-btn>
  </div>
  <TemplatesViewComponent :showSubscriptions="false" />
</template>
