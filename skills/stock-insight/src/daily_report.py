"""
Stock Insight - 每日复盘报告生成器
整合所有模块，生成完整的投资分析报告
"""

import argparse
import os
import sys
from datetime import datetime

# 添加src目录到path
sys.path.insert(0, os.path.dirname(__file__))

from data_fetcher import get_market_indices, get_sector_data, get_concept_data, format_pct
from stock_monitor import load_portfolio, monitor_stocks


def generate_daily_report(portfolio: list = None) -> str:
    """生成盘后复盘报告"""
    now = datetime.now()
    date_str = now.strftime('%Y年%m月%d日')
    
    lines = []
    lines.append(f"# {date_str} 盘后复盘")
    lines.append("")
    lines.append("> Stock Insight · 自动复盘报告")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # 一、市场数据
    lines.append("## 一、今日市场")
    lines.append("")
    indices = get_market_indices()
    for name, idx in indices.items():
        emoji = "🟢" if idx.change_pct > 0 else "🔴"
        lines.append(f"- {emoji} **{name}**: {idx.price} ({format_pct(idx.change_pct)})")
    lines.append("")
    
    # 二、板块主线
    lines.append("## 二、板块主线")
    lines.append("")
    sectors = get_sector_data(5)
    if sectors:
        lines.append("**行业涨幅TOP5：**")
        for i, s in enumerate(sectors, 1):
            lines.append(f"{i}. {s.name}: {format_pct(s.change_pct)}")
        lines.append("")
    
    concepts = get_concept_data(5)
    if concepts:
        lines.append("**概念涨幅TOP5：**")
        for i, c in enumerate(concepts, 1):
            lines.append(f"{i}. {c.name}: {format_pct(c.change_pct)}")
        lines.append("")
    
    # 三、持仓复盘
    if portfolio:
        lines.append("## 三、持仓复盘")
        lines.append("")
        for stock in portfolio:
            code = stock['code']
            market = stock.get('market', 'sh')
            name = stock.get('name', code)
            cost = stock.get('cost', 0)
            
            from data_fetcher import get_stock_quote
            quote = get_stock_quote(code, market)
            if quote:
                pnl = (quote.price - cost) / cost * 100 if cost > 0 else 0
                lines.append(f"**{name}** ({code})")
                lines.append(f"- 现价: {quote.price}，涨跌: {format_pct(quote.change_pct)}")
                if cost > 0:
                    lines.append(f"- 成本: {cost}，盈亏: {format_pct(pnl)}")
                lines.append("")
    
    # 四、操作建议
    lines.append("## 四、操作建议")
    lines.append("")
    lines.append("*（请根据自身判断操作，本报告仅供参考）*")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*自动生成 by Stock Insight · 不构成投资建议*")
    
    return "\n".join(lines)


def generate_weekend_report(portfolio: list = None) -> str:
    """生成周末深度复盘"""
    report = generate_daily_report(portfolio)
    # 周末版本加更多分析内容
    report = report.replace("盘后复盘", "周末深度复盘")
    return report


def save_report(content: str, report_type: str = 'daily') -> str:
    """保存报告到文件"""
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    date_str = datetime.now().strftime('%Y%m%d')
    filename = f"{date_str}_{report_type}.md"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath


def main():
    parser = argparse.ArgumentParser(description='生成投资复盘报告')
    parser.add_argument('--type', choices=['daily', 'weekend', 'morning'], default='daily')
    parser.add_argument('--config', help='持仓配置文件路径')
    parser.add_argument('--output', help='输出文件路径')
    args = parser.parse_args()
    
    # 加载持仓
    portfolio = load_portfolio(args.config)
    
    # 生成报告
    if args.type == 'daily':
        content = generate_daily_report(portfolio)
    elif args.type == 'weekend':
        content = generate_weekend_report(portfolio)
    else:
        content = generate_daily_report(portfolio)
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"报告已保存到: {args.output}")
    else:
        filepath = save_report(content, args.type)
        print(f"报告已保存到: {filepath}")
        print()
        print(content)


if __name__ == '__main__':
    main()
