<script setup>
const props = defineProps({
  errors: Array,
});
</script>

<template>
  <q-banner
    v-if="props.errors"
    inline-actions
    class="q-ma-md text-white bg-red"
  >
    <div class="text-h6">
      <q-icon left size="md" name="mdi-alert" />
      Input errors
    </div>

    <q-separator dark class="q-my-md" inset />

    <div class="self-center">
      <ul v-if="Array.isArray(props.errors)">
        <li v-for="(err, index) in props.errors.flat()" :key="index">
          {{ err }}
        </li>
      </ul>
      <div v-else>{{ props.errors }}</div>
    </div>
  </q-banner>
</template>
