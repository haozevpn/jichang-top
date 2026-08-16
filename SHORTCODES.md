# Shortcodes 使用指南

本文档说明如何在 Markdown 文章中使用自定义 shortcodes 组件。

## 1. rating-card - 评分卡片

**用途**：在评测文章顶部显示机场核心信息（评分、价格、线路类型等）

**使用示例**：

```markdown
{{< rating-card name="瞬云机场" rating="9.9" price="8.25" route="Anycast直连" unlimited="true" trial="false" >}}
```

**参数说明**：
- `name`: 机场名称（必填）
- `rating`: 评分，满分 10.0（可选，默认 9.0）
- `price`: 起步价格，单位元（可选，默认 10.00）
- `route`: 线路类型，如"IEPL专线"、"BGP中转"（可选，默认"中转线路"）
- `unlimited`: 是否支持不限时流量，true/false（可选，默认 true）
- `trial`: 是否有免费试用，true/false（可选，默认 false）

**效果**：显示一个紫色渐变背景的卡片，展示评分、价格、线路类型、不限时流量、试用状态等核心信息。

---

## 2. filter-tags - 筛选标签

**用途**：在机场推荐页添加按线路类型筛选表格的交互功能

**使用示例**：

```markdown
{{< filter-tags >}}
```

**参数说明**：无需参数，直接调用

**效果**：
- 显示一组可点击的筛选按钮：全部机场、IEPL专线、IPLC专线、BGP中转、Anycast直连、直连公网
- 点击按钮后，下方的表格会自动过滤，只显示匹配线路类型的行
- 支持按"线路类型"列的内容进行文本匹配

**注意**：必须放在表格**之前**，且页面上必须有一个 `<table>` 标签才能正常工作。

---

## 3. related-airports - 相关推荐

**用途**：在文章末尾或中间插入相关机场推荐链接，增加内部链接密度

**使用示例**：

```markdown
{{< related-airports "瞬云机场,极连云,光年梯" >}}
```

**参数说明**：
- 第一个参数：逗号分隔的机场名称列表（必填）
- 不要有空格，直接用英文逗号分隔

**效果**：显示一个带边框的推荐区块，每个机场名称都是可点击的链接，链接到 `/airport/#机场名称` 锚点。

---

## 4. newbie-guide - 新手指南

**用途**：在首页或指南页显示 4 步上手流程

**使用示例**：

```markdown
{{< newbie-guide >}}
```

**参数说明**：无需参数，这是一个 partial，在 Markdown 中通过 shortcode 形式调用，或在模板中用 `{{- partial "newbie-guide.html" . -}}` 调用。

**效果**：显示 4 个卡片：
1. 选择机场 → 链接到 /airport/
2. 注册购买 → 链接到教程分类
3. 下载客户端 → 链接到教程分类
4. 导入订阅 → 链接到教程分类

---

## 实战示例

### 评测文章结构

```markdown
---
title: "2026 瞬云机场测评"
date: 2026-06-06
categories: ["机场测评"]
tags: ["瞬云机场", "Anycast直连", "机场评测"]
---

{{< rating-card name="瞬云机场" rating="9.9" price="8.25" route="Anycast直连" unlimited="true" trial="false" >}}

## 基本介绍

全站一倍率无虚标的高性价比机场...

## 线路测试

实测香港节点速度...

## 总结

瞬云机场适合...

{{< related-airports "寰宇云,极连云,光年梯" >}}
```

### 机场推荐页结构

```markdown
---
title: "2026年机场推荐"
---

## 🏆 2026核心机场关键参数对比表格

{{< filter-tags >}}

| 排名 | 机场名称 | 线路类型 | 起步价格 | 不限时流量 | 官网注册通道 |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 瞬云机场 | Anycast直连 | ¥ 8.25/月起 | ✅ 支持 | [点此前往官网注册](https://example.com) |
| 2 | 寰宇云 | BGP多线中转 | ¥ 7.40/月起 | ✅ 支持 | [点此前往官网注册](https://example.com) |
...
```

---

## 注意事项

1. **Shortcode 语法**：Hugo shortcode 必须用 `{{< >}}` 或 `{{% %}}` 包裹，不是 `{{ }}`
2. **参数引号**：字符串参数建议加引号，布尔值 true/false 不加引号
3. **逗号分隔**：`related-airports` 的名称列表用英文逗号，不要有空格
4. **表格筛选**：`filter-tags` 必须放在表格前面，且表格必须有"线路类型"列
5. **链接锚点**：`related-airports` 生成的链接格式是 `/airport/#机场名称`，确保目标页面有对应的锚点或 ID

---

## 文件位置

- Shortcodes: `/layouts/shortcodes/*.html`
- Partials: `/layouts/partials/*.html`
- 样式: `/assets/scss/custom.scss`

如需修改组件样式或行为，直接编辑对应文件即可。
