<script setup>
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();
// script中需使用computed否则不会动态刷新
const title = computed(() => t('home'));
</script>

<template>
    <div class="home">
        {{ title }} - {{ $t('homeTip') }}
    </div>
</template>

<style lang="scss" scoped>
.home {
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    padding: 16px;
}
</style>
