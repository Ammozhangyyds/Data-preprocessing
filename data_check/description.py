# -*- coding: UTF-8 -*-
"""
@Project     ：STEP1-Data Processing-Built by Yitao_Zhang
@File        ：description.py
@IDE         ：PyCharm
@Author      ：Yitao Zhang.
@Email       ：yitao_zhang1999@outlook.com
@Created Date：2026/3/10 18:09
"""

import pandas as pd
import matplotlib.pyplot as plt

class DataDescriber:
    """
    对给定的 DataFrame 进行各种描述性统计。
    """
    def __init__(self, df):
        """
        参数:
            df (pandas.DataFrame): 要分析的数据框
        """
        self.df = df

    # ---------- 私有辅助方法 ----------
    def get_column_stats(self, col):
        """
        获取列的基本统计信息（非空数量、缺失数量、非空占比）
        参数:
            col (pandas.Series): 数据列
        返回:
            dict: 包含 non_null, null_count, non_null_pct 的字典
        """
        total_rows = len(self.df)  # 注意：这里依赖 self.df 的总行数，也可从 col 所在 df 获取
        non_null = col.count()
        null_count = col.isnull().sum()
        non_null_pct = (non_null / total_rows * 100) if total_rows > 0 else 0
        return {
            'non_null': non_null,
            'null_count': null_count,
            'non_null_pct': non_null_pct
        }

    @staticmethod
    def get_numeric_stats(col):
        """
        获取数值列的详细统计量（使用 describe）
        参数:
            col (pandas.Series): 数值列
        返回:
            dict: 包含 max, min, mean, median, std, 25%, 50%, 75% 等
        """
        desc = col.describe(percentiles=[.25, .5, .75]).to_dict()
        return {
            'max': desc.get('max', None),
            'min': desc.get('min', None),
            'mean': desc.get('mean', None),
            'median': desc.get('50%', None),
            'std': desc.get('std', None),
            '25%': desc.get('25%', None),
            '50%': desc.get('50%', None),
            '75%': desc.get('75%', None)
        }

    @staticmethod
    def get_categorical_stats(col, max_unique_for_full=20):
        """
        获取分类列的统计量（唯一值数量、频数分布）
        参数:
            col (pandas.Series): 分类列
            max_unique_for_full (int): 当唯一值数量小于等于此值时，返回完整频数（前10），否则返回最常见的前5个
        返回:
            dict: 包含 unique_count, 以及频数字典（键为 'value_counts_top10' 或 'top5_values'）
        """
        unique_count = col.nunique()
        result = {'unique_count': unique_count}
        if unique_count <= max_unique_for_full:
            # 返回前10个值的频数（包含 NaN）
            value_counts = col.value_counts(dropna=False).head(10)
            result['value_counts_top10'] = value_counts.to_dict()
        else:
            top_values = col.value_counts(dropna=False).head(5)
            result['top5_values'] = top_values.to_dict()
        return result

    # ---------- 公共接口 ----------
    def basic_description(self):
        """
        对 DataFrame 进行基本描述统计。
        """
        df = self.df
        total_rows, total_cols = df.shape
        print(f"===== 数据的基本描述统计 =====")
        print(f"数据总量: {total_rows} 行, {total_cols} 列\n")

        stats = []
        for col in df.columns:
            dtype = df[col].dtype
            basic = self.get_column_stats(df[col])

            row = {
                '列名': col,
                '数据类型': dtype,
                '非空数量': basic['non_null'],
                '缺失数量': basic['null_count'],
                '非空占比(%)': basic['non_null_pct']
            }

            if pd.api.types.is_numeric_dtype(df[col]):
                num_stats = self.get_numeric_stats(df[col])
                row.update({
                    '最大值': num_stats['max'],
                    '中位数': num_stats['median'],
                    '平均值': num_stats['mean'],
                    '最小值': num_stats['min']
                })
            else:
                row.update({
                    '最大值': None,
                    '中位数': None,
                    '平均值': None,
                    '最小值': None
                })

            stats.append(row)

        result_df = pd.DataFrame(stats)

        print("各列统计信息：")
        print(result_df.to_string(
            index=False,
            float_format='%.4f',
            justify='center'
        ))

        result_df.to_html('basic_description.html', index=False, float_format='%.4f')
        return result_df

    def column_description(self, column_name):
        """
        对指定列进行详细描述统计。
        参数:
            column_name (str): 要描述的列名
        返回:
            dict: 包含该列统计信息的字典
        """
        if column_name not in self.df.columns:
            raise ValueError(f"列 '{column_name}' 不存在于数据框中。")

        col = self.df[column_name]
        dtype = col.dtype
        basic = self.get_column_stats(col)

        info = {
            '列名': column_name,
            '数据类型': dtype,
            '总行数': len(self.df),
            '非空数量': basic['non_null'],
            '缺失数量': basic['null_count'],
            '非空占比(%)': basic['non_null_pct']
        }

        if pd.api.types.is_numeric_dtype(col):
            num_stats = self.get_numeric_stats(col)
            info.update({
                '均值': num_stats['mean'],
                '标准差': num_stats['std'],
                '最小值': num_stats['min'],
                '25%分位数': num_stats['25%'],
                '中位数': num_stats['50%'],
                '75%分位数': num_stats['75%'],
                '最大值': num_stats['max']
            })
        else:
            cat_stats = self.get_categorical_stats(col)
            info['唯一值数量'] = cat_stats['unique_count']
            if 'value_counts_top10' in cat_stats:
                info['值频数（前10）'] = cat_stats['value_counts_top10']
            else:
                info['最常见的5个值'] = cat_stats['top5_values']

        # 打印信息
        self.print_column_info(column_name, info)
        return info

    @staticmethod
    def print_column_info(column_name, info):
        """
        打印列详细统计信息（供 column_description 调用）
        """
        print(f"\n===== 列 '{column_name}' 的描述统计 =====")
        for key, value in info.items():
            if key in ['值频数（前10）', '最常见的5个值']:
                continue
            if isinstance(value, float):
                print(f"{key}: {value:.4f}")
            else:
                print(f"{key}: {value}")

        if '值频数（前10）' in info:
            print("值频数（前10）:")
            for val, cnt in info['值频数（前10）'].items():
                print(f"    {val}: {cnt}")
        if '最常见的5个值' in info:
            print("最常见的5个值:")
            for val, cnt in info['最常见的5个值'].items():
                print(f"    {val}: {cnt}")

        print("=" * 40)

    def plot_column_distribution(self, column_name, bins=30):
        """
        绘制指定列的分布直方图（仅数值列有效）。

        参数:
            column_name (str): 要绘制的列名
            bins (int): 直方图的组数，默认30

        返回:
            None: 直接显示图形或打印提示信息
        """
        plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Microsoft YaHei', 'SimHei']  # 指定默认字体
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题

        if column_name not in self.df.columns:
            raise ValueError(f"列 '{column_name}' 不存在于数据框中。")

        col = self.df[column_name]

        # 检查是否为数值列
        if not pd.api.types.is_numeric_dtype(col):
            print(f"该变量是字符型，无分布直方图")
            return

        # 去除缺失值
        data = col.dropna()
        if len(data) == 0:
            print("该列所有值均为缺失，无法绘制直方图")
            return

        # 绘制直方图
        plt.figure(figsize=(8, 5))
        plt.hist(data, bins=bins, edgecolor='white', alpha=0.7)

        # 去除上边框和右边框
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.xlabel('数值范围')
        plt.ylabel('频数')
        plt.title(f'列 "{column_name}" 的分布直方图')
        plt.grid(axis='y', alpha=0.3)
        plt.show()

