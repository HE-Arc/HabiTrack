<script setup>
import ErrorBanner from "../components/ErrorBanner.vue";
import { ref, onMounted } from "vue";
import { fetchSubscriptions } from "../utils/subscription";
import { getCurrentUser } from "../utils/auth";

const templates = ref([]);
const user = ref(null);
const errors = ref(null);

onMounted(async () => {
  user.value = await getCurrentUser();
  if (user.value) {
    templates.value = await fetchSubscriptions(user);
  } else {
    templates.value = [];
    errors.value = "You must be logged in to view this page.";
  }
});
</script>

<template>
  <div class="q-gutter-md">
    <q-page>
      <ErrorBanner :errors="errors" />

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
