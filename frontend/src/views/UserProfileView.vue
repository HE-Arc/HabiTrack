<script setup>
import { ref } from "vue";
import { onMounted } from "vue";
import { Notify } from "quasar";
import { deleteAccount, getCurrentUsername } from "@/utils/auth";
import DeleteDialog from "../components/DeleteDialog.vue";
import router from "@/router";

import { getTemplatesCount, fetchTemplates } from "@/utils/template";

import { getEntriesCount, fetchEntries } from "@/utils/entry";

import {
  getSubscriptionsCount,
  fetchSubscriptions,
} from "@/utils/subscription";

const username = ref(""); // Set initial values
const templatesCount = ref(0);
const subscriptionsCount = ref(0);
const entriesCount = ref(0);

// Lists
const templates = ref([]);
const subscriptions = ref([]);
const entries = ref([]);
const loaded = ref(false);

const errors = ref(null);

const changePassword = async () => {
  // redirect to password change page
  router.push({ name: "change-password" });
};

const deleteConfirmed = async () => {
  // delete account
  const response = await deleteAccount(username.value);
  if (response.success) {
    Notify.create({
      message: "Account successfully deleted!",
      color: "positive",
      position: "top",
    });
    setTimeout(() => {
      router.push({ name: "login" });
    }, 1000);
  } else {
    console.log(response.errors);
    errors.value = response.errors;
  }
};

const fetchData = async () => {
  try {
    const templateCountResp = await getTemplatesCount(username.value);
    if (templateCountResp.success) {
      templatesCount.value = templateCountResp.count;
    } else {
      errors.value = templateCountResp.errors;
    }
    const entriesCountResp = await getEntriesCount(username.value);
    if (entriesCountResp.success) {
      entriesCount.value = entriesCountResp.count;
    } else {
      errors.value = entriesCountResp.errors;
    }
    const subscriptionCountResp = await getSubscriptionsCount(username.value);
    if (subscriptionCountResp.success) {
      subscriptionsCount.value = subscriptionCountResp.count;
    } else {
      errors.value = subscriptionCountResp.errors;
    }

    const templatesResp = await fetchTemplates(username.value);
    if (templatesResp.success) {
      templates.value = templatesResp.data;
    } else {
      errors.value = templatesResp.errors;
    }
    const subscriptionsResp = await fetchSubscriptions(username.value);
    if (subscriptionsResp.success) {
      subscriptions.value = subscriptionsResp.data;
    } else {
      errors.value = subscriptionsResp.errors;
    }
    const entriesResp = await fetchEntries(username.value);
    if (entriesResp.success) {
      entries.value = entriesResp.data;
    } else {
      errors.value = entriesResp.errors;
    }

    // check if data is loaded
    if (
      templatesCount.value &&
      subscriptionsCount.value &&
      entriesCount.value &&
      templates.value &&
      subscriptions.value
    ) {
      return;
    } else {
      errors.value = "Failed to load user data";
    }
  } catch (error) {
    Notify.create({
      message: "Failed to load user data",
      color: "negative",
      position: "top",
    });
  }
};

// Load user data and counts on component mount
onMounted(async () => {
  username.value = await getCurrentUsername();
  if (username.value) {
    await fetchData();
    loaded.value = true;
  } else {
    errors.value = "You must be logged in to view this page.";
  }
});
</script>

<template>
  <q-page v-if="loaded">
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
          style="max-height: 10rem; overflow-y: auto"
          class="rounded-borders q-ma-md"
        >
          <q-expansion-item :label="`Templates (${templatesCount})`">
            <q-q-expansion-item
              v-for="(template, index) in templates"
              :key="index"
            >
              <div class="q-pa-md">
                <q-card>
                  <q-card-section>
                    <div class="text-h6">{{ template.name }}</div>
                    <div class="text-body">{{ template.description }}</div>
                  </q-card-section>
                </q-card>
              </div>
            </q-q-expansion-item>
          </q-expansion-item>
        </q-list>

        <q-list
          bordered
          style="max-height: 10rem; overflow-y: auto"
          class="rounded-borders q-ma-md"
        >
          <q-expansion-item :label="`Subscriptions (${subscriptionsCount})`">
            <q-q-expansion-item
              v-for="(subscription, index) in subscriptions"
              :key="index"
            >
              <div class="q-pa-md">
                <q-card>
                  <q-card-section>
                    <div class="text-h6">{{ subscription.name }}</div>
                    <div class="text-body">{{ subscription.description }}</div>
                  </q-card-section>
                </q-card>
              </div>
            </q-q-expansion-item>
          </q-expansion-item>
        </q-list>

        <!-- simple Entries count -->
        <div class="text-h6 q-ma-md">Entries: {{ entriesCount }}</div>
      </q-card-section>

      <q-card-section>
        <div class="text-center">
          <q-btn color="secondary" @click="changePassword" class="q-mr-md">
            <q-icon :name="'mdi-form-textbox-password'" left />
            <div>Change Password</div>
          </q-btn>
          <DeleteDialog
            :message="`Are you sure you want to delete your account?
          This action cannot be undone.`"
            :confirmFunction="deleteConfirmed"
          />
        </div>
      </q-card-section>
    </q-card>
  </q-page>
  <q-page v-else>
    <div class="text-center">
      <q-spinner-dots size="100px" color="secondary" />
    </div>
  </q-page>
</template>
