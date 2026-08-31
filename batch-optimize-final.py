#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""优化最后10篇文章（此前误改了content/post目录，现修正astro-site版本）"""

import os
import re

POSTS_DIR = "/Users/macbook/Desktop/网站/jichang-top/astro-site/src/content/posts"

DESC_MAP = {
    "airport-blocked-switch-node.md": (
        "机场推荐突然断线、连不上节点，不一定是机场跑路了。DNS污染、机场节点被封、本地网络问题都可能导致连接失败。本文整理了5个实用排查步骤与应急方案，帮你快速定位问题、切换节点恢复连接，并教你如何选择稳定机场推荐减少断线烦恼。",
        "机场连不上,节点切换,机场推荐,稳定机场推荐,机场封锁,科学上网故障排查,梯子推荐"),
    "airport-chatgpt-unlock.md": (
        "用机场推荐访问ChatGPT频繁遇到封号或无法注册？核心原因在于节点IP类型。本文详解原生IP和中转IP的区别、为什么某些机场推荐节点容易触发OpenAI风控、如何判断节点质量。教你选对支持ChatGPT解锁的AI机场推荐，避免账号被封，稳定使用AI工具。",
        "机场推荐,ChatGPT机场,原生IP机场推荐,AI机场推荐,稳定机场推荐,ChatGPT解锁,机场节点选择"),
    "airport-multiple-devices-setup.md": (
        "机场推荐账号的设备数限制是怎么回事？同时在线几台、订阅能否分享？本文解释不同机场推荐的设备数规则、超出限制的多种解决方案，包括升级套餐、路由器翻墙与软路由配置思路。教你如何选择不限设备的稳定机场推荐，实现全家多设备共享科学上网。",
        "多设备翻墙,机场设备数,订阅分享,路由器翻墙,机场推荐,稳定机场推荐,不限设备机场"),
    "airport-node-latency-optimization.md": (
        "机场推荐延迟高、网速慢不一定是机场本身的问题，很多时候是节点没选对或配置不当。本文从手动选节点、测速工具使用、分流规则优化、避开高峰期等实际操作角度出发，分享几个真正有效的延迟优化方法，帮你充分发挥稳定机场推荐的性能潜力。",
        "延迟优化,节点配置,机场使用技巧,机场节点,机场推荐,稳定机场推荐,高速机场推荐"),
    "airport-traffic-limit-vs-unlimited.md": (
        "机场套餐按量计费还是不限时不限量，选哪个更值？本文从日常用量场景出发，分析轻度用户、重度用户、团队用户各自的最优选择，帮你算清楚机场推荐套餐的真实性价比。教你根据实际需求选择合适的稳定机场推荐套餐，避免流量浪费或不够用。",
        "机场推荐,套餐选择,不限时流量,机场套餐,稳定机场推荐,按量计费,梯子推荐"),
    "anti-exit-scam-airport-guide.md": (
        "专业的稳定机场推荐防跑路指南，揭秘年付低价诱惑背后的跑路机制。本文教你如何识别跑路征兆、选择可靠的机场推荐服务、坚持月付避坑策略。涵盖线路辨别、口碑查询、退款政策等实用技巧，帮助新手找到真正稳定不跑路的科学上网梯子推荐。",
        "稳定机场推荐,机场推荐,梯子推荐,防跑路,机场避坑,月付策略,科学上网"),
    "cheap-airport-recommendation-2026.md": (
        "2026年便宜机场推荐指南：月付10元以内的低价机场推荐真的能用吗？本文从实际体验出发，评测性价比稳定机场推荐，分析低价梯子推荐的常见取舍、哪些值得买哪些是坑，以及靠谱的便宜机场推荐选择思路，帮你用最低预算找到能稳定使用的机场。",
        "便宜机场推荐,低价机场推荐,性价比机场推荐,稳定机场推荐,梯子推荐,机场推荐,10元机场"),
    "clash-rule-smart-split-traffic.md": (
        "Clash分流规则配置完整教程，教你实现国内流量直连、国外流量走代理的智能分流。本文详解机场推荐订阅中的直连规则、代理规则、Final规则、规则集与DNS配置方法，帮你优化访问速度并节省流量，充分发挥稳定机场推荐的性能。",
        "Clash分流规则,智能分流配置,Clash规则教程,机场分流设置,机场推荐,代理规则配置,稳定机场推荐"),
    "how-to-choose-stable-airport.md": (
        "专业的机场推荐与稳定机场推荐选购指南。本文教你如何辨别真假IEPL/IPLC专线、识别跑路套路、选择可靠的梯子推荐服务。涵盖线路类型对比、价格陷阱分析、节点测试技巧与口碑查询方法，帮你从繁杂市场中找到真正稳定的科学上网机场推荐。",
        "机场推荐,稳定机场推荐,梯子推荐,新手指南,机场选购,IEPL专线,防跑路"),
    "vpn-vs-airport-difference.md": (
        "详解机场推荐与VPN推荐的本质区别。本文对比稳定机场推荐与传统VPN的协议差异、稳定性、适用场景，解析为什么国内科学上网机场比VPN更实用。帮你理清机场与VPN的概念混淆，选择最适合的梯子推荐方案，避免走弯路。",
        "机场推荐,VPN推荐,稳定机场推荐,梯子推荐,机场和VPN区别,科学上网工具对比,翻墙工具选择"),
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
