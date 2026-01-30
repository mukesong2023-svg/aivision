import os
from dotenv import load_dotenv
import ctypes
import requests
from eth_account import Account

load_dotenv()

PRIVATE_KEY = os.getenv('ETH_PRIVATE_KEY')
MAINNET_URL = os.getenv('MAINNET_URL', 'https://mainnet.zklighter.elliot.ai')
CHAIN_ID = int(os.getenv('CHAIN_ID', '42161'))
DLL_PATH = os.path.join(os.getcwd(), "build", "Release", "lighter_signer.dll")

if not PRIVATE_KEY:
    raise ValueError("❌ 错误：未设置ETH_PRIVATE_KEY环境变量！\n请在.env文件中设置：ETH_PRIVATE_KEY=your_private_key")

class ApiKeyResponse(ctypes.Structure):
    _fields_ = [("private_key", ctypes.c_char_p),
                ("public_key", ctypes.c_char_p),
                ("err", ctypes.c_char_p)]

class StrOrErr(ctypes.Structure):
    _fields_ = [("str", ctypes.c_char_p),
                ("err", ctypes.c_char_p)]

class SecureLighterClient:
    def __init__(self):
        self.private_key = PRIVATE_KEY
        self.api_key_private = None
        self.api_key_public = None
        self.account_index = -1
        self.api_key_index = 0
        self.lib = None
        
    def init_signer(self):
        print("[Step 1] 初始化 Signer DLL...")
        
        if not os.path.exists(DLL_PATH):
            print(f"  ❌ 未找到 DLL: {DLL_PATH}")
            return False
        
        self.lib = ctypes.CDLL(DLL_PATH)
        self.lib.GenerateAPIKey.restype = ApiKeyResponse
        self.lib.CreateClient.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_longlong]
        self.lib.CreateClient.restype = StrOrErr
        
        print("  ✅ Signer DLL 初始化成功")
        return True
    
    def generate_api_key(self):
        print("[Step 2] 生成 Lighter API Key...")
        
        resp = self.lib.GenerateAPIKey()
        
        if resp.err:
            err_msg = resp.err.decode('utf-8') if resp.err else "Unknown error"
            print(f"  ❌ 生成 API Key 失败: {err_msg}")
            return False
        
        self.api_key_private = resp.private_key
        self.api_key_public = resp.public_key.decode('utf-8')
        
        print(f"  ✅ Session Key 生成成功")
        return True
    
    def get_account_index(self, eth_address):
        print("[Step 3] 获取账户索引...")
        
        url = f"{MAINNET_URL}/api/v1/accountsByL1Address"
        params = {"l1_address": eth_address}
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        try:
            r = requests.get(url, params=params, headers=headers, timeout=30)
            
            if r.status_code == 200:
                data = r.json()
                
                if "sub_accounts" in data and len(data["sub_accounts"]) > 0:
                    self.account_index = data["sub_accounts"][0]["index"]
                    print(f"  ✅ 找到账户索引: {self.account_index}")
                    return True
                else:
                    print(f"  ❌ 账户未在 Lighter 上注册")
                    return False
            else:
                print(f"  ❌ 请求失败: {r.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ 网络请求异常: {e}")
            return False
    
    def create_client_context(self):
        print("[Step 4] 创建客户端上下文...")
        
        if self.account_index == -1:
            print("  ❌ 无效的账户索引")
            return False
        
        res = self.lib.CreateClient(
            MAINNET_URL.encode('utf-8'),
            self.api_key_private,
            CHAIN_ID,
            self.api_key_index,
            self.account_index
        )
        
        if res.err:
            err_msg = res.err.decode('utf-8') if res.err else "Unknown error"
            print(f"  ❌ 创建客户端失败: {err_msg}")
            return False
        
        print("  ✅ 客户端上下文创建成功")
        return True
    
    def login(self):
        print("=" * 60)
        print("Lighter 登录流程（安全版本）")
        print("=" * 60)
        print()
        
        account = Account.from_key(self.private_key)
        eth_address = account.address
        
        print(f"🔐 钱包地址: {eth_address}")
        print(f"🔒 私钥来源: 环境变量（已安全）")
        print()
        
        if not self.init_signer():
            return False
        
        if not self.generate_api_key():
            return False
        
        if not self.get_account_index(eth_address):
            return False
        
        if not self.create_client_context():
            return False
        
        print()
        print("=" * 60)
        print("✅ 登录成功!")
        print("=" * 60)
        print()
        print(f"📋 账户信息:")
        print(f"  钱包地址: {eth_address}")
        print(f"  Session Key: {self.api_key_public}")
        print(f"  Account Index: {self.account_index}")
        print(f"  Chain ID: {CHAIN_ID}")
        print(f"  网络: Arbitrum One")
        print()
        print("💡 安全提示:")
        print("  ✅ 私钥已从环境变量读取")
        print("  ✅ .env 文件已在 .gitignore 中")
        print("  ✅ 不会提交到版本控制系统")
        print()
        print("=" * 60)
        
        return True

if __name__ == "__main__":
    try:
        client = SecureLighterClient()
        success = client.login()
        
        if success:
            print("\n✅ 安全登录成功！")
            print("💡 提示: 访问官网查看详细余额")
            print("🔗 https://mainnet.zklighter.elliot.ai")
        else:
            print("\n❌ 登录失败，请检查配置")
            print("\n📋 请确保：")
            print("  1. 已创建 .env 文件")
            print("  2. 在 .env 中设置了 ETH_PRIVATE_KEY")
            print("  3. .env 文件在 .gitignore 中")
            print("\n📝 示例 .env 文件:")
            print("  ETH_PRIVATE_KEY=0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")
    except ValueError as e:
        print(f"\n{e}")
        print("\n📝 请按以下步骤操作：")
        print("  1. 复制 .env.template 为 .env")
        print("  2. 在 .env 中填入真实私钥")
        print("  3. 运行此脚本")
        print("\n📋 命令示例:")
        print("  cp .env.template .env")
        print("  # 然后编辑 .env 文件")
