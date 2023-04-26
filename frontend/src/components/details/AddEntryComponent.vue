<script setup>
import { ref, onMounted } from "vue";
import { entryAction } from "../../utils/entry";
import { getTemplateEntries, getTemplateEntriesToday } from "../../utils/entry";
import GraphComponent from "./GraphComponent.vue";
import GridComponent from "./GridComponent.vue";
import { Notify } from "quasar";

const props = defineProps({
  propTemplate: {},
});

const entries = ref([]);
const errors = ref([]);
const selected_option = ref("");
const entry = ref({});
const entryToday = ref([]);
const alreadyEnteredToday = ref(false);
const loaded = ref(false);

const actionEntryClicked = async (update) => {
  if (selected_option.value === "") {
    Notify.create({
      message: "Please select an option",
      color: "negative",
      position: "top",
    });
    return;
  }
  entry.value = {
    template_id: props.propTemplate.id,
    selected_option: selected_option.value.value,
  };
  let response;
  if (update) {
    entry.value.id = entryToday.value.id;
    response = await entryAction("update", entry.value);
  } else {
    response = await entryAction("create", entry.value);
  }
  if (response.success) {
    Notify.create({
      message: "Entry saved!",
      color: "positive",
      position: "top",
    });
    await updateEntries();
  } else {
    Notify.create({
      message: response.errors.errors,
      color: "negative",
      position: "top",
    });
  }
};

const updateEntries = async () => {
  const response = await getTemplateEntries(props.propTemplate.id);
  if (response.success) {
    entries.value = response.data;
  } else {
    errors.value = response.errors;
  }
  const responseToday = await getTemplateEntriesToday(props.propTemplate.id);
  if (responseToday.success && responseToday.data !== null) {
    entryToday.value = responseToday.data;
    alreadyEnteredToday.value = true;
  } else {
    errors.value = responseToday.errors;
  }
  loaded.value = true;
};

onMounted(async () => {
  await updateEntries();
});
</script>

<template>
  <GraphComponent :propTemplate="propTemplate" :propEntries="entries" />
  <GridComponent
    v-if="loaded"
    :propTemplate="propTemplate"
    :propEntries="entries"
  />

  <q-form>
    <q-select
      v-model="selected_option"
      :options="[
        { label: props.propTemplate.option_1, value: 0 },
        { label: props.propTemplate.option_2, value: 1 },
        { label: props.propTemplate.option_3, value: 2 },
        { label: props.propTemplate.option_4, value: 3 },
      ]"
      label="Select an option"
      option-value="value"
      class="q-mb-md"
    />
    <q-btn
      v-if="!alreadyEnteredToday"
      label="Add Entry"
      color="primary"
      @click="actionEntryClicked(false)"
    />
    <q-btn
      v-else
      label="Update Entry"
      color="primary"
      @click="actionEntryClicked(true)"
    />
  </q-form>
</template>
