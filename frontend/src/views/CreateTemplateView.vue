<script setup>
import { ref, onMounted } from "vue";
import { getCurrentUser } from "@/utils/auth.js";
import { templateAction } from "@/utils/template.js";

const success = ref(false);
const errors = ref(null);

// "name", "description", "option_1", "option_2", "option_3", "option_4"
const name = ref("");
const description = ref("");
const option_1 = ref("");
const option_2 = ref("");
const option_3 = ref("");
const option_4 = ref("");

const user = ref(null);

// Execute le code quand le composant démarre
onMounted(async () => {
  user.value = await getCurrentUser();
});
</script>

<template>
  <q-page class="q-ma-auto" padding>
    <ErrorBanner :errors="errors" />
    <q-form
      class=""
      @submit="
        templateAction('create', {
          name,
          description,
          option_1,
          option_2,
          option_3,
          option_4,
        })
      "
    >
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
            <div class="text-h5">Create a new template</div>
          </q-card-section>

          <q-card-section>
            <q-input
              v-model="name"
              label="Name"
              filled
              stack-label
              class="q-mb-md"
            />

            <q-input
              v-model="description"
              label="Description"
              filled
              stack-label
              type="textarea"
              class="q-mb-md"
            />

            <q-input
              v-model="option_1"
              label="Option 1"
              square
              outlined
              class="q-mb-md"
            />

            <q-input
              v-model="option_2"
              label="Option 2"
              outlined
              square
              class="q-mb-md"
            />

            <q-input
              v-model="option_3"
              label="Option 3"
              outlined
              square
              class="q-mb-md"
            />

            <q-input
              v-model="option_4"
              label="Option 4"
              outlined
              square
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
              New template successfully created!
            </div>
          </q-banner>

          <q-card-section class="q-gutter-y-sm">
            <div class="text-center">
              <q-btn type="submit" color="primary" label="Submit" />
            </div>
          </q-card-section>
        </q-card>
      </div>
    </q-form>
  </q-page>
</template>
