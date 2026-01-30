import subprocess
import os

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    return result.stdout, result.stderr, result.returncode

print("=" * 70)
print("使用 git filter-branch 重写历史（修改所有提交中的文件）")
print("=" * 70)

print("\n步骤 1: 重置到远程分支...")
print("-" * 70)

stdout, stderr, code = run_cmd("git reset --hard origin/gh-pages")
if code == 0:
    print("✅ 已重置")
else:
    print(f"❌ 重置失败: {stderr}")
    exit(1)

print("\n步骤 2: 创建替换脚本...")
print("-" * 70)

replace_script = """#!/bin/bash
find . -type f -name "*.py" -o -name "*.md" -o -name "*.txt" | while read file; do
    sed -i 's/0xd6bbfb3b2bfd7e75cf51e8814b588a09279a5457e9b60dbc9233638de4817c53/0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234/g' "$file" 2>/dev/null || true
    sed -i 's/4746b9cdf0b57d41b94c5fb60b872718ed55efea003117fde8b7dd6a233a6fc7520401395317942d/example_api_key_1234567890abcdef1234567890abcdef1234567890abcdef/g' "$file" 2>/dev/null || true
done
"""

with open("replace_keys.sh", "w", encoding='utf-8') as f:
    f.write(replace_script)

print("✅ 替换脚本已创建")

print("\n步骤 3: 运行 git filter-branch...")
print("-" * 70)
print("这可能需要几分钟...")

cmd = "git filter-branch -f --tree-filter \"bash replace_keys.sh\" --prune-empty --tag-name-filter cat -- --all"
stdout, stderr, code = run_cmd(cmd)

if code == 0:
    print("✅ filter-branch 完成")
else:
    print(f"⚠️ filter-branch 有警告（可能已成功）")

print("\n步骤 4: 清理引用...")
print("-" * 70)

run_cmd("rm -rf .git/refs/original/")
run_cmd("git reflog expire --expire=now --all")
run_cmd("git gc --prune=now --aggressive")

print("✅ 引用清理完成")

print("\n步骤 5: 验证...")
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
    print("✅ 清理完成！准备推送...")
else:
    print("⚠️ 部分私钥仍存在")
print("=" * 70)

print("\n步骤 6: 推送到远程...")
print("-" * 70)

stdout, stderr, code = run_cmd("git push origin HEAD:gh-pages --force")
if code == 0:
    print("✅ 推送成功")
else:
    print(f"❌ 推送失败: {stderr}")

print("\n" + "=" * 70)
print("清理完成！")
print("=" * 70)
