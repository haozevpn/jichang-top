#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补充优化仍偏短的文章description，确保达到120-160字符"""

import os
import re

POSTS_DIR = "/Users/macbook/Desktop/网站/jichang-top/astro-site/src/content/posts"

DESC_MAP = {
    "proxy-security-and-privacy-protection.md": (
        "科学上网的安全与隐私保护完全指南。本文详解代理流量加密原理、DNS泄漏防护措施、机场日志隐私风险，以及如何选择不记录日志的稳定机场推荐。教你规避常见隐私陷阱、保护个人数据与账号安全，安全放心地使用机场推荐与梯子推荐服务翻墙上网。",
        "代理安全,隐私保护,DNS泄漏,机场推荐,稳定机场推荐,数据安全,科学上网安全"),
    "netflix-disney-streaming-unlock-principles.md": (
        "详解Netflix、Disney+等流媒体解锁的原理与机场节点选择技巧。本文深入解析流媒体地区检测机制、原生IP与DNS解锁的区别、为什么某些节点无法解锁奈飞。教你如何选择能完美解锁4K流媒体的稳定机场推荐，畅享全球影视内容与独占剧集。",
        "Netflix解锁,Disney+解锁,流媒体机场,机场推荐,稳定机场推荐,原生IP,4K流媒体"),
    "network-routing-cross-border-dev-work.md": (
        "面向跨境开发者的网络路由优化完全指南。本文详解如何为GitHub、Docker、npm、Hugging Face、AI API等开发工具配置稳定的科学上网环境，优化跨国网络延迟与连接稳定性。推荐适合程序员的低延迟稳定机场推荐，全面提升跨境开发工作效率。",
        "跨境开发,网络路由,GitHub加速,机场推荐,稳定机场推荐,开发者翻墙,程序员科学上网"),
    "share-computer-proxy-to-switch-ps5.md": (
        "详解如何将电脑代理共享给Switch、PS5等游戏主机实现科学上网。本文提供电脑热点共享、路由器配置、局域网代理等多种实用方案，实现游戏机翻墙与加速。配合低延迟稳定机场推荐，畅玩海外游戏、下载更新、访问eShop与PSN商店，告别锁区烦恼。",
        "游戏机翻墙,Switch科学上网,PS5代理,游戏加速,机场推荐,稳定机场推荐,主机代理"),
    "what-is-iepl-iplc-private-line.md": (
        "深入解析IEPL与IPLC国际专线的原理、区别与核心优势。本文详解物理专线为何不经过GFW防火墙、延迟为何更低、高峰期稳定性为何更强，全面对比专线与公网中转的本质差异。帮你理解高端机场推荐的核心技术，选择真正的IEPL/IPLC专线稳定机场推荐服务。",
        "IEPL专线,IPLC专线,国际专线,机场推荐,稳定机场推荐,物理专线,专线机场"),
    "why-migrate-from-clash-to-singbox.md": (
        "详解为什么越来越多用户从Clash迁移到Sing-box内核。本文全面对比Clash与Sing-box的性能表现、协议支持、配置方式与稳定性差异，并提供完整的迁移教程与配置示例。帮你了解新一代科学上网内核，配合稳定机场推荐订阅，获得更快更稳定的翻墙体验。",
        "Sing-box,Clash迁移,科学上网内核,机场推荐,稳定机场推荐,Clash对比,翻墙客户端"),
    "why-speedtest-looks-good-but-actual-experience-slow.md": (
        "揭秘为什么机场测速跑分很高但实际使用却很慢卡顿。本文深入解析多线程测速与单线程真实体验的区别、丢包率与延迟抖动的关键影响、如何科学评估机场真实性能。教你避开测速陷阱与虚标跑分，选择真正好用的高速稳定机场推荐，获得流畅上网体验。",
        "机场测速,单线程速度,机场推荐,稳定机场推荐,测速陷阱,高速机场推荐,机场评测"),
    "home-router-openwrt-setup-guide.md": (
        "从零开始搭建软路由的完整教程，实现家庭网络全设备无感翻墙。本文详解OpenWrt固件刷写、OpenClash插件安装、机场订阅导入、智能分流规则配置与常见故障排查。适合家庭多设备用户，配合稳定机场推荐使用，让电视、手机、游戏机全部自动科学上网。",
        "软路由,OpenWrt,路由器翻墙,家庭网络,机场推荐,OpenClash,全设备翻墙"),
}

def optimize_file(filepath, new_desc, keywords):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'^description:\s*".*?"', f'description: "{new_desc}"',
                     content, count=1, flags=re.MULTILINE)
    if re.search(r'^keywords:', content, flags=re.MULTILINE):
        content = re.sub(r'^keywords:\s*".*?"', f'keywords: "{keywords}"',
                         content, count=1, flags=re.MULTILINE)
    else:
        content = re.sub(r'(^description:\s*".*?"\n)', rf'\1keywords: "{keywords}"\n',
                         content, count=1, flags=re.MULTILINE)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return len(new_desc)

if __name__ == "__main__":
    for filename, (desc, kw) in DESC_MAP.items():
        filepath = os.path.join(POSTS_DIR, filename)
        if os.path.exists(filepath):
            length = optimize_file(filepath, desc, kw)
            print(f"✅ {filename} ({length}字符)")
