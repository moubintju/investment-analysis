from flask import Flask, render_template, jsonify, send_file
import pandas as pd
import json
from datetime import datetime
import os
import sys
import glob
from Investment_evaluation import InvestmentPerformanceAnalyzer

# 设置控制台编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'ignore')

app = Flask(__name__)

# 全局变量存储分析器实例
analyzer = None

def find_excel_file():
    """查找Excel文件"""
    # 在当前目录查找Excel文件
    excel_files = glob.glob("*.xlsx")
    if excel_files:
        return excel_files[0]

    # 在父目录查找
    excel_files = glob.glob("../*.xlsx")
    if excel_files:
        return excel_files[0]

    return None

def initialize_analyzer():
    """初始化分析器"""
    global analyzer

    # 查找Excel文件
    excel_file = find_excel_file()

    if excel_file is None:
        print("错误: 未找到Excel数据文件")
        print("请将包含投资数据的Excel文件放在当前目录下")
        return False

    print(f"找到数据文件: {excel_file}")

    try:
        analyzer = InvestmentPerformanceAnalyzer(
            data_file=excel_file,
            risk_free_rate=0.015,
            chart_title="投资业绩分析"
        )
        if analyzer.load_data():
            analyzer.calculate_performance_metrics()
            return True
    except Exception as e:
        print(f"初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    return False

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """获取净值数据"""
    if analyzer is None or analyzer.data is None:
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
    if analyzer is None or not analyzer.results:
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
    if analyzer is None or analyzer.data is None:
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

@app.route('/api/export/excel')
def export_excel():
    """导出Excel报告"""
    if analyzer is None:
        return jsonify({'error': '数据未加载'}), 500

    output_file = "投资业绩分析报告.xlsx"
    try:
        analyzer.save_results(
            output_excel=output_file,
            chart_png="净值曲线图.png",
            chart_html="净值曲线图.html"
        )
        return send_file(output_file, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("正在初始化投资业绩分析系统...")
    if initialize_analyzer():
        print("数据加载成功")
        print("指标计算完成")
        print("\n" + "="*50)
        print("服务已启动!")
        print("请在浏览器中访问: http://localhost:5000")
        print("="*50 + "\n")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("初始化失败，请检查数据文件是否存在")
