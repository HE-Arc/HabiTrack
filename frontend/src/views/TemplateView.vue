<script setup>
import { ref, onMounted } from "vue";
import ErrorBanner from "../components/ErrorBanner.vue";
import TemplateComponent from "../components/TemplateComponent.vue";

// Import necessary custom tools
import { getCurrentUsername } from "@/utils/auth.js";
import { templateAction } from "@/utils/template.js";

const templates = ref([]);
const username = ref(null);

// We need error handling
const errors = ref(null);

onMounted(async () => {
  username.value = await getCurrentUsername();
  const response = await templateAction("get");
  if (response == null) {
    errors.value = "Couldn't fetch templates.";
  } else if (response.success) {
    templates.value = response.data;
  } else if (response.errors) {
    errors.value = response.errors;
  }
});
</script>

<template>
  <q-page padding>
    <ErrorBanner :errors="errors" />
    <div class="q-pa-md">
      <q-btn
        class="q-ma-auto"
        color="primary"
        :to="{ name: 'templates.create' }"
      >
        <q-icon left name="mdi-plus-box" />
        <q-label for="add_template">Create a new template</q-label>
      </q-btn>
    </div>

    <div class="q-pa-md items-start q-gutter-md">
      <q-card
        class="template-card q-pa-sm"
        style="background: radial-gradient(circle, #35a2ff 0%, #014a88 100%)"
        v-for="(template, index) in templates"
        :key="index"
        flat
        bordered
      >
        <TemplateComponent :propTemplate="template" :username="username" />
      </q-card>
    </div>
  </q-page>
</template>

<style lang="sass" scoped>
.template-card
  width: 100%
  height: 100%
  max-width: 20rem
</style>
