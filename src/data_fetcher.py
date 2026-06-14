"""
Stock Insight - A股数据获取模块
使用腾讯/东方财富免费API，无需任何Key
"""

import requests
import json
from typing import Dict, List, Optional
from dataclasses import dataclass

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# ============ 数据结构 ============

@dataclass
class StockQuote:
    """个股行情"""
    name: str
    code: str
    price: float
    prev_close: float
    open: float
    high: float
    low: float
    change: float
    change_pct: float
    volume: int
    amount: float

@dataclass
class IndexQuote:
    """指数行情"""
    name: str
    code: str
    price: float
    change: float
    change_pct: float
    high: float
    low: float

@dataclass
class SectorData:
    """板块数据"""
    name: str
    change_pct: float


# ============ 腾讯API（稳定可靠）============

def get_stock_quote(code: str, market: str = 'sh') -> Optional[StockQuote]:
    """获取个股实时行情
    
    Args:
        code: 股票代码，如 '600089'
        market: 市场，'sh' 或 'sz'
    
    Returns:
        StockQuote 对象，失败返回 None
    """
    symbol = f"{market}{code}"
    try:
        r = requests.get(f'https://qt.gtimg.cn/q={symbol}', headers=HEADERS, timeout=15)
        parts = r.text.split('~')
        if len(parts) < 35:
            return None
        
        return StockQuote(
            name=parts[1],
            code=code,
            price=float(parts[3]),
            prev_close=float(parts[4]),
            open=float(parts[5]),
            high=float(parts[33]),
            low=float(parts[34]),
            change=float(parts[31]),
            change_pct=float(parts[32]),
            volume=int(parts[36]) if parts[36] else 0,
            amount=float(parts[37]) if parts[37] else 0,
        )
    except Exception as e:
        print(f"获取 {code} 行情失败: {e}")
        return None


def get_index_quote(symbol: str) -> Optional[IndexQuote]:
    """获取指数行情
    
    Args:
        symbol: 指数代码，如 'sh000001' (上证), 'sz399001' (深证), 'sz399006' (创业板)
    
    Returns:
        IndexQuote 对象
    """
    try:
        r = requests.get(f'https://qt.gtimg.cn/q={symbol}', headers=HEADERS, timeout=15)
        parts = r.text.split('~')
        if len(parts) < 35:
            return None
        
        return IndexQuote(
            name=parts[1],
            code=parts[2],
            price=float(parts[3]),
            change=float(parts[31]),
            change_pct=float(parts[32]),
            high=float(parts[33]),
            low=float(parts[34]),
        )
    except Exception as e:
        print(f"获取指数 {symbol} 失败: {e}")
        return None


def get_market_indices() -> Dict[str, IndexQuote]:
    """获取三大指数"""
    indices = {}
    for name, symbol in [('上证指数', 'sh000001'), ('深证成指', 'sz399001'), ('创业板指', 'sz399006')]:
        q = get_index_quote(symbol)
        if q:
            indices[name] = q
    return indices


# ============ 东方财富API（板块数据）============

def get_sector_data(top_n: int = 15) -> List[SectorData]:
    """获取行业板块涨幅排名
    
    Args:
        top_n: 返回前N个板块
    
    Returns:
        SectorData 列表
    """
    url = f"https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz={top_n}&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:90+t:2&fields=f2,f3,f4,f12,f14"
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        data = r.json()
        sectors = []
        for s in data.get('data', {}).get('diff', []):
            sectors.append(SectorData(
                name=s.get('f14', ''),
                change_pct=s.get('f3', 0),
            ))
        return sectors
    except Exception as e:
        print(f"获取板块数据失败: {e}")
        return []


def get_concept_data(top_n: int = 15) -> List[SectorData]:
    """获取概念板块涨幅排名"""
    url = f"https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz={top_n}&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:90+t:3&fields=f2,f3,f4,f12,f14"
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        data = r.json()
        concepts = []
        for c in data.get('data', {}).get('diff', []):
            concepts.append(SectorData(
                name=c.get('f14', ''),
                change_pct=c.get('f3', 0),
            ))
        return concepts
    except Exception as e:
        print(f"获取概念数据失败: {e}")
        return []


# ============ 工具函数 ============

def format_money(amount: float) -> str:
    """格式化金额"""
    if amount >= 1e8:
        return f"{amount/1e8:.1f}亿"
    elif amount >= 1e4:
        return f"{amount/1e4:.1f}万"
    else:
        return f"{amount:.0f}"


def format_pct(pct: float) -> str:
    """格式化百分比"""
    if pct > 0:
        return f"+{pct:.2f}%"
    else:
        return f"{pct:.2f}%"


if __name__ == '__main__':
    # 测试
    print("=== 大盘指数 ===")
    for name, idx in get_market_indices().items():
        print(f"  {name}: {idx.price} ({format_pct(idx.change_pct)})")
    
    print("\n=== 行业板块 TOP10 ===")
    for s in get_sector_data(10):
        print(f"  {s.name}: {format_pct(s.change_pct)}")
