# Git历史记录清理指南

## 紧急：私钥已泄露到代码中

**重要！请立即执行以下步骤清理Git历史记录中的私钥！**

## 受影响的文件清单

以下文件需要立即清理（仅存在于本地，未提交到Git）：
- query_realtime_balance.py
- query_balance_simple.py
- query_balance_final.py
- query_balance_dll.py
- login_success.py
- login_lighter_official.py
- login_and_query.py
- get_balance_direct.py
- check_my_balance.py
- check_lighter_balance.py
- check_balance_now.py
- crack_the_code.py
- my_trade.py
- my_secrets.py
- derive_key_test.py
- force_register_v2.py
- setup_api_key.py
- config.py
- real_trade.py

## 未来安全实践

### 1. 使用环境变量
```python
import os
from dotenv import load_dotenv

load_dotenv()

PRIVATE_KEY = os.getenv('ETH_PRIVATE_KEY')
```

### 2. 使用配置模板
```python
# .env.template (安全提交到Git)
ETH_PRIVATE_KEY=your_ethereum_private_key_here
LIGHTER_API_PRIVATE_KEY=your_lighter_api_private_key_here

# .env (不提交到Git)
ETH_PRIVATE_KEY=0x123...
LIGHTER_API_PRIVATE_KEY=0x456...
```

### 3. 验证.gitignore
```bash
# 检查.gitignore是否正确
git status --ignored
```

### 4. 定期检查
```bash
# 定期检查Git历史
git log --all -p --grep="private_key\\|API_KEY\\|SECRET"

# 定期检查当前文件
grep -r "PRIVATE_KEY.*=" --include="*.py" .
```

## 总结

1. 立即转移资产
2. 清理Git历史记录
3. 创建新的GitHub私有仓库
4. 更新.gitignore
5. 使用环境变量存储私钥
6. 定期检查安全状态

**请立即执行这些步骤保护您的资产！**
