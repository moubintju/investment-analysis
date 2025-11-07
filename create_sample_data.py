import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 创建示例数据
np.random.seed(42)
start_date = datetime(2024, 1, 1)
days = 250  # 一年的交易日

# 生成日期序列
dates = [start_date + timedelta(days=i) for i in range(days)]

# 生成净值数据 (模拟正收益的净值曲线)
initial_nav = 1.0
daily_returns = np.random.normal(0.0005, 0.01, days)  # 日均收益率0.05%, 波动率1%
nav_values = [initial_nav]

for ret in daily_returns[1:]:
    nav_values.append(nav_values[-1] * (1 + ret))

# 创建DataFrame
df = pd.DataFrame({
    '统计日期': dates,
    '单元资产净值(净价)': nav_values
})

# 保存到Excel
output_file = "示例投资数据.xlsx"
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='单元资产2025', index=False)

print(f"示例数据已创建: {output_file}")
print(f"数据范围: {df['统计日期'].min()} 到 {df['统计日期'].max()}")
print(f"起始净值: {df['单元资产净值(净价)'].iloc[0]:.4f}")
print(f"最终净值: {df['单元资产净值(净价)'].iloc[-1]:.4f}")
print(f"总收益率: {(df['单元资产净值(净价)'].iloc[-1] / df['单元资产净值(净价)'].iloc[0] - 1):.2%}")
