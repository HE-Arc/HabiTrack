<script setup>
import { ref } from "vue";
const props = defineProps({
  message: {
    type: String,
    required: true,
  },
  confirmFunction: {
    type: Function,
    required: true,
  },
});

// Dialog
const confirmDelete = ref(false);

const deleteClicked = () => {
  props.confirmFunction();
};
</script>
<template>
  <q-btn label="Delete" color="negative" @click="confirmDelete = true" />
  <q-dialog v-model="confirmDelete" persistent>
    <q-card>
      <q-card-section class="row items-center">
        <q-avatar icon="mdi-delete-alert" color="negative" text-color="white" />
        <span class="q-ml-sm">{{ props.message }}</span>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Cancel" color="primary" v-close-popup />
        <q-btn flat label="Delete" color="negative" @click="deleteClicked" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>
