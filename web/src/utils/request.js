import i18n from "./i18n";
import axios from "axios";
import { ElNotification } from "element-plus";
import router from "@/router";
const { t } = i18n.global;
let timeout = 90000;

axios.defaults.headers["Content-Type"] = "application/json;charset=utf-8";
const service = axios.create({
  baseURL: "/svr",
  timeout,
});
// request拦截器
service.interceptors.request.use(
  (config) => {
    config.headers["Accept-Language"] = localStorage.getItem("lang") || "zh-CN";
    return config;
  },
  (error) => {
    console.log(error);
    Promise.reject(error);
  }
);

// 响应拦截器
service.interceptors.response.use(
  async (res) => {
    // 导出等二进制响应错误处理
    if (res.data.type == "application/json") {
      const blob = new Blob([res.data], { type: "application/json" });
      const rdt = await blob.text();
      res.data = JSON.parse(rdt);
    }
    const code = res.data?.code || 200;
    let msg = res.data?.msg || `errorCode: ${code}`;
    if (msg.includes("timed out")) {
      msg = t("network.timeout");
    }
    // 二进制数据则直接返回
    const contentType = res.headers["content-type"] || "application/json; charset=UTF-8";
    if (!contentType.includes("application/json") && !contentType.includes("text/html")) {
      return res;
    }
    if (code === 401) {
      window.$store.set("user", null);
      ElNotification({
        message: t("network.loginExpired"),
        type: "error",
        duration: 2 * 1000,
      });
      router.replace("/login");
      return Promise.reject(t("network.loginExpired"));
    } else if (code !== 200) {
      ElNotification({
        message: msg,
        type: "error",
        duration: 5 * 1000,
      });
      return Promise.reject(msg);
    } else {
      return res.data;
    }
  },
  (error) => {
    console.log("err" + error);
    let { message } = error;
    if (message == "Network Error") {
      message = t("network.networkErr");
    } else if (message.includes("timeout")) {
      message = t("network.timeout");
    } else if (message.includes("Request failed with status code")) {
      message = t("network.codeErr", { code: message.substr(message.length - 3) });
    }
    ElNotification({
      message: message,
      type: "error",
      duration: 5 * 1000,
    });
    return Promise.reject(error);
  }
);

export default service;
