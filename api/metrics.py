from flask import Flask, jsonify
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

app = Flask(__name__)

def generate_sample_data():
    np.random.seed(42)
    start_date = datetime(2024, 1, 1)
    days = 250
    dates = [start_date + timedelta(days=i) for i in range(days)]
    initial_nav = 1.0
    daily_returns = np.random.normal(0.0005, 0.01, days)
    nav_values = [initial_nav]
    for ret in daily_returns[1:]:
        nav_values.append(nav_values[-1] * (1 + ret))
    return pd.DataFrame({
        '统计日期': dates,
        '单元资产净值(净价)': nav_values
    })

class InvestmentPerformanceAnalyzer:
    def __init__(self, data, risk_free_rate=0.015):
        self.risk_free_rate = risk_free_rate
        self.data = data
        self.results = {}
        self.days_trade = 251

    def calculate_performance_metrics(self):
        if self.data is None or len(self.data) == 0:
            return
        initial_nav = self.data['单元资产净值(净价)'].iloc[0]
        self.data['归一化净值'] = self.data['单元资产净值(净价)'] / initial_nav
        self.data['日收益率'] = self.data['归一化净值'].pct_change()
        self.data['累计收益率'] = self.data['归一化净值'] - 1
        self.data['滚动最大净值'] = self.data['归一化净值'].expanding().max()
        self.data['回撤'] = (self.data['归一化净值'] - self.data['滚动最大净值']) / self.data['滚动最大净值']
        self.calculate_key_metrics()
        self.calculate_period_metrics()

    def calculate_key_metrics(self):
        total_days = len(self.data)
        trading_days_per_year = self.days_trade
        total_return = self.data['归一化净值'].iloc[-1] - 1
        years = total_days / trading_days_per_year
        annual_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
        daily_volatility = self.data['日收益率'].std()
        annual_volatility = daily_volatility * np.sqrt(trading_days_per_year)
        sharpe_ratio = (annual_return - self.risk_free_rate) / annual_volatility if annual_volatility > 0 else 0
        max_drawdown = self.data['回撤'].min()
        calmar_ratio = annual_return / abs(max_drawdown) if max_drawdown != 0 else 0
        self.results['总体指标'] = {
            '总收益率': total_return,
            '年化收益率': annual_return,
            '年化波动率': annual_volatility,
            '夏普比率': sharpe_ratio,
            '最大回撤': max_drawdown,
            '卡玛比率': calmar_ratio,
            '数据天数': total_days
        }

    def calculate_period_metrics(self):
        if len(self.data) == 0:
            return
        end_date = self.data['统计日期'].max()
        trading_days_per_year = self.days_trade
        periods = {
            '近三个月': timedelta(days=90),
            '近半年': timedelta(days=180),
            '近一年': timedelta(days=365),
            '近三年': timedelta(days=1095),
            '成立以来': timedelta(days=365*10)
        }
        for period_name, delta in periods.items():
            start_date = end_date - delta
            period_data = self.data[self.data['统计日期'] >= start_date]
            if len(period_data) < 2:
                continue
            period_return = period_data['归一化净值'].iloc[-1] / period_data['归一化净值'].iloc[0] - 1
            period_days = len(period_data)
            period_years = period_days / trading_days_per_year
            annual_return = (1 + period_return) ** (1 / period_years) - 1 if period_years > 0 else 0
            daily_volatility = period_data['日收益率'].std()
            annual_volatility = daily_volatility * np.sqrt(trading_days_per_year)
            sharpe_ratio = (annual_return - self.risk_free_rate) / annual_volatility if annual_volatility > 0 else 0
            max_drawdown = period_data['回撤'].min()
            calmar_ratio = annual_return / abs(max_drawdown) if max_drawdown != 0 else 0
            self.results[period_name] = {
                '总收益率': period_return,
                '年化收益率': annual_return,
                '年化波动率': annual_volatility,
                '夏普比率': sharpe_ratio,
                '最大回撤': max_drawdown,
                '卡玛比率': calmar_ratio,
                '数据天数': period_days,
                '开始日期': period_data['统计日期'].min()
            }

sample_data = generate_sample_data()
analyzer = InvestmentPerformanceAnalyzer(sample_data, risk_free_rate=0.015)
analyzer.calculate_performance_metrics()

@app.route('/api/metrics')
def get_metrics():
    if not analyzer.results:
        return jsonify({'error': '指标未计算'}), 500

    metrics_data = []
    all_periods = ['近三个月', '近半年', '近一年', '近三年', '成立以来']

    for period in all_periods:
        if period in analyzer.results:
            metrics = analyzer.results[period]
            metrics_data.append({
                'period': period,
                'total_return': f"{metrics['总收益率']:.2%}",
                'annual_return': f"{metrics['年化收益率']:.2%}",
                'annual_volatility': f"{metrics['年化波动率']:.2%}",
                'sharpe_ratio': f"{metrics['夏普比率']:.2f}",
                'max_drawdown': f"{metrics['最大回撤']:.2%}",
                'calmar_ratio': f"{metrics['卡玛比率']:.2f}",
                'days': metrics['数据天数']
            })

    return jsonify(metrics_data)
