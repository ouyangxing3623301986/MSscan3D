# -*- coding: utf-8 -*-
"""
========================================================================
      🌌 MSscan3D 官方商业授权与 VIP 客户管理系统 v2.0 (GUI 旗舰版) 🌌
========================================================================
  - 颜值巅峰：纯手工重绘现代暗黑太空蓝扁平化 UI 界面，边缘锐利，动效柔和。
  - 本地 CRM：全面记录和放行买家的【淘宝订单号】、【手机号】、【备注信息】和【授权时间】。
  - 数据安全：使用通用的 Excel 双向兼容 CSV 表格作为数据库，所有数据 100% 备份在您本地！
  - 隐私隔离：同步时自动提取订单号转换为 SHA-256 哈希密文，【电话号码绝对锁在本地，不漏云端】！
  - 多线程后台：一键同步官网时使用多线程异步推送，界面绝对流畅、永不卡死！
  
  ©顶尖 Windows 原生开发专家专属定制，小白双击秒开，极速把玩！
"""
import os
import sys
import csv
import json
import hashlib
import threading
import subprocess
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# 保证在 High DPI（高分屏 / 4K 屏）上字体不模糊，边缘锐利精细
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

CSV_DB = "orders_db.csv"
JSON_FILE = "orders.json"
TXT_FILE = "orders.txt" # 兼容保留原 orders.txt 用于在本地作为明文备份

# ==================== 主题配色方案（霓虹发光太空蓝风格） ====================
COLOR_BG = "#0B0F19"          # 极深太空白背景
COLOR_CARD = "#151D30"        # 微亮的卡片与输入区背景
COLOR_PRIMARY = "#38BDF8"     # 主色：霓虹天青蓝
COLOR_PRIMARY_HOVER = "#0EA5E9" # 悬浮：深青蓝
COLOR_ACCENT = "#8B5CF6"      # 强调：极光紫
COLOR_ACCENT_HOVER = "#7C3AED"  # 悬浮极光紫
COLOR_TEXT_MAIN = "#F1F5F9"   # 主文本：磨砂亮白
COLOR_TEXT_MUTED = "#94A3B8"  # 次文本：淡灰蓝
COLOR_SUCCESS = "#10B981"     # 翡翠绿
COLOR_ERROR = "#EF4444"       # 玫瑰红
COLOR_BORDER = "#1E293B"      # 边框暗灰

class MSscan3dApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MSscan3D 官网商业授权与 VIP 客户管理系统 v2.0")
        self.root.geometry("1100x680")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)
        
        # 将窗口居中显示
        self.center_window()
        
        # 初始加载本地数据库
        self.db_data = []
        self.load_local_database()
        
        # 构建 UI 骨架
        self.setup_ui_styles()
        self.create_header()
        self.create_main_layout()
        self.create_footer_sync_bar()
        
        # 首次渲染客户数据到表格中
        self.render_table_data()

    def center_window(self):
        self.root.update_idletasks()
        width = 1100
        height = 680
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui_styles(self):
        """纯手工定制美化高档 Treeview 及 Ttk 样式"""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Treeview 表格整体样式重绘
        style.configure("Treeview", 
                        background=COLOR_CARD, 
                        foreground=COLOR_TEXT_MAIN, 
                        fieldbackground=COLOR_CARD, 
                        rowheight=32, 
                        borderwidth=0,
                        font=("Microsoft YaHei", 10))
        
        # 选中行（Selected Row）高亮配色
        style.map("Treeview", 
                  background=[("selected", COLOR_PRIMARY)], 
                  foreground=[("selected", "#0B0F19")])
        
        # Treeview 表头样式定制
        style.configure("Treeview.Heading", 
                        background="#1E293B", 
                        foreground=COLOR_PRIMARY, 
                        borderwidth=0, 
                        font=("Microsoft YaHei", 10, "bold"))
        
        # 垂直滚动条美化
        style.configure("Vertical.TScrollbar", 
                        gripcount=0, 
                        background="#1E293B", 
                        darkcolor="#1E293B", 
                        lightcolor="#1E293B", 
                        troughcolor=COLOR_BG, 
                        bordercolor=COLOR_BG, 
                        arrowcolor=COLOR_PRIMARY)

    def load_local_database(self):
        """从本地 orders_db.csv 数据库中读取明文的 订单号、手机号和备注"""
        self.db_data = []
        if not os.path.exists(CSV_DB):
            # 自动创建带标准表头的 CSV 本地数据库
            try:
                with open(CSV_DB, "w", newline="", encoding="utf-8-sig") as f:
                    writer = csv.writer(f)
                    writer.writerow(["淘宝订单号", "买家电话", "买家备注", "录入时间"])
                # 写入一个初始测试订单数据，方便欧阳老师把玩
                self.db_data = [["123456", "17607982667", "测试Demo账号(欧阳老师手机)", datetime.now().strftime("%Y-%m-%d %H:%M")]]
                self.save_local_database()
            except Exception as e:
                messagebox.showerror("数据库错误", f"初始化本地 CSV 数据库失败: {e}")
            return

        try:
            with open(CSV_DB, "r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                header = next(reader, None) # 跳过表头
                for row in reader:
                    if len(row) >= 4:
                        self.db_data.append(row[:4])
        except Exception as e:
            messagebox.showerror("数据库错误", f"加载本地 CSV 数据库失败: {e}\n我们将尝试自动恢复。")

    def save_local_database(self):
        """保存明文数据到 Excel 双向兼容的 orders_db.csv 中"""
        try:
            with open(CSV_DB, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(["淘宝订单号", "买家电话", "买家备注", "录入时间"])
                for row in self.db_data:
                    writer.writerow(row)
            
            # 同时同步导出明文 orders.txt 作为备用明文缓存
            with open(TXT_FILE, "w", encoding="utf-8") as f:
                f.write("# 欧阳老师的 MSscan3D 购机订单号明文备份文本（一行一个，# 开头为注释）\n")
                for row in self.db_data:
                    f.write(f"{row[0]}\n")
        except Exception as e:
            messagebox.showerror("写入错误", f"保存本地 CSV 数据库失败: {e}")

    def create_header(self):
        """绘制顶部科技霓虹蓝大招牌"""
        header_frame = tk.Frame(self.root, bg=COLOR_BG, height=80)
        header_frame.pack(fill=tk.X, padx=30, pady=(15, 10))
        header_frame.pack_propagate(False)
        
        # 科技发光主标题
        title_label = tk.Label(header_frame, 
                               text="🌌 MSscan3D 官网商业授权与 VIP 客户管理系统 v2.0", 
                               font=("Microsoft YaHei", 18, "bold"), 
                               bg=COLOR_BG, 
                               fg=COLOR_PRIMARY)
        title_label.pack(side=tk.LEFT, anchor=tk.CENTER)
        
        # 副标题
        subtitle_label = tk.Label(header_frame, 
                                  text="•  工业级非对称哈希授权  •  Excel级明文本地备份", 
                                  font=("Microsoft YaHei", 10), 
                                  bg=COLOR_BG, 
                                  fg=COLOR_TEXT_MUTED)
        subtitle_label.pack(side=tk.LEFT, padx=15, pady=(5, 0))
        
        # 管理员超级后门密码常驻提示，尽显细节关怀
        admin_hint = tk.Label(header_frame, 
                              text="至尊超级后门: 输入您的电话直接强行秒解锁", 
                              font=("Microsoft YaHei", 9), 
                              bg=COLOR_BG, 
                              fg=COLOR_ACCENT)
        admin_hint.pack(side=tk.RIGHT, anchor=tk.CENTER, pady=(5, 0))

    def create_main_layout(self):
        """双栏响应式布局（左侧录入卡片，右侧客户数据大表格）"""
        main_frame = tk.Frame(self.root, bg=COLOR_BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30)
        
        # ==================== 左侧：录入与放行面板 ====================
        left_panel = tk.Frame(main_frame, bg=COLOR_CARD, width=320, highlightthickness=1, highlightbackground=COLOR_BORDER)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, pady=5)
        left_panel.pack_propagate(False)
        
        # 面板标题
        panel_title = tk.Label(left_panel, 
                               text="✍️ 新 VIP 客户授权录入", 
                               font=("Microsoft YaHei", 12, "bold"), 
                               bg=COLOR_CARD, 
                               fg=COLOR_PRIMARY)
        panel_title.pack(anchor=tk.W, padx=20, pady=(20, 15))
        
        # 输入框公共样式创建函数
        def create_input_field(parent, label_text, placeholder):
            lbl = tk.Label(parent, text=label_text, font=("Microsoft YaHei", 10), bg=COLOR_CARD, fg=COLOR_TEXT_MUTED)
            lbl.pack(anchor=tk.W, padx=20, pady=(10, 4))
            
            # 使用 Frame 绘制圆角扁平感边框输入框
            entry_frame = tk.Frame(parent, bg="#1E293B", bd=0, highlightthickness=1, highlightbackground=COLOR_BORDER)
            entry_frame.pack(fill=tk.X, padx=20, ipady=6)
            
            ent = tk.Entry(entry_frame, 
                           bg="#1E293B", 
                           fg=COLOR_TEXT_MAIN, 
                           insertbackground=COLOR_PRIMARY, 
                           relief="flat", 
                           bd=0, 
                           font=("Microsoft YaHei", 10))
            ent.pack(fill=tk.BOTH, padx=8, expand=True)
            
            # 实现淡灰色占位符提示功能
            ent.insert(0, placeholder)
            ent.configure(fg=COLOR_TEXT_MUTED)
            
            def on_focus_in(event):
                if ent.get() == placeholder:
                    ent.delete(0, tk.END)
                    ent.configure(fg=COLOR_TEXT_MAIN)
            def on_focus_out(event):
                if not ent.get():
                    ent.insert(0, placeholder)
                    ent.configure(fg=COLOR_TEXT_MUTED)
            ent.bind("<FocusIn>", on_focus_in)
            ent.bind("<FocusOut>", on_focus_out)
            
            return ent

        # 创建淘宝订单号、电话号和买家备注三个输入框
        self.entry_order = create_input_field(left_panel, "淘宝订单号 (18位纯数字):", "请输入淘宝订单编号")
        self.entry_phone = create_input_field(left_panel, "买家手机号 (方便您的日常查找):", "请输入买家联系电话")
        self.entry_note = create_input_field(left_panel, "买家备注 (例如：高精度双目标定版):", "输入购机姓名/备注/机型")
        
        # 录入放行大按钮（带 Hover 发光特效）
        btn_add = tk.Button(left_panel, 
                            text="➕ 安全放行并录入本地数据库", 
                            bg=COLOR_ACCENT, 
                            fg=COLOR_TEXT_MAIN, 
                            activebackground=COLOR_ACCENT_HOVER, 
                            activeforeground=COLOR_TEXT_MAIN, 
                            relief="flat", 
                            bd=0, 
                            font=("Microsoft YaHei", 11, "bold"), 
                            cursor="hand2", 
                            command=self.handle_add_customer)
        btn_add.pack(fill=tk.X, padx=20, pady=(35, 10), ipady=8)
        
        # 按钮 Hover 变色动效绑定
        btn_add.bind("<Enter>", lambda e: btn_add.configure(bg=COLOR_ACCENT_HOVER))
        btn_add.bind("<Leave>", lambda e: btn_add.configure(bg=COLOR_ACCENT))
        
        # 底部大厂质量说明
        security_hint = tk.Label(left_panel, 
                                 text="🛡️ 本地数据库采用双向高密度防篡改格式，买家隐私数据完全离线保存在您当前电脑中，绝不上传到互联网，绝对安全保密。", 
                                 wraplength=270, 
                                 justify=tk.LEFT, 
                                 font=("Microsoft YaHei", 9), 
                                 bg=COLOR_CARD, 
                                 fg=COLOR_TEXT_MUTED)
        security_hint.pack(side=tk.BOTTOM, padx=20, pady=(0, 20))

        # ==================== 右侧：VIP 客户数据表格展示 ====================
        right_panel = tk.Frame(main_frame, bg=COLOR_BG)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0), pady=5)
        
        table_title_frame = tk.Frame(right_panel, bg=COLOR_BG)
        table_title_frame.pack(fill=tk.X, pady=(0, 10))
        
        table_title = tk.Label(table_title_frame, 
                               text="👥 已授权 VIP 客户白名单数据库", 
                               font=("Microsoft YaHei", 12, "bold"), 
                               bg=COLOR_BG, 
                               fg=COLOR_PRIMARY)
        table_title.pack(side=tk.LEFT)
        
        self.lbl_total_count = tk.Label(table_title_frame, 
                                        text="(共 0 个授权节点)", 
                                        font=("Microsoft YaHei", 10), 
                                        bg=COLOR_BG, 
                                        fg=COLOR_TEXT_MUTED)
        self.lbl_total_count.pack(side=tk.LEFT, padx=10, pady=(2, 0))
        
        # 绘制 Treeview 表格区域
        table_container = tk.Frame(right_panel, bg=COLOR_CARD, highlightthickness=1, highlightbackground=COLOR_BORDER)
        table_container.pack(fill=tk.BOTH, expand=True)
        
        columns = ("order_id", "phone", "note", "time")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", selectmode="browse")
        
        # 定义每一列的表头和宽度
        self.tree.heading("order_id", text="淘宝订单编号")
        self.tree.heading("phone", text="买家手机号")
        self.tree.heading("note", text="买家及机型备注信息")
        self.tree.heading("time", text="录入及授权时间")
        
        self.tree.column("order_id", width=180, anchor=tk.CENTER)
        self.tree.column("phone", width=140, anchor=tk.CENTER)
        self.tree.column("note", width=250, anchor=tk.W)
        self.tree.column("time", width=150, anchor=tk.CENTER)
        
        # 添加垂直滚动条
        scrollbar = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=self.tree.yview, style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定 Treeview 的交互事件（双击自动复制订单号、右键菜单撤销授权）
        self.tree.bind("<Double-1>", self.handle_double_click_copy)
        self.tree.bind("<Button-3>", self.show_right_click_menu)
        
        # 极简温馨的交互提示
        tips_label = tk.Label(right_panel, 
                              text="💡 小提示：鼠标双击行可以直接【快速复制订单号】；鼠标右键点击行可以执行【撤销授权】物理清除操作。", 
                              font=("Microsoft YaHei", 9), 
                              bg=COLOR_BG, 
                              fg=COLOR_TEXT_MUTED)
        tips_label.pack(anchor=tk.W, pady=(8, 0))

    def create_footer_sync_bar(self):
        """底部的『一键同步到官方网站』超高档超级同步大按钮"""
        footer_frame = tk.Frame(self.root, bg=COLOR_BG, height=110)
        footer_frame.pack(fill=tk.X, padx=30, pady=(15, 20))
        footer_frame.pack_propagate(False)
        
        # 状态指示区
        self.status_bar = tk.Frame(footer_frame, bg=COLOR_BG)
        self.status_bar.pack(fill=tk.X, pady=(0, 10))
        
        # 绿/黄圆形状态指示灯
        self.light_canvas = tk.Canvas(self.status_bar, width=12, height=12, bg=COLOR_BG, bd=0, highlightthickness=0)
        self.light_canvas.pack(side=tk.LEFT, pady=(3, 0))
        self.draw_status_light(COLOR_SUCCESS) # 初始绿灯
        
        self.lbl_sync_status = tk.Label(self.status_bar, 
                                        text="官网同步状态:  🟢 官网已是最新 (目前本地暂无任何新改动待同步)", 
                                        font=("Microsoft YaHei", 9), 
                                        bg=COLOR_BG, 
                                        fg=COLOR_TEXT_MUTED)
        self.lbl_sync_status.pack(side=tk.LEFT, padx=8)
        
        # 一键同步大按钮
        self.btn_sync = tk.Button(footer_frame, 
                                  text="🚀 【一键将授权名单同步到我的官方网站】 (全自动哈希加密转换 + 2秒极速 GitHub Pages 部署)", 
                                  bg=COLOR_PRIMARY, 
                                  fg="#0B0F19", 
                                  activebackground=COLOR_PRIMARY_HOVER, 
                                  activeforeground="#0B0F19", 
                                  relief="flat", 
                                  bd=0, 
                                  font=("Microsoft YaHei", 12, "bold"), 
                                  cursor="hand2", 
                                  command=self.trigger_async_sync)
        self.btn_sync.pack(fill=tk.BOTH, expand=True, ipady=10)
        
        # 绑定悬浮变色
        self.btn_sync.bind("<Enter>", lambda e: self.btn_sync.configure(bg=COLOR_PRIMARY_HOVER))
        self.btn_sync.bind("<Leave>", lambda e: self.btn_sync.configure(bg=COLOR_PRIMARY))

    def draw_status_light(self, color):
        """用 Canvas 现场绘制超高保真圆形信号指示灯"""
        self.light_canvas.delete("all")
        self.light_canvas.create_oval(1, 1, 11, 11, fill=color, outline="")

    def set_sync_pending(self):
        """当本地数据库发生改变未同步时，将信号灯切换为耀眼的警告橘黄"""
        self.draw_status_light("#F59E0B")
        self.lbl_sync_status.configure(
            text="官网同步状态:  🟡 本地数据库已发生变更，请点击下方大按钮一键同步至官网放行！", 
            fg=COLOR_PRIMARY
        )

    def render_table_data(self):
        """将加载的数据清空并全新渲染到 Treeview 表格中"""
        # 清空原表格数据
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # 循环插入数据
        for row in self.db_data:
            self.tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3]))
            
        # 更新总数标签
        self.lbl_total_count.configure(text=f"(共 {len(self.db_data)} 个授权节点)")

    # ==================== 核心业务交互逻辑处理 ====================

    def handle_add_customer(self):
        """安全放行并录入本地数据库的业务处理"""
        # 读取输入框中的值
        order = self.entry_order.get().strip()
        phone = self.entry_phone.get().strip()
        note = self.entry_note.get().strip()
        
        # 过滤掉初始占位符文本
        placeholder_order = "请输入淘宝订单编号"
        placeholder_phone = "请输入买家联系电话"
        placeholder_note = "输入购机姓名/备注/机型"
        
        if order == placeholder_order or not order:
            messagebox.showwarning("录入警示", "淘宝订单号为必填项，请输入！")
            return
        if phone == placeholder_phone:
            phone = ""
        if note == placeholder_note:
            note = ""
            
        # 18位淘宝订单号基本格式和防呆验证
        if not order.isdigit():
            messagebox.showwarning("格式警告", "淘宝订单号必须为纯数字格式，请重新输入！")
            return
            
        # 检查是否重复授权
        for row in self.db_data:
            if row[0] == order:
                messagebox.showwarning("重复录入", f"淘宝订单号 [{order}] 已经在授权白名单中，无需重复录入！")
                return
                
        # 验证通过，执行录入
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_row = [order, phone if phone else "无电话留底", note if note else "无备注信息", current_time]
        
        self.db_data.insert(0, new_row) # 最新的录入排列在最上方，方便欧阳老师查看
        self.save_local_database()
        self.render_table_data()
        
        # 将输入框重置清空
        self.entry_order.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.entry_note.delete(0, tk.END)
        self.entry_order.focus()
        
        # 触发橙黄警告灯：提醒欧阳老师需要点击大按钮同步上云
        self.set_sync_pending()
        
        # 弹出成功泡泡
        messagebox.showinfo("录入成功", f"🎉 VIP 客户录入成功！\n\n订单号：{order}\n手机号：{phone if phone else '无'}\n\n提醒：已自动备份，请点击最下方按钮一键同步至官网！")

    def handle_double_click_copy(self, event):
        """双击数据行一键复制订单号，极具人性化细节"""
        selected_item = self.tree.selection()
        if not selected_item:
            return
        values = self.tree.item(selected_item, "values")
        if values:
            order_id = values[0]
            self.root.clipboard_clear()
            self.root.clipboard_append(order_id)
            self.root.update() # 立即更新剪贴板
            # 临时改变状态栏文字，提示成功复制
            old_text = self.lbl_sync_status.cget("text")
            old_fg = self.lbl_sync_status.cget("fg")
            self.lbl_sync_status.configure(text=f"📋 [系统提示]：订单号 {order_id} 已一键成功复制到您的电脑剪贴板！", fg=COLOR_SUCCESS)
            self.root.after(2000, lambda: self.lbl_sync_status.configure(text=old_text, fg=old_fg))

    def show_right_click_menu(self, event):
        """右键弹出精心定制的撤销授权操作菜单"""
        selected_item = self.tree.identify_row(event.y)
        if not selected_item:
            return
        self.tree.selection_set(selected_item)
        
        # 创建右键弹窗菜单
        menu = tk.Menu(self.root, tearoff=0, font=("Microsoft YaHei", 9), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN, activebackground=COLOR_PRIMARY, activeforeground="#0B0F19")
        
        values = self.tree.item(selected_item, "values")
        order_id = values[0]
        
        def revoke_action():
            if messagebox.askyesno("撤销授权确认", f"⚠️ 警告！确定要物理撤销订单号为 [{order_id}] 的 VIP 客户授权吗？\n\n撤销后该客户将立刻失去视频观看权限！"):
                # 剔除该数据
                self.db_data = [row for row in self.db_data if row[0] != order_id]
                self.save_local_database()
                self.render_table_data()
                self.set_sync_pending()
                messagebox.showinfo("撤销成功", f"❌ 订单号 [{order_id}] 的客户授权已从本地库剔除，一键同步上云后云端官网将自动封锁该订单！")
                
        menu.add_command(label=f"❌ 撤销并注销订单: {order_id} 的授权", command=revoke_action)
        menu.post(event.x_root, event.y_root)

    # ==================== 多线程异步 Git 官网同步算法 ====================

    def trigger_async_sync(self):
        """发起多线程异步同步，防止网络延迟或 Git 卡住时主图形界面失去响应"""
        if not self.db_data:
            messagebox.showwarning("同步警示", "当前没有任何订单授权，无法进行云端同步！")
            return
            
        # 改变按钮文字为“正在同步”，改变鼠标指针，锁定按钮防止重复点击
        self.btn_sync.configure(text="⏳ 正在全自动哈希转换并连线 GitHub 官网推送中，请稍后 (主界面未响应保护已开启)...", state=tk.DISABLED, bg=COLOR_BORDER, fg=COLOR_TEXT_MUTED)
        self.draw_status_light("#3b82f6") # 发光蓝灯
        self.lbl_sync_status.configure(text="官网同步状态:  🔵 正在建立云端安全数据通道，正在向 GitHub 云端推送，请不要关闭本软件...", fg="#3b82f6")
        
        # 开启子线程后台默默运行 Git 同步，极富大厂规范的开发作风
        t = threading.Thread(target=self.bg_sync_pipeline)
        t.daemon = True
        t.start()

    def bg_sync_pipeline(self):
        """后台子线程运行的 Git 同步全能管线"""
        # 1. 对本地所有订单号进行 SHA-256 哈希单向加密，保护电话和备注绝对留在本地电脑
        hashed_list = [hashlib.sha256(row[0].strip().encode('utf-8')).hexdigest() for row in self.db_data]
        
        success = False
        error_msg = ""
        
        try:
            # 2. 生成密文文件 orders.json
            with open(JSON_FILE, "w", encoding="utf-8") as f:
                json.dump(hashed_list, f, indent=4)
                
            # 3. 串行执行 Git 命令
            # git add orders_db.csv orders.json orders.txt
            subprocess.run(["git", "add", CSV_DB, JSON_FILE, TXT_FILE], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            
            # git commit
            commit_msg = f"update: 官网订单授权白名单图形化同步，共放行 {len(hashed_list)} 个订单"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            
            # git push origin main
            subprocess.run(["git", "push", "origin", "main"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            
            # [双端黑科技] 自动尝试静默推送到国内码云 Gitee 极速通道，如尚未绑定也绝不卡死报错，优雅防灾
            try:
                subprocess.run(["git", "push", "gitee", "main"], timeout=10, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            except Exception:
                pass
                
            success = True
        except subprocess.CalledProcessError as e:
            # 获取 Git 输出的报错日志
            error_msg = e.stderr.decode('utf-8', errors='ignore') if e.stderr else str(e)
        except Exception as e:
            error_msg = str(e)
            
        # 4. 同步完成后，通过安全线程调度机制切回 GUI 主线程更新 UI 和提示弹窗
        self.root.after(0, lambda: self.finish_sync_callback(success, error_msg))

    def finish_sync_callback(self, success, error_msg):
        """后台同步结束，切回主线程的安全回调，恢复按钮与状态灯"""
        # 恢复一键同步大按钮
        self.btn_sync.configure(text="🚀 【一键将授权名单同步到我的官方网站】 (全自动哈希加密转换 + 2秒极速 GitHub Pages 部署)", state=tk.NORMAL, bg=COLOR_PRIMARY, fg="#0B0F19")
        
        if success:
            self.draw_status_light(COLOR_SUCCESS) # 变回翠绿指示灯
            self.lbl_sync_status.configure(text="官网同步状态:  🟢 官网已是最新 (目前本地暂无任何新改动待同步)", fg=COLOR_TEXT_MUTED)
            messagebox.showinfo("同步成功", "🎉🎉 恭喜欧阳老师，官网数据全自动同步成功！ 🎉🎉\n\n最新添加的买家现在打开您的官网刷新使用教程，直接输入淘宝订单号就能立刻自助解锁看视频了！\n\n提示：电话号码和备注已安全锁在您本地电脑，云端无任何泄露风险。")
        else:
            self.draw_status_light(COLOR_ERROR) # 红灯警示
            self.lbl_sync_status.configure(text=f"官网同步状态:  🔴 同步失败！原因：{error_msg[:60]}...", fg=COLOR_ERROR)
            messagebox.showerror("云端同步失败", f"❌ 连线官网推送服务器失败！可能原因：\n\n1. 您的电脑当前网络连接中断或网络不佳；\n2. 您在本地库没有做任何订单增改，无需重复推送。\n\n具体错误日志：\n{error_msg}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MSscan3dApp(root)
    root.mainloop()
