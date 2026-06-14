"""
Stock Insight - 大盘概览模块
展示三大指数 + 板块涨跌排名
"""

from data_fetcher import get_market_indices, get_sector_data, get_concept_data, format_pct


def show_market_overview() -> str:
    """生成大盘概览报告"""
    lines = []
    lines.append("📈 A股大盘概览")
    lines.append("=" * 50)
    
    # 三大指数
    indices = get_market_indices()
    for name, idx in indices.items():
        emoji = "🟢" if idx.change_pct > 0 else "🔴" if idx.change_pct < 0 else "⚪"
        lines.append(f"{emoji} {name}: {idx.price} ({format_pct(idx.change_pct)})")
    
    lines.append("")
    
    # 行业板块
    sectors = get_sector_data(10)
    if sectors:
        lines.append("🔥 行业板块 TOP10")
        lines.append("-" * 30)
        for i, s in enumerate(sectors, 1):
            emoji = "🔴" if s.change_pct > 3 else "🟠" if s.change_pct > 1 else "🟡"
            lines.append(f"  {i:>2}. {s.name:<12} {emoji} {format_pct(s.change_pct)}")
    
    lines.append("")
    
    # 概念板块
    concepts = get_concept_data(10)
    if concepts:
        lines.append("💡 概念板块 TOP10")
        lines.append("-" * 30)
        for i, c in enumerate(concepts, 1):
            emoji = "🔴" if c.change_pct > 3 else "🟠" if c.change_pct > 1 else "🟡"
            lines.append(f"  {i:>2}. {c.name:<12} {emoji} {format_pct(c.change_pct)}")
    
    lines.append("=" * 50)
    return "\n".join(lines)


if __name__ == '__main__':
    print(show_market_overview())
