## 📖 项目简介

这是一个轻量级、易用的 Python 数据描述统计及数据预处理工具，旨在帮助基础学者快速了解数据集的基本情况。通过简单的 API 调用，您可以获得数据集的整体概览、单列详细统计信息并进行简单的数据预处理。

项目代码结构清晰，易于扩展，适合集成到数据预处理流程中。

项目处于持续更新中...

---

## 🔧 安装

### 依赖库
- `pandas == 3.0.1`
- `matplotlib == 3.10.8` （用于变量绘图）

### 项目结构
建议将本项目克隆或下载后，保持如下目录结构：
```
your_project/
├── data_check/
│   ├── __init__.py
│   └── description.py      # 包含 DataDescriber 类
│   └── processing.py       # 包含 DataProcessor 类
├── machine_learning        # 包含 各机器学习方法
└── main.py                 # 你的主程序（或测试脚本）
```

---

## 🚀 快速开始

main文件中演示了如何使用 `DataDescriber及DataProcessor` 对一份简单的 DataFrame 进行描述统计和预处理。

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
