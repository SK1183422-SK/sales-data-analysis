"""
Sales Data Analysis & Business Insights Dashboard
Author: Sandeep Kushwaha
Description: End-to-end analysis of retail sales data to uncover revenue trends,
             top products, regional performance, and customer behavior.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')
os.makedirs('outputs', exist_ok=True)

# ── STYLE ──────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#0f0f1a',
    'axes.facecolor':   '#1a1a2e',
    'axes.edgecolor':   '#333355',
    'axes.labelcolor':  '#ccccee',
    'xtick.color':      '#aaaacc',
    'ytick.color':      '#aaaacc',
    'text.color':       '#e0e0ff',
    'grid.color':       '#2a2a4a',
    'grid.alpha':       0.5,
    'font.family':      'DejaVu Sans',
    'axes.titlesize':   13,
    'axes.titleweight': 'bold',
    'axes.titlecolor':  '#ffffff',
})

COLORS = ['#e94560', '#0f3460', '#533483', '#05c46b', '#f5a623',
          '#00b4d8', '#ff6b6b', '#ffd93d', '#6bcb77', '#4d96ff']
ACCENT = '#e94560'


# ════════════════════════════════════════════════════════════════════════════
# 1. LOAD & CLEAN DATA
# ════════════════════════════════════════════════════════════════════════════
print("=" * 55)
print("  SALES DATA ANALYSIS — Sandeep Kushwaha")
print("=" * 55)

df = pd.read_csv('data/sales_data.csv', parse_dates=['Date'])

print(f"\n📦 Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"📅 Date range   : {df['Date'].min().date()} → {df['Date'].max().date()}")
print(f"❓ Missing values: {df.isnull().sum().sum()}")

# Feature engineering
df['Month']      = df['Date'].dt.month
df['Month_Name'] = df['Date'].dt.strftime('%b')
df['Quarter']    = df['Date'].dt.quarter.map({1:'Q1',2:'Q2',3:'Q3',4:'Q4'})
df['Week']       = df['Date'].dt.isocalendar().week.astype(int)

print("\n✅ Data cleaned. New features: Month, Quarter, Week")


# ════════════════════════════════════════════════════════════════════════════
# 2. SUMMARY STATISTICS
# ════════════════════════════════════════════════════════════════════════════
total_revenue  = df['Revenue'].sum()
total_orders   = df['Order_ID'].nunique()
avg_order      = df['Revenue'].mean()
total_units    = df['Quantity'].sum()
avg_rating     = df['Customer_Rating'].mean()
top_product    = df.groupby('Product')['Revenue'].sum().idxmax()
top_city       = df.groupby('City')['Revenue'].sum().idxmax()

print("\n" + "─" * 55)
print("  📊  KEY BUSINESS METRICS")
print("─" * 55)
print(f"  Total Revenue     : ₹{total_revenue:>15,.0f}")
print(f"  Total Orders      : {total_orders:>15,}")
print(f"  Avg Order Value   : ₹{avg_order:>15,.0f}")
print(f"  Units Sold        : {total_units:>15,}")
print(f"  Avg Rating        : {avg_rating:>15.2f} / 5.0")
print(f"  Top Product       : {top_product:>15}")
print(f"  Top City          : {top_city:>15}")
print("─" * 55)


# ════════════════════════════════════════════════════════════════════════════
# 3. VISUALIZATIONS
# ════════════════════════════════════════════════════════════════════════════

def fmt_crore(x, _):
    if x >= 1e7:   return f'₹{x/1e7:.1f}Cr'
    if x >= 1e5:   return f'₹{x/1e5:.0f}L'
    return f'₹{x:,.0f}'


# ── Chart 1: Monthly Revenue Trend ─────────────────────────────────────────
monthly = (df.groupby(['Month','Month_Name'])['Revenue']
             .sum().reset_index()
             .sort_values('Month'))

fig, ax = plt.subplots(figsize=(12, 4.5))
ax.fill_between(monthly['Month_Name'], monthly['Revenue'],
                alpha=0.15, color=ACCENT)
ax.plot(monthly['Month_Name'], monthly['Revenue'],
        color=ACCENT, linewidth=2.5, marker='o', markersize=7)

for _, row in monthly.iterrows():
    ax.annotate(fmt_crore(row['Revenue'], None),
                (row['Month_Name'], row['Revenue']),
                textcoords='offset points', xytext=(0, 10),
                ha='center', fontsize=8, color='#ffffff')

ax.set_title('Monthly Revenue Trend — 2023', pad=14)
ax.set_xlabel('Month');  ax.set_ylabel('Revenue')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_crore))
ax.grid(axis='y');  ax.set_facecolor('#1a1a2e')
fig.patch.set_facecolor('#0f0f1a')
plt.tight_layout()
plt.savefig('outputs/01_monthly_revenue.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n✅ Chart 1 saved: Monthly Revenue Trend")


# ── Chart 2: Top Products by Revenue ───────────────────────────────────────
prod_rev = (df.groupby('Product')['Revenue'].sum()
              .sort_values(ascending=True))

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(prod_rev.index, prod_rev.values,
               color=COLORS[:len(prod_rev)], edgecolor='none', height=0.6)
for bar, val in zip(bars, prod_rev.values):
    ax.text(val + prod_rev.max()*0.01, bar.get_y() + bar.get_height()/2,
            fmt_crore(val, None), va='center', fontsize=9, color='#ffffff')

ax.set_title('Top Products by Total Revenue')
ax.set_xlabel('Total Revenue')
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_crore))
ax.set_facecolor('#1a1a2e');  fig.patch.set_facecolor('#0f0f1a')
plt.tight_layout()
plt.savefig('outputs/02_product_revenue.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart 2 saved: Product Revenue")


# ── Chart 3: Regional Revenue Heatmap (City × Category) ────────────────────
pivot = df.pivot_table(values='Revenue', index='Region',
                       columns='Category', aggfunc='sum', fill_value=0)
pivot = pivot.div(1e5).round(1)   # in Lakhs

fig, ax = plt.subplots(figsize=(10, 4))
sns.heatmap(pivot, annot=True, fmt='.0f', cmap='RdYlGn',
            linewidths=0.5, linecolor='#0f0f1a',
            ax=ax, cbar_kws={'label': 'Revenue (₹ Lakhs)'})
ax.set_title('Region × Category Revenue Heatmap (₹ Lakhs)')
ax.set_xlabel('Category');  ax.set_ylabel('Region')
fig.patch.set_facecolor('#0f0f1a')
plt.tight_layout()
plt.savefig('outputs/03_region_category_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart 3 saved: Region × Category Heatmap")


# ── Chart 4: Quarterly Revenue + Growth ────────────────────────────────────
qtr = df.groupby('Quarter')['Revenue'].sum()
growth = qtr.pct_change().mul(100).fillna(0)

fig, ax1 = plt.subplots(figsize=(9, 4.5))
ax2 = ax1.twinx()

bars = ax1.bar(qtr.index, qtr.values, color=COLORS[:4], alpha=0.8,
               width=0.5, edgecolor='none')
ax2.plot(qtr.index, growth.values, color='#ffd93d', linewidth=2,
         marker='D', markersize=8, zorder=5)
ax2.axhline(0, color='#ffffff', linewidth=0.5, linestyle='--', alpha=0.4)

for bar, val in zip(bars, qtr.values):
    ax1.text(bar.get_x() + bar.get_width()/2, val + qtr.max()*0.01,
             fmt_crore(val, None), ha='center', fontsize=9, color='#ffffff')

ax1.set_title('Quarterly Revenue & Growth Rate')
ax1.set_ylabel('Revenue');  ax2.set_ylabel('Growth % (QoQ)', color='#ffd93d')
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_crore))
ax2.tick_params(colors='#ffd93d')
ax1.set_facecolor('#1a1a2e');  fig.patch.set_facecolor('#0f0f1a')
plt.tight_layout()
plt.savefig('outputs/04_quarterly_growth.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart 4 saved: Quarterly Growth")


# ── Chart 5: Payment Method & Rating Distribution ──────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

pay = df['Payment_Method'].value_counts()
wedges, texts, autotexts = ax1.pie(
    pay.values, labels=pay.index, autopct='%1.1f%%',
    colors=COLORS[:len(pay)], startangle=140,
    wedgeprops={'edgecolor': '#0f0f1a', 'linewidth': 2})
for t in autotexts: t.set_color('white'); t.set_fontsize(9)
ax1.set_title('Payment Method Distribution')
ax1.set_facecolor('#1a1a2e')

sns.histplot(df['Customer_Rating'], bins=15, kde=True,
             color=ACCENT, ax=ax2, edgecolor='none')
ax2.set_title('Customer Rating Distribution')
ax2.set_xlabel('Rating');  ax2.set_ylabel('Count')
ax2.set_facecolor('#1a1a2e')
ax2.axvline(df['Customer_Rating'].mean(), color='#ffd93d',
            linestyle='--', linewidth=1.5,
            label=f"Mean: {df['Customer_Rating'].mean():.2f}")
ax2.legend()

fig.patch.set_facecolor('#0f0f1a')
plt.tight_layout()
plt.savefig('outputs/05_payment_ratings.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart 5 saved: Payment & Ratings")


# ── Chart 6: Top 10 Cities by Revenue ──────────────────────────────────────
city_rev = (df.groupby('City')['Revenue'].sum()
              .sort_values(ascending=False).head(10))

fig, ax = plt.subplots(figsize=(11, 4.5))
bars = ax.bar(city_rev.index, city_rev.values,
              color=COLORS[:10], edgecolor='none', width=0.6)
for bar, val in zip(bars, city_rev.values):
    ax.text(bar.get_x() + bar.get_width()/2, val + city_rev.max()*0.01,
            fmt_crore(val, None), ha='center', fontsize=8.5, color='#ffffff')

ax.set_title('Top 10 Cities by Revenue')
ax.set_ylabel('Total Revenue')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_crore))
ax.set_facecolor('#1a1a2e');  fig.patch.set_facecolor('#0f0f1a')
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('outputs/06_city_revenue.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Chart 6 saved: City Revenue")


# ════════════════════════════════════════════════════════════════════════════
# 4. BUSINESS INSIGHTS
# ════════════════════════════════════════════════════════════════════════════
monthly_growth = monthly['Revenue'].pct_change().mean() * 100
best_month     = monthly.loc[monthly['Revenue'].idxmax(), 'Month_Name']
best_quarter   = qtr.idxmax()
best_region    = df.groupby('Region')['Revenue'].sum().idxmax()
best_category  = df.groupby('Category')['Revenue'].sum().idxmax()
top_payment    = df['Payment_Method'].value_counts().idxmax()
discount_corr  = df['Discount_Pct'].corr(df['Revenue'])

print("\n" + "═" * 55)
print("  💡  KEY BUSINESS INSIGHTS")
print("═" * 55)
print(f"  1. Best month       : {best_month} had highest sales")
print(f"  2. Best quarter     : {best_quarter} drove peak revenue")
print(f"  3. Avg monthly growth: {monthly_growth:+.1f}%")
print(f"  4. Top region       : {best_region}")
print(f"  5. Top category     : {best_category}")
print(f"  6. Preferred payment: {top_payment}")
print(f"  7. Discount vs Rev  : correlation = {discount_corr:.2f}")
print(f"  8. Avg customer rating: {avg_rating:.2f}/5 — positive experience")
print("═" * 55)

print("\n📁 All charts saved to: outputs/")
print("\n🎉 Analysis complete!\n")
