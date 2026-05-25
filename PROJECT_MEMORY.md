# 项目记忆

## 项目目标
- 三维扫描仪展示网站，用于介绍设备、展示 3D 样件、引导客户联系咨询。

## 当前进度
- 已完成首页关键修复并推送到 GitHub `main` 分支，等待 GitHub Pages 自动部署。

## 已修改的文件
- `PROJECT_MEMORY.md`
- `index.html`
- `style.css`
- `assets/models/calibration-block.glb`
- `assets/models/industrial-gear.glb`
- `assets/models/color-sample-car.glb`
- `assets/samples/calibration-block.stl`
- `assets/samples/industrial-gear.stl`
- `assets/samples/color-sample-car.stl`
- `assets/samples/README.txt`

## 已确认结论
- 项目根目录：`F:\三维扫描仪网站`
- 当前根目录未发现已有 `PROJECT_MEMORY.md`。
- 首页可通过本机临时服务正常打开。
- Polyga 的 GLB/ZIP 直链返回 `403 Forbidden`，3D 样件区会一直加载，当前方案不稳定。
- 手机端汉堡菜单点击后菜单仍不显示，原因是 CSS 缺少 `.nav-menu.active` 显示规则。
- 安装包下载链接、`manual.html`、淘宝商品页、网页版旺旺链接当前可访问。
- `index.html` 第 323 行有一个 FontAwesome 类名写错：`fa-solid = fa-check-double`。
- 已移除 Polyga CDN 热链，改用站内轻量 GLB 演示模型，避免 403 和外站防盗链。
- 已将 `model-viewer` 从 Google CDN 改到 jsDelivr CDN。
- 已修复手机端 `.nav-menu.active` 样式，汉堡菜单可展开并在点击导航后收起。
- 已修复错误图标类名。
- 已将旺旺链接改为可降级：有 JS 时尝试唤起旺旺客户端，同时打开网页版；无 JS 时直接打开网页版。
- 已给外部新窗口链接补充 `rel="noopener noreferrer"`。
- 2026-05-25：修复提交已推送到 `origin/main`，提交包含网站修复与站内 3D 演示资源。

## 未解决问题
- 当前 3D 样件是轻量演示模型，不是真实高精扫描数据；真实模型建议后续放到 GitHub Releases、对象存储或由旺旺发送。
- 站点仍缺少真实扫描仪照片、扫描过程视频和误差报告，这些会更利于成交。

## 下一步行动
- 等待 GitHub Pages 自动部署生效后，打开线上网址复查。
- 后续可补充真实设备图片、真实扫描样件和淘宝转化按钮。

## 开始行动
- 2026-05-25：创建项目记忆文件并开始网站改进点检查。
