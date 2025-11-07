# 投资业绩分析系统

一个基于 Flask 的投资组合业绩分析 Web 应用，提供交互式前端页面查看投资业绩指标。

## 功能特点

- 📊 **实时数据可视化** - 净值曲线、回撤图表
- 📈 **多维度指标分析** - 夏普比率、卡玛比率、最大回撤等
- 🎯 **多时间段对比** - 近三个月、半年、一年、三年、成立以来
- 💼 **Excel 报告导出** - 一键导出完整分析报告
- 🎨 **现代化界面** - 响应式设计，支持移动端访问

## 安装步骤

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 准备数据文件

确保在项目目录下有以下文件：
- `林相宜单元资产.xlsx` - 包含 "单元资产2025" sheet 的 Excel 文件
- 需要包含以下列：
  - 统计日期
  - 单元资产净值(净价)

## 使用方法

### 启动应用

```bash
python app.py
```

### 访问界面

启动后在浏览器中访问：
```
http://localhost:5000
```

## 项目结构

```
investment evaluation/
├── app.py                          # Flask Web 应用主文件
├── Investment_evaluation.py        # 核心分析引擎
├── requirements.txt                # Python 依赖包
├── README.md                       # 项目说明文档
├── templates/                      # HTML 模板目录
│   └── index.html                  # 前端页面
└── 林相宜单元资产.xlsx              # 数据文件
```

## API 接口

- `GET /` - 主页面
- `GET /api/data` - 获取净值数据
- `GET /api/metrics` - 获取业绩指标
- `GET /api/summary` - 获取概览信息
- `GET /api/export/excel` - 导出 Excel 报告

## 配置说明

在 `app.py` 中可以修改以下配置：

```python
analyzer = InvestmentPerformanceAnalyzer(
    data_file="林相宜单元资产.xlsx",  # 数据文件路径
    risk_free_rate=0.015,             # 无风险利率 (1.5%)
    chart_title="林相宜-投资业绩分析"  # 图表标题
)
```

## 技术栈

- **后端**: Flask, Pandas, NumPy, Matplotlib
- **前端**: HTML5, CSS3, JavaScript, Chart.js
- **数据处理**: Pandas, OpenPyXL
- **可视化**: Matplotlib, Plotly, Chart.js

## 注意事项

1. 确保 Excel 数据文件格式正确
2. 日期格式应为标准日期类型
3. 净值数据不应包含空值或异常值
4. 建议使用 Python 3.8 或更高版本

## 常见问题

### 数据加载失败
- 检查 Excel 文件路径是否正确
- 确认 sheet 名称为 "单元资产2025"
- 验证列名是否匹配

### 端口被占用
修改 `app.py` 中的端口号：
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # 改为 5001 或其他端口
```

## 许可证

本项目仅供学习和研究使用。
