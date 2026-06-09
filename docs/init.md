
# 初始化
首次运行前后，需要做的修改

## 后端
- 修改 backend/env/.env.环境, 中的数据库和redis配置
- 进入目录 backend/app/scripts/data，这里是初始化数据，在 sys_param.json 中修改 sys_web_logo 的域名， 也可在登陆后台之后修改(平台管理->参数管理)

## 前端
修改 frontend/web/.env.环境，中的 VITE_API_BASE_URL


## 首次登陆后台
平台管理->参数管理，修改 sys_web_logo 的 config_value 的域名
