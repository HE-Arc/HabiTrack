<script setup>
import { ref } from "vue";
import { onMounted } from "vue";
import { Notify } from "quasar";
import { deleteAccount, getCurrentUsername } from "@/utils/auth";

import {
  getTemplatesCount,
  getEntriesCount,
  fetchTemplates,
  getEntries,
} from "@/utils/template";

import {
  getSubscriptionsCount,
  fetchSubscriptions,
} from "@/utils/subscription";

const username = ref(""); // Set initial values
const templatesCount = ref(0);
const subscriptionsCount = ref(0);
const entriesCount = ref(0);

// Dialog
const confirmDelete = ref(false);

// Lists
const templates = ref([]);
const subscriptions = ref([]);
const entry = ref([]);

const errors = ref(null);

const passwordChange = async () => {
  // redirect to password change page
  window.location.href = "/change-password";
};

const deleteClicked = async () => {
  if (confirmDelete.value) {
    const response = await deleteAccount(username.value);
    if (response.success != null) {
      Notify.create({
        message: "Account deleted",
        color: "positive",
        position: "top",
      });
      setTimeout(() => {
        window.location.href = "/login";
      }, 1000);
    } else {
      console.log(response.errors);
      errors.value = response.errors;
    }
  }
};

// Load user data and counts on component mount
onMounted(async () => {
  username.value = await getCurrentUsername();
  if (username.value) {
    try {
      templatesCount.value = await getTemplatesCount(username.value);
      subscriptionsCount.value = await getSubscriptionsCount(username.value);
      entriesCount.value = await getEntriesCount(username.value);

      templates.value = await fetchTemplates(username.value);
      subscriptions.value = await fetchSubscriptions(username.value);
      entry.value = await getEntries(username.value);
    } catch (error) {
      console.error(error);
      Notify.create({
        message: "Failed to load user data",
        color: "negative",
        position: "top",
      });
    }
  } else {
    errors.value = "You must be logged in to view this page.";
  }
});
</script>

<template>
  <q-page>
    <q-card class="q-ma-md">
      <q-card-section>
        <div class="text-h5">My Profile</div>
      </q-card-section>

      <q-card-section class="row items-center">
        <div class="col text-h6">{{ username }}</div>
      </q-card-section>

      <q-card-section>
        <q-list
          bordered
          style="max-height: 10rem"
          class="rounded-borders q-ma-md"
        >
          <q-expansion-item :label="`Templates (${templatesCount})`">
            <q-q-expansion-item
              v-for="(template, index) in templates"
              :key="index"
              >{{ template.name }}</q-q-expansion-item
            >
          </q-expansion-item>
        </q-list>

        <q-list
          bordered
          style="max-height: 10rem"
          class="rounded-borders q-ma-md"
        >
          <q-expansion-item :label="`Subscriptions (${subscriptionsCount})`">
            <q-q-expansion-item
              v-for="(subscription, index) in subscriptions"
              :key="index"
              >{{ subscription.name }}</q-q-expansion-item
            >
          </q-expansion-item>
        </q-list>

        <!--<q-list bordered class="rounded-borders q-ma-md">
          <q-expansion-item :label="`Entries (${templatesCount})`">
            <q-q-expansion-item
              v-for="entry in entries.value"
              :key="entry.title"
            />
          </q-expansion-item>
        </q-list>-->
      </q-card-section>

      <q-card-section>
        <div class="text-center">
          <q-btn color="secondary" @click="passwordChange" class="q-mr-md">
            <q-icon :name="'mdi-form-textbox-password'" left />
            <div>Change Password</div>
          </q-btn>
          <q-btn
            label="Delete"
            color="negative"
            @click="confirmDelete = true"
          />
          <q-dialog v-model="confirmDelete" persistent>
            <q-card>
              <q-card-section class="row items-center">
                <q-avatar
                  icon="mdi-delete-alert"
                  color="negative"
                  text-color="white"
                />
                <span class="q-ml-sm"
                  >Are you sure you want to delete your account?</span
                >
              </q-card-section>

              <q-card-actions align="right">
                <q-btn flat label="Cancel" color="primary" v-close-popup />
                <q-btn
                  flat
                  label="Delete Account"
                  color="negative"
                  @click="deleteClicked"
                />
              </q-card-actions>
            </q-card>
          </q-dialog>
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>
