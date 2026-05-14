import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs("assets", exist_ok=True)

np.random.seed(42)
n = 1200

products = np.random.choice(["Chair", "Desk", "Laptop", "Monitor", "Phone", "Printer", "Tablet"], n)
payment_methods = np.random.choice(["Cash", "Credit Card", "Debit Card", "Gift Card", "Online"], n)
statuses = np.random.choice(["Cancelled", "Delivered", "Pending", "Returned", "Shipped"], n)

df = pd.DataFrame({
    "OrderID": [f"ORD{200000 + i}" for i in range(n)],
    "Date": pd.date_range("2023-01-01", periods=n, freq="h")[:n],
    "CustomerID": [f"C{np.random.randint(10000, 90000)}" for _ in range(n)],
    "Product": products,
    "Quantity": np.random.randint(1, 6, n),
    "UnitPrice": np.round(np.random.uniform(10, 700, n), 2),
    "PaymentMethod": payment_methods,
    "OrderStatus": statuses,
})
df["TotalPrice"] = np.round(df["Quantity"] * df["UnitPrice"] * np.random.uniform(0.9, 1.1, n), 2)

sns.set_style("whitegrid")
plt.rcParams.update({"figure.dpi": 120, "savefig.dpi": 150, "savefig.bbox": "tight"})

fig, axes = plt.subplots(1, 2, figsize=(16, 5))

counts = df.groupby("Product").size().sort_values()
counts.plot(kind="bar", ax=axes[0], color="#4A72B0")
axes[0].set_title("Product Counts — SQL: GROUP BY Product", fontsize=13, fontweight="bold")
axes[0].set_xlabel("Product")
axes[0].set_ylabel("Count")

revenue = df.groupby("Product")["TotalPrice"].sum().sort_values(ascending=False)
revenue.plot(kind="bar", ax=axes[1], color="#4A72B0")
axes[1].set_title("Revenue by Product — SQL: GROUP BY + ORDER BY", fontsize=13, fontweight="bold")
axes[1].set_xlabel("Product")
axes[1].set_ylabel("Revenue ($)")

plt.tight_layout()
plt.savefig("assets/sql_product_analysis.png")
plt.close()

fig, axes = plt.subplots(1, 2, figsize=(16, 5))

pmt = df["PaymentMethod"].value_counts()
pmt.plot(kind="bar", ax=axes[0], color="#4A72B0")
axes[0].set_title("Payment Methods — SQL: GROUP BY", fontsize=13, fontweight="bold")
axes[0].set_xlabel("Payment Method")
axes[0].set_ylabel("Count")

ost = df["OrderStatus"].value_counts()
ost.plot(kind="bar", ax=axes[1], color="#4A72B0")
axes[1].set_title("Order Statuses — SQL: GROUP BY", fontsize=13, fontweight="bold")
axes[1].set_xlabel("Order Status")
axes[1].set_ylabel("Count")

plt.tight_layout()
plt.savefig("assets/sql_payment_status.png")
plt.close()

fig, ax = plt.subplots(figsize=(10, 6))
laptop_data = df[df["Product"] == "Laptop"]
ax.scatter(range(len(laptop_data)), laptop_data["TotalPrice"], alpha=0.5, color="#4A72B0", s=30)
ax.set_title("Laptop Orders — SQL: WHERE Product = 'Laptop'", fontsize=13, fontweight="bold")
ax.set_xlabel("Order Index")
ax.set_ylabel("Total Price ($)")

plt.tight_layout()
plt.savefig("assets/sql_laptop_filter.png")
plt.close()

print("All screenshots saved to assets/")
