<script setup>
import ErrorBanner from "../components/ErrorBanner.vue";
import { ref, onMounted } from "vue";
import { fetchSubscriptions } from "../utils/subscription";
import { getCurrentUsername } from "../utils/auth";

const templates = ref([]);
const username = ref(null);
const errors = ref(null);

onMounted(async () => {
  username.value = await getCurrentUsername();
  if (username.value) {
    templates.value = await fetchSubscriptions(username.value);
  } else {
    templates.value = [];
    errors.value = "You must be logged in to view this page.";
  }
});
</script>

<template>
  <q-page padding>
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
</template>

<style lang="sass" scoped>
.template-card
  width: 100%
  height: 100%
  max-width: 20rem
</style>
