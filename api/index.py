from flask import Flask, jsonify
from api.analyzer import InvestmentPerformanceAnalyzer, generate_sample_data

app = Flask(__name__)

# 初始化分析器（使用示例数据）
sample_data = generate_sample_data()
analyzer = InvestmentPerformanceAnalyzer(sample_data, risk_free_rate=0.015)
analyzer.calculate_performance_metrics()

@app.route('/api/data')
def get_data():
    """获取净值数据"""
    if analyzer.data is None:
        return jsonify({'error': '数据未加载'}), 500

    # 转换数据为JSON格式
    data = {
        'dates': analyzer.data['统计日期'].dt.strftime('%Y-%m-%d').tolist(),
        'nav': analyzer.data['归一化净值'].tolist(),
        'drawdown': (analyzer.data['回撤'] * 100).tolist(),
        'cumulative_return': (analyzer.data['累计收益率'] * 100).tolist()
    }
    return jsonify(data)

@app.route('/api/metrics')
def get_metrics():
    """获取业绩指标"""
    if not analyzer.results:
        return jsonify({'error': '指标未计算'}), 500

    # 准备指标数据
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

@app.route('/api/summary')
def get_summary():
    """获取概览信息"""
    if analyzer.data is None:
        return jsonify({'error': '数据未加载'}), 500

    latest_metrics = analyzer.results.get('成立以来', {})

    summary = {
        'latest_nav': f"{analyzer.data['归一化净值'].iloc[-1]:.4f}",
        'latest_date': analyzer.data['统计日期'].iloc[-1].strftime('%Y-%m-%d'),
        'start_date': analyzer.data['统计日期'].iloc[0].strftime('%Y-%m-%d'),
        'total_days': len(analyzer.data),
        'total_return': f"{latest_metrics.get('总收益率', 0):.2%}",
        'annual_return': f"{latest_metrics.get('年化收益率', 0):.2%}",
        'sharpe_ratio': f"{latest_metrics.get('夏普比率', 0):.2f}",
        'max_drawdown': f"{latest_metrics.get('最大回撤', 0):.2%}",
        'risk_free_rate': f"{analyzer.risk_free_rate:.2%}"
    }

    return jsonify(summary)

# Vercel 需要这个处理函数
def handler(request):
    return app(request)
