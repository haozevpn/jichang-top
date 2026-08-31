#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量优化指南/教程类文章及剩余评测文章的description"""

import os
import re

POSTS_DIR = "/Users/macbook/Desktop/网站/jichang-top/astro-site/src/content/posts"

# 文件名 -> (新description, keywords)
DESC_MAP = {
    # 剩余机场评测
    "bianjieyun-review.md": (
        "边界云稳定机场推荐深度评测。作为2026年备受关注的高性价比机场推荐，边界云提供IEPL专线、50+全球节点、3天无理由退款保障。本文从线路架构、晚高峰延迟、吞吐速度、套餐性价比到流媒体与ChatGPT等AI解锁情况进行全方位实测，帮您选择最适合的稳定机场推荐服务。",
        "边界云,机场推荐,稳定机场推荐,IEPL专线机场,梯子推荐,机场测评,科学上网推荐"),
    "dageyun-review.md": (
        "大哥云稳定机场推荐深度评测。作为2026年备受关注的高性价比机场推荐，大哥云提供自研客户端一键连接、免费试用、多节点覆盖。本文从线路架构、晚高峰延迟、吞吐速度、套餐性价比到流媒体与ChatGPT等AI解锁情况进行全方位实测，帮您选择最适合的稳定机场推荐服务。",
        "大哥云,机场推荐,稳定机场推荐,自研客户端机场,梯子推荐,机场测评,科学上网推荐"),
    "guangnianti-review.md": (
        "光年梯稳定机场推荐深度评测。作为2026年老牌高口碑机场推荐，光年梯提供IEPL物理专线、不限速、不限时套餐、7.5元起超低价格。本文从线路架构、晚高峰延迟、吞吐速度、套餐性价比到流媒体与ChatGPT等AI解锁情况进行全方位实测，帮您选择最适合的稳定机场推荐服务。",
        "光年梯,机场推荐,稳定机场推荐,IEPL专线机场,老牌机场推荐,梯子推荐,机场测评"),
    "jilianyun-review.md": (
        "极连云稳定机场推荐深度评测。作为2026年高性价比机场推荐，极连云提供IEPL专线、不限速、不限设备数、1倍率无虚耗。本文从线路架构、晚高峰延迟、吞吐速度、套餐性价比到流媒体与ChatGPT等AI解锁情况进行全方位实测，帮您选择最适合的稳定机场推荐与AI专用机场服务。",
        "极连云,机场推荐,稳定机场推荐,IEPL专线机场,AI机场推荐,梯子推荐,机场测评"),
    # 技术教程类
    "gfw-operation-principles.md": (
        "深入解析GFW防火墙的工作原理与机场流量特征混淆机制。本文详解DPI深度包检测、IP封锁、DNS污染、SNI阻断等封锁技术，以及Shadowsocks、Trojan、VLESS Reality等协议如何对抗检测，帮您理解科学上网的底层原理，选择抗封锁能力强的稳定机场推荐。",
        "GFW原理,防火墙,流量混淆,机场推荐,科学上网原理,协议对抗,DPI检测"),
    "home-router-openwrt-setup-guide.md": (
        "从零开始搭建软路由的完整教程，实现家庭网络全设备无感翻墙。本文详解OpenWrt固件刷写、OpenClash插件安装、机场订阅导入、智能分流配置与故障排查。适合家庭多设备用户，配合稳定机场推荐使用，让电视、手机、游戏机全部自动科学上网。",
        "软路由,OpenWrt,路由器翻墙,家庭网络,机场推荐,OpenClash,全设备翻墙"),
    "proxy-protocols-ss-trojan-vless-hysteria2.md": (
        "深度解析Shadowsocks、Trojan、VLESS、Hysteria2四大主流代理协议的原理与区别。本文对比各协议的加密方式、抗封锁能力、传输速度与适用场景，帮您理解机场推荐使用的核心技术，选择最适合的协议与稳定机场推荐服务，优化科学上网体验。",
        "代理协议,Shadowsocks,Trojan,VLESS,Hysteria2,机场推荐,协议对比"),
    "proxy-security-and-privacy-protection.md": (
        "科学上网的安全与隐私保护完全指南。本文详解代理流量加密原理、DNS泄漏防护、日志隐私风险、如何选择不记录日志的稳定机场推荐。教你规避隐私陷阱、保护个人数据安全，安全放心地使用机场推荐与梯子推荐服务。",
        "代理安全,隐私保护,DNS泄漏,机场推荐,稳定机场推荐,数据安全,科学上网安全"),
    "netflix-disney-streaming-unlock-principles.md": (
        "详解Netflix、Disney+等流媒体解锁的原理与机场节点选择技巧。本文解析流媒体地区检测机制、原生IP与DNS解锁的区别、为什么某些节点无法解锁。教你如何选择能完美解锁4K流媒体的稳定机场推荐，畅享全球影视内容。",
        "Netflix解锁,Disney+解锁,流媒体机场,机场推荐,稳定机场推荐,原生IP,4K流媒体"),
    "network-routing-cross-border-dev-work.md": (
        "面向跨境开发者的网络路由优化指南。本文详解如何为GitHub、Docker、npm、AI API等开发工具配置稳定的科学上网环境，优化跨国网络延迟与稳定性。推荐适合程序员的低延迟稳定机场推荐，提升跨境开发工作效率。",
        "跨境开发,网络路由,GitHub加速,机场推荐,稳定机场推荐,开发者翻墙,程序员科学上网"),
    "setup-proxy-on-apple-tv-smart-tv.md": (
        "Apple TV与智能电视科学上网完整配置教程。本文详解如何为Apple TV、安卓电视、智能电视盒子配置代理，实现4K流媒体解锁。涵盖路由器方案、DNS方案与客户端方案，配合稳定机场推荐使用，让大屏设备畅享Netflix、YouTube 4K内容。",
        "Apple TV翻墙,智能电视科学上网,电视盒子代理,机场推荐,稳定机场推荐,4K流媒体"),
    "share-computer-proxy-to-switch-ps5.md": (
        "详解如何将电脑代理共享给Switch、PS5等游戏主机。本文提供电脑热点共享、路由器配置、局域网代理等多种方案，实现游戏机科学上网与加速。配合低延迟稳定机场推荐，畅玩海外游戏、下载更新、访问eShop与PSN商店。",
        "游戏机翻墙,Switch科学上网,PS5代理,游戏加速,机场推荐,稳定机场推荐,主机代理"),
    "solve-chatgpt-claude-access-denied.md": (
        "彻底解决ChatGPT、Claude提示Access Denied无法访问的问题。本文详解OpenAI风控原理、原生IP与中转IP区别、如何选择支持AI解锁的稳定机场推荐。教你正确配置节点、避免账号封禁，稳定使用ChatGPT、Claude等AI大模型工具。",
        "ChatGPT无法访问,Claude解锁,Access Denied,AI机场推荐,机场推荐,原生IP,稳定机场推荐"),
    "what-is-iepl-iplc-private-line.md": (
        "深入解析IEPL与IPLC国际专线的原理、区别与优势。本文详解物理专线为何不经过GFW、延迟为何更低、稳定性为何更强，对比专线与公网中转的差异。帮你理解高端机场推荐的核心技术，选择真正的IEPL/IPLC专线稳定机场推荐服务。",
        "IEPL专线,IPLC专线,国际专线,机场推荐,稳定机场推荐,物理专线,专线机场"),
    "why-migrate-from-clash-to-singbox.md": (
        "详解为什么越来越多用户从Clash迁移到Sing-box。本文对比Clash与Sing-box的性能、协议支持、配置方式与稳定性差异，提供完整的迁移教程。帮你了解新一代科学上网内核，配合稳定机场推荐订阅，获得更好的翻墙体验。",
        "Sing-box,Clash迁移,科学上网内核,机场推荐,稳定机场推荐,Clash对比,翻墙客户端"),
    "why-speedtest-looks-good-but-actual-experience-slow.md": (
        "揭秘为什么机场测速跑分很高但实际使用却很慢。本文解析多线程测速与单线程体验的区别、丢包率与延迟抖动的影响、如何科学评估机场真实性能。教你避开测速陷阱，选择真正好用的高速稳定机场推荐，而非虚标跑分的机场。",
        "机场测速,单线程速度,机场推荐,稳定机场推荐,测速陷阱,高速机场推荐,机场评测"),
}

def optimize_file(filepath, new_desc, keywords):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 替换description
    content = re.sub(
        r'^description:\s*".*?"',
        f'description: "{new_desc}"',
        content,
        count=1,
        flags=re.MULTILINE
    )

    # 添加或更新keywords
    if re.search(r'^keywords:', content, flags=re.MULTILINE):
        content = re.sub(
            r'^keywords:\s*".*?"',
            f'keywords: "{keywords}"',
            content,
            count=1,
            flags=re.MULTILINE
        )
    else:
        content = re.sub(
            r'(^description:\s*".*?"\n)',
            rf'\1keywords: "{keywords}"\n',
            content,
            count=1,
            flags=re.MULTILINE
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return len(new_desc)

if __name__ == "__main__":
    print("开始批量优化指南/教程类文章...")
    print("=" * 50)
    for filename, (desc, kw) in DESC_MAP.items():
        filepath = os.path.join(POSTS_DIR, filename)
        if os.path.exists(filepath):
            length = optimize_file(filepath, desc, kw)
            print(f"✅ {filename} (description: {length}字符)")
        else:
            print(f"⚠️  {filename} - 文件不存在")
    print("=" * 50)
    print("完成！")
