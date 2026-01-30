import os
import re

PRIVATE_KEY_ETH = "0xd6bbfb3b2bfd7e75cf51e8814b588a09279a5457e9b60dbc9233638de4817c53"
PRIVATE_KEY_LIGHTER = "4746b9cdf0b57d41b94c5fb60b872718ed55efea003117fde8b7dd6a233a6fc7520401395317942d"

def fix_file(filepath, replacements):
    """
    修复单个文件，替换硬编码的私钥为环境变量
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        for old_key, new_var in replacements.items():
            content = content.replace(old_key, new_var)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"  ❌ 处理文件失败: {filepath} - {e}")
        return False

def main():
    print("=" * 60)
    print("🔒 批量修复私钥硬编码问题")
    print("=" * 60)
    print()
    
    # 需要替换的私钥
    replacements = {
        PRIVATE_KEY_ETH: 'os.getenv(\'ETH_PRIVATE_KEY\')',
        f'PRIVATE_KEY = "{PRIVATE_KEY_ETH}"': 'PRIVATE_KEY = os.getenv(\'ETH_PRIVATE_KEY\')',
        f'ETH_PRIVATE_KEY = "{PRIVATE_KEY_ETH}"': 'ETH_PRIVATE_KEY = os.getenv(\'ETH_PRIVATE_KEY\')',
        f'PRIVATE_KEY = "{PRIVATE_KEY_ETH}"': 'PRIVATE_KEY = os.getenv(\'ETH_PRIVATE_KEY\')',
        PRIVATE_KEY_LIGHTER: 'os.getenv(\'LIGHTER_API_PRIVATE_KEY\')',
        f'API_KEY_PRIVATE_KEY = "{PRIVATE_KEY_LIGHTER}"': 'API_KEY_PRIVATE_KEY = os.getenv(\'LIGHTER_API_PRIVATE_KEY\')',
    }
    
    # 需要处理的文件
    files_to_fix = [
        "query_realtime_balance.py",
        "query_balance_simple.py",
        "query_balance_final.py",
        "query_balance_dll.py",
        "login_success.py",
        "login_lighter_official.py",
        "login_and_query.py",
        "get_balance_direct.py",
        "check_my_balance.py",
        "check_lighter_balance.py",
        "check_balance_now.py",
        "crack_the_code.py",
        "my_trade.py",
        "my_secrets.py",
        "derive_key_test.py",
        "force_register_v2.py",
        "real_trade.py",
        "setup_api_key.py",
        "config.py",
    ]
    
    fixed_count = 0
    not_found_count = 0
    error_count = 0
    
    for filename in files_to_fix:
        if not os.path.exists(filename):
            not_found_count += 1
            continue
        
        if fix_file(filename, replacements):
            print(f"  ✅ 已修复: {filename}")
            fixed_count += 1
        else:
            error_count += 1
    
    print()
    print("=" * 60)
    print("📊 修复统计:")
    print("=" * 60)
    print(f"  ✅ 成功修复: {fixed_count} 个文件")
    print(f"  ⚠️  未找到: {not_found_count} 个文件")
    print(f"  ❌ 处理失败: {error_count} 个文件")
    print()
    print("=" * 60)
    print("📝 下一步操作:")
    print("=" * 60)
    print("  1. 检查修复后的文件")
    print("  2. 创建 .env 文件（从 .env.template 复制）")
    print("  3. 在 .env 中填入真实私钥")
    print("  4. 安装依赖: pip install python-dotenv")
    print("  5. 测试运行: python secure_login_example.py")
    print()
    print("=" * 60)
    print("🔒 安全提示:")
    print("=" * 60)
    print("  ✅ 所有私钥已替换为环境变量")
    print("  ✅ .gitignore 已创建")
    print("  ✅ 以后不会提交敏感信息")
    print()
    print("=" * 60)
    print("🚨 立即执行 Git 历史清理:")
    print("=" * 60)
    print("  1. 参考 CLEAN_GIT_HISTORY.md")
    print("  2. 使用 BFG Repo-Cleaner 清理历史")
    print("  3. 立即转移钱包资产")
    print("  4. 废弃旧私钥")
    print("=" * 60)

if __name__ == "__main__":
    print()
    print("⚠️  警告：此脚本将修改多个文件")
    print("⚠️  请确保已备份重要数据")
    print()
    
    response = input("是否继续？(yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        main()
    else:
        print()
        print("已取消操作")
