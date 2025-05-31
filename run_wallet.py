#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JokeWallet 启动脚本
简化的启动方式，自动处理路径和依赖检查
"""

import os
import sys

def check_dependencies():
    """检查必要的依赖项"""
    required_modules = ['ecdsa', 'requests', 'qrcode_terminal', 'base58']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print("❌ 缺少以下依赖项:")
        for module in missing_modules:
            print(f"   - {module}")
        print("\n请运行以下命令安装依赖:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def main():
    """主启动函数"""
    print("🚀 正在启动 JokeWallet...")
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 添加jokewallet模块到路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    jokewallet_dir = os.path.join(current_dir, 'jokewallet')
    
    if not os.path.exists(jokewallet_dir):
        print("❌ 找不到jokewallet目录")
        sys.exit(1)
    
    sys.path.insert(0, jokewallet_dir)
    
    try:
        # 导入并运行主程序
        from jokewallet import main as wallet_main
        wallet_main()
    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 程序被用户中断，再见!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()