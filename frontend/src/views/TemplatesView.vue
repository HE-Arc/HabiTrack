<script setup>
import TemplatesViewComponent from "../components/TemplatesViewComponent.vue";
</script>
<template>
  <div class="q-pa-md">
    <q-btn class="q-ma-auto" color="primary" :to="{ name: 'templates.create' }">
      <q-icon left name="mdi-plus-box" />
      <q-label for="add_template">Create a new template</q-label>
    </q-btn>
  </div>
  <TemplatesViewComponent :showSubscriptions="false" />
</template>
