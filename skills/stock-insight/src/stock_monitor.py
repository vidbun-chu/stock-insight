"""
Stock Insight - 持仓监控模块
实时获取持仓股行情，计算盈亏，发出预警
"""

import argparse
import yaml
import os
from data_fetcher import get_stock_quote, format_pct


def load_portfolio(config_path: str = None) -> list:
    """加载持仓配置"""
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'portfolio.yaml')
    
    if not os.path.exists(config_path):
        return []
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config.get('portfolio', [])


def monitor_stocks(stocks: list, costs: list = None) -> str:
    """监控持仓股并生成报告
    
    Args:
        stocks: 股票列表 [(code, market, name), ...] 或从配置加载
        costs: 成本价列表（可选）
    
    Returns:
        格式化的监控报告
    """
    if not stocks:
        return "⚠️ 没有配置持仓股"
    
    lines = []
    lines.append("📊 持仓监控报告")
    lines.append("=" * 50)
    lines.append(f"{'股票':<10} {'现价':>8} {'涨跌':>8} {'成本':>8} {'盈亏':>8}")
    lines.append("-" * 50)
    
    for i, stock in enumerate(stocks):
        if isinstance(stock, dict):
            code = stock['code']
            market = stock.get('market', 'sh')
            name = stock.get('name', code)
            cost = stock.get('cost', 0)
        else:
            code, market, name = stock
            cost = costs[i] if costs and i < len(costs) else 0
        
        quote = get_stock_quote(code, market)
        if not quote:
            lines.append(f"{name:<10} {'获取失败':>8}")
            continue
        
        pnl_str = ""
        if cost > 0:
            pnl = (quote.price - cost) / cost * 100
            pnl_str = format_pct(pnl)
            
            # 预警判断
            if pnl <= -20:
                pnl_str += " 🔴清仓!"
            elif pnl <= -10:
                pnl_str += " 🟠减仓!"
            elif pnl <= -5:
                pnl_str += " 🟡预警"
        
        lines.append(f"{name:<10} {quote.price:>8.2f} {format_pct(quote.change_pct):>8} {cost:>8.2f} {pnl_str:>8}")
    
    lines.append("=" * 50)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='A股持仓监控')
    parser.add_argument('--stock', nargs='+', help='股票代码列表')
    parser.add_argument('--cost', nargs='+', type=float, help='成本价列表')
    parser.add_argument('--market', default='sh', help='市场 (sh/sz)')
    parser.add_argument('--config', help='配置文件路径')
    args = parser.parse_args()
    
    if args.config or not args.stock:
        # 从配置文件加载
        portfolio = load_portfolio(args.config)
        if portfolio:
            print(monitor_stocks(portfolio))
        else:
            print("⚠️ 没有配置持仓股，请编辑 config/portfolio.yaml 或用 --stock 参数指定")
    else:
        # 从命令行参数
        stocks = []
        for code in args.stock:
            market = 'sz' if code.startswith(('0', '3')) else 'sh'
            stocks.append((code, market, code))
        print(monitor_stocks(stocks, args.cost))


if __name__ == '__main__':
    main()
