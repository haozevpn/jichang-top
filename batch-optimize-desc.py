#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量优化机场评测文章的description，扩展到150-160字符并融入关键词"""

import os
import re

POSTS_DIR = "/Users/macbook/Desktop/网站/jichang-top/astro-site/src/content/posts"

# 机场评测文章的优化映射：文件名 -> (机场名, 线路特色描述)
REVIEW_MAP = {
    "shunyun-review.md": ("瞬云机场", "Anycast高速直连、1倍率无虚标、大带宽不限时"),
    "jisuyun-review.md": ("极速云机场", "中转加速直连、大带宽、不限时套餐、多平台兼容"),
    "shanshuiyun-review.md": ("山水云", "隧道中转、流媒体解锁、按量付费、设备无限制"),
    "lizione-review.md": ("LiZione", "Shadowsocks协议、BGP中转、多端支持、原生IP解锁"),
    "longmaoyun-review.md": ("龙猫云", "专线中转、多端自适应、安全稳定"),
    "qingyunti-review.md": ("青云梯", "隧道中转、支持不限时、大带宽秒开、高性价比"),
    "kedajiasudu-review.md": ("可达加速度", "混合专线、价格实惠、多线负载、节点丰富"),
    "edgex-review.md": ("Edge-X机场", "IPLC专线、低延迟、不限设备数、大流量支持"),
    "doraemon-review.md": ("哆啦A梦", "三网IEPL专线、千兆大带宽、原生IP解锁、支持不限时"),
    "feiniaojichang-review.md": ("飞鸟机场", "BGP多线中转、支持不限时、高速平稳、全节点解锁"),
    "guangshuyun-review.md": ("光速云", "BGP+IEPL专线、不限时套餐、1倍率无虚耗、全节点解锁"),
    "huanyuyun-review.md": ("寰宇云", "BGP多线中转、支持不限时、按量付费、高性价比"),
    "huayun-review.md": ("花云", "跨境物理专线、高防中转、稳定老厂、多平台优化"),
    "naiyun-review.md": ("奈云", "跨境专线、AI与Netflix解锁、全客户端支持、不限时"),
    "quanqiuyun-review.md": ("寰球云", "多线专线中转、全球节点覆盖、稳定高速"),
    "shanhai-review.md": ("山海云", "专线中转、流媒体解锁、稳定可靠"),
    "xingdaomeng-review.md": ("星岛盟", "IEPL专线、多地区节点、高速稳定"),
    "xundavpn-review.md": ("迅达", "专线加速、多协议支持、高速稳定"),
    "yinyun-review.md": ("音云", "BGP中转、流媒体解锁、性价比高"),
    "miaomiaoyun-review.md": ("喵喵云", "专线中转、多端支持、稳定高速"),
}

def build_description(name, features):
    """构建140-160字符的description"""
    desc = (f"{name}稳定机场推荐深度评测。作为2026年备受关注的高性价比机场推荐，"
            f"{name}提供{features}等核心优势。本文从线路架构、晚高峰延迟、吞吐速度、"
            f"套餐性价比到流媒体与ChatGPT等AI大模型解锁情况进行全方位实测，"
            f"帮您选择最适合的稳定机场推荐与梯子推荐服务。")
    return desc

def optimize_file(filepath, name, features):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_desc = build_description(name, features)

    # 替换description行
    new_content = re.sub(
        r'^description:\s*".*?"',
        f'description: "{new_desc}"',
        content,
        count=1,
        flags=re.MULTILINE
    )

    # 如果没有keywords字段，在description后添加
    if 'keywords:' not in new_content:
        keywords = f'机场推荐,稳定机场推荐,{name},梯子推荐,机场测评,科学上网推荐,高速机场推荐'
        new_content = re.sub(
            r'(^description:\s*".*?"\n)',
            rf'\1keywords: "{keywords}"\n',
            new_content,
            count=1,
            flags=re.MULTILINE
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return len(new_desc)

if __name__ == "__main__":
    print("开始批量优化机场评测文章description...")
    print("=" * 50)
    for filename, (name, features) in REVIEW_MAP.items():
        filepath = os.path.join(POSTS_DIR, filename)
        if os.path.exists(filepath):
            length = optimize_file(filepath, name, features)
            print(f"✅ {filename} - {name} (description: {length}字符)")
        else:
            print(f"⚠️  {filename} - 文件不存在，跳过")
    print("=" * 50)
    print("批量优化完成！")
