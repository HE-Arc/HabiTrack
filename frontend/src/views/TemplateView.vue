<script setup>
import { ref, onMounted } from "vue";
import ErrorBanner from "../components/ErrorBanner.vue";

// Import necessary custom tools
import { getCurrentUsername } from "@/utils/auth.js";
import { isUserSubscribed, subOrUnsubScribe } from "@/utils/subscription.js";
import { templateAction } from "@/utils/template.js";
import { Notify } from "quasar";

const templates = ref([]);
const username = ref(false);
let loaded = false;

// We need error handling
const errors = ref(null);

const isSubbed = async (template_id) => {
  if (!username.value || username.value == null) {
    console.log("No one is logged in.");
    return false;
  }
  const response = await isUserSubscribed(username.value, template_id);
  if (response.success) {
    return response.subscribed;
  } else if (response.errors) {
    Notify.create({
      message: response.errors,
      color: "negative",
      position: "top",
    });
  }
};

const subscribe = async (template_id) => {
  if (username.value == null) {
    Notify.create({
      message: "You must be logged in to subscribe to a template.",
      color: "negative",
      position: "top",
    });
    // ask if user wants to login
    Notify.create({
      message: "Would you like to login?",
      color: "primary",
      position: "top",
      actions: [
        {
          label: "Yes",
          color: "white",
          handler: () => {
            window.location.href = "/login";
          },
        },
        {
          label: "No",
          color: "white",
          handler: () => {
            return;
          },
        },
      ],
    });
    return;
  }
  const response = await subOrUnsubScribe(
    "subscribe",
    username.value,
    template_id
  );
  if (response.success) {
    Notify.create({
      message: response.success,
      color: "positive",
      position: "top",
    });
  } else if (response.errors) {
    Notify.create({
      message: response.errors,
      color: "negative",
      position: "top",
    });
  }
};

const unsubscribe = async (template_id) => {
  const response = await subOrUnsubScribe(
    "unsubscribe",
    username.value,
    template_id
  );
  if (response.success) {
    Notify.create({
      message: response.success,
      color: "positive",
      position: "top",
    });
  } else if (response.errors) {
    Notify.create({
      message: response.errors,
      color: "negative",
      position: "top",
    });
  }
};

let test = async (template_id) => {
  const res = await isSubbed(template_id);
  console.log(res);
  return res;
};

onMounted(async () => {
  username.value = await getCurrentUsername();
  if (username.value == null) {
    username.value = false;
  }
  const response = await templateAction("get");
  if (response == null) {
    errors.value = "Couldn't fetch templates.";
  } else if (response.success) {
    templates.value = response.data;
  } else if (response.errors) {
    errors.value = response.errors;
  }
  loaded = true;
});
</script>

<template>
  <q-page padding>
    <ErrorBanner :errors="errors" />
    <div class="q-pa-md">
      <q-btn
        class="q-ma-auto"
        color="primary"
        :to="{ name: 'templates.create' }"
      >
        <q-icon left name="mdi-plus-box" />
        <q-label for="add_template">Create a new template</q-label>
      </q-btn>
    </div>

    <div class="q-pa-md items-start q-gutter-md">
      <q-card
        class="template-card q-pa-sm"
        style="background: radial-gradient(circle, #35a2ff 0%, #014a88 100%)"
        v-for="(template, index) in templates"
        :key="index"
        flat
        bordered
      >
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
          <div class="text-h6">Created by: {{ template.creator.username }}</div>
        </q-card-section>

        <q-card-actions vertical>
          <q-btn
            v-if="test(template.id)"
            push
            @click="unsubscribe(template.id)"
            color="red"
            label="Unsubscribe"
            dense
          >
            <q-icon size="md" name="mdi-numeric-negative-1" />
          </q-btn>
          <q-btn
            v-else
            push
            @click="subscribe(template.id)"
            color="secondary"
            label="Subscribe"
            dense
          >
            <q-icon size="md" name="mdi-numeric-positive-1" />
          </q-btn>
        </q-card-actions>

        <q-card-actions vertical>
          <q-btn
            push
            v-if="username.value == template.creator.username"
            @click="templateAction('delete', template)"
            color="red"
            label="Delete"
            dense
          >
            <q-icon size="md" name="mdi-delete-forever" />
          </q-btn>
        </q-card-actions>
      </q-card>
    </div>
  </q-page>
</template>

<style lang="sass" scoped>
.template-card
  width: 100%
  height: 100%
  max-width: 20rem
</style>
