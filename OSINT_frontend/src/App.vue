<script setup>
import Flowchart from './pages/Flowchart.vue'
</script>

<template>
  <main>
    <router-view />
  </main>
</template>

<style lang="scss">
@font-face {
  font-family: 'Roboto';
  src: url('./assets/fonts/Roboto-Regular.ttf');
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Roboto', sans-serif;
}

main {
  background: rgba($first-color, 0.3);
}


/* width */
::-webkit-scrollbar {
  width: 1rem;
}

/* Track */
::-webkit-scrollbar-track {
  background: rgba($third-color, 0.2); 
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: $first-color; 

  &:hover {
    background: rgba($first-color, 0.7);
  }
}

</style>
