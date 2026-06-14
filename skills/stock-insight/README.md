# 📈 Stock Insight — A股智能监控系统

<p align="center">
  <strong>持仓监控 | 主线追踪 | 大周期定位 | 自动复盘</strong>
</p>

<p align="center">
  <a href="#快速开始">快速开始</a> ·
  <a href="#功能特性">功能特性</a> ·
  <a href="#使用方法">使用方法</a> ·
  <a href="#配置说明">配置说明</a> ·
  <a href="#投资体系">投资体系</a>
</p>

---

## 🎯 这是什么？

Stock Insight 是一个**全自动A股投资分析系统**，基于"弱弱投资体系"构建，帮助散户：

- 📊 **实时监控持仓** — 股价变动、盈亏计算、止损预警
- 🔍 **追踪市场主线** — 板块资金流向、龙头识别、主线评分
- 📐 **大周期定位** — 基于5月线判断牛熊，动态调整仓位
- 📝 **自动复盘** — 每日/每周自动生成分析报告

> **核心理念**：市值最重要，多和股票交朋友，少和股票谈恋爱。

---

## ⚡ 快速开始

### 环境要求

- Python 3.8+
- 无需任何API Key（使用腾讯/东方财富免费接口）

### 安装

```bash
git clone https://github.com/vidbun-chu/stock-insight.git
cd stock-insight
pip install -r requirements.txt
```

### 5分钟跑起来

```bash
# 1. 查看持仓股实时行情
python src/stock_monitor.py --stock 600000 000001

# 2. 获取大盘数据
python src/market_overview.py

# 3. 生成每日复盘报告
python src/daily_report.py

# 4. 大周期定位分析
python src/market_cycle.py
```

---

## 🔥 功能特性

### 1. 持仓监控

```bash
python src/stock_monitor.py --stock 600000 000001 --cost 10.00 15.00
```

输出：
```
┌──────────────┬────────┬────────┬──────────┬──────────┐
│ 股票         │ 现价   │ 涨跌   │ 成本     │ 盈亏     │
├──────────────┼────────┼────────┼──────────┼──────────┤
│ 示例股票A    │ 10.20  │ +0.50% │ 10.00    │ +2.0%    │
│ 示例股票B    │ 14.80  │ -0.30% │ 15.00    │ -1.3%    │
└──────────────┴────────┴────────┴──────────┴──────────┘
```

### 2. 市场主线追踪

```bash
python src/mainline_tracker.py
```

自动分析行业板块和概念板块，找出当日市场主线。

### 3. 大周期定位

```bash
python src/market_cycle.py
```

基于5月线系统判断当前市场处于哪个阶段：
- 🟢 牛市（>1.02）：仓位80-100%
- 🟡 结构性（1.00-1.02）：仓位60-80%
- 🟠 猴市（0.98-1.00）：仓位40-60%
- 🔴 熊市（<0.98）：仓位0-30%

### 4. 自动复盘报告

```bash
python src/daily_report.py --type daily    # 盘后复盘
python src/daily_report.py --type weekend  # 周末深度
python src/daily_report.py --type morning  # 盘前策略
```

### 5. 定时任务

```bash
# 每天下午3:30自动生成复盘报告
python src/scheduler.py --schedule "30 15 * * 1-5" --task daily_report
```

---

## 📁 项目结构

```
stock-insight/
├── src/
│   ├── stock_monitor.py      # 持仓监控
│   ├── market_overview.py    # 大盘概览
│   ├── mainline_tracker.py   # 主线追踪
│   ├── market_cycle.py       # 大周期定位
│   ├── daily_report.py       # 复盘报告生成
│   ├── data_fetcher.py       # 数据获取（腾讯/东方财富API）
│   └── scheduler.py          # 定时任务
├── scripts/
│   └── xueqiu_content_generator.py  # 雪球内容生成
├── config/
│   └── portfolio.yaml        # 持仓配置
├── docs/
│   └── investment_system.md  # 投资体系说明
├── examples/
│   └── sample_report.md      # 示例报告
├── requirements.txt
└── README.md
```

---

## ⚙️ 配置说明

编辑 `config/portfolio.yaml` 配置你的持仓：

```yaml
portfolio:
  - name: 示例股票A
    code: "600000"
    market: sh
    shares: 1000
    cost: 10.00
  - name: 示例股票B
    code: "000001"
    market: sh
    shares: 500
    cost: 15.00

settings:
  stop_loss_warn: -5      # 预警线
  stop_loss_cut: -10      # 减仓线
  stop_loss_clear: -20    # 清仓线
  max_single: 0.4         # 单只最大仓位
```

---

## 📊 投资体系

本系统基于"弱弱投资体系"构建，核心原则：

1. **市值最重要** — 一切围绕市值复利
2. **5月线定牛熊** — 大于1.02为牛市，小于0.98为熊市
3. **市值止损** — 回撤3%降半仓，回撤5%清仓
4. **主线优先** — 跟随市场主线，不和股票谈恋爱
5. **小资金策略** — 单只≤30-40%，集中火力复利增长

详见 [投资体系文档](docs/investment_system.md)

---

## 🤝 参与贡献

欢迎提Issue和PR！

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/xxx`
3. 提交更改：`git commit -m 'Add xxx'`
4. 推送分支：`git push origin feature/xxx`
5. 提交 Pull Request

---

## 📄 开源协议

MIT License

---

## ⚠️ 免责声明

本项目仅供学习交流，**不构成任何投资建议**。股市有风险，投资需谨慎。使用者需自行承担投资风险。

---

<p align="center">
  如果觉得有用，请给个 ⭐ Star 支持一下！
</p>

---

## ☕ 请作者喝杯咖啡

如果这个项目对你有帮助，欢迎请作者喝杯咖啡 ☕

<p align="center">
  <img src="assets/wechat_pay.jpg" width="200" alt="微信赞赏码" />
</p>
<p align="center">
  <strong>微信扫码赞赏</strong>
</p>
