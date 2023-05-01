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
  <div class="row justify-center">
    <div class="col-md-4 q-ma-md">
      <!--{{ users }}-->
      <div class="q-body-1">
        The goal of this project is to be able to follow your habits, it is
        possible to create Templates, subscribe to them and once a day fill a
        mini-survey according to the habit you want to follow.
      </div>
    </div>
  </div>
  <img src="../static/logo-hearc.png" class="float-right vertical-bottom" />
</template>
