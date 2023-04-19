<script setup>
import { ref, onMounted } from "vue";
import { getCurrentUsername } from "../utils/auth";
import { isUserSubscribed, subOrUnsubScribe } from "../utils/subscription";
import { templateAction } from "../utils/template";
import { Notify } from "quasar";
import ErrorBanner from "./ErrorBanner.vue";
import DeleteDialog from "./DeleteDialog.vue";

const props = defineProps({
  propTemplate: {},
  username: {},
  showEdit: {
    type: Boolean,
    default: false,
  },
});

const deleteClicked = async () => {
  const response = await templateAction(
    "delete",
    props.propTemplate,
    props.username
  );
  if (response.success) {
    Notify.create({
      message: "Template successfully deleted!",
      color: "positive",
      position: "top",
    });
    window.location.href = "/templates";
  } else {
    Notify.create({
      message: response.errors.errors,
      color: "negative",
      position: "top",
    });
  }
};

const updateClicked = async () => {
  const response = await templateAction(
    "update",
    props.propTemplate,
    props.username
  );
  if (response.success) {
    Notify.create({
      message: "Template successfully deleted!",
      color: "positive",
      position: "top",
    });
  } else {
    Notify.create({
      message: response.errors.errors,
      color: "negative",
      position: "top",
    });
  }
};

const isSubbed = async (template_id) => {
  if (!username.value || username.value == null) {
    console.log("No one is logged in.");
    return false;
  }
  const response = await isUserSubscribed(username.value, template_id);
  if (response.success) {
    return response.subscribed;
  } else if (response.errors) {
    Notify.create({
      message: response.errors,
      color: "negative",
      position: "top",
    });
  }
};

const subscribe = async (template_id) => {
  if (username.value == null) {
    Notify.create({
      message: "You must be logged in to subscribe to a template.",
      color: "negative",
      position: "top",
    });
    // ask if user wants to login
    Notify.create({
      message: "Would you like to login?",
      color: "primary",
      position: "top",
      actions: [
        {
          label: "Yes",
          color: "white",
          handler: () => {
            window.location.href = "/login";
          },
        },
        {
          label: "No",
          color: "white",
          handler: () => {
            return;
          },
        },
      ],
    });
    return;
  }
  const response = await subOrUnsubScribe(
    "subscribe",
    username.value,
    template_id
  );
  if (response.success) {
    Notify.create({
      message: response.success,
      color: "positive",
      position: "top",
    });
  } else if (response.errors) {
    Notify.create({
      message: response.errors,
      color: "negative",
      position: "top",
    });
  }
  subbed.value = await isSubbed(template.value.id);
};

const unsubscribe = async (template_id) => {
  const response = await subOrUnsubScribe(
    "unsubscribe",
    username.value,
    template_id
  );
  if (response.success) {
    Notify.create({
      message: response.success,
      color: "positive",
      position: "top",
    });
  } else if (response.errors) {
    Notify.create({
      message: response.errors,
      color: "negative",
      position: "top",
    });
  }
  subbed.value = await isSubbed(template.value.id);
};

const username = ref(null);
const subbed = ref(false);
const creator = ref(false);
const errors = ref(null);
const template = ref(null);
const loaded = ref(false);
const isEdit = ref(false);

onMounted(async () => {
  username.value = await getCurrentUsername();
  template.value = props.propTemplate;
  subbed.value = await isSubbed(template.value.id);
  creator.value = username.value == props.propTemplate.creator.username;
  isEdit.value = props.showEdit;
  loaded.value = true;
});
</script>

<template>
  <q-card v-if="loaded">
    <ErrorBanner :errors="errors" />
    <q-card-section class="text-center">
      <div class="text-h5">{{ template.name }}</div>
    </q-card-section>

    <q-card-section class="text-center">
      <div v-if="!isEdit" class="text-h6">{{ template.description }}</div>
      <q-input
        v-else
        v-model="template.description"
        outlined
        label="Description"
        dense
        placeholder="Description"
      />
    </q-card-section>

    <q-card-section class="text-center">
      <div v-if="!isEdit" class="text-h6">{{ template.option_1 }}</div>
      <q-input
        v-else
        v-model="template.option_1"
        outlined
        label="Option 1"
        dense
        placeholder="Option 1"
      />
    </q-card-section>

    <q-card-section class="text-center">
      <div v-if="!isEdit" class="text-h6">{{ template.option_2 }}</div>
      <q-input
        v-else
        v-model="template.option_2"
        outlined
        label="Option 2"
        dense
        placeholder="Option 2"
      />
    </q-card-section>

    <q-card-section class="text-center">
      <div v-if="!isEdit" class="text-h6">{{ template.option_3 }}</div>
      <q-input
        v-else
        v-model="template.option_3"
        outlined
        label="Option 3"
        dense
        placeholder="Option 3"
      />
    </q-card-section>

    <q-card-section class="text-center">
      <div v-if="!isEdit" class="text-h6">{{ template.option_4 }}</div>
      <q-input
        v-else
        v-model="template.option_4"
        outlined
        label="Option 4"
        dense
        placeholder="Option 4"
      />
    </q-card-section>

    <q-card-section class="text-center" v-if="!isEdit">
      <div class="text-h6">Created by: {{ template.creator.username }}</div>
    </q-card-section>

    <q-card-actions vertical v-if="!isEdit">
      <q-btn
        v-if="subbed"
        push
        @click="unsubscribe(template.id)"
        color="red"
        label="Unsubscribe"
        dense
      >
        <q-icon size="md" name="mdi-numeric-negative-1" />
      </q-btn>
      <q-btn
        v-else
        push
        @click="subscribe(template.id)"
        color="secondary"
        label="Subscribe"
        dense
      >
        <q-icon size="md" name="mdi-numeric-positive-1" />
      </q-btn>
    </q-card-actions>

    <q-card-actions vertical v-if="isEdit">
      <q-btn push @click="updateClicked" color="secondary" label="Update" />
    </q-card-actions>

    <q-card-actions vertical v-if="creator && isEdit">
      <DeleteDialog
        :message="`Are you sure you want to delete this template?`"
        :confirmFunction="deleteClicked"
      />
    </q-card-actions>
  </q-card>
  <q-card v-else class="loading-ghost">
    <q-card-section class="text-center">
      <div class="ghost-avatar"></div>
      <div class="ghost-text"></div>
      <div class="ghost-text"></div>
      <div class="ghost-text"></div>
      <div class="ghost-text"></div>
      <div class="ghost-text"></div>
      <div class="ghost-text"></div>
    </q-card-section>
  </q-card>
</template>

<style>
.loading-ghost {
  animation: ghost-pulse 2s infinite;
}

@keyframes ghost-pulse {
  0% {
    opacity: 0.2;
  }

  50% {
    opacity: 1;
  }

  100% {
    opacity: 0.2;
  }
}

.ghost-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #ddd;
  margin: 0 auto;
}

.ghost-text {
  width: 80%;
  height: 20px;
  margin: 20px auto 0;
  background-color: #ddd;
}
</style>
