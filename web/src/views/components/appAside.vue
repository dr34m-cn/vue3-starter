<script setup>
import { ref, computed, markRaw } from 'vue'
const props = defineProps(['isCollapse'])
const emit = defineEmits(['changeCollapse'])
const changeCollapse = function changeCollapse() {
    emit('changeCollapse', !props.isCollapse);
}
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
import { HomeFilled, UserFilled } from '@element-plus/icons-vue';
const menuList = ref([{
    index: '/home',
    icon: markRaw(HomeFilled),
    title: computed(() => t('menu.home'))
}, {
    index: '/users',
    icon: markRaw(UserFilled),
    title: computed(() => t('menu.users'))
}])
import { useRoute } from 'vue-router'
const route = useRoute()
const leftIndex = computed(() => route.meta?.leftIndex)
</script>

<template>
    <div class="aside-box">
        <div class="aside-main">
            <el-menu :default-active="leftIndex" :router="true" :collapse="isCollapse">
                <template v-for="menuItem in menuList" :key="menuItem.index">
                    <el-menu-item :index="menuItem.index" v-if="!menuItem.children">
                        <el-icon>
                            <component :is="menuItem.icon" />
                        </el-icon>
                        <template #title>{{ menuItem.title }}</template>
                    </el-menu-item>
                    <el-sub-menu :index="menuItem.index" v-else>
                        <template #title>
                            <el-icon>
                                <component :is="menuItem.icon" />
                            </el-icon>
                            <span>{{ menuItem.title }}</span>
                        </template>
                        <el-menu-item :index="subItem.index" :key="subItem.index" v-for="subItem in menuItem.children">
                            {{ subItem.title }}
                        </el-menu-item>
                    </el-sub-menu>
                </template>
            </el-menu>
        </div>
        <div class="aside-bottom">
            <el-icon style="cursor: pointer;" size="30" @click="changeCollapse">
                <Expand v-if="isCollapse" />
                <Fold v-else />
            </el-icon>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.aside-box {
    border-right: 1px solid var(--border-color);

    .aside-main {
        height: calc(100% - 40px);
        overflow-y: auto;
        overflow-x: hidden;

        .el-menu {
            background-color: var(--app-left-background-color);
            border-right: none;
        }

        .el-menu--vertical {
            height: 100%;
        }
    }

    .aside-bottom {
        height: 40px;
        border-top: 1px solid var(--border-color);
        box-sizing: border-box;
        display: flex;
        align-items: center;
        padding: 0 18px;
    }
}
</style>
