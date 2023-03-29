<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import ErrorBanner from "../components/ErrorBanner.vue";
import Cookies from "js-cookie";

// Fecth all Template from DB
const templates = ref([]);

const fetchTemplates = async () => {
  const result = await axios.get("/templates/");

  templates.value = result.data;
};

let user = ref(null);

// We need error handling
const errors = ref(null);

const fetchCurrentUser = async () => {
  const result = await axios.get("/current_user/");
  user.value = result.data.user;
  console.log(user);
};

// Allow subscription to a new Template
const subscribe = async (template) => {
  console.log(Cookies.get("csrftoken"));
  await axios
    .post(`/users/${user_id}/subscribe/${template.id}/`, {})
    .then((response) => {
      // handle success response
      fetchTemplates();

      console.log(response.data);
    })
    .catch((error) => {
      // handle error response
      console.error(error);
    });
};

// Allow unsubscription from a Template
const unsubscribe = async (template) => {
  await axios
    .post(`/users/${user.value.id}/unsubscribe/${template.id}/`, {})
    .then((response) => {
      // handle success response
      fetchTemplates();

      console.log(response.data);
    })
    .catch((error) => {
      // handle error response
      console.error(error);
    });
};

const deleteTemplate = async (template) => {
  try {
    errors.value = null;

    await axios.delete(`/templates/${template.id}/`);

    // remove the template from the local array
    templates.value = templates.value.filter((t) => t.id !== template.id);
  } catch (err) {
    errors.value = err.message;
  }
};

onMounted(() => {
  fetchCurrentUser();
  fetchTemplates();
});
</script>

<template>
  <q-page padding>
    <ErrorBanner :errors="errors" />

    <q-btn id="add_template" color="primary" :to="{ name: 'templates.create' }">
      <q-icon left name="mdi-plus-box" />
      <q-label for="add_template">Create a new template</q-label>
    </q-btn>

    <div class="q-pa-md items-start q-gutter-md">
      <q-card
        class="template-card q-pa-sm"
        style="background: radial-gradient(circle, #35a2ff 0%, #014a88 100%)"
        v-for="(template, index) in templates"
        :key="index"
        flat
        bordered
      >
        <q-card-section class="text-center">
          <div class="text-h5">{{ template.name }}</div>
        </q-card-section>

        <q-card-section class="text-center">
          <div class="text-h6">{{ template.description }}</div>
        </q-card-section>

        <q-card-section class="text-center">
          <div class="text-h6">{{ template.option_1 }}</div>
        </q-card-section>

        <q-card-section class="text-center">
          <div class="text-h6">{{ template.option_2 }}</div>
        </q-card-section>

        <q-card-section class="text-center">
          <div class="text-h6">{{ template.option_3 }}</div>
        </q-card-section>

        <q-card-section class="text-center">
          <div class="text-h6">{{ template.option_4 }}</div>
        </q-card-section>

        <q-card-section class="text-center">
          <div class="text-h6">Created by: {{ template.creator_username }}</div>
        </q-card-section>

        <q-card-actions
          vertical
          v-if="template.subscribers.includes(user.value)"
        >
          <q-btn
            push
            @click="unsubscribe(template)"
            color="red"
            label="Unsubscribe"
            dense
          >
            <q-icon size="md" name="mdi-numeric-negative-1" />
          </q-btn>
        </q-card-actions>

        <q-card-actions vertical v-else>
          <q-btn
            push
            @click="subscribe(template)"
            color="secondary"
            label="Subscribe"
            dense
          >
            <q-icon size="md" name="mdi-numeric-positive-1" />
          </q-btn>
        </q-card-actions>
        <q-card-actions vertical>
          <q-btn
            push
            @click="deleteTemplate(template)"
            color="red"
            label="Delete"
            dense
          >
            <q-icon size="md" name="mdi-delete-forever" />
          </q-btn>
        </q-card-actions>
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
