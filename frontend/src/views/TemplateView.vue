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
  <!-- Old Version-->
  <div class="q-pa-md">
    <div class="q-gutter-md" style="max-width: 500px">
      <q-responsive :ratio="16 / 9">
        <q-page>
          <ErrorBanner :errors="errors" />

          <!-- TODO: Get current user -->
          <q-select
            v-model="currentUser"
            option-value="id"
            option-label="username"
            :options="users"
            label="User"
            outlined
          />

          <q-btn color="primary" :to="{ name: 'templates.create' }">
            <q-icon left size="xl" name="mdi-plus-box" />
            <div>Create a new template</div>
          </q-btn>

          <div class="row">
            <div
              class="text-center col-md-6 col-lg-4 col-xl-3 q-pa-sm"
              v-for="(template, index) in templates"
              :key="index"
            >
              <q-card class="q-pa-md">
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
                  <div class="text-h6">
                    Created by: {{ template.creator_username }}
                  </div>
                </q-card-section>

                <!--<q-card-section class="text-center">
            <q-btn color="primary" :to="{ name: 'templates.edit', params: { id: template.id } }">
              <q-icon left name="mdi-pencil" />
              <div>Edit</div>
            </q-btn>
          </q-card-section>-->
                <!--TODO hide the subscribe button if user is already subscribed to the template-->
                <q-card-actions vertical>
                  <q-btn
                    push
                    @click="submit(template)"
                    class="q-ma-xs"
                    color="primary"
                    dense
                  >
                    <q-icon left size="xl" name="mdi-numeric-positive-1" />
                    <div>Subscribe</div>
                  </q-btn>
                </q-card-actions>

                <q-card-actions vertical>
                  <q-btn
                    push
                    @click="deleteTemplate(template)"
                    class="q-ma-xs"
                    color="red"
                    dense
                  >
                    <q-icon self-center size="xl" name="mdi-delete-forever" />
                    <div>Delete</div>
                  </q-btn>
                </q-card-actions>
              </q-card>
            </div>
          </div>
        </q-page>
      </q-responsive>
    </div>
  </div>
</template>
