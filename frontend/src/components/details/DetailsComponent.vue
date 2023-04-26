<script setup>
import ErrorBanner from "../ErrorBanner.vue";
import AddEntryComponent from "./AddEntryComponent.vue";

const props = defineProps({
  propTemplate: {},
});

props; // stop eslint complaining
</script>

<template>
  <q-page padding>
    <ErrorBanner :errors="errors" />
    <q-card>
      <q-card-section>
        <h2 class="text-h4">{{ propTemplate.name }}</h2>
      </q-card-section>
      <q-card-section>
        <h3 class="text-h6">{{ propTemplate.description }}</h3>
        <AddEntryComponent
          :propTemplate="propTemplate"
          :propEntries="entries"
        />
      </q-card-section>
    </q-card>
  </q-page>
</template>
