<script setup>
import TemplatesViewComponent from "../components/TemplatesViewComponent.vue";
import { getCurrentUsername } from "../utils/auth";
import { ref, onMounted } from "vue";

const username = ref(null);

onMounted(() => {
  username.value = getCurrentUsername();
});
</script>
<template>
  <div v-if="username" class="q-pa-md">
    <q-btn class="q-ma-auto" color="primary" :to="{ name: 'templates.create' }">
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
