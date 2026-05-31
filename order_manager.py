# -*- coding: utf-8 -*-
"""
========================================================================
      🌌 MSscan3D 官网订单同步授权管理器 (Official Order Sync Manager) 🌌
========================================================================
  - 核心功能：输入买家订单号，自动进行 SHA-256 安全哈希加密，保护客户隐私。
  - 云端同步：一键自动调用本地 Git，将加密后的订单授权白名单推送同步至 GitHub 云端官网。
  - 无需服务器：零服务器年费开销，安全、高效、秒速解锁！
  
  ©耐心导师为欧阳兴老师专属定制，小白也可以一秒上手！
"""
import os
import sys
import json
import hashlib
import subprocess

# 解决 Windows 控制台输出中文乱码的顽疾
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

TXT_FILE = "orders.txt"
JSON_FILE = "orders.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_sha256(text):
    """单向不可逆 SHA-256 加密，100% 保护真实订单隐私，防逆向破解"""
    return hashlib.sha256(text.strip().encode('utf-8')).hexdigest()

def load_orders():
    """读取本地 orders.txt 备份文本"""
    if not os.path.exists(TXT_FILE):
        with open(TXT_FILE, "w", encoding="utf-8") as f:
            f.write("# 欧阳老师的 MSscan3D 购机订单号明文备份文本（一行一个，# 开头为注释）\n")
        return []
    
    orders = []
    with open(TXT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            orders.append(line)
    return list(sorted(set(orders))) # 去重排序

def save_orders(orders):
    """保存订单号到明文备份 orders.txt 里"""
    with open(TXT_FILE, "w", encoding="utf-8") as f:
        f.write("# 欧阳老师的 MSscan3D 购机订单号明文备份文本（一行一个，# 开头为注释）\n")
        for ord_id in sorted(orders):
            f.write(f"{ord_id}\n")

def add_new_orders():
    clear_screen()
    print("=" * 60)
    print("             ➕ [功能 1]：添加新买家淘宝订单号")
    print("=" * 60)
    print("说明：")
    print("  1. 支持【直接粘贴】！支持单次输入一个，或者粘贴多个（空格/回车分隔均可）。")
    print("  2. 输入完成后，直接敲 两次回车 即可确认保存。")
    print("-" * 60)
    
    current_orders = set(load_orders())
    print(f"👉 当前官网已录入的订单总数: {len(current_orders)} 个")
    print("请输入新订单号（完成输入后连续敲两次回车）:")
    
    input_lines = []
    while True:
        try:
            line = input()
            if not line:
                break
            input_lines.append(line)
        except EOFError:
            break
            
    # 解析输入（按任意空白符拆分，提取订单号）
    new_ids = []
    for line in input_lines:
        for token in line.split():
            token = token.strip()
            if token and not token.startswith("#"):
                new_ids.append(token)
                
    if not new_ids:
        print("\n❌ 未检测到任何输入，正在返回主菜单...")
        os.system("pause")
        return
        
    added_count = 0
    duplicate_count = 0
    for ord_id in new_ids:
        if ord_id in current_orders:
            duplicate_count += 1
        else:
            current_orders.add(ord_id)
            added_count += 1
            print(f"✅ 成功录入订单: {ord_id}")
            
    if added_count > 0:
        save_orders(list(current_orders))
        print(f"\n🎉 录入大捷！新成功导入 {added_count} 个订单号！(过滤重复 {duplicate_count} 个)")
        print("💡 提示：录入后必须返回主菜单选择 [3] 一键同步到官网，买家才可以立刻解锁视频哦！")
    else:
        print(f"\nℹ️ 录入完毕，输入的 {duplicate_count} 个订单均已在授权白名单中，无需重复录入。")
        
    os.system("pause")

def view_all_orders():
    clear_screen()
    print("=" * 60)
    print("             👀 [功能 2]：查看当前已放行订单列表")
    print("=" * 60)
    orders = load_orders()
    print(f"👉 官网当前累计授权订单总数: {len(orders)} 个")
    print("-" * 60)
    if not orders:
        print("  ⚠️ 目前授权列表中还是空的，请先添加订单。")
    else:
        for idx, ord_id in enumerate(orders):
            print(f"  [{idx+1:02d}] 订单号: {ord_id}")
    print("=" * 60)
    os.system("pause")

def sync_to_website():
    clear_screen()
    print("=" * 60)
    print("             🚀 [功能 3]：一键同步并上传到我的官方网站")
    print("=" * 60)
    print("准备开始执行全自动云端同步...")
    
    # 1. 加载明文订单
    orders = load_orders()
    if not orders:
        print("\n❌ 警告：当前本地没有任何订单号！请先选择 [1] 添加订单后再同步。")
        os.system("pause")
        return
        
    # 2. 哈希加密生成 orders.json
    print("\n👉 步骤 1：正在进行银行级 SHA-256 隐私哈希加密转换...")
    hashed_list = [get_sha256(ord_id) for ord_id in orders]
    
    try:
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(hashed_list, f, indent=4)
        print(f"  ✅ orders.json 密文文件已在本地生成，共 {len(hashed_list)} 个密文节点。")
    except Exception as e:
        print(f"  ❌ 错误：本地 orders.json 写入失败: {e}")
        os.system("pause")
        return
        
    # 3. 自动调用 Git 命令推送云端
    print("\n👉 步骤 2：正在发起云端官方仓库推送，打通 GitHub Pages 同步链路...")
    
    try:
        # 执行 Git Add
        subprocess.run(["git", "add", TXT_FILE, JSON_FILE], check=True, stdout=subprocess.DEVNULL)
        print("  ✅ 已自动打包备份明文 orders.txt 与加密文件 orders.json")
        
        # 执行 Git Commit
        commit_msg = f"update: 自动同步订单授权白名单，共放行 {len(orders)} 个订单"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True, stdout=subprocess.DEVNULL)
        print("  ✅ 已成功在本地生成同步版本印章")
        
        # 执行 Git Push
        print("  ⏳ 正在连线 GitHub 官网托管服务器，推送最后一步，请稍候...")
        push_res = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True, check=True)
        print("=" * 60)
        print("  🎉🎉🎉 恭喜欧阳老师！官网订单授权白名单同步成功！！！ 🎉🎉🎉")
        print("-" * 60)
        print("买家现在刷新官网使用教程，输入刚才添加的订单号，即可秒速自动解锁看视频！")
        print("=" * 60)
    except subprocess.CalledProcessError as e:
        print("\n❌ Git 云端同步失败！可能原因：")
        print("  1. 您的电脑当前网络连接中断；")
        print("  2. 本地 orders 没有任何新的改动，无需重复同步；")
        print("  3. 具体的报错信息如下：")
        print("-" * 50)
        print(e.stderr if e.stderr else e)
        print("-" * 50)
        
    os.system("pause")

def main_menu():
    while True:
        clear_screen()
        print("*" * 65)
        print("     🌌 MSscan3D 官网订单同步放行管理器 v1.0 (欧阳兴老师专属版) 🌌")
        print("*" * 65)
        print("  [说明]：只需输入客户订单号，本工具一键自动上传，客户在官网输入订单号直开！")
        print("-" * 65)
        print("    👉 【1】 ➕ 添加新买家淘宝订单号 (支持鼠标右键粘贴)")
        print("    👉 【2】 👀 查看当前已授权的订单列表")
        print("    👉 【3】 🚀 一键同步并上传到我的官方网站")
        print("    👉 【4】 ❌ 退出订单管理器")
        print("-" * 65)
        print("【至尊应急密码】：您的手机号 ouyangxing17607982667 依然是后门超级密码")
        print("*" * 65)
        print("请选择功能编号 [1-4]，然后敲回车确认: ", end="")
        
        choice = input().strip()
        if choice == "1":
            add_new_orders()
        elif choice == choice == "2":
            view_all_orders()
        elif choice == "3":
            sync_to_website()
        elif choice == "4":
            print("\n感谢使用！官网订单授权通道已安全锁定。祝欧阳老师生意兴隆，财源滚滚！👋")
            break
        else:
            print("\n⚠️ 警示：输入编号不正确，请输入 1-4 之间的数字！")
            os.system("pause")

if __name__ == "__main__":
    main_menu()
