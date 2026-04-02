# -*- coding: UTF-8 -*-
"""
@Project     ：STEP1-Data Processing-Built by Yitao_Zhang
@File        ：processing.py
@IDE         ：PyCharm
@Author      ：Yitao Zhang.
@Email       ：yitao_zhang1999@outlook.com
@Created Date：2026/3/11 15:22
"""

import warnings
from typing import List, Optional, Union
import pandas as pd
import numpy as np

class DataProcessing:
    """
    缺失值处理类。

    Parameters
    ----------
    df : pandas.DataFrame
        输入的数据框。
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self._original_df = df.copy()

    def check_missing(self, columns: Optional[Union[str, List[str]]] = None) -> pd.DataFrame:
        """
        检查指定列或全部列的缺失情况。

        Parameters
        ----------
        columns : str or list of str, optional
            需要检查的列名，若为 None 则检查所有列。

        Returns
        -------
        pd.DataFrame
            包含列名、缺失数量、缺失比例的信息表。
        """
        if columns is None:
            cols = self.df.columns.tolist()
        elif isinstance(columns, str):
            cols = [columns]
        else:
            cols = columns

        missing_info = []
        total_rows = len(self.df)
        for col in cols:
            if col not in self.df.columns:
                raise ValueError(f"列 '{col}' 不存在于数据框中。")
            null_cnt = self.df[col].isnull().sum()
            null_pct = (null_cnt / total_rows) * 100
            missing_info.append({
                '列名': col,
                '缺失数量': null_cnt,
                '缺失比例(%)': round(null_pct, 2)
            })
        return pd.DataFrame(missing_info)

    def drop_missing(self, columns: Optional[Union[str, List[str]]] = None, axis: int = 0) -> pd.DataFrame:
        """
        删除缺失样本（行）或删除指定列。

        Parameters
        ----------
        columns : str or list of str, optional
            用于检查缺失的列。若为 None，则对所有列进行判断（axis=0 时删除任何含缺失的行）。
        axis : int, default 0
            0：删除包含缺失值的行；
            1：删除指定的列（此时 columns 必须指定）。

        Returns
        -------
        pd.DataFrame
            处理后的数据框（原数据不变，返回新对象）。
        """
        df_new = self.df.copy()
        if axis == 0:
            if columns is None:
                df_new = df_new.dropna()
            else:
                cols = [columns] if isinstance(columns, str) else columns
                df_new = df_new.dropna(subset=cols)
        elif axis == 1:
            if columns is None:
                raise ValueError("axis=1 时请指定要删除的列 columns。")
            cols = [columns] if isinstance(columns, str) else columns
            df_new = df_new.drop(columns=cols)
        else:
            raise ValueError("axis 必须为 0 或 1。")
        return df_new

    def fill_mean_median(self, columns: Union[str, List[str]], method: str = 'mean') -> pd.DataFrame:
        """
        对连续型变量的缺失值用均值或中位数填充。
        """
        df_new = self.df.copy()
        cols = [columns] if isinstance(columns, str) else columns

        for col in cols:
            if col not in df_new.columns:
                raise ValueError(f"列 '{col}' 不存在。")
            if not pd.api.types.is_numeric_dtype(df_new[col]):
                raise TypeError(f"列 '{col}' 不是数值类型，请使用 fill_mode 填充离散型数据。")
            if method == 'mean':
                fill_value = df_new[col].mean(skipna=True)
            elif method == 'median':
                fill_value = df_new[col].median(skipna=True)
            else:
                raise ValueError("method 必须为 'mean' 或 'median'。")
            # 修改：避免链式赋值警告
            df_new[col] = df_new[col].fillna(fill_value, inplace=False)
        return df_new

    def fill_mode(self, columns: Union[str, List[str]]) -> pd.DataFrame:
        """
        对离散型变量的缺失值用众数填充。
        """
        df_new = self.df.copy()
        cols = [columns] if isinstance(columns, str) else columns

        for col in cols:
            if col not in df_new.columns:
                raise ValueError(f"列 '{col}' 不存在。")
            mode_val = df_new[col].mode()
            if len(mode_val) == 0:
                warnings.warn(f"列 '{col}' 全部缺失，无法计算众数，将保持缺失。")
                continue
            fill_value = mode_val[0]
            # 修改：避免链式赋值警告
            df_new[col] = df_new[col].fillna(fill_value, inplace=False)
        return df_new

    def regression_impute(self,
                          target_col: str,
                          predictor_cols: List[str],
                          model=None) -> pd.DataFrame:
        """
        使用回归模型对目标列的缺失值进行预测填充。

        Parameters
        ----------
        target_col : str
            需要填充的目标列名（必须是数值型，且存在缺失值）。
        predictor_cols : list of str
            用于预测的协变量列名（必须完整无缺失，且为数值型）。
        model : sklearn estimator, optional
            回归模型，默认使用线性回归。需遵循 sklearn 接口（fit, predict）。

        Returns
        -------
        pd.DataFrame
            填充后的数据框。
        """
        df_new = self.df.copy()
        if target_col not in df_new.columns:
            raise ValueError(f"目标列 '{target_col}' 不存在。")
        for col in predictor_cols:
            if col not in df_new.columns:
                raise ValueError(f"预测变量列 '{col}' 不存在。")
            if df_new[col].isnull().any():
                raise ValueError(f"预测变量列 '{col}' 存在缺失值，请先处理。")

        # 提取完整数据用于训练
        complete_mask = df_new[predictor_cols].notna().all(axis=1) & df_new[target_col].notna()
        x_train = df_new.loc[complete_mask, predictor_cols].values
        y_train = df_new.loc[complete_mask, target_col].values

        if len(x_train) == 0:
            raise ValueError("没有完整样本可用于训练回归模型。")

        # 如果未提供模型，使用线性回归
        if model is None:
            from sklearn.linear_model import LinearRegression
            model = LinearRegression()

        model.fit(x_train, y_train)

        # 预测缺失值
        missing_mask = df_new[target_col].isnull() & df_new[predictor_cols].notna().all(axis=1)
        if missing_mask.any():
            x_missing = df_new.loc[missing_mask, predictor_cols].values
            y_pred = model.predict(x_missing)
            df_new.loc[missing_mask, target_col] = y_pred

        return df_new

    # 辅助方法：重置为原始数据
    def reset(self):
        """
        将数据重置为初始化时的原始状态。
        """
        self.df = self._original_df.copy()

    def plot_distributions(self,
                           columns: Optional[Union[str, List[str]]] = None,
                           save_dir: str = './变量分布直方图/',
                           bins: int = 30,
                           color: str = '#4575B4',  # 默认改为海军蓝
                           alpha: float = 1,
                           show_count: bool = True,
                           filter_condition: Optional[Union[str, callable]] = None,
                           dpi: int = 800,
                           figsize: tuple = (8, 5),
                           interactive: bool = True):
        """
        绘制指定列（数值型）的分布直方图，支持交互式选择变量和数值范围。

        Parameters
        ----------
        columns : str or list of str, optional
            需要绘制的列名。若为 None 且 interactive=True，则交互式选择。
        save_dir : str, default './变量分布直方图/'
            保存图片的目录，会自动创建。
        bins : int, default 20
            直方图的组数。
        color : str, default 'navy'
            直方图的填充颜色（海军蓝）。
        alpha : float, default 0.5
            直方图的透明度。
        show_count : bool, default True
            是否在每个柱子上方显示样本数。
        filter_condition : str or callable, optional
            对数据进行筛选的条件（可先于数值范围过滤）。
        dpi : int, default 100
            保存图片的分辨率。
        figsize : tuple, default (8, 5)
            图形大小（宽，高）。
        interactive : bool, default True
            是否启用交互模式（询问变量和数值范围）。若为 False，则按原有参数执行。
        """
        import matplotlib.pyplot as plt
        import os

        # 1. 准备数据（复制一份，避免修改原数据）
        plot_df = self.df.copy()

        # 2. 应用过滤条件（如果有）
        if filter_condition is not None:
            if isinstance(filter_condition, str):
                plot_df = plot_df.query(filter_condition)
            elif callable(filter_condition):
                plot_df = filter_condition(plot_df)
            else:
                raise TypeError("filter_condition 必须是字符串或可调用对象。")

        if plot_df.empty:
            print("警告：过滤后无数据，无法绘图。")
            return

        # 3. 确定要绘制的列（交互或参数指定）
        numeric_cols = plot_df.select_dtypes(include=[np.number]).columns.tolist()
        if not numeric_cols:
            print("没有数值列可供绘图。")
            return

        if columns is None and interactive:
            # 交互式选择列
            print("\n===== 可用的数值列 =====")
            for idx, col in enumerate(numeric_cols):
                print(f"{idx + 1}. {col}")
            while True:
                try:
                    choice = input("请选择要绘图的变量（输入序号或列名）：").strip()
                    if choice.isdigit():
                        idx = int(choice) - 1
                        if 0 <= idx < len(numeric_cols):
                            selected_col = numeric_cols[idx]
                            break
                        else:
                            print(f"序号超出范围（1-{len(numeric_cols)}），请重新输入。")
                    else:
                        if choice in numeric_cols:
                            selected_col = choice
                            break
                        else:
                            print(f"列 '{choice}' 不存在，请重新输入。")
                except Exception:
                    print("输入无效，请重新输入。")
            cols = [selected_col]
        elif columns is not None:
            cols = [columns] if isinstance(columns, str) else columns
            for col in cols:
                if col not in plot_df.columns:
                    raise ValueError(f"列 '{col}' 不存在。")
                if not pd.api.types.is_numeric_dtype(plot_df[col]):
                    raise TypeError(f"列 '{col}' 不是数值类型，无法绘制直方图。")
        else:
            # columns 为 None 且 interactive=False，则绘制所有数值列
            cols = numeric_cols

        # 4. 创建保存目录
        os.makedirs(save_dir, exist_ok=True)

        # 5. 设置中文字体（避免中文乱码）
        plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Microsoft YaHei', 'SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        # 6. 对每一列绘图
        for feature in cols:
            # 交互式输入数值范围（如果 interactive 且用户选择了该列）
            lower, upper = None, None
            if interactive and len(cols) == 1 and feature == cols[0]:
                print(f"\n===== 变量 '{feature}' 的数据范围 =====")
                print(f"实际最小值: {plot_df[feature].min():.4f}, 实际最大值: {plot_df[feature].max():.4f}")
                print("请输入你想展示的数值范围（留空则使用全部数据）：")
                while True:
                    range_input = input("格式: 最小值,最大值 (例如 0,100): ").strip()
                    if range_input == "":
                        lower, upper = None, None
                        break
                    try:
                        parts = range_input.split(',')
                        if len(parts) != 2:
                            print("输入格式错误，请用英文逗号分隔两个数字。")
                            continue
                        lower = float(parts[0].strip())
                        upper = float(parts[1].strip())
                        if lower >= upper:
                            print("最小值必须小于最大值。")
                            continue
                        break
                    except ValueError:
                        print("请输入有效的数字。")
                # 根据范围筛选数据
                data_series = plot_df[feature].dropna()
                if lower is not None:
                    data_series = data_series[data_series >= lower]
                if upper is not None:
                    data_series = data_series[data_series <= upper]
                if len(data_series) == 0:
                    print(f"在指定范围 {lower}-{upper} 内没有有效数据，跳过绘图。")
                    continue
            else:
                data_series = plot_df[feature].dropna()
                if len(data_series) == 0:
                    print(f"列 '{feature}' 无有效数据，跳过绘图。")
                    continue

            # 绘制直方图
            fig, ax = plt.subplots(figsize=figsize)
            counts, bins_edges, patches = ax.hist(data_series, bins=bins, color=color, alpha=alpha, edgecolor='white')
            ax.set_xlabel('数值范围')
            ax.set_ylabel('频数')
            title = f'列 "{feature}" 的分布直方图'
            if interactive and (lower is not None or upper is not None):
                range_str = f" (范围: {lower if lower is not None else '全部'} ~ {upper if upper is not None else '全部'})"
                title += range_str
            ax.set_title(title)
            ax.grid(axis='y', alpha=0.3)

            # 去除上框线和右框线
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            # 在每个柱子上方显示样本数
            if show_count:
                bin_width = bins_edges[1] - bins_edges[0] if len(bins_edges) > 1 else 1
                for count, bin_edge in zip(counts, bins_edges):
                    if count > 0:
                        x_pos = bin_edge + bin_width / 2
                        ax.text(x_pos, count + max(counts) * 0.01, str(int(count)),
                                ha='center', va='bottom', fontsize=9)

            # 保存图片
            save_path = os.path.join(save_dir, f'{feature}.jpg')
            plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
            plt.close()
            print(f"已保存: {save_path}")