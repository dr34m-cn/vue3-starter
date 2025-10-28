import request from "@/utils/request";

// 登录
export function login(data) {
  return request({
    url: "/noAuth/login",
    method: "post",
    data,
  });
}

// 登出
export function logout() {
  return request({
    url: "/noAuth/login",
    method: "delete",
  });
}

// 获取当前用户信息
export function getUser() {
  return request({
    url: "/user",
    method: "get",
  });
}

// 修改当前用户密码
export function putUser(data) {
  return request({
    url: "/user",
    method: "put",
    data,
  });
}

// 修改当前用户信息
export function postUser(data) {
  return request({
    url: "/user",
    method: "post",
    data,
  });
}

// 用户列表
export function getUsers(params) {
  return request({
    url: "/users",
    method: "get",
    params,
  });
}

// 重置密码用户
export function putUsers(data) {
  return request({
    url: "/users",
    method: "put",
    data,
  });
}

// 更新用户
export function postUsers(data) {
  return request({
    url: "/users",
    method: "post",
    data,
  });
}

export function getUsersExport(params) {
  return request({
    url: "/users/export",
    method: "get",
    params,
    responseType: "blob",
  });
}
