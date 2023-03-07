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

// Fecth all User from DB

const users = ref([]);
const currentUser = ref(null);

const fetchUsers = async () => {
  users.value = (await axios.get("/users/")).data;
};

// We need error handling
const errors = ref(null);

// Allow subscription to a new Template
const submit = async (template) => {
  // set CSRF token as header
  // TODO - may need this for later so leaving it here...
  const csrfToken = Cookies.get("csrftoken");
  const headers = {
    "X-CSRFToken": csrfToken,
  };

  // make POST request with headers
  axios
    .post(`/templates/subscribe/${template.id}/`, {}, { headers })
    .then((response) => {
      // handle success response
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
  fetchTemplates();
  fetchUsers();
});
</script>

<template>
  <q-page padding>
    <ErrorBanner :errors="errors" />
    <!--START TEMPORARY ELEMENTS-->

    <q-btn id="add_template" color="primary" :to="{ name: 'templates.create' }">
      <q-icon left name="mdi-plus-box" />
      <q-label for="add_template">Create a new template</q-label>
    </q-btn>

    <q-select
      id="user_select"
      v-model="currentUser"
      option-value="id"
      option-label="username"
      :options="users"
      label="Select a user to subscribe them to a template"
    />

    <!--END TEMPORARY ELEMENTS-->
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

        <q-card-actions vertical>
          <q-btn
            push
            @click="submit(template)"
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
