"""
Stock Insight - 大周期定位模块
基于5月线系统判断牛熊周期
"""

from data_fetcher import get_index_quote, format_pct


def get_market_cycle() -> dict:
    """获取当前大周期定位
    
    基于上证指数与100日均线（≈5月线）的比值判断：
    - > 1.02: 牛市（仓位80-100%）
    - 1.00 ~ 1.02: 结构性行情（仓位60-80%）
    - 0.98 ~ 1.00: 猴市（仓位40-60%）
    - < 0.98: 熊市（仓位0-30%）
    """
    idx = get_index_quote('sh000001')
    if not idx:
        return {'error': '无法获取上证指数数据'}
    
    # 注意：这里用当前价格与前一日收盘的比值做简化判断
    # 完整版需要用100日均线数据
    # 实际使用时建议结合历史K线数据计算准确的5月线
    
    return {
        'index': '上证指数',
        'price': idx.price,
        'change_pct': idx.change_pct,
        'note': '完整大周期分析需要历史K线数据，建议配合 market_cycle.py 使用'
    }


def analyze_cycle_simple(price: float, ma5_monthly: float) -> dict:
    """简化版大周期分析
    
    Args:
        price: 当前价格
        ma5_monthly: 5月均线值
    
    Returns:
        分析结果字典
    """
    if ma5_monthly <= 0:
        return {'error': '5月线数据无效'}
    
    ratio = price / ma5_monthly
    
    if ratio > 1.02:
        cycle = '牛市'
        position = '80-100%'
        emoji = '🟢'
        advice = '积极参与，重仓主线'
    elif ratio > 1.00:
        cycle = '结构性行情'
        position = '60-80%'
        emoji = '🟡'
        advice = '跟随主线，控制仓位'
    elif ratio > 0.98:
        cycle = '猴市'
        position = '40-60%'
        emoji = '🟠'
        advice = '轻仓试探，快进快出'
    else:
        cycle = '熊市'
        position = '0-30%'
        emoji = '🔴'
        advice = '空仓观望，等待机会'
    
    return {
        'index_price': price,
        'ma5_monthly': round(ma5_monthly, 2),
        'ratio': round(ratio, 4),
        'cycle': cycle,
        'emoji': emoji,
        'suggested_position': position,
        'advice': advice,
    }


def format_cycle_report(result: dict) -> str:
    """格式化大周期报告"""
    if 'error' in result:
        return f"⚠️ {result['error']}"
    
    lines = []
    lines.append(f"{result['emoji']} 大周期定位：{result['cycle']}")
    lines.append(f"  上证指数: {result['index_price']}")
    lines.append(f"  5月均线:  {result['ma5_monthly']}")
    lines.append(f"  比值:     {result['ratio']}")
    lines.append(f"  建议仓位: {result['suggested_position']}")
    lines.append(f"  操作建议: {result['advice']}")
    return "\n".join(lines)


if __name__ == '__main__':
    # 示例：假设5月线在3900点
    demo = analyze_cycle_simple(4031.51, 3900)
    print(format_cycle_report(demo))
