# SEO 优化实施清单

本文档记录已完成的 SEO 优化措施和后续建议。

## ✅ 已完成的优化

### 1. 结构化数据（Schema.org）

**文件**: `layouts/partials/head/custom.html`

已实现的 Schema 类型：

- **Organization Schema**: 网站主体信息（名称、URL、Logo、描述）
- **Article Schema**: 文章页面（标题、作者、发布时间、修改时间、图片、关键词）
- **Review Schema**: 评测文章（自动检测标题中的"测评"关键词）
- **BreadcrumbList Schema**: 面包屑导航（首页 → 分类 → 文章）
- **ItemList Schema**: 机场推荐页的排行榜列表

**验证方法**：
```bash
# 构建后检查生成的 HTML
grep -A 20 'application/ld+json' public/airport/index.html
```

或使用 Google Rich Results Test：https://search.google.com/test/rich-results

---

### 2. Meta 标签优化

**Open Graph (Facebook/社交媒体)**：
- og:title, og:description, og:type, og:image
- article:published_time, article:modified_time
- article:tag（自动从 frontmatter tags 生成）

**Twitter Card**：
- twitter:card, twitter:title, twitter:image
- 使用 summary_large_image 类型

**动态 og:image**：
优先级顺序：
1. 文章 frontmatter 的 `image` 字段
2. 文章目录下的 `cover.*` 图片
3. 默认 fallback: `/img/og-default.jpg`（需要手动添加）

---

### 3. Robots.txt

**文件**: `static/robots.txt`

配置内容：
- 允许所有搜索引擎爬取（Googlebot, Bingbot, Baiduspider, Sogou spider）
- 禁止爬取搜索页和分页（`/search/`, `/page/`, `/tags/page/`, `/categories/page/`）
- 设置 Crawl-delay 为 1 秒
- 指向 sitemap.xml

**验证方法**：
```bash
curl https://jichang-top.com/robots.txt
```

---

### 4. Sitemap

**配置文件**: `config/_default/hugo.toml`

已添加配置：
```toml
[sitemap]
  changefreq = "weekly"
  filename = "sitemap.xml"
  priority = 0.5

[sitemap.home]
  changefreq = "daily"
  priority = 1.0

[sitemap.section]
  changefreq = "weekly"
  priority = 0.7

[sitemap.page]
  changefreq = "monthly"
  priority = 0.6
```

Hugo 自动生成 sitemap.xml（已验证生成成功，24KB）

**提交到搜索引擎**：
- Google Search Console: https://search.google.com/search-console
- Bing Webmaster Tools: https://www.bing.com/webmasters
- 百度搜索资源平台: https://ziyuan.baidu.com

---

### 5. UI/UX 优化

**首页英雄区块** (`layouts/partials/hero-section.html`)：
- 紫色渐变背景 + 装饰性光晕
- 核心卖点突出：IEPL专线、流媒体解锁、AI工具、低价月付
- 双 CTA 按钮：查看推荐机场 + 新手教程

**特色标签栏**：
- 4 个关键特性徽章（⚡ IEPL专线、🎬 流媒体解锁、🤖 ChatGPT/Claude、💰 月付低至¥7）

**新手指南** (`layouts/partials/newbie-guide.html`)：
- 4 步上手流程卡片
- 悬停动画效果
- 直接链接到关键页面

**筛选组件** (`layouts/shortcodes/filter-tags.html`)：
- 按线路类型动态过滤表格
- JavaScript 交互无需刷新页面

---

### 6. 内容可读性

**字体放大**：
- 正文：1.4rem（原 1.25rem）
- 段落：1.35rem
- 表格：1.25rem（表头 1.3rem）
- 列表：1.3rem

**去除干扰元素**：
- 移除所有标题左侧紫色竖线
- 移除引用块左侧紫色竖线
- 优化表格边框为细线灰色

---

## 📋 待优化项（按优先级）

### 高优先级

#### 1. 添加 og:image 默认图片

**操作**：
```bash
# 创建一张 1200x630px 的默认 Open Graph 图片
# 放置到 static/img/og-default.jpg
```

**内容建议**：
- 网站名称：机场Top
- Slogan："2026年最新稳定高速机场推荐"
- 简洁的视觉元素（避免过多文字）

#### 2. 为每篇评测文章添加封面图

**操作**：
在每篇文章的 frontmatter 中添加：
```yaml
image: /img/covers/shunyun-review.jpg
```

或在文章目录下放置 `cover.jpg`/`cover.png`

**设计建议**：
- 机场 Logo + 名称
- 核心卖点（如"Anycast直连"、"¥8.25/月起"）
- 统一的品牌视觉风格

#### 3. 内部链接优化

**操作**：
在相关文章中添加：
```markdown
{{< related-airports "瞬云机场,极连云,光年梯" >}}
```

**策略**：
- 评测文章末尾推荐 3-5 个相关机场
- 教程文章中推荐适合的机场
- 建立主题集群（Topic Cluster）

#### 4. 添加 FAQ Schema

**实现**：
创建 `layouts/shortcodes/faq.html`：
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "什么是 IEPL 专线？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "IEPL（International Ethernet Private Line）是..."
      }
    }
  ]
}
</script>
```

在文章中使用：
```markdown
{{< faq >}}
```

---

### 中优先级

#### 5. 页面加载速度优化

**检测工具**：
- Google PageSpeed Insights: https://pagespeed.web.dev
- GTmetrix: https://gtmetrix.com

**优化建议**：
- 压缩图片（使用 WebP 格式）
- 启用 Cloudflare 的 Auto Minify（HTML/CSS/JS）
- 使用 Hugo 的 image processing 功能生成响应式图片

#### 6. 添加面包屑导航 UI

**操作**：
在 `layouts/partials/article/header.html` 或模板中添加可见的面包屑导航：
```html
<nav aria-label="breadcrumb">
  <ol>
    <li><a href="/">首页</a></li>
    <li><a href="/{{ .Section }}/">{{ .Section }}</a></li>
    <li>{{ .Title }}</li>
  </ol>
</nav>
```

已有 BreadcrumbList Schema，但页面上还没有可见的面包屑 UI。

#### 7. 添加 Article 作者信息

**操作**：
在 `config/_default/params.toml` 或文章 frontmatter 中添加：
```yaml
author:
  name: "机场Top编辑部"
  link: "https://jichang-top.com/about/"
```

更新 Article Schema 中的 author 字段使用真实数据。

---

### 低优先级

#### 8. 添加评论区（可选）

当前配置了 Disqus，但可以考虑：
- Utterances（基于 GitHub Issues，免费无广告）
- Giscus（基于 GitHub Discussions）

#### 9. 添加阅读时间和字数统计

Hugo 内置支持：
```html
<span>阅读时间：{{ .ReadingTime }} 分钟</span>
<span>字数：{{ .WordCount }}</span>
```

#### 10. 添加目录（TOC）跳转

Stack 主题已内置 TOC widget，可以在 `params.toml` 中启用：
```toml
[widgets.toc]
  enable = true
```

---

## 🔍 SEO 验证清单

部署后请验证以下项目：

- [ ] 访问 https://jichang-top.com/robots.txt，确认内容正确
- [ ] 访问 https://jichang-top.com/sitemap.xml，确认包含所有页面
- [ ] 使用 Google Rich Results Test 验证首页和文章页的 Schema
- [ ] 在社交媒体分享链接，检查 Open Graph 卡片显示
- [ ] 使用 Chrome DevTools 的 Lighthouse 运行 SEO 审计
- [ ] 提交 sitemap 到 Google Search Console 和 Bing Webmaster
- [ ] 检查 Google Search Console 的"覆盖率"报告，确认无错误

---

## 📊 监控指标

建议监控的关键指标：

**Google Search Console**：
- 展示次数（Impressions）
- 点击次数（Clicks）
- 平均排名（Average Position）
- CTR（点击率）

**目标关键词**：
- 机场推荐
- IEPL 机场
- 翻墙梯子
- 科学上网
- [机场名称] + 测评

**追踪工具**：
- Google Analytics 4
- 百度统计

---

## 🚀 下一步行动

1. **立即**：添加 `/static/img/og-default.jpg` 默认图片
2. **本周**：为前 10 篇评测文章添加封面图
3. **本周**：在相关文章中添加 `{{< related-airports >}}` 内部链接
4. **本月**：创建 FAQ shortcode 并在主要文章中使用
5. **持续**：每周发布 2-3 篇高质量原创内容

---

## 参考资源

- [Google 搜索中心 - 结构化数据指南](https://developers.google.com/search/docs/appearance/structured-data)
- [Schema.org 官方文档](https://schema.org)
- [Hugo SEO 最佳实践](https://gohugo.io/templates/rss/)
- [Open Graph 协议](https://ogp.me)
- [Twitter Card 文档](https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards)
