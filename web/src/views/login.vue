<script setup>
import { ref, computed, onMounted } from 'vue'
import logo from '@/views/components/logo.vue'
import lightDark from './components/lightDark.vue';
import locale from './components/locale.vue';
import { login } from '@/api/user';
import { useI18n } from 'vue-i18n';
import { User, Lock } from '@element-plus/icons-vue'
const { t } = useI18n()
const params = ref({
  username: '',
  passwd: ''
})
const rules = ref({
  username: [{
    required: true,
    min: 3,
    message: computed(() => t('login.usernameRule')),
    trigger: ['blur', 'change']
  }],
  passwd: [{
    required: true,
    message: computed(() => t('login.passwdRule')),
    min: 6,
    trigger: ['blur', 'change']
  }]
})
import Motion from '@/utils/motion';
const remberPwd = ref(false);
const loginFormRef = ref();
const loading = ref(false)
import { useAppStore } from '@/store/useAppStore';
const appStore = useAppStore();
import { useRouter } from 'vue-router'
const router = useRouter()
const doLogin = () => {
  loginFormRef.value.validate((valid) => {
    if (valid) {
      loading.value = true;
      login(params.value).then(res => {
        if (remberPwd.value) {
          appStore.set('login', {
            username: params.value.username,
            passwd: btoa(unescape(encodeURIComponent(params.value.passwd)))
          });
        } else {
          appStore.set('login', null);
        }
        appStore.set('user', res.data);
        router.replace('/home');
      }).finally(() => {
        loading.value = false;
      })
    }
  })
}
onMounted(() => {
  if (appStore.login) {
    remberPwd.value = true;
    params.value = {
      username: appStore.login.username,
      passwd: decodeURIComponent(escape(atob(appStore.login.passwd)))
    };
  }
})
</script>

<template>
  <div class="login">
    <div class="login-box">
      <div class="login-header">
        <Motion>
          <locale class="locale" />
        </Motion>
        <Motion>
          <lightDark />
        </Motion>
      </div>
      <Motion :delay="100">
        <logo class="logo" />
      </Motion>
      <el-form ref="loginFormRef" :model="params" :rules="rules" label-width="0">
        <Motion :delay="150">
          <el-form-item prop="username">
            <el-input :prefix-icon="User" v-model="params.username" :placeholder="$t('login.username')"></el-input>
          </el-form-item>
        </Motion>
        <Motion :delay="200">
          <el-form-item prop="passwd">
            <el-input :prefix-icon="Lock" type="password" show-password v-model="params.passwd"
              :placeholder="$t('login.passwd')" @keyup.enter="doLogin"></el-input>
          </el-form-item>
        </Motion>
        <Motion :delay="250">
          <el-form-item>
            <el-checkbox v-model="remberPwd" label="记住密码" />
          </el-form-item>
        </Motion>
        <Motion :delay="300">
          <el-form-item>
            <el-button :loading="loading" @click="doLogin" type="primary">{{ $t('login.loginBtn')
              }}</el-button>
          </el-form-item>
        </Motion>
      </el-form>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.login {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px;
  display: flex;
  align-items: center;
  background: url('@/assets/images/login-bg.jpg') no-repeat center;
  background-size: cover;

  .login-box {
    position: relative;
    box-sizing: border-box;
    width: 520px;
    margin-left: 12%;
    background-color: var(--app-login-background-color);
    border-radius: 2px;
    display: flex;
    flex-direction: column;
    align-items: center;

    .login-header {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: right;
      box-sizing: border-box;
      padding: 32px;

      .locale {
        margin-right: 16px;
      }
    }

    .logo {
      margin: 40px;
    }

    :deep(.el-input) {
      font-size: 20px;

      .el-input__inner {
        height: 40px;
        font-size: 20px;
      }
    }

    :deep(.el-form-item) {
      margin: 37px;

      .el-form-item__error {
        font-size: 16px;
      }
    }

    :deep(.el-button) {
      margin: 30px 0;
      font-size: 20px;
      padding: 22px 20px;
      width: 400px;
    }
  }
}
</style>
