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
  try {
    const response = await axios.post("/login/", {
      username: username.value,
      password: password.value,
    });

    if (response.data.error) {
      errors.value = response.data.error;
      return;
    }
    if (response.data.success) {
      success.value = true;
      setTimeout(() => {
        window.location.href = "/subscriptions/";
      }, 1000);
    }
  } catch (err) {
    success.value = false;
    errors.value = err.response.data;
  }
};
</script>
<template>
  <q-page>
    <ErrorBanner :errors="errors" />
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
              />

              <q-input
                v-model="password"
                label="Password"
                type="password"
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
                Login successful!
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
