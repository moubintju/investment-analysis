# 部署到 Vercel 指南

本项目已配置为可直接部署到 Vercel。

## 📋 前置要求

1. GitHub 账号
2. Vercel 账号（可使用 GitHub 登录）
3. Git 已安装

## 🚀 部署步骤

### 方法一：通过 GitHub（推荐）

#### 1. 创建 GitHub 仓库

```bash
# 进入项目目录
cd "c:\Users\moubin\Desktop\investment evaluation"

# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 创建初始提交
git commit -m "Initial commit: Investment Analysis System"

# 在 GitHub 上创建新仓库，然后关联远程仓库
git remote add origin https://github.com/你的用户名/investment-analysis.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

#### 2. 在 Vercel 上部署

1. 访问 [Vercel](https://vercel.com)
2. 使用 GitHub 账号登录
3. 点击 "New Project"
4. 从 GitHub 导入你刚创建的仓库
5. Vercel 会自动检测配置并开始部署
6. 等待部署完成（通常 1-2 分钟）
7. 获得你的应用 URL（格式：`https://your-project.vercel.app`）

### 方法二：使用 Vercel CLI

```bash
# 安装 Vercel CLI
npm install -g vercel

# 进入项目目录
cd "c:\Users\moubin\Desktop\investment evaluation"

# 登录 Vercel
vercel login

# 部署
vercel

# 部署到生产环境
vercel --prod
```

## 📁 项目结构（Vercel 版本）

```
investment evaluation/
├── api/                          # Serverless API 函数
│   ├── index.py                  # 主 API 入口
│   └── analyzer.py               # 分析引擎
├── public/                       # 静态文件
│   └── index.html                # 前端页面
├── vercel.json                   # Vercel 配置文件
├── requirements.txt              # Python 依赖
└── README_VERCEL.md              # 部署文档
```

## ⚙️ 配置说明

### vercel.json
配置文件定义了：
- Python API 函数的构建方式
- 静态文件的服务方式
- 路由规则

### API 端点

部署后可用的 API：
- `/api/data` - 获取净值数据
- `/api/metrics` - 获取业绩指标
- `/api/summary` - 获取概览信息

## 📊 使用自定义数据

当前版本使用示例数据。如果要使用真实数据，有两种方式：

### 方式一：修改代码中的示例数据

编辑 `api/analyzer.py` 中的 `generate_sample_data()` 函数，替换为你的真实数据。

### 方式二：使用外部数据源

修改 `api/index.py`，从外部 API 或数据库读取数据：

```python
# 示例：从外部 API 获取数据
import requests

def load_data_from_api():
    response = requests.get('https://your-api.com/data')
    data = response.json()
    # 转换为 DataFrame
    return pd.DataFrame(data)

# 在初始化时使用
sample_data = load_data_from_api()
analyzer = InvestmentPerformanceAnalyzer(sample_data)
```

## 🔧 环境变量（可选）

如果需要配置环境变量（如 API 密钥），在 Vercel 项目设置中添加：

1. 进入 Vercel 项目设置
2. 选择 "Environment Variables"
3. 添加变量，如：
   - `RISK_FREE_RATE`: 无风险利率
   - `API_KEY`: 数据源 API 密钥

在代码中使用：
```python
import os
risk_free_rate = float(os.environ.get('RISK_FREE_RATE', 0.015))
```

## ⚠️ 限制说明

Vercel Serverless 函数有以下限制：

1. **执行时间**：
   - Hobby 计划：10秒
   - Pro 计划：60秒

2. **内存**：
   - 默认：1024 MB
   - 最大：3008 MB（Pro）

3. **文件大小**：
   - 部署包：50 MB（压缩后）

4. **无状态**：
   - 每次请求都是独立的
   - 不能保存文件到本地
   - 不支持 Excel 导出（已移除）

## 🐛 故障排查

### 部署失败

1. 检查 `requirements.txt` 中的依赖版本
2. 查看 Vercel 部署日志
3. 确保 `vercel.json` 配置正确

### API 返回错误

1. 在 Vercel Dashboard 查看函数日志
2. 检查数据格式是否正确
3. 验证 API 路径是否正确

### 前端无法加载数据

1. 打开浏览器开发者工具查看网络请求
2. 确认 API 端点返回正确的 JSON
3. 检查 CORS 设置

## 📝 更新部署

### 通过 GitHub
```bash
git add .
git commit -m "Update: 描述你的更改"
git push
```
Vercel 会自动检测更改并重新部署。

### 通过 CLI
```bash
vercel --prod
```

## 🔗 有用链接

- [Vercel 文档](https://vercel.com/docs)
- [Vercel Python Runtime](https://vercel.com/docs/runtimes#official-runtimes/python)
- [Vercel CLI 文档](https://vercel.com/docs/cli)

## 💡 提示

1. 首次部署可能需要较长时间
2. 使用自定义域名需在 Vercel 项目设置中配置
3. 可以设置自动部署（推送到特定分支时）
4. Vercel 提供免费的 HTTPS 和 CDN

## 📧 需要帮助？

如有问题，可以：
1. 查看 Vercel 部署日志
2. 访问 [Vercel 社区](https://github.com/vercel/vercel/discussions)
3. 查看项目 README.md
