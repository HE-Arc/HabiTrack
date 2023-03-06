<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
const users = ref([]);

const fetchUsers = async () => {
  const res = await axios.get("/users/");
  users.value = res.data;
};

onMounted(() => {
  fetchUsers();
});
</script>

<template>
  {{ users }}
</template>
