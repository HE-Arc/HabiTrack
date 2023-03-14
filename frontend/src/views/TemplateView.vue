<script setup>
import { ref, onMounted } from "vue";
import ErrorBanner from "../components/ErrorBanner.vue";

// Import necessary custom tools
import { getCurrentUsername } from "@/utils/auth.js";
import { isUserSubscribed, subOrUnsubScribe } from "@/utils/subscription.js";
import { templateAction } from "@/utils/template.js";

const templates = ref([]);
const username = ref(null);

// We need error handling
const errors = ref(null);

onMounted(async () => {
  templates.value = await templateAction("get");
  username.value = await getCurrentUsername();
});
</script>

<template>
  <q-page>
    <ErrorBanner :errors="errors" />

    <q-btn
      v-if="username"
      id="add_template"
      color="primary"
      :to="{ name: 'templates.create' }"
    >
      <q-icon left name="mdi-plus-box" />
      <q-label for="add_template">Create a new template</q-label>
    </q-btn>

    <div class="q-pa-md items-start q-gutter-md">
      <q-card
        style="background: radial-gradient(circle, #35a2ff 0%, #014a88 100%)"
        class="template-card q-ma-sm"
        flat
        bordered
      >
        <q-card-section class="text-center">
          <div class="text-h5">{{ template.name }}</div>
        </q-card-section>

        <q-card-section class="text-center">
          <div class="text-h6">{{ template.description }}</div>
        </q-card-section>

        <q-card-section class="text-left">
          <div class="text-h6">{{ template.option_1 }}</div>
        </q-card-section>

        <q-card-section class="text-left">
          <div class="text-h6">{{ template.option_2 }}</div>
        </q-card-section>

        <q-card-section class="text-left">
          <div class="text-h6">{{ template.option_3 }}</div>
        </q-card-section>

        <q-card-section class="text-left">
          <div class="text-h6">{{ template.option_4 }}</div>
        </q-card-section>

        <q-card-section class="text-center">
          <div class="text-h6">Created by: {{ template.creator.username }}</div>
        </q-card-section>

        <q-card-actions
          vertical
          v-if="user && isUserSubscribed(user, template)"
        >
          <q-btn
            push
            @click="subOrUnsubScribe('unsubscribe', user, template)"
            color="red"
            label="Unsubscribe"
            dense
          >
            <q-icon size="md" name="mdi-numeric-negative-1" />
          </q-btn>
        </q-card-actions>

        <q-card-actions vertical v-else>
          <q-btn
            push
            @click="subOrUnsubScribe('subscribe', user, template)"
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
  min-width: 20rem
  max-width: 25rem
</style>
