import os
import sys
import json
import hashlib
import base58
import ecdsa
import requests
import qrcode_terminal
from typing import Optional

def save_to_file(wallet_name: str, file_name: str, contents: str) -> bool:
    """安全地保存文件内容"""
    try:
        with open(wallet_name + file_name, 'w', encoding='utf-8') as fh:
            fh.write(contents)
        return True
    except Exception as e:
        print(f"保存文件失败: {e}")
        return False

def read_from_file(file_path: str) -> Optional[str]:
    """安全地读取文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"文件不存在: {file_path}")
        return None
    except Exception as e:
        print(f"读取文件失败: {e}")
        return None

def account(wallet_name: str) -> None:
    """查看钱包账户信息"""
    address_file = wallet_name + '_address.txt'
    btcaddress = read_from_file(address_file)
    
    if not btcaddress:
        print("无法读取钱包地址文件")
        infi(wallet_name)
        return
    
    print(f"您的地址是: {btcaddress}")
    
    try:
        print("正在获取账户信息...")
        response = requests.get(f"https://blockchain.info/rawaddr/{btcaddress}", timeout=10)
        response.raise_for_status()
        
        # 格式化显示JSON数据
        try:
            data = response.json()
            print(f"余额: {data.get('final_balance', 0) / 100000000} BTC")
            print(f"交易总数: {data.get('n_tx', 0)}")
            print(f"已接收总额: {data.get('total_received', 0) / 100000000} BTC")
            print(f"已发送总额: {data.get('total_sent', 0) / 100000000} BTC")
        except json.JSONDecodeError:
            print("API返回数据格式错误")
            
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {e}")
    except Exception as e:
        print(f"获取账户信息时发生错误: {e}")
    
    infi(wallet_name)

def qr(wallet_name: str) -> None:
    """显示钱包地址的二维码"""
    address_file = wallet_name + '_address.txt'
    btcaddress = read_from_file(address_file)
    
    if not btcaddress:
        print("无法读取钱包地址文件")
        infi(wallet_name)
        return
    
    try:
        print(f"钱包地址: {btcaddress}")
        print("二维码:")
        qrcode_terminal.draw(btcaddress)
    except Exception as e:
        print(f"生成二维码失败: {e}")
    
    infi(wallet_name)
def generate_bitcoin_address(public_key_hex: str) -> str:
    """从公钥生成比特币地址"""
    try:
        # 添加压缩公钥前缀
        if len(public_key_hex) == 128:  # 未压缩公钥
            public_key_hex = '04' + public_key_hex
        
        # SHA256哈希
        public_key_bytes = bytes.fromhex(public_key_hex)
        sha256_hash = hashlib.sha256(public_key_bytes).digest()
        
        # RIPEMD160哈希
        ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
        
        # 添加版本字节(0x00 for mainnet)
        versioned_payload = b'\x00' + ripemd160_hash
        
        # 双SHA256校验和
        checksum = hashlib.sha256(hashlib.sha256(versioned_payload).digest()).digest()[:4]
        
        # 完整地址
        full_payload = versioned_payload + checksum
        
        # Base58编码
        address = base58.b58encode(full_payload).decode('utf-8')
        return address
    except Exception as e:
        print(f"生成地址失败: {e}")
        return ""

def newwallet(wallet_name: str) -> None:
    """创建新钱包"""
    print('未找到钱包密钥文件，正在创建新钱包...')
    
    try:
        # 生成私钥
        private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        private_key_hex = private_key.to_string().hex()
        
        # 生成公钥
        public_key = private_key.get_verifying_key()
        public_key_hex = public_key.to_string().hex()
        
        # 生成比特币地址
        btc_address = generate_bitcoin_address(public_key_hex)
        
        if not btc_address:
            print("地址生成失败")
            infi(wallet_name)
            return
        
        # 保存钱包文件
        if not save_to_file(wallet_name, '_private_key.txt', private_key_hex):
            print("保存私钥失败")
            return
            
        if not save_to_file(wallet_name, '_public_key.txt', public_key_hex):
            print("保存公钥失败")
            return
            
        if not save_to_file(wallet_name, '_address.txt', btc_address):
            print("保存地址失败")
            return
        
        print(f"钱包创建成功!")
        print(f"私钥: {private_key_hex}")
        print(f"公钥: {public_key_hex}")
        print(f"地址: {btc_address}")
        print("\n⚠️  警告: 请妥善保管您的私钥，丢失后无法恢复!")
        
    except Exception as e:
        print(f"创建钱包时发生错误: {e}")
    
    infi(wallet_name)
def gethistory(wallet_name: str) -> None:
    """获取钱包交易历史"""
    address_file = wallet_name + '_address.txt'
    btcaddress = read_from_file(address_file)
    
    if not btcaddress:
        print("无法读取钱包地址文件")
        infi(wallet_name)
        return
    
    try:
        print("正在获取交易历史...")
        # 使用更详细的API获取交易信息
        response = requests.get(f"https://blockchain.info/rawaddr/{btcaddress}?limit=10", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        transactions = data.get('txs', [])
        
        if not transactions:
            print("暂无交易记录")
        else:
            print(f"\n最近 {len(transactions)} 笔交易:")
            print("-" * 80)
            
            for i, tx in enumerate(transactions, 1):
                tx_hash = tx.get('hash', 'N/A')
                time_stamp = tx.get('time', 0)
                
                # 计算交易金额
                inputs_value = sum(inp.get('prev_out', {}).get('value', 0) for inp in tx.get('inputs', []))
                outputs_value = sum(out.get('value', 0) for out in tx.get('out', []))
                
                print(f"{i}. 交易哈希: {tx_hash[:16]}...")
                print(f"   时间戳: {time_stamp}")
                print(f"   输入总额: {inputs_value / 100000000:.8f} BTC")
                print(f"   输出总额: {outputs_value / 100000000:.8f} BTC")
                print()
                
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {e}")
    except json.JSONDecodeError:
        print("API返回数据格式错误")
    except Exception as e:
        print(f"获取交易历史时发生错误: {e}")
    
    infi(wallet_name)
def infi(wallet_name: str) -> None:
    """主菜单界面"""
    if os.path.exists(wallet_name + '_address.txt'):
        print("\n" + "="*50)
        print(f"🔐 比特币钱包管理系统")
        print(f"📁 当前钱包: {wallet_name}")
        print("⚠️  注意: 这是主网，不是测试网!")
        print("="*50)
        
        menu_options = {
            '1': '📊 查看钱包信息',
            '2': '🆕 创建新钱包', 
            '3': '📱 显示地址二维码',
            '4': '📜 查看交易历史',
            '5': '🔄 切换钱包',
            '0': '❌ 退出程序'
        }
        
        for key, value in menu_options.items():
            print(f"{key}. {value}")
        
        choice = input("\n请选择操作 (0-5): ").strip()
        
        if choice == '1':
            account(wallet_name)
        elif choice == '2':
            new_wallet_name = input("请输入新钱包名称: ").strip()
            if new_wallet_name:
                newwallet(new_wallet_name)
            else:
                print("钱包名称不能为空")
                infi(wallet_name)
        elif choice == '3':
            qr(wallet_name)
        elif choice == '4':
            gethistory(wallet_name)
        elif choice == '5':
            start()
        elif choice == '0':
            print("感谢使用，再见!")
            sys.exit(0)
        else:
            print("无效选择，请重新输入")
            infi(wallet_name)
    else:
        print(f"\n钱包 '{wallet_name}' 不存在")
        choice = input(f"是否创建名为 '{wallet_name}' 的新钱包? (y/n): ").strip().lower()
        if choice == 'y' or choice == 'yes':
            newwallet(wallet_name)
        elif choice == 'n' or choice == 'no':
            start()
        else:
            print("请输入 y 或 n")
            infi(wallet_name)
def start() -> None:
    """程序启动函数"""
    print("\n" + "="*60)
    print("🚀 欢迎使用 JokeWallet - 比特币钱包管理工具")
    print("📝 版本: 0.0.5 (优化版)")
    print("⚠️  警告: 请确保在安全环境中使用此工具")
    print("🔒 您的私钥将保存在本地文件中，请妥善保管")
    print("="*60)
    
    while True:
        wallet_name = input("\n请输入钱包名称: ").strip()
        if wallet_name:
            # 验证钱包名称格式
            if wallet_name.replace('_', '').replace('-', '').isalnum():
                infi(wallet_name)
                break
            else:
                print("钱包名称只能包含字母、数字、下划线和连字符")
        else:
            print("钱包名称不能为空")

def main() -> None:
    """主函数"""
    try:
        start()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n程序发生未预期错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()