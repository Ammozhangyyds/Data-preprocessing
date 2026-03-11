## 📖 项目简介

`DataDescriber` 是一个轻量级、易用的 Python 数据描述统计工具，基于 `pandas` 构建，旨在帮助数据科学家和分析师快速了解数据集的基本情况。通过简单的 API 调用，您可以获得数据集的整体概览、单列详细统计信息，并一键生成交互式分布直方图（数值列）。支持自动识别数值列与分类列，并针对不同类型输出相应的统计指标。

项目代码结构清晰，易于扩展，适合集成到数据预处理流程中。

项目处于持续更新中...

---

## ✨ 功能特性

- **整体概览**  
  输出数据总行数、总列数，并为每一列统计：数据类型、非空数量、缺失数量、非空占比。对数值列额外计算最大值、最小值、平均值、中位数。

- **单列详细统计**  
  - **数值列**：均值、标准差、最小值、最大值、四分位数（25%/50%/75%）。
  - **分类列**：唯一值数量、值频数分布（自动控制显示数量，避免输出过载）。

- **自动类型识别**  
  使用 `pandas.api.types.is_numeric_dtype` 准确判断列是否为数值类型，避免对字符串列误算统计量。

- **HTML 报告导出**  
  整体概览结果自动保存为 `basic_description.html`，方便离线查看和分享。

---

## 🔧 安装

### 依赖库
- `pandas == 3.0.1`
- `matplotlib == 3.10.8` （用于变量绘图）

使用 pip 安装所需依赖：
```bash
pip install pandas matplotlib
```

### 项目结构
建议将本项目克隆或下载后，保持如下目录结构：
```
your_project/
├── data_check/
│   ├── __init__.py
│   └── description.py      # 包含 DataDescriber 类
│   └── processing.py       # 包含 DataDescriber 类（开发中）
└── main.py                 # 你的主程序（或测试脚本）
```

---

## 🚀 快速开始

以下示例演示了如何使用 `DataDescriber` 对一份简单的 DataFrame 进行描述统计。

```python
# 0. 导入必要库
import pandas as pd
from data_check.description import DataDescriber

# 1. 准备数据（此处使用生成数据）
df = pd.DataFrame({
    'A': [1, 2, None, 4],
    'B': ['x', 'y', 'z', None],
    'C': [1.1, 2.2, 3.3, 4.4]
})

# 2. 创建描述器实例
describer = DataDescriber(df)

# 3. 使用功能
describer.basic_description()           # 打印整体概览，并生成 basic_description.html
describer.column_description('A')       # 对列 A 进行详细统计
describer.plot_column_distribution('A') # 绘制列 A 的交互式直方图
```

运行后，控制台将输出美观的表格，同时项目根目录下会生成 `basic_description.html` 文件。

---

## 🤝 贡献指南

欢迎任何形式的贡献！如果您有好的想法或发现 bug，请通过以下方式参与：

1. Fork 本仓库。
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)。
3. 提交您的改动 (`git commit -m 'Add some AmazingFeature'`)。
4. 推送到分支 (`git push origin feature/AmazingFeature`)。
5. 打开一个 Pull Request。

请确保代码风格符合 PEP 8，并在提交前运行现有测试（如有）。

---

## 📄 许可证

本项目采用 MIT 许可证，详情请参见 [LICENSE](LICENSE) 文件。

---

## 📮 联系方式

作者：Yitao Zhang  
邮箱：yitao_zhang1999@outlook.com  

---

> **提示**：如果您在使用过程中遇到任何问题，欢迎在 GitHub 上提交 Issue 或直接联系作者。
