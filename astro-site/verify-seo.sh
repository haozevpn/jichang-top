#!/bin/bash

# SEO验证脚本
# 用于检查网站的基本SEO配置是否正确

echo "======================================"
echo "机场TOP - SEO配置验证"
echo "======================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 项目路径
PROJECT_DIR="/Users/macbook/Desktop/网站/jichang-top/astro-site"

echo "📋 检查核心文件..."
echo ""

# 1. 检查robots.txt
echo "1. 检查 robots.txt"
if [ -f "$PROJECT_DIR/public/robots.txt" ]; then
    echo -e "${GREEN}✓${NC} robots.txt 存在"
else
    echo -e "${RED}✗${NC} robots.txt 不存在"
fi
echo ""

# 2. 检查sitemap配置
echo "2. 检查 sitemap 配置"
if grep -q "@astrojs/sitemap" "$PROJECT_DIR/astro.config.mjs"; then
    echo -e "${GREEN}✓${NC} sitemap 已配置"
else
    echo -e "${RED}✗${NC} sitemap 未配置"
fi
echo ""

# 3. 检查关键页面的关键词
echo "3. 检查关键页面关键词覆盖..."
echo ""

# 检查首页
echo "   📄 首页 (index.astro):"
keywords=("机场推荐" "稳定机场推荐" "梯子推荐" "VPN推荐")
for keyword in "${keywords[@]}"; do
    if grep -q "$keyword" "$PROJECT_DIR/src/pages/index.astro"; then
        echo -e "   ${GREEN}✓${NC} 包含: $keyword"
    else
        echo -e "   ${RED}✗${NC} 缺失: $keyword"
    fi
done
echo ""

# 检查机场页
echo "   📄 机场页 (airport.astro):"
for keyword in "${keywords[@]}"; do
    if grep -q "$keyword" "$PROJECT_DIR/src/pages/airport.astro"; then
        echo -e "   ${GREEN}✓${NC} 包含: $keyword"
    else
        echo -e "   ${RED}✗${NC} 缺失: $keyword"
    fi
done
echo ""

# 4. 检查BaseLayout中的SEO配置
echo "4. 检查 BaseLayout SEO 配置"
if grep -q "og:title" "$PROJECT_DIR/src/layouts/BaseLayout.astro"; then
    echo -e "${GREEN}✓${NC} Open Graph 标签已配置"
else
    echo -e "${RED}✗${NC} Open Graph 标签未配置"
fi

if grep -q "twitter:card" "$PROJECT_DIR/src/layouts/BaseLayout.astro"; then
    echo -e "${GREEN}✓${NC} Twitter Card 已配置"
else
    echo -e "${RED}✗${NC} Twitter Card 未配置"
fi

if grep -q "application/ld+json" "$PROJECT_DIR/src/layouts/BaseLayout.astro"; then
    echo -e "${GREEN}✓${NC} Schema.org 结构化数据已配置"
else
    echo -e "${RED}✗${NC} Schema.org 结构化数据未配置"
fi

if grep -q "canonical" "$PROJECT_DIR/src/layouts/BaseLayout.astro"; then
    echo -e "${GREEN}✓${NC} Canonical URL 已配置"
else
    echo -e "${RED}✗${NC} Canonical URL 未配置"
fi
echo ""

# 5. 统计关键词出现频率
echo "5. 统计关键词出现频率"
echo ""
echo "   首页关键词密度:"
for keyword in "${keywords[@]}"; do
    count=$(grep -o "$keyword" "$PROJECT_DIR/src/pages/index.astro" | wc -l)
    echo "   - $keyword: $count 次"
done
echo ""

echo "   机场页关键词密度:"
for keyword in "${keywords[@]}"; do
    count=$(grep -o "$keyword" "$PROJECT_DIR/src/pages/airport.astro" | wc -l)
    echo "   - $keyword: $count 次"
done
echo ""

# 6. 检查内部组件
echo "6. 检查 SEO 相关组件"
if [ -f "$PROJECT_DIR/src/components/InternalLinks.astro" ]; then
    echo -e "${GREEN}✓${NC} InternalLinks 组件已创建"
else
    echo -e "${RED}✗${NC} InternalLinks 组件不存在"
fi
echo ""

# 7. 检查文章数量
echo "7. 统计内容数量"
post_count=$(find "$PROJECT_DIR/src/content/posts" -name "*.md" | wc -l)
echo "   - 文章总数: $post_count 篇"
echo ""

echo "======================================"
echo "✅ SEO验证完成"
echo "======================================"
echo ""
echo "💡 建议："
echo "   1. 确保关键词自然融入内容"
echo "   2. 定期更新sitemap"
echo "   3. 监控Google Search Console"
echo "   4. 建立高质量外链"
echo ""
