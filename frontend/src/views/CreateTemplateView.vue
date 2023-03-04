<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

const success = ref(false);
const errors = ref(null);

// "name", "description", "option_1", "option_2", "option_3", "option_4"
const name = ref("");
const description = ref("");
const option_1 = ref("");
const option_2 = ref("");
const option_3 = ref("");
const option_4 = ref("");

// Fecth all User from DB

const users = ref([]);
const currentUser = ref(null);

const fetchUsers = async () => {
  users.value = (await axios.get("http://127.0.0.1:8000/api/users/")).data;
};

// Submit new Template
const submit = async () => {
  try {
    success.value = false;
    errors.value = false;

    // TODO: Check user login
    // Somehow??
    await axios.post("http://127.0.0.1:8000/api/templates/", {
      // TODO: Get current user
      creator: currentUser.value?.url,
      name: name.value,
      description: description.value,
      option_1: option_1.value,
      option_2: option_2.value,
      option_3: option_3.value,
      option_4: option_4.value,
    });
    success.value = true;
  } catch (err) {
    errors.value = true;
  }
};

// Execute le code quand le composant démarre
onMounted(() => {
  fetchUsers();
});
</script>

<template>
  <q-page class="q-ma-auto" padding>
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

    <q-form class="" @submit="submit()">
      <div>
        <div class="q-mt-md">
          <q-card>
            <q-card-section class="">
              <q-btn color="primary" :to="{ name: 'templates' }">
                <q-icon left name="mdi-arrow-left" />
                <div>Back</div>
              </q-btn>
            </q-card-section>

            <q-card-section class="text-center">
              <div class="text-h5">Create a new template</div>
            </q-card-section>

            <q-card-section>
              <q-input
                v-model="name"
                label="Name"
                filled
                stack-label
                class="q-mb-md"
              />

              <q-input
                v-model="description"
                label="Description"
                filled
                stack-label
                class="q-mb-md"
              />

              <q-input
                v-model="option_1"
                label="Option 1"
                filled
                stack-label
                class="q-mb-md"
              />

              <q-input
                v-model="option_2"
                label="Option 2"
                filled
                stack-label
                class="q-mb-md"
              />

              <q-input
                v-model="option_3"
                label="Option 3"
                filled
                stack-label
                class="q-mb-md"
              />

              <q-input
                v-model="option_4"
                label="Option 4"
                filled
                stack-label
                class="q-mb-md"
              />
            </q-card-section>

            <q-banner
              v-if="success"
              inline-actions
              class="q-mb-lg text-white bg-green"
            >
              <div class="text-h6">
                <q-icon left size="md" name="mdi-check-circle-outline" />
                New template successfully created!
              </div>
            </q-banner>

            <q-card-section class="q-gutter-y-sm">
              <div class="text-center">
                <q-btn type="submit" color="primary" label="Submit" />
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </q-form>
  </q-page>
</template>
