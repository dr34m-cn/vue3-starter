<script setup>
import { ref, onMounted, computed } from 'vue';
import { getUsers, putUsers, postUsers, getUsersExport } from '@/api/user';
import { Check, Close, EditPen, Lock } from '@element-plus/icons-vue';
import { parseTime, download } from '@/utils/utils';
const cuDataList = ref({
    count: 0,
    dataList: []
})
const params = ref({
    search: '',
    enable: null,
    pageNum: 1,
    pageSize: 30
})
const loading = ref(false);
const getDataList = () => {
    loading.value = true;
    getUsers(params.value).then(res => {
        cuDataList.value = res.data;
    }).finally(() => {
        loading.value = false;
    })
}
onMounted(() => {
    getDataList();
})
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const handleSizeChange = (val) => {
    params.value.pageSize = val;
    getDataList();
}
const handleCurrentChange = (val) => {
    params.value.pageNum = val;
    getDataList();
}

const postParams = ref({
    username: '',
    name: '',
    enable: 0,
});
const postShow = ref(false);
const postFormRef = ref();
const hidePost = () => {
    postFormRef.value.clearValidate();
    postShow.value = false;
}
const doPostUsers = () => {
    loading.value = true;
    postUsers(postParams.value).then(() => {
        ElMessage({
            message: t('user.success'),
            type: 'success'
        })
        getDataList();
        if (postShow.value) {
            hidePost();
        }
    }).finally(() => {
        loading.value = false;
    })
}

const enableUser = (user, enable) => {
    postParams.value = JSON.parse(JSON.stringify(user));
    postParams.value.enable = enable;
    doPostUsers();
}
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
const showPost = (user) => {
    postParams.value = JSON.parse(JSON.stringify(user));
    postShow.value = true;
}
const postSubmit = () => {
    postFormRef.value.validate((valid) => {
        if (valid) {
            doPostUsers();
        }
    })
}

const putParams = ref({
    userId: 0,
    passwd: '',
    passwd2: ''
})
const putFormRef = ref();
const putShow = ref(false);
const validatePass2 = (rule, value, callback) => {
    if (value == '' || value == null || value.length < 6) {
        callback(new Error(t('user.newPasswd2Rule')));
    } else if (value !== putParams.value.passwd) {
        callback(new Error(t('user.newPasswd2Error')));
    } else {
        callback();
    }
}
const putRules = ref({
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

const showPut = (user) => {
    postParams.value = JSON.parse(JSON.stringify(user));
    putParams.value.userId = user.id;
    putShow.value = true;
}

const hidePut = () => {
    putFormRef.value.clearValidate();
    putShow.value = false;
    putParams.value = {
        userId: 0,
        passwd: '',
        passwd2: ''
    }
}

const doPutUser = () => {
    putFormRef.value.validate((valid) => {
        if (valid) {
            loading.value = true;
            putUsers(putParams.value).then(() => {
                ElMessage({
                    message: t('user.success'),
                    type: 'success'
                })
                hidePut();
            }).finally(() => {
                loading.value = false;
            })
        }
    })
}


const expLoading = ref(false);
const exportExcel = () => {
    expLoading.value = true;
    getUsersExport(params.value).then(res => {
        const fileName = t('users.userList') + '.xlsx';
        download(res, fileName);
    }).finally(() => {
        expLoading.value = false;
    })
}
</script>

<template>
    <div class="users">
        <div class="users-header">
            <div class="left">
                <el-input @input="getDataList" clearable style="width: 480px;margin-right: 16px;"
                    v-model="params.search" :placeholder="$t('users.search')"></el-input>
                <el-select @change="getDataList" clearable :placeholder="$t('users.isEnabled')"
                    style="width: 100px;margin-right: 16px;" v-model="params.enable">
                    <el-option key="en_1" :label="$t('users.enable')" :value="1"></el-option>
                    <el-option key="en_0" :label="$t('users.disable')" :value="0"></el-option>
                </el-select>
            </div>
            <div class="right">
                <el-button :loading="expLoading" @click="exportExcel" type="primary">
                    {{ $t('users.export') }}
                </el-button>
            </div>
        </div>
        <el-table v-loading="loading" current-row-key="id" :data="cuDataList.dataList" stripe
            style="width: 100%;height: calc(100% - 96px)">
            <el-table-column prop="id" :label="$t('users.no')" width="60" />
            <el-table-column prop="enable" :label="$t('users.isEnabled')" width="90">
                <template #default="scope">
                    <span style="color: #67C23A;" v-if="scope.row.enable">{{ $t('users.enable') }}</span>
                    <span style="color: #F56C6C;" v-else>{{ $t('users.disable') }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="name" :label="$t('user.nameLabel')" />
            <el-table-column prop="username" :label="$t('login.usernameLabel')" />
            <el-table-column prop="role" :label="$t('users.role')" width="120">
                <template #default="scope">
                    <span v-if="scope.row.role == 2">{{ $t('users.admin') }}</span>
                    <span v-else-if="scope.row.role == 1">{{ $t('users.user') }}</span>
                    <span v-else-if="scope.row.role == 0">{{ $t('users.superAdmin') }}</span>
                    <span v-else>？？</span>
                </template>
            </el-table-column>
            <el-table-column prop="createTime" :label="$t('users.createTime')" width="180">
                <template #default="scope">
                    {{ parseTime(scope.row.createTime) }}
                </template>
            </el-table-column>
            <el-table-column prop="id" :label="$t('users.operate')" width="320">
                <template #default="scope">
                    <template v-if="scope.row.role != 0">
                        <el-button @click="enableUser(scope.row, 0)" v-if="scope.row.enable == 1" :icon="Close"
                            size="small" type="danger">{{ $t('users.disable') }}</el-button>
                        <el-button @click="enableUser(scope.row, 1)" v-else type="success" :icon="Check" size="small">{{
                            $t('users.enable') }}</el-button>
                        <el-button @click="showPost(scope.row)" :icon="EditPen" size="small" type="primary">{{
                            $t('users.edit') }}</el-button>
                        <el-button @click="showPut(scope.row)" :icon="Lock" size="small" type="warning">{{
                            $t('users.resetPwdOnly') }}</el-button>
                    </template>
                    <span v-else>--</span>
                </template>
            </el-table-column>
        </el-table>
        <div class="page-box">
            <el-pagination v-model:current-page="params.pageNum" v-model:page-size="params.pageSize"
                :page-sizes="[30, 50, 300, 500]" :background="true" layout="total, sizes, prev, pager, next, jumper"
                :total="cuDataList.count" @size-change="handleSizeChange" @current-change="handleCurrentChange" />
        </div>

        <el-dialog width="460px" :append-to-body="true" v-model="postShow" :title="$t('users.edit')"
            :before-close="hidePost">
            <el-form ref="postFormRef" :model="postParams" :rules="postRules" label-width="100">
                <el-form-item prop="enable" :label="$t('users.enable')">
                    <el-switch :active-value="1" :inactive-value="0" v-model="postParams.enable" />
                </el-form-item>
                <el-form-item prop="username" :label="$t('login.usernameLabel')">
                    <el-input v-model="postParams.username" :placeholder="$t('login.username')"></el-input>
                </el-form-item>
                <el-form-item prop="name" :label="$t('user.nameLabel')">
                    <el-input v-model="postParams.name" :placeholder="$t('user.name')"></el-input>
                </el-form-item>
                <el-form-item prop="role" :label="$t('users.role')">
                    <el-select v-model="postParams.role">
                        <el-option key="ro_1" :label="$t('users.user')" :value="1"></el-option>
                        <el-option key="ro_2" :label="$t('users.admin')" :value="2"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button :loading="loading" type="primary" @click="postSubmit">{{ $t('user.save') }}</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>

        <el-dialog width="520px" :append-to-body="true" v-model="putShow" :title="$t('users.resetPwd', {
            username: postParams.username,
            name: postParams.name
        })" :before-close="hidePut">
            <el-form ref="putFormRef" :model="putParams" :rules="putRules" label-width="120">

                <el-form-item prop="passwd" :label="$t('user.newPasswdLabel')">
                    <el-input type="password" show-password v-model="putParams.passwd"
                        :placeholder="$t('user.newPasswd')"></el-input>
                </el-form-item>
                <el-form-item prop="passwd2" :label="$t('user.newPasswd2Label')">
                    <el-input type="password" show-password v-model="putParams.passwd2"
                        :placeholder="$t('user.newPasswd2')"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button :loading="loading" type="primary" @click="doPutUser">{{ $t('user.save') }}</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>
    </div>
</template>

<style lang="scss" scoped>
.users {
    padding: 16px;
    height: 100%;
    box-sizing: border-box;

    .users-header {
        margin-bottom: 16px;
        display: flex;
        justify-content: space-between;

        .left {
            display: flex;
            align-items: center;
        }

        .right {
            display: flex;
            align-items: center;
        }
    }

    .page-box {
        display: flex;
        justify-content: right;
        margin-top: 16px;
    }
}
</style>
