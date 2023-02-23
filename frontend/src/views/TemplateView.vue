<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

// Fecth all Template from DB
const templates = ref([]);

const fetchTemplates = async () => {
  const result = await axios.get("http://127.0.0.1:8000/api/templates/");

  templates.value = result.data;
};

// Fecth all User from DB

const users = ref([]);
//const currentUser = ref(null);

const fetchUsers = async () => {
  users.value = (await axios.get("http://127.0.0.1:8000/api/users/")).data;
};

onMounted(() => {
  fetchTemplates();
  fetchUsers();
});
</script>

<template>
  {{ templates }}
</template>
