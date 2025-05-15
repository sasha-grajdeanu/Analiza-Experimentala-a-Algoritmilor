import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

#exercitiul 1
def exercise_1(df):
    print("==============EXERCITIUL 1=================")
    print("-----head-----")
    print(df.head())
    print("-----shape-----")
    print(df.shape)
    print("-----info-----")
    print(df.info())
    print("-----describe-----")
    print(df.describe())
    print("===============================")

    print("\nEducation\n", df["education"].count())
    print("Education: \n", df["education"].value_counts())
    print("----------------------------")
    print("\nRegion\n", df["region"].count())
    print("Region: \n", df["region"].value_counts())
    print("----------------------------")
    print("\nSex\n", df["sex"].count())
    print("Sex: \n", df["sex"].value_counts())
    print("----------------------------")
    print("\nVote\n", df["vote"].count())
    print("Vote: \n", df["vote"].value_counts())
    print("----------------------------")

    df["income"].dropna()
    print(df.groupby("income")["age"].mean())
    print("groupby:", df.groupby(["education", "vote"])["age"].mean())
    print("===============================")


#exercitul 2
def exercise_2(df):
    print("===============Exercitiul 2================")
    print("mean of income ", df["income"].mean())
    print("var of income ", df["income"].var())

    print("plot for income")
    plt.hist(df["income"].dropna())
    plt.show()

    print("plot for population")
    num_bins = 10
    plt.hist(df["population"], bins=num_bins, density=True, facecolor='blue', alpha=0.7)
    plt.show()

    print("boxplot for income")
    y = list(df["population"])
    plt.boxplot(y)
    plt.show()
    print("===============================")


#exercitiul 3
def exercise_3(df):
    print("===============Exercitiul 3================")
    print("First point")
    print("Covariance:\n", df[["age", "statusquo"]].cov())
    print("Correlation:\n", df[["age", "statusquo"]].corr())

    plt.figure(figsize=(5, 4))
    sns.heatmap(df[["age", "statusquo"]].corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Heatmap between Age and income")
    plt.show()

    print("\nSecond point")
    aligned_df = df[["age", "statusquo"]].dropna()
    corr_coef, p_value = pearsonr(aligned_df["age"], aligned_df["statusquo"])
    print(f"Pearson correlation coefficient: {corr_coef:.4f}")
    print(f"P-value: {p_value:.4f}")

    print("\nThird point")

    plt.figure(figsize=(6, 4))
    plt.scatter(aligned_df["age"], aligned_df["statusquo"], alpha=0.6)
    plt.xlabel("Age")
    plt.ylabel("Status quo")
    plt.title("Scatter Plot: Age vs Status quo")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    df = pd.read_csv("data/chile.csv")
    exercise_1(df)
    exercise_2(df)
    exercise_3(df)