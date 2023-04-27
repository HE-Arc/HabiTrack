<script setup>
import { ref, onMounted } from "vue";
import ErrorBanner from "./ErrorBanner.vue";
import TemplateComponent from "./TemplateComponent.vue";

// Import necessary custom tools
import { getCurrentUsername } from "@/utils/auth.js";
import { templateAction } from "@/utils/template.js";
import { fetchTemplates } from "@/utils/template.js";
import { fetchSubscriptions } from "@/utils/subscription.js";

const props = defineProps({
  showSubscriptions: {
    type: Boolean,
    default: false,
  },
  showEdit: {
    type: Boolean,
    default: false,
  },
});

const templates = ref([]);
const username = ref(null);
const showEntry = ref(false);
const errors = ref(null);
const notif = ref(null);

onMounted(async () => {
  username.value = await getCurrentUsername();
  let response;
  if (!props.showSubscriptions && !props.showEdit) {
    response = await templateAction("get");
  } else if (props.showSubscriptions && username.value) {
    response = await fetchSubscriptions(username.value);
    showEntry.value = true;
  } else if (props.showSubscriptions && !username.value) {
    errors.value = "You must be logged in to view your subscriptions.";
  } else if (props.showEdit && username.value) {
    response = await fetchTemplates(username.value);
  } else if (props.showEdit && !username.value) {
    errors.value = "You must be logged in to view your editables.";
  }
  if (response == null) {
    errors.value = "Couldn't fetch templates.";
  } else if (response.success && response.data === 0) {
    notif.value = "No templates found.";
  } else if (response.success && response.data.length === 0) {
    notif.value = "No subscriptions found.";
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
    <p v-if="notif">{{ notif }}</p>
    <div class="row justify-center">
      <div
        class="q-mx-md q-mt-md"
        v-for="(template, index) in templates"
        :key="index"
      >
        <q-card
          style="background: radial-gradient(circle, #35a2ff 0%, #014a88 100%)"
          class="template-card"
          flat
          bordered
        >
          <TemplateComponent
            :propTemplate="template"
            :username="username"
            :showEdit="showEdit"
            :showEntry="showEntry"
          />
        </q-card>
      </div>
    </div>
  </q-page>
</template>
