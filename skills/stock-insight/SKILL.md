---
name: stock-insight
description: "A股智能监控系统 — 持仓监控 + 主线追踪 + 大周期定位 + 自动复盘报告。基于腾讯/东方财富免费API，无需任何Key。"
version: 1.0.0
author: vidbun-chu
license: MIT
tags: [stock, investment, a-stock, monitoring, trading, china, quantitative]
---

# Stock Insight — A股智能监控系统

全自动A股投资分析工具，适合散户使用。

## 功能

- **持仓监控** — 实时获取股价、计算盈亏、止损预警
- **大盘概览** — 三大指数 + 行业/概念板块排名
- **大周期定位** — 基于5月线判断牛熊，动态调整仓位建议
- **自动复盘** — 每日/每周自动生成投资分析报告

## 安装

```bash
git clone https://github.com/vidbun-chu/stock-insight.git
cd stock-insight
pip install -r requirements.txt
```

## 使用

```bash
# 查看大盘
python src/market_overview.py

# 监控持仓
python src/stock_monitor.py --stock 600000 000001 --cost 10.00 15.00

# 生成复盘报告
python src/daily_report.py --type daily

# 大周期分析
python src/market_cycle.py
```

## 配置持仓

编辑 `config/portfolio.yaml`：

```yaml
portfolio:
  - name: 贵州茅台
    code: "600519"
    market: sh
    shares: 100
    cost: 1800.00
```

## 数据源

- 腾讯财经API（实时行情）
- 东方财富API（板块数据）
- 无需任何API Key，开箱即用
