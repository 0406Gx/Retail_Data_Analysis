import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)

# 创建输出目录
img_dir = os.path.join(project_dir, 'img')
os.makedirs(img_dir, exist_ok=True)

# 读取数据
data_path = os.path.join(project_dir, 'data', 'supermarket_sales.csv')
df = pd.read_csv(data_path)
print(f'原始数据行数: {len(df)}')

# 处理缺失值
df_clean = df.dropna()
print(f'剔除缺失值后行数: {len(df_clean)}')

# 过滤异常数据
df_clean = df_clean[(df_clean['Unit price'] >= 1) & (df_clean['Unit price'] <= 200)]
df_clean = df_clean[(df_clean['Quantity'] >= 1) & (df_clean['Quantity'] <= 10)]
df_clean = df_clean[(df_clean['Rating'] >= 0) & (df_clean['Rating'] <= 10)]

clean_rate = (len(df) - len(df_clean)) / len(df) * 100
print(f'清洗后数据行数: {len(df_clean)}')
print(f'无效数据占比: {clean_rate:.1f}%')

# 添加月份字段 - 使用try-except处理日期解析
def parse_date(date_str):
    try:
        # 先尝试DD/MM/YYYY格式
        return pd.to_datetime(date_str, format='%d/%m/%Y')
    except:
        try:
            # 再尝试MM/DD/YYYY格式
            return pd.to_datetime(date_str, format='%m/%d/%Y')
        except:
            return pd.NaT

df_clean['Date'] = df_clean['Date'].apply(parse_date)
df_clean = df_clean.dropna(subset=['Date'])
df_clean['Month'] = df_clean['Date'].dt.month

# 按分店统计营收
branch_revenue = df_clean.groupby('Branch')['Sales'].sum().sort_values(ascending=False)

# 按品类统计营收
category_revenue = df_clean.groupby('Product line')['Sales'].sum().sort_values(ascending=False)

# 按支付方式统计营收
payment_revenue = df_clean.groupby('Payment')['Sales'].sum().sort_values(ascending=False)

# 按月度统计营收
monthly_revenue = df_clean.groupby('Month')['Sales'].sum()

# 分店营收柱状图
plt.figure(figsize=(10, 6))
branch_revenue.plot(kind='bar', color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
plt.title('各分店营收对比')
plt.xlabel('分店')
plt.ylabel('营收 (USD)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(img_dir, 'branch_revenue.png'), dpi=100)
print('已生成: branch_revenue.png')

# 品类营收柱状图
plt.figure(figsize=(12, 6))
category_revenue.plot(kind='bar', color=['#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE'])
plt.title('各品类营收对比')
plt.xlabel('产品品类')
plt.ylabel('营收 (USD)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(img_dir, 'category_revenue.png'), dpi=100)
print('已生成: category_revenue.png')

# 支付方式营收饼图
plt.figure(figsize=(8, 8))
payment_revenue.plot(kind='pie', autopct='%1.1f%%', colors=['#FF6B6B', '#4ECDC4', '#45B7D1'])
plt.title('支付方式营收占比')
plt.ylabel('')
plt.tight_layout()
plt.savefig(os.path.join(img_dir, 'payment_revenue.png'), dpi=100)
print('已生成: payment_revenue.png')

# 月度营收趋势
plt.figure(figsize=(10, 6))
monthly_revenue.plot(kind='line', marker='o', color='#2C3E50', linewidth=2)
plt.title('月度营收趋势')
plt.xlabel('月份')
plt.ylabel('营收 (USD)')
plt.xticks([1, 2, 3])
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(img_dir, 'monthly_revenue.png'), dpi=100)
print('已生成: monthly_revenue.png')

# 会员vs非会员消费对比
member_stats = df_clean.groupby('Customer type')['Sales'].agg(['sum', 'mean', 'count'])
member_stats.columns = ['总消费', '客单价', '订单数']

# 会员vs非会员客单价对比
plt.figure(figsize=(8, 6))
member_stats['客单价'].plot(kind='bar', color=['#3498DB', '#E74C3C'])
plt.title('会员与非会员客单价对比')
plt.xlabel('客户类型')
plt.ylabel('客单价 (USD)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(img_dir, 'member_vs_normal.png'), dpi=100)
print('已生成: member_vs_normal.png')

# 男女消费统计
gender_stats = df_clean.groupby('Gender')['Sales'].agg(['sum', 'mean', 'count'])
gender_stats.columns = ['总消费', '客单价', '订单数']

# 男女客单价对比
plt.figure(figsize=(8, 6))
gender_stats['客单价'].plot(kind='bar', color=['#FF69B4', '#4169E1'])
plt.title('男女客单价对比')
plt.xlabel('性别')
plt.ylabel('客单价 (USD)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(img_dir, 'gender_comparison.png'), dpi=100)
print('已生成: gender_comparison.png')

# K-Means用户聚类
user_features = df_clean.groupby('Invoice ID').agg({
    'Sales': 'sum',
    'Quantity': 'sum',
    'Rating': 'mean'
}).reset_index()

scaler = StandardScaler()
features_scaled = scaler.fit_transform(user_features[['Sales', 'Quantity']])

kmeans = KMeans(n_clusters=3, random_state=42)
user_features['Cluster'] = kmeans.fit_predict(features_scaled)

cluster_means = user_features.groupby('Cluster')['Sales'].mean()
sorted_clusters = cluster_means.sort_values(ascending=False).index.tolist()
cluster_names = {
    sorted_clusters[0]: '高价值客户',
    sorted_clusters[1]: '普通客户',
    sorted_clusters[2]: '低频客户'
}
user_features['Cluster_Name'] = user_features['Cluster'].map(cluster_names)

# 聚类结果可视化
plt.figure(figsize=(12, 8))
colors = ['#E74C3C', '#3498DB', '#2ECC71']
markers = ['o', 's', '^']

for cluster in range(3):
    subset = user_features[user_features['Cluster'] == cluster]
    plt.scatter(subset['Sales'], subset['Quantity'], 
                c=colors[cluster], marker=markers[cluster],
                label=cluster_names[cluster], alpha=0.7, s=100)

centers = scaler.inverse_transform(kmeans.cluster_centers_)
plt.scatter(centers[:, 0], centers[:, 1], c='black', marker='*', s=300, label='聚类中心')

plt.title('K-Means用户聚类结果')
plt.xlabel('消费总额 (USD)')
plt.ylabel('购买数量')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(img_dir, 'kmeans_clusters.png'), dpi=100)
print('已生成: kmeans_clusters.png')

# 各类别占比饼图
cluster_counts = user_features['Cluster_Name'].value_counts()
plt.figure(figsize=(8, 8))
cluster_counts.plot(kind='pie', autopct='%1.1f%%', colors=['#E74C3C', '#3498DB', '#2ECC71'])
plt.title('客户群体分布')
plt.ylabel('')
plt.tight_layout()
plt.savefig(os.path.join(img_dir, 'cluster_distribution.png'), dpi=100)
print('已生成: cluster_distribution.png')

print('')
print('='*60)
print('零售销售数据挖掘分析报告')
print('='*60)
print(f'总营收: {df_clean["Sales"].sum():,.2f} USD')
print(f'平均客单价: {df_clean["Sales"].mean():,.2f} USD')
print(f'最高营收分店: {branch_revenue.idxmax()} ({branch_revenue.max():,.2f} USD)')
print(f'最高营收品类: {category_revenue.idxmax()} ({category_revenue.max():,.2f} USD)')
print('分析完成！所有可视化图表已保存至 img 目录。')
