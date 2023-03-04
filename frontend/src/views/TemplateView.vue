<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import ErrorBanner from "../components/ErrorBanner.vue";

// Fecth all Template from DB
const templates = ref([]);

const fetchTemplates = async () => {
  const result = await axios.get("http://127.0.0.1:8000/api/templates/");

  templates.value = result.data;
};

// Fecth all User from DB

const users = ref([]);
const currentUser = ref(null);

const fetchUsers = async () => {
  users.value = (await axios.get("http://127.0.0.1:8000/api/users/")).data;
};

// We need error handling
const errors = ref(null);

// Allow creation of a new Template
const submit = async (template) => {
  try {
    errors.value = null;

    const res = await axios.post("http://127.0.0.1:8000/api/templates/", {
      user: currentUser.value?.url,
      name: template.name,
      description: template.description,
      option_1: template.option_1,
      option_2: template.option_2,
      option_3: template.option_3,
      option_4: template.option_4,
    });

    console.log(res);
  } catch (error) {
    errors.value = error;
    console.log(error.response.data);
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

    <q-btn color="primary" :to="{ name: 'templates.create' }">
      <q-icon left size="xl" name="mdi-plus-box" />
      <div>Create a new template</div>
    </q-btn>

    <div class="row">
      <div
        class="text-center col-12 col-sm-6 col-md-4 col-lg-3 q-pa-sm"
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

          <!--<q-card-section class="text-center">
            <q-btn color="primary" :to="{ name: 'templates.edit', params: { id: template.id } }">
              <q-icon left name="mdi-pencil" />
              <div>Edit</div>
            </q-btn>
          </q-card-section>-->

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
        </q-card>
      </div>
    </div>
  </q-page>
</template>
