# MSscan3D 官网项目进度与运维记忆 (PROGRESS.md)

## 1. 核心目录与发布规范 (永久生效)
* **安装包本地标准源路径**：`F:\3D3YC\MSscan3D-Setup.exe`
* **官网代码主仓库**：`F:\三维扫描仪网站`
* **官方发布托管库**：GitHub `ouyangxing3623301986/MSscan3D` (Release 标签: `v3.3`)
* **官网下载直链**：`https://github.com/ouyangxing3623301986/MSscan3D/releases/download/v3.3/MSscan3D-Setup.exe`
* **专用上传工具**：`F:\三维扫描仪网站\gh_cli\bin\gh.exe`

## 2. 最近关键里程碑
* **2026-10-14**：
  - 【风格全面重塑】落地“国际工业光学旗舰风”：升级顶栏为悬浮毛玻璃药丸胶囊（Pill Nav），底色升级为极致曜石黑与深空 CAD 工程坐标微网格，首屏软件窗口植入动态青蓝激光扫描光束（Laser Scanner Line），视觉质感全面媲美基恩士/徕卡/苹果Pro；
  - 成功将本地最新主程序安装包 `MSscan3D-Setup.exe`（1,140,199,471 字节，约 1.06GB，修改时间 2026/10/14 20:58:28）上传覆盖至 GitHub Releases `v3.3`；
  - 官网中英文主页下载按钮同步更新标注为 `(1.06GB)` 并推送到 Gitee 和 GitHub；
  - 云端直链核验通过，HTTP 200 OK，体积与本地 100% 吻合。
* **2026-09-12**：
  - 固化 `F:\3D3YC` 为最新主程序安装包上传源目录；
  - 成功将本地最新安装包 `MSscan3D-Setup.exe`（943,226,646 字节，约 899.5MB，修改时间 2026/09/12 01:49:48）上传覆盖至 GitHub Releases `v3.3`；
  - 线上直链测试通过，HTTP 状态码 200 OK，体积与本地完全一致；
  - 官网首页下载按钮与动态下载量统计逻辑正常工作。
* **2026-06-18**：完成 1200C 规格书网页 (`1200C_spec.html`) 与 FEA 方案说明书 (`Msscan_1200C_FEA_方案说明书.html`)，并于官网配置黄金渐变微动效入口。
* **2026-06-12**：完成官网双语切换、光栅工作流、折叠更新日志与 FAQ 问答系统。

## 3. 标准发版维护流程
每次在 `F:\3D3YC` 编译生成新的 `MSscan3D-Setup.exe` 后，仅需执行以下命令即可一键无缝覆盖官网下载包：
```powershell
& "F:\三维扫描仪网站\gh_cli\bin\gh.exe" release upload v3.3 "F:\3D3YC\MSscan3D-Setup.exe" --clobber --repo ouyangxing3623301986/MSscan3D
```
如安装包体积发生显著变化，同步核对 `index.html` 与 `index_en.html` 中的大小文字标注即可。
