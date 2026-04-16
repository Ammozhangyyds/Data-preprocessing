# -*- coding: UTF-8 -*-
"""
@Project     ：STEP1-Data Processing-Built by Yitao_Zhang
@File        ：main.py
@IDE         ：PyCharm
@Author      ：Yitao Zhang.
@Email       ：yitao_zhang1999@outlook.com
@Created Date：2026/3/10 17:47
"""

# ==== Instructions ====

# 0.导包 如有必要
import pandas as pd

# 1.获取数据 此处使用生成数据
df = pd.DataFrame({
    'A': [1, 2, None, 4, 5],
    'B': ['x', 'y', None, 'x', 'z'],
    'C': [1.5, 2.5, 3.5, None, 5.5],
    'D': [10, 20, 30, 40, 50],
    'E': [1, 2, 3, 4, 5]
})

# 2.1调用数据描述函数
from data_check.description import DataDescriber
describer = DataDescriber(df)

# 2.2使用数据描述函数
describer.basic_description()           # 对DataFrame进行基本描述统计（同时在根目录下生成html文件便于查看）
describer.column_description('A')       # 对指定列进行详细描述统计
describer.plot_column_distribution('A') # 绘制指定列的分布直方图（仅数值列有效）
describer.get_percentiles('A',     # 输出指定变量的分位数
                          [1, 5, 95])# 例如：[1, 5, 95]为1%、5%、95%分位数


# 3.1调用数据处理函数
from data_check.processing import DataProcessing
processor = DataProcessing(df)

# 3.2使用函数检查缺失值
processor.check_missing()
processor.drop_missing(axis=0)                                         # 删除包含缺失值的行
processor.fill_mean_median(columns=['A', 'C'], method='mean')          # 均值填充（连续变量）# "method = 'mean' or method = 'median'
processor.fill_mode(columns=['B'])                                     # 众数填充（离散变量）
# 回归插补（使用 A, D 预测 C）
# 先得到填充后的 DataFrame，直接使用processor.regression_impute(target_col='C', predictor_cols=['A', 'D']) 会报错
filled_df = processor.fill_mean_median(columns=['A', 'C'], method='mean')
# 用新的 DataFrame 创建新的 DataProcessing 对象进行回归插补（使用 A, D 预测 C）
new_processor = DataProcessing(filled_df)
new_processor.regression_impute(target_col='C', predictor_cols=['A', 'D'])

# 3.3使用函数检查异常值
# columns='列名'指定列, interactive=False取消交互


