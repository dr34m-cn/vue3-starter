# Vue3-Starter

演示地址DEMO: [http://vue3-demo.dr34m.cn/](http://vue3-demo.dr34m.cn/)

根目录为python后端（推荐python3.11），使用方法为

```sh
pip install -r requirements.txt
python main.py
```

web目录为前端（推荐node22），使用方法为

```sh
npm install
# 运行
npm run dev
# 打包
npm run build
```

前端打包后，可把`dist`目录下的所有文件放到根目录`front`下（没有则创建，后端会代理该目录），启动后端后访问[http://127.0.0.1:8023](http://127.0.0.1:8023)即可访问前端，并且无须担心跨域等问题
