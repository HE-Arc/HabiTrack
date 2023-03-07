<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import ErrorBanner from "../components/ErrorBanner.vue";

const currentUser = ref(null);
const templates = ref([]);

// eslint-disable-next-line no-unused-vars
const fetchTemplates = async () => {
  // only get user's templates
  const result = await axios.get(`/templates/?user=${currentUser.value.id}`);
  templates.value = result.data;
};

// Fecth all User from DB

const users = ref([]);

const fetchUsers = async () => {
  users.value = (await axios.get("/users/")).data;
};

onMounted(() => {
  fetchUsers();
});
</script>

<template>
  <div class="q-gutter-md">
    <q-page>
      <ErrorBanner :errors="errors" />

      <!-- TODO: Get current user -->
      <q-select
        v-model="currentUser"
        option-value="id"
        option-label="username"
        :options="users"
        label="Select a user that will be the creator of the template"
        outlined
      />

      <q-btn color="primary" @click="fetchTemplates()">
        <q-icon left size="xl" name="mdi-plus-box" />
        <div>Fetch subscriptions TEMPORARY</div>
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

            <!-- TODO unsubscribe -->
            <!--<q-card-actions vertical>
                  <q-btn
                    push
                    @click="unscubscribeTemplate(template)"
                    class="q-ma-xs"
                    color="red"
                    dense
                    <q-icon self-center size="xl" name="mdi-delete-forever" />
                    <div>Delete</div>
                  </q-btn>
                </q-card-actions>
                >-->
          </q-card>
        </div>
      </div>
    </q-page>
  </div>
</template>
