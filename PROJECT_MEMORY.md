# 项目记忆

## 项目目标
- 三维扫描仪展示网站，用于介绍设备、展示 3D 样件、引导客户联系咨询。

## 当前进度
- 已完成首页四大核心模块（中英文切换、扫描工作流、折叠更新日志、折叠 FAQ 问答）开发并生成 index_en.html 英文主页，并在本地和 Git 暂存通过。
- 已参考 Polyga FlexScan3D 手册结构，重写 `manual.html` 为 MSscan3D 自有中文用户手册。
- 已将手册“脚本与自动化接口”改为 FlexScan3D/MSscan3D 通用的 Lua 函数命令表。

## 已修改的文件
- `PROJECT_MEMORY.md`
- `index.html`
- `style.css`
- `index_en.html` [NEW]
- `assets/models/calibration-block.glb`
- `assets/models/industrial-gear.glb`
- `assets/models/color-sample-car.glb`
- `assets/samples/calibration-block.stl`
- `assets/samples/industrial-gear.stl`
- `assets/samples/color-sample-car.stl`
- `assets/samples/README.txt`
- `manual.html`

## 已确认结论
- 项目根目录：`F:\三维扫描仪网站`
- 当前项目已建立并持续维护 `PROJECT_MEMORY.md`。
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
- 2026-05-25：`manual.html` 已重写为 6 大章、12 小节，覆盖安装、硬件、标定、扫描、点云处理、导出、自动化和故障排查。
- 新手册内容为 MSscan3D 自有中文说明，没有复制 Polyga 原文。
- 2026-05-25：已核对 Polyga/FlexScan3D 手册函数目录，脚本章节应使用 Lua 函数调用，不使用 XML 指令。
- 2026-05-25：本地验证 `manual.html#ch6-1` 可显示 `ScannerConnect()`、`SetScannerExposure(...)`、`Rotary360Scan(...)` 等命令，旧 XML 开销不会在页面显示。
- 2026-05-25：转台脚本示例按第一个电机写为 `motor=1`，避免把电机编号误写成 0。
- 2026-05-27：【重要开发规范】已确认最新编译的三维扫描仪主程序安装包物理存放路径为 `F:\3D3YC\MSscan3D-Setup.exe`。以后每次软件更新或发布时，均需使用项目本地的 `gh_cli` 工具将该文件覆盖上传至官方的 Releases 托管仓库中，并同步修正 `index.html` 的前台下载大小数字标识。
- 2026-05-31：Antigravity 登录卡住的原因不是账号问题，而是 FlClash 虚拟网卡未真正启动；根因是 `kuaimiaoHelperService` 占用 `127.0.0.1:47890`，导致 `FlClashHelperService` 崩溃。已停止 `kuaimiaoHelperService`，启动 `FlClashHelperService`，并让 FlClash TUN 网卡 `Meta Tunnel` 变为 `Up`，Antigravity 已可连接。
- 2026-05-31：快猫卸载后残留的 `kuaimiaoHelperService` 服务已删除；`127.0.0.1:47890` 当前由 `FlClashHelperService` 占用，FlClash 虚拟网卡仍为 `Up`。
- 2026-06-03：已清理三张消防图素材的棋盘格残留，保留原图并输出 `fire_extinguisher_clean.png`、`alarm_bell_clean.png`、`fire_engine_clean.png`。
- 2026-06-03：已为 `Gemini_Generated_Image_w1ztlww1ztlww1zt.png` 扣除白色背景，输出透明版 `Gemini_Generated_Image_w1ztlww1ztlww1zt_transparent.png`。
- 2026-06-12：官网四大全新优化模块（中英文双语一键切换、相移结构光工作流、软件折叠更新日志、折叠 FAQ 风琴问答）开发完毕，通过本地 HTML 结构闭合测试与 Git 暂存。

## 未解决问题
- 当前 3D 样件是轻量演示模型，不是真实高精扫描数据；真实模型建议后续放到 GitHub Releases、对象存储或由旺旺发送。
- 站点仍缺少真实扫描仪照片、扫描过程视频和误差报告，这些会更利于成交。
- 手册里的部分参数仍是通用建议，后续可根据真实硬件套装型号继续细化。
- 脚本示例里的扫描仪名称、旋转台插件 ID、COM 口仍需按用户电脑里的实际软件配置替换。

## 下一步行动
- 推送新版脚本手册到 GitHub，并等待 GitHub Pages 自动部署生效。
- 后续可补充真实设备图片、真实扫描样件和淘宝转化按钮。

## 开始行动
- 2026-05-25：创建项目记忆文件并开始网站改进点检查。
