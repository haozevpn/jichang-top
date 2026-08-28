#!/bin/bash

# 批量优化description长度的脚本
# 将所有过短的description扩展到150-160字符

cd /Users/macbook/Desktop/网站/jichang-top/astro-site/src/content/posts

echo "开始优化文章description..."
echo "================================"

# 统计需要优化的文章数量
count=0
for file in *.md; do
  desc=$(grep '^description:' "$file" | head -1 | sed 's/description: *"//; s/"$//')
  if [ ${#desc} -lt 120 ]; then
    count=$((count + 1))
  fi
done

echo "发现 $count 篇文章的description需要优化（少于120字符）"
echo ""
echo "建议的优化策略："
echo "1. 机场评测文章: 添加'作为2026年XX机场推荐，提供XX线路、XX特色。本文详细测评...帮您选择最适合的稳定机场推荐服务。'"
echo "2. 技术教程文章: 添加'完整教程包括XX配置、XX优化、XX注意事项。适合XX用户，提供详细步骤和实战案例。'"
echo "3. 指南类文章: 添加'本指南涵盖XX场景、XX方法、XX建议，帮助您XX，提升XX体验。'"
echo ""
echo "================================"
echo "需要优化的文章列表："
echo ""

for file in *.md; do
  desc=$(grep '^description:' "$file" | head -1 | sed 's/description: *"//; s/"$//')
  if [ ${#desc} -lt 120 ]; then
    echo "- $file (当前: ${#desc}字符)"
  fi
done

echo ""
echo "================================"
echo "建议使用Claude逐个优化，确保描述准确且吸引人"
