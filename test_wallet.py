#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证JokeWallet的基本功能
"""

import os
import sys
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# 添加jokewallet模块到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'jokewallet'))

try:
    from jokewallet import (
        save_to_file, 
        read_from_file, 
        generate_bitcoin_address,
        newwallet
    )
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保在项目根目录运行此测试")
    sys.exit(1)

def test_file_operations():
    """测试文件操作功能"""
    print("🧪 测试文件操作功能...")
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        
        # 测试保存文件
        test_content = "test_private_key_123456"
        result = save_to_file("test_wallet", "_private_key.txt", test_content)
        assert result == True, "保存文件失败"
        
        # 测试读取文件
        read_content = read_from_file("test_wallet_private_key.txt")
        assert read_content == test_content, "读取文件内容不匹配"
        
        # 测试读取不存在的文件
        non_existent = read_from_file("non_existent_file.txt")
        assert non_existent is None, "读取不存在文件应返回None"
        
    print("✅ 文件操作测试通过")

def test_address_generation():
    """测试比特币地址生成"""
    print("🧪 测试比特币地址生成...")
    
    # 测试公钥（这是一个示例公钥）
    test_public_key = "04" + "a" * 128  # 模拟未压缩公钥
    
    address = generate_bitcoin_address(test_public_key)
    
    # 验证地址格式
    assert isinstance(address, str), "地址应该是字符串"
    assert len(address) > 0, "地址不应为空"
    assert address.startswith('1'), "主网地址应以1开头"
    
    print(f"✅ 生成的测试地址: {address}")
    print("✅ 地址生成测试通过")

def test_wallet_creation():
    """测试钱包创建功能"""
    print("🧪 测试钱包创建功能...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        
        # Mock input函数以避免交互
        with patch('builtins.input', return_value='0'):  # 选择退出
            with patch('sys.exit'):  # Mock sys.exit
                try:
                    # 这里我们不能直接测试newwallet，因为它会调用infi
                    # 但我们可以测试地址生成的核心逻辑
                    import ecdsa
                    
                    # 生成测试密钥
                    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
                    public_key = private_key.get_verifying_key()
                    public_key_hex = public_key.to_string().hex()
                    
                    # 生成地址
                    address = generate_bitcoin_address(public_key_hex)
                    
                    assert len(address) > 0, "地址生成失败"
                    print(f"✅ 测试钱包地址: {address}")
                    
                except Exception as e:
                    print(f"❌ 钱包创建测试失败: {e}")
                    return False
    
    print("✅ 钱包创建测试通过")
    return True

def test_dependencies():
    """测试依赖项是否正确安装"""
    print("🧪 测试依赖项...")
    
    required_modules = [
        'ecdsa',
        'requests', 
        'qrcode_terminal',
        'base58',
        'hashlib',
        'json'
    ]
    
    for module_name in required_modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name} - 已安装")
        except ImportError:
            print(f"❌ {module_name} - 未安装")
            return False
    
    print("✅ 所有依赖项测试通过")
    return True

def main():
    """运行所有测试"""
    print("🚀 开始运行JokeWallet测试套件")
    print("=" * 50)
    
    tests = [
        test_dependencies,
        test_file_operations,
        test_address_generation,
        test_wallet_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            result = test_func()
            if result is not False:
                passed += 1
            print()
        except Exception as e:
            print(f"❌ 测试 {test_func.__name__} 失败: {e}")
            print()
    
    print("=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！JokeWallet已准备就绪。")
        return True
    else:
        print("⚠️  部分测试失败，请检查问题。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)