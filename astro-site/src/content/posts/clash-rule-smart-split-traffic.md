---
title: "Clash 分流规则怎么配？让国内国外流量自动分开走"
description: "Clash分流规则配置完整教程，教你实现国内网站直连、国外代理走机场的高效智能分流。本文详细讲解DOMAINS、IP-CIDR、Rule-Set与Final默认规则的设置方法，帮您优化网络访问速度、降低节点延迟并节省机场流量，发挥稳定机场推荐的最佳性能。"
keywords: "Clash分流规则,智能分流配置,Clash规则教程,机场分流设置,机场推荐,代理规则配置,稳定机场推荐"
date: 2026-08-16
tags: ["Clash分流","规则配置","智能分流"]
categories: ["科学上网指南"]
slug: "clash-rule-smart-split-traffic"
---

刚开始用Clash的时候，我也是直接用"全局代理"模式，所有流量全部走代理。后来发现国内网站访问反而变慢，而且流量消耗特别快——国内网站本来直连就行，绕到境外节点再回来，纯属浪费。

分流规则就是解决这个问题的：让该走代理的流量走代理，该直连的流量直连，自动判断。配好之后，打开百度、bilibili直接本地访问，打开Google、YouTube自动走代理，完全无感切换。

## 分流规则的基本逻辑

Clash的规则模式（Rule Mode）会按照配置文件里的规则列表，从上到下逐条匹配每一个网络请求，匹配到了就执行对应动作（代理、直连），匹配不到就往下走，最后走到Final兜底规则。

一条规则通常长这样：
```
DOMAIN-SUFFIX,google.com,Proxy
```
意思是：如果访问的域名以google.com结尾（比如www.google.com、mail.google.com），就走Proxy策略组。

规则类型有很多种，常见的是：
- `DOMAIN`：完整域名匹配
- `DOMAIN-SUFFIX`：域名后缀匹配
- `DOMAIN-KEYWORD`：域名包含关键词
- `IP-CIDR`：IP地址段匹配
- `GEOIP`：根据IP归属地匹配

## 一个典型的分流配置结构

大部分机场订阅下载下来的配置文件里都有规则部分，打开配置文件（YAML格式），能看到类似这样的结构：

```yaml
rules:
  - DOMAIN-SUFFIX,google.com,Proxy
  - DOMAIN-SUFFIX,youtube.com,Proxy
  - DOMAIN-SUFFIX,facebook.com,Proxy
  - DOMAIN-SUFFIX,baidu.com,DIRECT
  - DOMAIN-SUFFIX,bilibili.com,DIRECT
  - GEOIP,CN,DIRECT
  - MATCH,Proxy
```

这段规则的含义：
1. Google、YouTube、Facebook走代理
2. 百度、B站直连
3. 如果目标IP是中国大陆的IP段（GEOIP,CN），直连
4. 以上都不匹配，走代理（MATCH是兜底规则，相当于Final）

## 直连规则：国内流量不走代理

最简单粗暴的直连规则：用`GEOIP,CN,DIRECT`这一条。

这条规则的意思是，只要目标IP属于中国大陆IP段，一律直连。Clash内置了GEOIP数据库，可以自动判断IP归属地。

有了这一条，绝大部分国内网站（百度、淘宝、B站、微信服务器等等）都会直连，不走代理。

但有时候这条不够：比如某些国内网站的DNS解析被污染了，或者某些国内服务的域名没正确解析成国内IP，这时候单靠GEOIP还不够，需要配合域名规则：

```yaml
  - DOMAIN-SUFFIX,cn,DIRECT
  - DOMAIN-SUFFIX,baidu.com,DIRECT
  - DOMAIN-SUFFIX,qq.com,DIRECT
  - DOMAIN-SUFFIX,163.com,DIRECT
```

`.cn`后缀的域名通常是国内网站，直连。其他常用的国内域名也可以加进去。

更完整的方式是引用规则集，下面会讲。

## 代理规则：境外服务走代理

同样的逻辑，把常用的境外域名列出来，让它们走代理：

```yaml
  - DOMAIN-SUFFIX,google.com,Proxy
  - DOMAIN-SUFFIX,youtube.com,Proxy
  - DOMAIN-SUFFIX,twitter.com,Proxy
  - DOMAIN-SUFFIX,facebook.com,Proxy
  - DOMAIN-SUFFIX,openai.com,Proxy
```

手动列举太麻烦，可以用规则集（Rule Provider），后面会说。

## MATCH规则：兜底策略

规则列表最后通常有一条`MATCH`规则，这是兜底：

```yaml
  - MATCH,Proxy
```

意思是前面所有规则都没匹配到的流量，全部走Proxy。

有人喜欢设成`MATCH,DIRECT`，也就是默认直连，只有明确规则匹配到的才走代理。这两种策略各有利弊：

- `MATCH,Proxy`：保守派做法，有可能被墙的流量都走代理，确保能访问，但可能会浪费流量。
- `MATCH,DIRECT`：激进派做法，默认直连，减少流量消耗，但碰到新的被墙网站需要手动补规则。

我个人习惯用`MATCH,Proxy`，因为国内常用的网站基本都能用GEOIP和域名规则覆盖到，剩下的默认走代理比较省心。

## 用规则集简化配置

手动维护几百条规则太累，可以用规则集（Rule Provider）：

```yaml
rule-providers:
  reject:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/reject.txt"
    path: ./ruleset/reject.yaml
    interval: 86400

  direct:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/direct.txt"
    path: ./ruleset/direct.yaml
    interval: 86400

  proxy:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/proxy.txt"
    path: ./ruleset/proxy.yaml
    interval: 86400

rules:
  - RULE-SET,reject,REJECT
  - RULE-SET,direct,DIRECT
  - RULE-SET,proxy,Proxy
  - GEOIP,CN,DIRECT
  - MATCH,Proxy
```

这些规则集由社区维护（比如Loyalsoldier的规则），定期更新，覆盖了主流的广告域名、国内域名、国际域名。Clash会自动下载规则文件，按设定的时间间隔更新。

用规则集的好处是不用自己维护规则列表，规则更全面，而且自动更新。

## DNS配置对分流的影响

分流规则要生效，DNS配置也很重要。

如果DNS配置不对，域名解析出来的IP是错的，分流规则也会失效。比如某个国内网站的DNS被污染，解析出境外IP，那`GEOIP,CN,DIRECT`规则就匹配不到，流量可能错误地走了代理。

在Clash配置里，DNS部分推荐这样配：

```yaml
dns:
  enable: true
  listen: 0.0.0.0:53
  enhanced-mode: fake-ip
  nameserver:
    - 223.5.5.5
    - 119.29.29.29
  fallback:
    - 1.1.1.1
    - 8.8.8.8
```

`enhanced-mode: fake-ip`让Clash返回虚假IP，流量经过Clash后再进行真正的DNS解析，避免DNS污染。`nameserver`是国内DNS，`fallback`是境外DNS，Clash会根据规则选择合适的DNS服务器。

## 检查分流是否生效

配置完之后，怎么确认分流有没有生效？

在Clash的日志面板里可以看到每个请求匹配到的规则。访问百度，日志显示`baidu.com -> DIRECT`，说明直连了；访问Google，日志显示`google.com -> Proxy`，说明走代理了。

或者用测速工具：直连百度测一次速，走代理访问Google测一次速，如果延迟差距明显（国内直连延迟通常几十ms，走代理延迟100ms以上），说明分流生效了。

## 推荐阅读

- [2026年最新稳定机场推荐排行榜](/airport/)
- [极连云测评 - IEPL专线首选](/p/jilianyun-review/)
- [瞬云机场测评 - Anycast直连](/p/shunyun-review/)

## 常见问题：某些网站走错了

配好规则后，发现某个国内网站还是走了代理，或者某个国外网站没走代理，怎么办？

可以在规则列表最前面手动加一条规则：

```yaml
rules:
  - DOMAIN-SUFFIX,example.com,DIRECT  # 手动指定这个域名直连
  - RULE-SET,direct,DIRECT
  - RULE-SET,proxy,Proxy
  # ... 其他规则
```

规则是从上到下匹配的，越靠前优先级越高。如果某个网站需要特殊处理，手动加一条规则放在最前面就行。

---

分流配置一次搞定，后面就不用管了，国内国外流量自动分流，体验顺滑，流量也省了不少。用规则集省去手动维护的麻烦，是目前最省心的方案。
