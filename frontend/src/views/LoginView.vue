<script setup>
import axios from "axios";
import { ref } from "vue";
import ErrorBanner from "@/components/ErrorBanner.vue";

const success = ref(false);
const errors = ref(null);
const username = ref("");
const password = ref("");

// Submit user login
const submit = async () => {
  if (!username.value || !password.value) {
    errors.value = ["Please enter a username and password"];
    return;
  }
  axios
    .post(
      "login/",
      {
        username: username.value,
        password: password.value,
      },
      {
        withCredentials: true,
      }
    )
    .then((response) => {
      if (response.data.success) {
        setTimeout(() => {
          window.location.href = "/subscriptions/";
        }, 1000);
      } else {
        errors.value = [response.data.error];
      }
    })
    .catch((error) => {
      errors.value = error.response.data;
    });
};
</script>
<template>
  <q-page>
    <q-form class="" @submit="submit()">
      <div>
        <div class="q-ma-md">
          <q-card>
            <q-card-section class="">
              <q-btn color="primary" :to="{ name: 'templates' }">
                <q-icon left name="mdi-arrow-left" />
                <div>Back</div>
              </q-btn>
            </q-card-section>

            <q-card-section class="text-center">
              <div class="text-h5">Login</div>
            </q-card-section>

            <q-card-section>
              <q-input
                v-model="username"
                label="Username"
                type="text"
                filled
                stack-label
                class="q-mb-md"
                lazy-rules
                :rules="[
                  (val) => (val && val.length > 0) || 'Please type something',
                ]"
              />

              <q-input
                v-model="password"
                label="Password"
                type="password"
                filled
                stack-label
                class="q-mb-md"
                lazy-rules
                :rules="[
                  (val) => (val && val.length > 0) || 'Please type something',
                ]"
              />
            </q-card-section>

            <q-banner
              v-if="success"
              inline-actions
              class="q-mb-lg text-white bg-green"
            >
              <div class="text-h6">
                <q-icon left size="md" name="mdi-check-circle-outline" />
                Login successful!
              </div>
            </q-banner>
            <ErrorBanner :errors="errors" />

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
