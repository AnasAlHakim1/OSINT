<script setup>
import { ref, onMounted } from "vue";
import { Icon } from "@iconify/vue";
import { useRoute } from "vue-router";

const route = useRoute();

const resultName = ref(null);
const result = ref(null);

onMounted(async _ => {
    resultName.value = route.query.name;
    result.value = route.query.result;
})

const closeScripts = _ => {
    window.close();
};
</script>

<template>
    <section>
        <Icon icon="ph:x-circle-duotone" class="close" @click="closeScripts" />

        <h1>Result of {{ resultName }} :</h1>

        <pre>{{ result }}</pre>
    </section>
</template>

<style lang="scss" scoped>
section {
    padding-top: 2rem;
    padding-inline: 3rem;
    width: 100%;
    min-height: 100vh;
    background: rgba($first-color, 0.3);

    .close {
        width: 28px;
        height: 28px;
        position: absolute;
        top: 1rem;
        right: 1rem;
        color: $error-color;
        cursor: pointer;
    }

    h1 {
        font-size: 2rem;
    }

    pre {
        padding: 1rem;
    }
}
</style>