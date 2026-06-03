import pandas as pd
import numpy as np

np.random.seed(42)

products = {
    'Laptop':      (45000, 80000),
    'Smartphone':  (12000, 35000),
    'Headphones':  (1500,  8000),
    'Tablet':      (15000, 40000),
    'Smartwatch':  (3000,  12000),
    'Camera':      (20000, 60000),
    'Speaker':     (2000,  10000),
    'Monitor':     (8000,  25000),
}

categories = {
    'Laptop': 'Computers', 'Tablet': 'Computers', 'Monitor': 'Computers',
    'Smartphone': 'Mobile', 'Smartwatch': 'Mobile',
    'Headphones': 'Audio', 'Speaker': 'Audio',
    'Camera': 'Photography',
}

cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Pune',
          'Chennai', 'Kolkata', 'Raipur', 'Bhopal', 'Ahmedabad']

regions = {
    'Mumbai': 'West', 'Pune': 'West', 'Ahmedabad': 'West',
    'Delhi': 'North', 'Bhopal': 'North',
    'Bangalore': 'South', 'Hyderabad': 'South', 'Chennai': 'South',
    'Kolkata': 'East', 'Raipur': 'East',
}

payment_methods = ['Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Cash']

rows = []
for _ in range(1200):
    product = np.random.choice(list(products.keys()))
    low, high = products[product]
    price = round(np.random.uniform(low, high), -2)
    qty = np.random.randint(1, 6)
    city = np.random.choice(cities)
    date = pd.Timestamp('2023-01-01') + pd.Timedelta(days=np.random.randint(0, 365))
    discount = np.random.choice([0, 5, 10, 15, 20], p=[0.4, 0.2, 0.2, 0.1, 0.1])
    final_price = price * (1 - discount / 100)
    revenue = round(final_price * qty, 2)

    rows.append({
        'Order_ID':        f'ORD{10000 + _}',
        'Date':            date.strftime('%Y-%m-%d'),
        'Product':         product,
        'Category':        categories[product],
        'City':            city,
        'Region':          regions[city],
        'Quantity':        qty,
        'Unit_Price':      price,
        'Discount_Pct':    discount,
        'Final_Price':     round(final_price, 2),
        'Revenue':         revenue,
        'Payment_Method':  np.random.choice(payment_methods),
        'Customer_Rating': round(np.random.uniform(2.5, 5.0), 1),
    })

df = pd.DataFrame(rows).sort_values('Date').reset_index(drop=True)
df.to_csv('data/sales_data.csv', index=False)
print(f"Dataset created: {len(df)} rows")
print(df.head())
