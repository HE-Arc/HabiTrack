<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
const users = ref([]);

const fetchUsers = async () => {
  const res = await axios.get("http://localhost:8000/api/users/");
  users.value = res.data;
};

onMounted(() => {
  fetchUsers();
});
</script>

<template>
  {{ users }}
</template>
