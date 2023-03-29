<script setup>
import axios from "axios";
import { ref } from "vue";
const success = ref(false);
const errors = ref(null);
const username = ref("");
const password = ref("");
const password_again = ref("");

// Submit user login
const submit = async () => {
  
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
              <div class="text-h5">Register</div>
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
                  (val) => val.length < 30 || 'Size limit is 30',
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
              <q-input
                v-model="password_again"
                label="Type Password Again"
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
                Registration successful!
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
