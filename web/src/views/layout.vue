<script setup>
import { ref } from 'vue';
import appHeader from '@/views/components/appHeader.vue';
import appLeft from './components/appAside.vue';
let isCollapse = ref(false);
const changeCollapse = function changeCollapse(val) {
    isCollapse.value = val;
}
</script>

<template>
    <div class="app-main">
        <appHeader class="app-header" />
        <appLeft :isCollapse="isCollapse" @changeCollapse="changeCollapse"
            :class="`app-left${isCollapse ? ' left-collapse' : ''}`" />
        <div :class="`app-content${isCollapse ? ' content-collapse' : ''}`">
            <router-view />
        </div>
    </div>
</template>

<style lang="scss" scoped>
.app-main {
    width: 100%;
    height: 100vh;
    box-sizing: border-box;
    position: relative;
    overflow-y: auto;

    .app-header {
        position: fixed;
        z-index: 2;
        top: 0;
        left: 0;
        right: 0;
        height: 50px;
        width: 100%;
        box-sizing: border-box;
        box-shadow: 0 5px 10px var(--app-header-shadow-color);

        background: var(--app-header-background-color);
        backdrop-filter: blur(4px);
    }

    .app-left {
        position: fixed;
        left: 0;
        top: 50px;
        bottom: 0;
        transition: all .3s ease-in-out;
        width: 201px;
        box-sizing: border-box;
        background: var(--app-left-background-color);
    }

    .left-collapse {
        width: 65px;
    }

    .app-content {
        width: 100%;
        height: 100%;
        padding-left: 201px;
        padding-top: 50px;
        transition: all .3s ease-in-out;
        box-sizing: border-box;
    }

    .content-collapse {
        padding-left: 65px;
    }


}
</style>
