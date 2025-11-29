import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

# -----------------------------
# 1. Load Data
# -----------------------------
df = pd.read_csv("amazon_mobiles_under_30k.csv")

# -----------------------------
# 2. Clean Price Column
# -----------------------------
df["Price (INR)"] = (
    df["Price (INR)"].astype(str)
    .str.replace(",", "", regex=False)
    .str.extract(r'(\d+)', expand=False)
)
df["Price (INR)"] = pd.to_numeric(df["Price (INR)"], errors="coerce")

# -----------------------------
# 3. Clean Rating Column
# -----------------------------
df["Rating"] = (
    df["Rating"].astype(str)
    .str.extract(r'(\d+\.\d+)', expand=False)
)
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

# -----------------------------
# 4. Extract Brand
# -----------------------------
df["Brand"] = df["Product Name"].astype(str).str.split().str[0]

# -----------------------------
# 5. Extract RAM
# -----------------------------
df["RAM"] = df["Product Name"].astype(str).str.extract(r'(\d+\s?GB)', expand=False)
df["RAM"] = df["RAM"].str.replace(" ", "", regex=False)

# -----------------------------
# 6. Save Cleaned CSV
# -----------------------------
df.to_csv("cleaned_amazon_mobiles_under_30k.csv", index=False)
print("✔ Cleaned CSV saved as: cleaned_amazon_mobiles_under_30k.csv")

# -----------------------------
# 7. Create FIGURE folder
# -----------------------------
os.makedirs("figs", exist_ok=True)
fig_files = []

# -----------------------------
# 8. Price Histogram
# -----------------------------
plt.figure(figsize=(7,5))
plt.hist(df["Price (INR)"].dropna(), bins=15)
plt.title("Price Distribution of Mobiles (INR)")
plt.xlabel("Price (INR)")
plt.ylabel("Count")
p1 = "figs/price_hist.png"
plt.savefig(p1, bbox_inches="tight")
plt.close()
fig_files.append(p1)

# -----------------------------
# 9. Rating Histogram
# -----------------------------
plt.figure(figsize=(7,5))
plt.hist(df["Rating"].dropna(), bins=10)
plt.title("Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Count")
p2 = "figs/rating_hist.png"
plt.savefig(p2, bbox_inches="tight")
plt.close()
fig_files.append(p2)

# -----------------------------
# 10. Brand Pie Chart
# -----------------------------
brand_counts = df["Brand"].value_counts().nlargest(6)
plt.figure(figsize=(7,7))
plt.pie(brand_counts, labels=brand_counts.index, autopct="%1.1f%%")
plt.title("Top Brand Share")
p3 = "figs/brand_pie.png"
plt.savefig(p3, bbox_inches="tight")
plt.close()
fig_files.append(p3)

# -----------------------------
# 11. RAM Pie Chart
# -----------------------------
ram_counts = df["RAM"].fillna("Unknown").value_counts().nlargest(6)
plt.figure(figsize=(7,7))
plt.pie(ram_counts, labels=ram_counts.index, autopct="%1.1f%%")
plt.title("RAM Distribution")
p4 = "figs/ram_pie.png"
plt.savefig(p4, bbox_inches="tight")
plt.close()
fig_files.append(p4)

# -----------------------------
# 12. Average Price by Brand
# -----------------------------
avg_price_brand = df.groupby("Brand")["Price (INR)"].mean().dropna().sort_values().tail(10)
plt.figure(figsize=(10,5))
plt.bar(avg_price_brand.index, avg_price_brand.values)
plt.title("Average Price by Brand (Top 10)")
plt.xlabel("Brand")
plt.ylabel("Average Price (INR)")
plt.xticks(rotation=45)
p5 = "figs/avg_price_brand.png"
plt.savefig(p5, bbox_inches="tight")
plt.close()
fig_files.append(p5)

# -----------------------------
# 13. Scatter Plot (Price vs Rating)
# -----------------------------
plt.figure(figsize=(8,5))
plt.scatter(df["Price (INR)"], df["Rating"])
plt.title("Price vs Rating")
plt.xlabel("Price (INR)")
plt.ylabel("Rating")
p6 = "figs/price_vs_rating.png"
plt.savefig(p6, bbox_inches="tight")
plt.close()
fig_files.append(p6)

# -----------------------------
# 14. Create PDF Report
# -----------------------------
pdf_path = "EDA_report_amazon_mobiles_under_30k.pdf"

with PdfPages(pdf_path) as pdf:
    
    # Title Page
    plt.figure(figsize=(11,8.5))
    plt.text(0.5, 0.6, "📊 EDA Report\nAmazon - Mobiles Under 30,000", 
             ha='center', fontsize=24)
    plt.text(0.5, 0.45, f"Total Rows: {df.shape[0]}\nTotal Columns: {df.shape[1]}", 
             ha='center', fontsize=14)
    plt.axis("off")
    pdf.savefig()
    plt.close()
    
    # Summary Page
    plt.figure(figsize=(11,8.5))
    text = (
        f"✔ Total products: {df.shape[0]}\n"
        f"✔ Unique Brands: {df['Brand'].nunique()}\n"
        f"✔ Min Price: {df['Price (INR)'].min()}\n"
        f"✔ Median Price: {df['Price (INR)'].median()}\n"
        f"✔ Max Price: {df['Price (INR)'].max()}\n"
        f"✔ Ratings Available: {df['Rating'].notnull().sum()}"
    )
    plt.text(0.05, 0.9, "Summary Statistics", fontsize=18)
    plt.text(0.05, 0.8, text, fontsize=12)
    plt.axis("off")
    pdf.savefig()
    plt.close()
    
    # Add all saved figures
    for f in fig_files:
        img = plt.imread(f)
        plt.figure(figsize=(11,8.5))
        plt.imshow(img)
        plt.axis("off")
        pdf.savefig()
        plt.close()

print("✔ PDF report created:", pdf_path)
print("✔ Figures saved in 'figs/' folder")
