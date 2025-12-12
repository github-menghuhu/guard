#!/bin/bash
# ruff检查
echo "🔍 开始 Ruff 检查..."
echo "📋 运行 ruff linting..."
ruff check src --fix

echo "🎨 格式化代码..."
ruff format src

echo -e "✅ Ruff 检查和格式化完成！\n"


# mypy检查
echo "🔍 开始 Mypy 类型分析检查..."
mypy src
echo -e "✅ Mypy 类型分析检查完成！\n"