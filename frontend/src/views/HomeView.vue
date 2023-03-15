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
        Le but de se projet est de pouvoir suivre ses habitudes, il est possible
        de créer des Templates, d'y souscrire ainsi que une fois par jour
        remplir un mini-sondage selon l'habitude qu'on veut suivre.
      </div>
    </div>
  </div>
  <img src="../assets/logo-hearc.png" class="float-right vertical-bottom" />
</template>
