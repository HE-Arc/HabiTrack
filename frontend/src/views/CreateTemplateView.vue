<script setup>
import { ref, onMounted } from "vue";
import { getCurrentUsername } from "@/utils/auth.js";
import { templateAction } from "@/utils/template.js";
import { Notify } from "quasar";
import router from "@/router";

const errors = ref(null);

// "name", "description", "option_1", "option_2", "option_3", "option_4"
const name = ref("");
const description = ref("");
const option_1 = ref("");
const option_2 = ref("");
const option_3 = ref("");
const option_4 = ref("");

const username = ref(null);

const submit = async () => {
  const response = await templateAction(
    "create",
    {
      name: name.value,
      description: description.value,
      option_1: option_1.value,
      option_2: option_2.value,
      option_3: option_3.value,
      option_4: option_4.value,
    },
    username.value
  );
  if (response.success) {
    Notify.create({
      message: "Template successfully created!",
      color: "positive",
      position: "top",
    });
    setTimeout(() => {
      router.push({ name: "edits" });
    }, 1000);
  } else {
    errors.value = response.errors;
  }
};

// Execute le code quand le composant démarre
onMounted(async () => {
  username.value = await getCurrentUsername();
  if (username.value) {
    errors.value = "You must be logged in to view this page.";
  }
});
</script>

<template>
  <div class="row justify-center q-mx-xl q-pt-md">
    <q-page class="create-template-card">
      <ErrorBanner :errors="errors" />
      <q-form class="" @submit="submit">
        <!-- <div class="q-mt-md"> -->
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
              :rules="[
                (val) => (val && val.length > 0) || 'Please type something',
                (val) => val.length < 100 || 'Size limit is 100',
              ]"
            />

            <q-input
              v-model="description"
              label="Description"
              filled
              stack-label
              class="q-mb-md"
              type="textarea"
              lazy-rules
              :rules="[
                (val) => (val && val.length > 0) || 'Please type something',
                (val) => val.length < 2000 || 'Size limit is 2000',
              ]"
            />

            <q-input
              v-model="option_1"
              label="Option 1"
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
              v-model="option_2"
              label="Option 2"
              filled
              stack-label
              class="q-mb-md"
            />

            <q-input
              v-model="option_3"
              label="Option 3"
              filled
              stack-label
              class="q-mb-md"
            />

            <q-input
              v-model="option_4"
              label="Option 4"
              filled
              stack-label
              class="q-mb-md"
            />
          </q-card-section>

          <q-card-section class="q-gutter-y-sm">
            <div class="text-center">
              <q-btn type="submit" color="primary" label="Submit" />
            </div>
          </q-card-section>
        </q-card>
        <!-- </div> -->
      </q-form>
    </q-page>
  </div>
</template>
