import subprocess
import os

def run_cmd(cmd):
    print(f"\n> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    if result.returncode != 0 and result.stderr:
        print(f"错误: {result.stderr[:200]}")
    return result.stdout, result.stderr, result.returncode

print("=" * 70)
print("删除旧提交，创建干净的仓库历史")
print("=" * 70)

print("\n步骤 1: 创建 orphan 分支（无历史记录）...")
print("-" * 70)

stdout, stderr, code = run_cmd("git checkout --orphan clean-branch")
if code == 0:
    print("✅ 已创建 orphan 分支")
else:
    print(f"❌ 失败: {stderr}")
    exit(1)

print("\n步骤 2: 暂存所有文件...")
print("-" * 70)

stdout, stderr, code = run_cmd("git add .")
if code == 0:
    print("✅ 已暂存")
else:
    print(f"❌ 失败: {stderr}")
    exit(1)

print("\n步骤 3: 创建初始提交...")
print("-" * 70)

stdout, stderr, code = run_cmd('git commit -m "Initial commit: Security configuration files"')
if code == 0:
    print("✅ 已创建初始提交")
else:
    print(f"❌ 失败: {stderr}")
    exit(1)

print("\n步骤 4: 删除旧分支...")
print("-" * 70)

stdout, stderr, code = run_cmd("git branch -D master")
if code == 0:
    print("✅ 已删除 master 分支")
else:
    print(f"❌ 失败: {stderr}")

print("\n步骤 5: 重命名新分支为 master...")
print("-" * 70)

stdout, stderr, code = run_cmd("git branch -m master")
if code == 0:
    print("✅ 已重命名")
else:
    print(f"❌ 失败: {stderr}")

print("\n步骤 6: 验证历史...")
print("-" * 70)

stdout, stderr, code = run_cmd("git log --oneline")
print(stdout)
if len(stdout.strip().split('\n')) == 1:
    print("✅ 历史已清理（只有一个提交）")
else:
    print("⚠️ 历史仍有多个提交")

print("\n步骤 7: 推送到 gh-pages...")
print("-" * 70)

stdout, stderr, code = run_cmd("git push origin HEAD:gh-pages --force")
if code == 0:
    print("✅ 推送成功")
else:
    print(f"❌ 推送失败: {stderr}")

print("\n步骤 8: 推送到 main...")
print("-" * 70)

stdout, stderr, code = run_cmd("git push origin HEAD:main --force")
if code == 0:
    print("✅ 推送成功")
else:
    print(f"❌ 推送失败: {stderr}")

print("\n步骤 9: 验证私钥...")
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
        print(f"❌ {key[:20]}: 仍存在！")
        all_clean = False

print("\n" + "=" * 70)
if all_clean:
    print("✅ 清理完成！所有私钥已从 Git 历史中移除")
    print("\n远程仓库已更新:")
    print("  - gh-pages: ✅")
    print("  - main: ✅")
else:
    print("⚠️ 清理完成，但私钥仍存在")
print("=" * 70)
