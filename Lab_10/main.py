import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

df = pd.read_csv("data/chile.csv")

print(df.head())
print(df.shape)
print(df.info())
print(df.describe())

print("\neducation\n", df["education"].count())
print(df["education"].value_counts())
print("vote: \n", df["vote"].value_counts())

df["income"].dropna()
print(df.groupby("income")["age"].mean())

print("groupby:", df.groupby(["education", "vote"])["age"].mean())


print("mean of income ", df["income"].mean())
print("var of income ", df["income"].var())

plt.hist(df["income"].dropna())
plt.show()

num_bins = 10
plt.hist(df["population"], bins=num_bins, density=True, facecolor='blue', alpha=0.7)
plt.show()

y = list(df["population"])
plt.boxplot(y)
plt.show()

print("Covariance:\n", df[["age", "income"]].cov())
print("Correlation:\n", df[["age", "income"]].corr())

sns.heatmap(df[["age", "income"]].corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap between Age and income")
plt.show()

age = df["age"].dropna()
income = df["income"].dropna()
aligned_df = df[["age", "income"]].dropna()
corr_coef, p_value = pearsonr(aligned_df["age"], aligned_df["income"])

print(f"Pearson correlation coefficient: {corr_coef:.4f}")
print(f"P-value: {p_value:.4f}")

plt.scatter(aligned_df["age"], aligned_df["income"], alpha=0.6, color='purple')
plt.xlabel("Age")
plt.ylabel("Income")
plt.title("Scatter Plot: Age vs Income")
plt.grid(True)
plt.show()