<script setup>
import { ref, onMounted } from "vue";
import { entryAction } from "../../utils/entry";
import { getTemplateEntries } from "../../utils/entry";
import GraphComponent from "./GraphComponent.vue";
import { Notify } from "quasar";

const props = defineProps({
  propTemplate: {},
});

const entries = ref([]);
const errors = ref([]);
const selected_option = ref("");
const entry = ref({});

const addEntryClicked = async () => {
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
  const response = await entryAction("create", entry.value);
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
};

onMounted(async () => {
  await updateEntries();
});
</script>

<template>
  <GraphComponent :propTemplate="propTemplate" :propEntries="entries" />
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
    <q-btn label="Add Entry" color="primary" @click="addEntryClicked" />
  </q-form>
</template>
