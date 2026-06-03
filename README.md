# 📊 Sales Data Analysis & Business Insights Dashboard

**Author:** Sandeep Kushwaha  
**Tools:** Python, Pandas, NumPy, Matplotlib, Seaborn  
**Dataset:** 1,200 retail transactions across 10 Indian cities (2023)

---

## 🎯 Project Overview

This project performs end-to-end analysis of a retail electronics sales dataset to uncover:
- Monthly and quarterly revenue trends
- Top-performing products and categories
- Regional and city-wise performance
- Customer payment preferences and ratings
- Business recommendations backed by data

---

## 📁 Project Structure

```
sales-data-analysis/
│
├── data/
│   ├── sales_data.csv          # Main dataset (1200 rows)
│   └── generate_data.py        # Script used to create dataset
│
├── outputs/
│   ├── 01_monthly_revenue.png
│   ├── 02_product_revenue.png
│   ├── 03_region_category_heatmap.png
│   ├── 04_quarterly_growth.png
│   ├── 05_payment_ratings.png
│   └── 06_city_revenue.png
│
├── sales_analysis.py           # Main analysis script
├── requirements.txt
└── README.md
```

---

## 📈 Key Business Insights

| # | Insight |
|---|---------|
| 1 | **May** recorded the highest monthly revenue — seasonal demand spike |
| 2 | **Q2** was the strongest quarter with consistent month-on-month growth |
| 3 | Average monthly revenue growth of **+3.0%** shows positive trend |
| 4 | **Laptops** are the highest revenue-generating product |
| 5 | **West region** (Mumbai, Pune, Ahmedabad) leads in total sales |
| 6 | **Computers** category dominates revenue across all regions |
| 7 | Discount percentage shows low negative correlation (-0.06) with revenue — discounts alone don't drive sales |
| 8 | Average customer rating of **3.73/5** — room for improvement in service quality |

---

## 📊 Visualizations

### 1. Monthly Revenue Trend
![Monthly Revenue](outputs/01_monthly_revenue.png)

### 2. Top Products by Revenue
![Product Revenue](outputs/02_product_revenue.png)

### 3. Region × Category Heatmap
![Heatmap](outputs/03_region_category_heatmap.png)

### 4. Quarterly Revenue & Growth
![Quarterly](outputs/04_quarterly_growth.png)

### 5. Payment Methods & Customer Ratings
![Payment Ratings](outputs/05_payment_ratings.png)

### 6. Top 10 Cities by Revenue
![City Revenue](outputs/06_city_revenue.png)

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/sales-data-analysis.git
cd sales-data-analysis
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the analysis
```bash
python sales_analysis.py
```

Charts will be saved in the `outputs/` folder.

---

## 🛠️ Technologies Used

| Tool | Purpose |
|------|---------|
| **Python 3.x** | Core programming language |
| **Pandas** | Data loading, cleaning, manipulation |
| **NumPy** | Numerical computations |
| **Matplotlib** | Charts and visualizations |
| **Seaborn** | Statistical plots and heatmaps |

---

## 📬 Contact

**Sandeep Kushwaha**  
📧 sk1183422@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/your-profile)  
💻 [GitHub](https://github.com/your-username)

---

*This project was built as part of my Data Analyst portfolio to demonstrate skills in Python-based data analysis and visualization.*
