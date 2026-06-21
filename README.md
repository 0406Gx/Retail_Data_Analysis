
# Supermarket Sales Data Analysis

## 项目介绍
基于Kaggle公开连锁超市交易数据集，使用Python完成数据清洗、营收多维分析与用户分群建模，输出经营优化建议。

## 技术栈
Python: Pandas, Numpy, Matplotlib, Scikit-learn

## 分析内容
1. 原始数据1000条，完成空值、异常数据清洗
2. 从门店、品类、用户属性做多维度营收可视化
3. K-Means聚类实现用户分层，划分三类客户，针对性给出备货、会员营销方案

## 文件说明
- data：原始数据集
- code：完整分析代码
- img：可视化结果图

## 目录结构
```
Retail_Data_Analysis/
├─ data/
│   └─ supermarket_sales.csv
├─ code/
│   └─ sales_analysis.ipynb
├─ img/
└─ README.md
```

## 运行方式

### 方式一：双击运行（推荐）
直接双击运行根目录下的 `run_analysis.bat` 文件即可。

### 方式二：命令行运行
```powershell
# 进入项目目录
cd Retail_Data_Analysis

# 安装依赖（首次运行）
pip install pandas numpy matplotlib scikit-learn

# 运行Python脚本
python code/sales_analysis.py

# 或者运行Jupyter Notebook
jupyter notebook code/sales_analysis.ipynb
```

## 分析结果
- **数据清洗**：原始数据1000条，有效数据占比100%
- **营收分析**：总营收322,966.75 USD，平均客单价322.97 USD
- **最高营收分店**：Giza (110,568.71 USD)
- **最高营收品类**：Food and beverages (56,144.84 USD)
- **用户画像**：会员vs非会员消费对比、男女客单价对比
- **用户聚类**：K-Means划分高价值/普通/低频三类客群

## 经营优化建议
1. 会员营销：会员客单价高于非会员，建议推出更多会员专属优惠
2. 品类优化：根据各品类营收调整库存，重点关注高营收品类
3. 客户分层运营：针对不同客群制定差异化策略
4. 支付方式：支持多种支付方式，优化支付体验
