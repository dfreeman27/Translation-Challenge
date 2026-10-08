
import sqlite3
import pandas as pd

# ==================================================
# 1. SALES DATA
# ==================================================

sales_data = [
    ("Widget A", "Electronics", 29.99, 150, "2025-Q1"),
    ("Widget B", "Electronics", 49.99, 89, "2025-Q1"),
    ("Gadget X", "Accessories", 15.99, 300, "2025-Q1"),
    ("Widget A", "Electronics", 29.99, 200, "2025-Q2"),
    ("Gadget Y", "Accessories", 22.99, 175, "2025-Q2"),
    ("Widget C", "Electronics", 79.99, 50, "2025-Q2"),
    ("Gadget X", "Accessories", 15.99, 280, "2025-Q2"),
    ("Widget B", "Electronics", 49.99, 120, "2025-Q3"),
]

columns = [
    "product",
    "category",
    "unit_price",
    "quantity",
    "quarter"
]

# ==================================================
# 2. LOAD DATA INTO PANDAS
# ==================================================

df = pd.DataFrame(sales_data, columns=columns)

print("ORIGINAL PANDAS DATAFRAME")
print(df.to_string(index=False))


# ==================================================
# 3. CREATE SQLITE DATABASE AND LOAD DATA
# ==================================================

connection = sqlite3.connect("sales.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT NOT NULL,
        category TEXT NOT NULL,
        unit_price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        quarter TEXT NOT NULL
    )
""")

# Clear previous records to avoid duplicates when rerunning.
cursor.execute("DELETE FROM sales")

cursor.executemany("""
    INSERT INTO sales (
        product, category, unit_price, quantity, quarter
    )
    VALUES (?, ?, ?, ?, ?)
""", sales_data)

connection.commit()

print("\nSales data loaded into SQLite and pandas.")


# ==================================================
# 4. QUESTION 1: TOTAL REVENUE PER PRODUCT
# Revenue = unit_price * quantity
# ==================================================

print("\n" + "=" * 50)
print("QUESTION 1: TOTAL REVENUE PER PRODUCT")
print("=" * 50)

sql_query = """
    SELECT
        product,
        ROUND(SUM(unit_price * quantity), 2) AS total_revenue
    FROM sales
    GROUP BY product
    ORDER BY total_revenue DESC
"""

print("\nSQL Results:")
print(pd.read_sql_query(sql_query, connection).to_string(index=False))

print("\nPandas Results:")
revenue = (
    df.assign(revenue=df["unit_price"] * df["quantity"])
      .groupby("product")["revenue"]
      .sum()
      .round(2)
      .sort_values(ascending=False)
)

print(revenue.to_string())


# ==================================================
# 5. QUESTION 2: QUARTER WITH HIGHEST TOTAL QUANTITY
# ==================================================

print("\n" + "=" * 50)
print("QUESTION 2: HIGHEST-SELLING QUARTER")
print("=" * 50)

sql_query = """
    SELECT
        quarter,
        SUM(quantity) AS total_quantity
    FROM sales
    GROUP BY quarter
    ORDER BY total_quantity DESC
    LIMIT 1
"""

print("\nSQL Results:")
print(pd.read_sql_query(sql_query, connection).to_string(index=False))

print("\nPandas Results:")
quarter_totals = df.groupby("quarter")["quantity"].sum()
print(quarter_totals.sort_values(ascending=False).head(1).to_string())


# ==================================================
# 6. QUESTION 3: AVERAGE UNIT PRICE PER CATEGORY
# ==================================================

print("\n" + "=" * 50)
print("QUESTION 3: AVERAGE UNIT PRICE PER CATEGORY")
print("=" * 50)

sql_query = """
    SELECT
        category,
        ROUND(AVG(unit_price), 2) AS average_price
    FROM sales
    GROUP BY category
    ORDER BY category
"""

print("\nSQL Results:")
print(pd.read_sql_query(sql_query, connection).to_string(index=False))

print("\nPandas Results:")
average_prices = (
    df.groupby("category")["unit_price"]
      .mean()
      .round(2)
      .sort_index()
)

print(average_prices.to_string())


# ==================================================
# 7. QUESTION 4: PRODUCTS WITH TOTAL QUANTITY OVER 200
# ==================================================

print("\n" + "=" * 50)
print("QUESTION 4: PRODUCTS WITH QUANTITY OVER 200")
print("=" * 50)

sql_query = """
    SELECT
        product,
        SUM(quantity) AS total_quantity
    FROM sales
    GROUP BY product
    HAVING SUM(quantity) > 200
    ORDER BY total_quantity DESC
"""

print("\nSQL Results:")
print(pd.read_sql_query(sql_query, connection).to_string(index=False))

print("\nPandas Results:")
product_totals = df.groupby("product")["quantity"].sum()

print(
    product_totals[product_totals > 200]
    .sort_values(ascending=False)
    .to_string()
)


# ==================================================
# 8. CLOSE DATABASE CONNECTION
# ==================================================

connection.close()

print("\nAll questions answered using SQL and pandas!")










# ==================================================
# 5. CLOSE DATABASE CONNECTION
# ==================================================

connection.close()

print("\nDatabase connection closed.")
