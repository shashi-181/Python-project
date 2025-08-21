# --- Import Libraries ---
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import json

# --- Load Dataset (Canada) ---
df = pd.read_csv("data/CAvideos.csv")

# --- Load Category Mapping (Canada JSON) ---
with open("data/CA_category_id.json", "r") as f:
    categories = json.load(f)

# Convert JSON into dictionary {id: category_name}
category_dict = {}
for item in categories["items"]:
    category_dict[int(item["id"])] = item["snippet"]["title"]

# Add a new column with category names
df["category_name"] = df["category_id"].map(category_dict)

print("✅ Data Loaded Successfully!\n")
print(df.head())   # preview first few rows

# -------------------------------------------------
# 1️⃣ Bar Chart: Top 10 Categories by Total Views
# -------------------------------------------------
top_categories = df.groupby("category_name")["views"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(
    x=top_categories.values,
    y=top_categories.index,
    hue=top_categories.index,    # fixes seaborn warning
    palette="viridis",
    legend=False
)
plt.title("Top 10 Video Categories by Total Views (Canada)")
plt.xlabel("Total Views")
plt.ylabel("Category")
plt.show()

# -------------------------------------------------
# 2️⃣ Scatter Plot: Likes vs Views
# -------------------------------------------------
plt.figure(figsize=(8,6))
sns.scatterplot(x="views", y="likes", data=df, alpha=0.5, color="blue")
plt.title("Likes vs Views (Canada)")
plt.xlabel("Views")
plt.ylabel("Likes")
plt.xlim(0, 1e7)   # avoid extreme outliers
plt.show()

# -------------------------------------------------
# 3️⃣ Scatter Plot: Dislikes vs Views
# -------------------------------------------------
plt.figure(figsize=(8,6))
sns.scatterplot(x="views", y="dislikes", data=df, alpha=0.5, color="red")
plt.title("Dislikes vs Views (Canada)")
plt.xlabel("Views")
plt.ylabel("Dislikes")
plt.xlim(0, 1e7)   # avoid extreme outliers
plt.show()

# -------------------------------------------------
# 4️⃣ Word Cloud: Common Keywords in Titles
# -------------------------------------------------
text = " ".join(title for title in df["title"].astype(str))
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

plt.figure(figsize=(12,6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Common Keywords in Trending Video Titles (Canada)")
plt.show()