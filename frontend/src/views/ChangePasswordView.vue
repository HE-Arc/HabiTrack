<script setup>
import { ref } from "vue";
import { Notify } from "quasar";
import ErrorBanner from "@/components/ErrorBanner.vue";
import { changePassword } from "@/utils/auth.js";
import { getCurrentUsername } from "@/utils/auth.js";
import { onMounted } from "vue";

const oldPassword = ref("");
const newPassword = ref("");
const confirmNewPassword = ref("");
const errors = ref([]);
const username = ref("");

const submit = async () => {
  const response = await changePassword(
    username.value,
    oldPassword.value,
    newPassword.value,
    confirmNewPassword.value
  );

  if (response.success) {
    Notify.create({
      message: "Password successfully changed!",
      color: "positive",
      position: "top",
    });
    // clear input fields
    oldPassword.value = "";
    newPassword.value = "";
    confirmNewPassword.value = "";
  } else {
    console.log(response.errors);
    errors.value = response.errors;
  }
};

onMounted(async () => {
  // clear input fields
  oldPassword.value = "";
  newPassword.value = "";
  confirmNewPassword.value = "";

  username.value = await getCurrentUsername();
  if (username.value == null) {
    errors.value = "You must be logged in to view this page.";
  }
});
</script>

<template>
  <q-page>
    <q-card class="max-w-sm mx-auto">
      <q-form @submit.prevent="submit">
        <q-card-section>
          <div class="text-h5">Change Password</div>
        </q-card-section>

        <q-card-section>
          <q-input
            v-model="oldPassword"
            label="Old Password"
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
            v-model="newPassword"
            label="New Password"
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
            v-model="confirmNewPassword"
            label="Confirm New Password"
            type="password"
            filled
            stack-label
            class="q-mb-md"
            lazy-rules
            :rules="[
              (val) => (val && val.length > 0) || 'Please type something',
              (val) =>
                val === newPassword ||
                'New password does not match confirmation',
            ]"
          />

          <ErrorBanner :errors="errors" />
        </q-card-section>

        <q-card-section class="q-gutter-y-sm">
          <div class="text-center">
            <q-btn type="submit" color="primary">
              <q-icon left name="mdi-account-key" />
              <div>Change Password</div>
            </q-btn>
          </div>
        </q-card-section>
      </q-form>
    </q-card>
  </q-page>
</template>
