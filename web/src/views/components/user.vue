<script setup>
import { ref, computed } from 'vue';
import { logout, putUser, postUser } from '@/api/user';
import { useAppStore } from '@/store/useAppStore';
const appStore = useAppStore();
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
const router = useRouter()
const doLogout = () => {
    logout().then(() => {
        appStore.set('user', null);
        router.replace('/login');
    })
}

import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const putUserParams = ref({
    oldPasswd: '',
    passwd: '',
    passwd2: ''
})
const validatePass2 = (rule, value, callback) => {
    if (value == '' || value == null || value.length < 6) {
        callback(new Error(t('user.newPasswd2Rule')));
    } else if (value !== putUserParams.value.passwd) {
        callback(new Error(t('user.newPasswd2Error')));
    } else {
        callback();
    }
}
const putRules = ref({
    oldPasswd: [{
        required: true,
        min: 6,
        message: computed(() => t('user.oldPasswdRule')),
        trigger: ['blur', 'change']
    }],
    passwd: [{
        required: true,
        min: 6,
        message: computed(() => t('user.newPasswdRule')),
        trigger: ['blur', 'change']
    }],
    passwd2: [{
        validator: validatePass2,
        trigger: ['blur', 'change']
    }]
})
const putFormRef = ref()
const putLoading = ref(false)
const doPutUser = () => {
    putFormRef.value.validate((valid) => {
        if (valid) {
            putLoading.value = true;
            putUser({
                oldPasswd: putUserParams.value.oldPasswd,
                passwd: putUserParams.value.passwd
            }).then(() => {
                ElMessage({
                    message: t('user.success'),
                    type: 'success'
                })
                closePut();
                appStore.set('user', null);
                router.replace('/login');
            }).finally(() => {
                putLoading.value = false;
            })
        }
    })

}
const putShow = ref(false);
const showPut = () => {
    putUserParams.value = {
        oldPasswd: '',
        passwd: '',
        passwd2: ''
    }
    putShow.value = true;
}
const closePut = () => {
    putFormRef.value.clearValidate();
    putShow.value = false;
}

const postUserParams = ref({
    username: '',
    name: ''
})
const postRules = ref({
    username: [{
        required: true,
        min: 3,
        message: computed(() => t('login.usernameRule')),
        trigger: ['blur', 'change']
    }],
    name: [{
        required: true,
        message: computed(() => t('user.name')),
        trigger: ['blur', 'change']
    }]
})
const postFormRef = ref()
const postLoading = ref(false)
const doPostUser = () => {
    postFormRef.value.validate((valid) => {
        if (valid) {
            postLoading.value = true;
            postUser(postUserParams.value).then(res => {
                appStore.set('user', res.data);
                ElMessage({
                    message: t('user.success'),
                    type: 'success'
                })
                closePost();
            }).finally(() => {
                postLoading.value = false;
            })
        }
    })
}
const postShow = ref(false);
const showPost = () => {
    postUserParams.value = {
        username: appStore.user.username,
        name: appStore.user.name
    }
    postShow.value = true;
}
const closePost = () => {
    postFormRef.value.clearValidate();
    postShow.value = false;
}


</script>
<template>
    <div class="header-user-box">
        <el-dropdown v-if="$store.user" trigger="click">
            <div class="header-user">
                <el-icon>
                    <Avatar />
                </el-icon>
                <span class="username">{{ $store.user.name }}</span>
                <el-icon>
                    <ArrowDown />
                </el-icon>
            </div>
            <template #dropdown>
                <el-dropdown-menu>
                    <el-dropdown-item @click="showPost">{{ $t('header.userinfo') }}</el-dropdown-item>
                    <el-dropdown-item @click="showPut">{{ $t('header.setPwd') }}</el-dropdown-item>
                    <el-dropdown-item @click="doLogout">{{ $t('header.logout') }}</el-dropdown-item>
                </el-dropdown-menu>
            </template>
        </el-dropdown>
        <el-dialog width="460px" :append-to-body="true" v-model="postShow" :title="$t('header.userinfo')"
            :before-close="closePost">
            <el-form ref="postFormRef" :model="postUserParams" :rules="postRules" label-width="100">
                <el-form-item prop="username" :label="$t('login.usernameLabel')">
                    <el-input v-model="postUserParams.username" :placeholder="$t('login.username')"></el-input>
                </el-form-item>
                <el-form-item prop="name" :label="$t('user.nameLabel')">
                    <el-input v-model="postUserParams.name" :placeholder="$t('user.name')"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button :loading="postLoading" type="primary" @click="doPostUser">{{ $t('user.save')
                    }}</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>
        <el-dialog width="520px" :append-to-body="true" v-model="putShow" :title="$t('header.setPwd')"
            :before-close="closePut">
            <el-form ref="putFormRef" :model="putUserParams" :rules="putRules" label-width="120">
                <el-form-item prop="oldPasswd" :label="$t('user.oldPasswdLabel')">
                    <el-input type="password" show-passward v-model="putUserParams.oldPasswd"
                        :placeholder="$t('user.oldPasswd')"></el-input>
                </el-form-item>
                <el-form-item prop="passwd" :label="$t('user.newPasswdLabel')">
                    <el-input type="password" show-password v-model="putUserParams.passwd"
                        :placeholder="$t('user.newPasswd')"></el-input>
                </el-form-item>
                <el-form-item prop="passwd2" :label="$t('user.newPasswd2Label')">
                    <el-input type="password" show-password v-model="putUserParams.passwd2"
                        :placeholder="$t('user.newPasswd2')"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button :loading="putLoading" type="primary" @click="doPutUser">{{ $t('user.save')
                    }}</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>
    </div>

</template>

<style lang="scss" scoped>
.header-user-box {
    display: flex;
    align-items: center;

    .header-user {
        display: flex;
        align-items: center;
        cursor: pointer;

        .username {
            margin: 0 4px;
        }
    }
}
</style>
