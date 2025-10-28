<script setup>
import lightDark from './lightDark.vue';
import locale from './locale.vue';
import logo from './logo.vue';
import user from './user.vue';
</script>

<template>
    <div class="header-box">
        <logo class="logo" @click="$router.push('/')" />
        <div class="header-right">
            <locale class="header-item" />
            <lightDark class="header-item" />
            <user class="header-item" />
        </div>
    </div>
</template>

<style lang="scss" scoped>
.header-box {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;

    .logo {
        cursor: pointer;
    }

    .header-right {
        display: flex;
        align-items: center;
        margin-right: -6px;
    }

    .header-item {
        margin: 0 12px;
    }
}
</style>
