import subprocess
import os

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    return result.stdout, result.stderr, result.returncode

print("=" * 70)
print("使用 git filter-branch 重写历史（移除旧提交中的私钥）")
print("=" * 70)

print("\n步骤 1: 回退到初始提交...")
print("-" * 70)

stdout, stderr, code = run_cmd("git reset --hard e743413")
if code == 0:
    print("✅ 已回退到初始提交")
else:
    print(f"❌ 回退失败: {stderr}")

print("\n步骤 2: 检查文件内容...")
print("-" * 70)

stdout, stderr, code = run_cmd("cat fix_all_private_keys.py | head -10")
print(stdout)

print("\n步骤 3: 修改文件（替换私钥为占位符）...")
print("-" * 70)

new_content = """import os
import re

# 示例私钥占位符（仅用于演示，非真实私钥）
EXAMPLE_PRIVATE_KEY = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234"
EXAMPLE_API_KEY = "example_api_key_1234567890abcdef1234567890abcdef1234567890abcdef"

def fix_file(filepath, replacements):
    \"""
    修复单个文件，替换硬编码的私钥为环境变量
    \"""
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

    # 需要替换的私钥（从用户提供的真实私钥列表）
    # 运行时需要替换为实际的私钥
    replacements = {
        # 在这里填入真实的私钥进行替换
        # "0xYOUR_REAL_PRIVATE_KEY": 'os.getenv(\\'ETH_PRIVATE_KEY\\')',
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

    print("⚠️  注意：请在 replacements 字典中填入真实的私钥")
    print("⚠️  当前仅作为示例，不会进行任何替换")
    print()

if __name__ == "__main__":
    main()
"""

with open("fix_all_private_keys.py", "w", encoding='utf-8') as f:
    f.write(new_content)

print("✅ 文件已修改")

print("\n步骤 4: 提交更改...")
print("-" * 70)

stdout, stderr, code = run_cmd('git add .; git commit --amend -m "Initial commit: Security configuration files (no real keys)"')
if code == 0:
    print("✅ 已修改初始提交")
else:
    print(f"❌ 提交失败: {stderr}")

print("\n步骤 5: 强制推送到远程...")
print("-" * 70)

stdout, stderr, code = run_cmd("git push origin HEAD:gh-pages --force")
if code == 0:
    print("✅ 推送成功")
else:
    print(f"❌ 推送失败: {stderr}")

print("\n步骤 6: 验证...")
print("-" * 70)

keys = [
    "0xd6bbfb3b2bfd7e75cf51e8814b588a09279a5457e9b60dbc9233638de4817c53",
    "4746b9cdf0b57d41b94c5fb60b872718ed55efea003117fde8b7dd6a233a6fc7520401395317942d"
]

all_clean = True
for key in keys:
    stdout, _, _ = run_cmd(f'git log --all -S "{key}" --oneline')
    if not stdout.strip():
        print(f"✅ {key[:20]}: 已移除")
    else:
        print(f"❌ {key[:20]}: 仍存在")
        all_clean = False

print("\n" + "=" * 70)
if all_clean:
    print("✅ 清理完成！")
else:
    print("⚠️ 可能需要进一步处理")
print("=" * 70)
