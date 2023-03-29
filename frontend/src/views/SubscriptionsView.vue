<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import ErrorBanner from "../components/ErrorBanner.vue";
import Cookies from "js-cookie";

const templates = ref([]);

// eslint-disable-next-line no-unused-vars
const fetchSubscriptions = async () => {
  axios
    .get("subscriptions/", {
      headers: {
        "X-CSRFToken": Cookies.get("csrftoken"),
      },
      withCredentials: true,
    }) // THIS IS WRONG
    .then((response) => {
      if (response.data.success) {
        templates.value = response.data.templates;
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

onMounted(() => {
  fetchSubscriptions();
});
</script>

<template>
  <div class="q-gutter-md">
    <q-page></q-page>
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
