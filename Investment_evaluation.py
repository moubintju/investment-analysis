import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import warnings
import matplotlib

warnings.filterwarnings('ignore')
matplotlib.rcParams['font.family'] = 'simHei'
matplotlib.rcParams['font.sans-serif'] = 'simHei'
plt.rcParams['axes.unicode_minus'] = False

class InvestmentPerformanceAnalyzer:
    def __init__(self, data_file, risk_free_rate=0.02, chart_title="投资组合净值曲线"):
        """
        初始化分析器
        
        参数:
        data_file: Excel文件路径
        risk_free_rate: 无风险年化收益率 (默认2%)
        chart_title: 图表标题
        """
        self.data_file = data_file
        self.risk_free_rate = risk_free_rate
        self.chart_title = chart_title
        self.data = None
        self.results = {}
        self.days_trade =251 # 年交易日数
        
    def load_data(self):
        """加载并预处理数据"""
        try:
            # 读取Excel文件
            self.data = pd.read_excel(self.data_file, sheet_name='单元资产2025')
            
            # 确保日期列是datetime类型
            self.data['统计日期'] = pd.to_datetime(self.data['统计日期'])
            
            # 按日期排序
            self.data = self.data.sort_values('统计日期').reset_index(drop=True)
            
            print(f"数据加载成功，共{len(self.data)}条记录")
            print(f"数据时间范围: {self.data['统计日期'].min()} 到 {self.data['统计日期'].max()}")
            
        except Exception as e:
            print(f"数据加载失败: {e}")
            return False
        return True
    
    def calculate_performance_metrics(self):
        """计算业绩指标"""
        if self.data is None:
            print("请先加载数据")
            return
        
        # 计算归一化净值 (起始值为1)
        initial_nav = self.data['单元资产净值(净价)'].iloc[0]
        self.data['归一化净值'] = self.data['单元资产净值(净价)'] / initial_nav
        
        # 计算每日收益率
        self.data['日收益率'] = self.data['归一化净值'].pct_change()
        
        # 计算累计收益率
        self.data['累计收益率'] = self.data['归一化净值'] - 1
        
        # 计算滚动最大净值 (用于计算回撤)
        self.data['滚动最大净值'] = self.data['归一化净值'].expanding().max()
        
        # 计算最大回撤率
        self.data['回撤'] = (self.data['归一化净值'] - self.data['滚动最大净值']) / self.data['滚动最大净值']
        
        # 计算关键投资评估指标 夏普比率、卡玛比率，总收益率等
        self.calculate_key_metrics()
        
        # 计算不同时间段的指标
        self.calculate_period_metrics()
        
    def calculate_key_metrics(self):
        """计算关键业绩指标"""
        total_days = len(self.data)
        trading_days_per_year = self.days_trade  # 年交易日数
        
        # 总收益率
        total_return = self.data['归一化净值'].iloc[-1] - 1
        
        # 年化收益率
        years = total_days / trading_days_per_year
        annual_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
        
        # 年化波动率
        daily_volatility = self.data['日收益率'].std()
        annual_volatility = daily_volatility * np.sqrt(trading_days_per_year)
        
        # 夏普比率
        sharpe_ratio = (annual_return - self.risk_free_rate) / annual_volatility if annual_volatility > 0 else 0
        
        # 最大回撤
        max_drawdown = self.data['回撤'].min()
        
        # 卡玛比率 (年化收益 / 最大回撤绝对值)
        calmar_ratio = annual_return / abs(max_drawdown) if max_drawdown != 0 else 0
        
        # 保存结果
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
        """计算不同时间段的业绩指标"""
        if len(self.data) == 0:
            print("请先加载数据")
            return
            
        end_date = self.data['统计日期'].max()
        trading_days_per_year = self.days_trade # 年交易日数
        
        # 定义时间段
        periods = {
            '近三个月': timedelta(days=90),
            '近半年': timedelta(days=180),
            '近一年': timedelta(days=365),
            '近三年': timedelta(days=1095),
            '成立以来': timedelta(days=365*10)  # 足够长的时间
        }
        
        for period_name, delta in periods.items():
            start_date = end_date - delta
            period_data = self.data[self.data['统计日期'] >= start_date]
            
            if len(period_data) < 2:  # 至少需要2个数据点
                continue
                
            # 计算该时间段的指标
            # 区间收益率
            period_return = period_data['归一化净值'].iloc[-1] / period_data['归一化净值'].iloc[0] - 1
            # 区间有数
            period_days = len(period_data)
            # 区间天数转换为年数
            period_years = period_days / trading_days_per_year
            # 年收益率
            annual_return = (1 + period_return) ** (1 / period_years) - 1 if period_years > 0 else 0
            # 波动率
            daily_volatility = period_data['日收益率'].std()
            annual_volatility = daily_volatility * np.sqrt(trading_days_per_year)
            # 夏普比率
            sharpe_ratio = (annual_return - self.risk_free_rate) / annual_volatility if annual_volatility > 0 else 0
            # 最大回撤
            max_drawdown = period_data['回撤'].min()
            # 卡玛比率
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
    
    def create_performance_chart(self):
        """创建业绩图表"""
        if self.data is None:
            print("请先加载数据并计算指标")
            return
        
        # 创建图表，调整布局为三个部分：净值图、回撤图、指标表格
        fig = plt.figure(figsize=(15, 14))
        gs = plt.GridSpec(3, 1, height_ratios=[3, 1, 1.5])
        
        ax1 = plt.subplot(gs[0])  # 净值图
        ax2 = plt.subplot(gs[1])  # 回撤图
        ax_table = plt.subplot(gs[2])  # 指标表格
        
        # 净值曲线
        ax1.plot(self.data['统计日期'], self.data['归一化净值'], 
                linewidth=2, color='#1f77b4', label='净值曲线')
        
        # 标记最后一个点的数值
        last_date = self.data['统计日期'].iloc[-1]
        last_value = self.data['归一化净值'].iloc[-1]
        ax1.plot(last_date, last_value, 'ro', markersize=8)
        ax1.annotate(f'{last_value:.3f}', 
                    xy=(last_date, last_value),
                    xytext=(10, 10), textcoords='offset points',
                    fontsize=12, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        ax1_chart_title = self.chart_title + ' 截止日期：' + self.data['统计日期'].max().strftime('%Y-%m-%d')
        ax1.set_title(ax1_chart_title, fontsize=16, fontweight='bold')
        ax1.set_ylabel('净值', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # 设置x轴格式
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        
        # 回撤图
        ax2.fill_between(self.data['统计日期'], self.data['回撤']*100, 0, 
                        alpha=0.3, color='red', label='回撤')
        ax2.plot(self.data['统计日期'], self.data['回撤']*100, 
                linewidth=1, color='red', alpha=0.8)
        ax2.set_ylabel('回撤 (%)', fontsize=12)
        ax2.set_xlabel('日期', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # 在图表下方添加指标表格
        self._add_metrics_table(ax_table)
        
        plt.tight_layout()
        return fig
    
    def _add_metrics_table(self, ax_table):
        """在图表下方添加指标表格"""
        # 确定可用的时间段 - 按时间从短到长排序
        all_periods = ['近三个月', '近半年', '近一年', '近三年', '成立以来']
        available_periods = []
        
        for period in all_periods:
            if period in self.results:
                available_periods.append(period)
        
        if not available_periods:
            ax_table.axis('off')
            ax_table.text(0.5, 0.5, '无足够数据计算指标', 
                         ha='center', va='center', transform=ax_table.transAxes)
            return
        
        # 准备表格数据
        table_data = []
        columns = ['时间段', '总收益率', '年化收益率', '年化波动率', 
                  '夏普比率', '最大回撤', '卡玛比率']
        
        for period in available_periods:
            metrics = self.results[period]
            row = [
                period,
                f"{metrics['总收益率']:.2%}",
                f"{metrics['年化收益率']:.2%}",
                f"{metrics['年化波动率']:.2%}",
                f"{metrics['夏普比率']:.2f}",
                f"{metrics['最大回撤']:.2%}",
                f"{metrics['卡玛比率']:.2f}"
            ]
            table_data.append(row)
        
        # 创建表格
        ax_table.axis('off')
        table = ax_table.table(cellText=table_data,
                              colLabels=columns,
                              cellLoc='center',
                              loc='center',
                              bbox=[0, 0, 1, 1])
        
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.8)
        
        # 设置表头样式
        for i in range(len(columns)):
            table[(0, i)].set_facecolor('#4C72B0')
            table[(0, i)].set_text_props(weight='bold', color='white')
    
    def save_results(self, output_excel="投资业绩分析结果.xlsx", 
                    chart_png="净值曲线.png", chart_html="净值曲线.html"):
        """保存分析结果"""
        if self.data is None:
            print("请先加载数据并计算指标")
            return
        
        # 保存图表
        fig = self.create_performance_chart()
        fig.savefig(chart_png, dpi=300, bbox_inches='tight')
        print(f"图表已保存为: {chart_png}")
        
        # 保存为HTML (使用plotly)
        try:
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            import plotly.offline as pyo
            
            # 确定可用的时间段
            all_periods = ['近三个月', '近半年', '近一年', '近三年', '成立以来']
            available_periods = [p for p in all_periods if p in self.results]
            
            # 创建Plotly图表 - 使用3个子图
            fig_plotly = make_subplots(
                rows=3, cols=1,
                subplot_titles=(self.chart_title, "回撤", "业绩指标"),
                vertical_spacing=0.08,
                row_heights=[0.5, 0.2, 0.3],
                specs=[
                    [{"type": "scatter"}],
                    [{"type": "scatter"}],
                    [{"type": "table"}]
                ]
            )
            
            # 净值曲线
            fig_plotly.add_trace(
                go.Scatter(
                    x=self.data['统计日期'], 
                    y=self.data['归一化净值'],
                    name='净值曲线', 
                    line=dict(color='#1f77b4', width=2),
                    hovertemplate='日期: %{x}<br>净值: %{y:.3f}<extra></extra>'
                ),
                row=1, col=1
            )
            
            # 标记最后一个点
            last_date = self.data['统计日期'].iloc[-1]
            last_value = self.data['归一化净值'].iloc[-1]
            fig_plotly.add_trace(
                go.Scatter(
                    x=[last_date], 
                    y=[last_value],
                    mode='markers+text',
                    marker=dict(size=12, color='red'),
                    text=[f'最新净值: {last_value:.3f}'],
                    textposition="top center",
                    showlegend=False,
                    hovertemplate=f'最新净值: {last_value:.3f}<extra></extra>'
                ),
                row=1, col=1
            )
            
            # 回撤图
            fig_plotly.add_trace(
                go.Scatter(
                    x=self.data['统计日期'], 
                    y=self.data['回撤']*100,
                    name='回撤', 
                    fill='tozeroy', 
                    line=dict(color='red', width=1),
                    hovertemplate='日期: %{x}<br>回撤: %{y:.2f}%<extra></extra>'
                ),
                row=2, col=1
            )
            
            # 添加指标表格
            if available_periods:
                # 准备表格数据
                header_values = ['时间段', '总收益率', '年化收益率', '年化波动率', '夏普比率', '最大回撤', '卡玛比率']
                cell_values = [[] for _ in range(len(header_values))]
                
                for period in available_periods:
                    metrics = self.results[period]
                    cell_values[0].append(period)
                    cell_values[1].append(f"{metrics['总收益率']:.2%}")
                    cell_values[2].append(f"{metrics['年化收益率']:.2%}")
                    cell_values[3].append(f"{metrics['年化波动率']:.2%}")
                    cell_values[4].append(f"{metrics['夏普比率']:.2f}")
                    cell_values[5].append(f"{metrics['最大回撤']:.2%}")
                    cell_values[6].append(f"{metrics['卡玛比率']:.2f}")
                
                # 添加表格
                fig_plotly.add_trace(
                    go.Table(
                        header=dict(
                            values=header_values,
                            fill_color='#4C72B0',
                            align='center',
                            font=dict(color='white', size=12)
                        ),
                        cells=dict(
                            values=cell_values,
                            fill_color='white',
                            align='center',
                            font=dict(size=11)
                        )
                    ),
                    row=3, col=1
                )
            
            # 更新布局
            fig_plotly.update_layout(
                height=1000,
                showlegend=True,
                title_text=f"{self.chart_title} (无风险利率: {self.risk_free_rate:.2%})",
                title_x=0.5
            )
            
            # 更新子图标题位置
            fig_plotly.update_annotations(font_size=14)
            
            # 保存HTML文件
            pyo.plot(fig_plotly, filename=chart_html, auto_open=False)
            print(f"HTML图表已保存为: {chart_html}")
            
        except ImportError:
            print("Plotly未安装，无法生成HTML图表")
        
        # 保存Excel结果
        with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
            # 保存原始数据（含计算列）
            self.data.to_excel(writer, sheet_name='分析数据', index=False)
            
            # 保存指标汇总
            metrics_summary = []
            all_periods = ['近三个月', '近半年', '近一年', '近三年', '成立以来']
            for period in all_periods:
                if period in self.results:
                    metrics = self.results[period]
                    row = {
                        '时间段': period,
                        '总收益率': f"{metrics['总收益率']:.4%}",
                        '年化收益率': f"{metrics['年化收益率']:.4%}",
                        '年化波动率': f"{metrics['年化波动率']:.4%}",
                        '夏普比率': f"{metrics['夏普比率']:.4f}",
                        '最大回撤': f"{metrics['最大回撤']:.4%}",
                        '卡玛比率': f"{metrics['卡玛比率']:.4f}",
                        '数据天数': metrics['数据天数']
                    }
                    if '开始日期' in metrics:
                        row['开始日期'] = metrics['开始日期'].strftime('%Y-%m-%d')
                    metrics_summary.append(row)
            
            pd.DataFrame(metrics_summary).to_excel(writer, sheet_name='业绩指标', index=False)
            
            # 保存详细计算
            calculation_details = {
                '参数': ['无风险利率', '年交易日数', '数据起始日期', '数据结束日期', '总数据点数'],
                '数值': [
                    f"{self.risk_free_rate:.2%}",
                    self.days_trade,
                    self.data['统计日期'].min().strftime('%Y-%m-%d'),
                    self.data['统计日期'].max().strftime('%Y-%m-%d'),
                    len(self.data)
                ]
            }
            pd.DataFrame(calculation_details).to_excel(writer, sheet_name='计算参数', index=False)
        
        print(f"分析结果已保存为: {output_excel}")
        plt.close('all')

# 使用示例
def main():
    # 初始化分析器 (您可以修改这些参数)
    analyzer = InvestmentPerformanceAnalyzer(
        data_file="林相宜单元资产.xlsx",
        risk_free_rate=0.015,  # 无风险利率，可以修改
        chart_title="林相宜-投资业绩分析"  # 图表标题，可以修改
    )
    
    # 加载数据
    if analyzer.load_data():
        # 计算业绩指标
        analyzer.calculate_performance_metrics()
        
        # 保存结果
        analyzer.save_results(
            output_excel="投资经理业绩评估/投资业绩分析报告.xlsx",
            chart_png="投资经理业绩评估/净值曲线图.png",
            chart_html="投资经理业绩评估/净值曲线图.html"
        )
        
        # 打印关键指标
        print("\n=== 关键业绩指标 ===")
        overall = analyzer.results.get('成立以来', {})
        if overall:
            print(f"总收益率: {overall['总收益率']:.2%}")
            print(f"年化收益率: {overall['年化收益率']:.2%}")
            print(f"年化波动率: {overall['年化波动率']:.2%}")
            print(f"夏普比率: {overall['夏普比率']:.2f}")
            print(f"最大回撤: {overall['最大回撤']:.2%}")
            print(f"卡玛比率: {overall['卡玛比率']:.2f}")

if __name__ == "__main__":
    main()