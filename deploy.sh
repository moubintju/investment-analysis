#!/bin/bash

echo "================================"
echo "投资业绩分析系统 - Vercel 部署"
echo "================================"
echo ""

# 检查是否已初始化 git
if [ ! -d ".git" ]; then
    echo "初始化 Git 仓库..."
    git init
    echo "✓ Git 仓库已初始化"
else
    echo "✓ Git 仓库已存在"
fi

# 添加文件
echo ""
echo "添加文件到 Git..."
git add .

# 创建提交
echo "创建提交..."
git commit -m "Deploy: Investment Analysis System to Vercel" || echo "没有新的更改需要提交"

# 提示用户创建 GitHub 仓库
echo ""
echo "================================"
echo "下一步：创建 GitHub 仓库"
echo "================================"
echo ""
echo "1. 访问 https://github.com/new"
echo "2. 创建一个新仓库（例如：investment-analysis）"
echo "3. 不要初始化 README, .gitignore 或 LICENSE"
echo "4. 创建后，运行以下命令（替换为你的仓库 URL）："
echo ""
echo "   git remote add origin https://github.com/你的用户名/investment-analysis.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "================================"
echo "部署到 Vercel"
echo "================================"
echo ""
echo "GitHub 推送完成后："
echo "1. 访问 https://vercel.com"
echo "2. 使用 GitHub 账号登录"
echo "3. 点击 'New Project'"
echo "4. 导入你的 GitHub 仓库"
echo "5. Vercel 会自动检测配置并部署"
echo ""
echo "或者使用 Vercel CLI："
echo "   npm install -g vercel"
echo "   vercel login"
echo "   vercel --prod"
echo ""
