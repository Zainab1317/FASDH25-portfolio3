import pandas as pd

# Load the dataset
df = pd.read_csv("C:/Users/batoo/Downloads/FASDH25-portfolio3/data/dataframes/topic-model/topic-model.csv")

#removing unclassified
df = df[df["Topic"] != -1]

# Print the first 20 rows of the DataFrame
print(df.head(20))

#View all the column names in the dataset
print("\nColumn names in the dataset:")
print(df.columns)

# Create a datetime column
df["date"] = pd.to_datetime({
    "year": df["year"],
    "month": df["month"],
    "day": df["day"]
})

# Filter for years 2023 and 2024
df_23_24 = df[df["date"].dt.year.isin([2023, 2024])]

# Group by year and count articles
articles_per_year = df_23_24.groupby(df_23_24["date"].dt.year).size().reset_index(name="Article Count")

# Rename the year column for clarity
articles_per_year = articles_per_year.rename(columns={"date": "Year"})

# Print the table
print("Articles published per year:")
print(articles_per_year)

# Print the total count
total_count = articles_per_year["Article Count"].sum()
print(f"\nTotal articles published in 2023 and 2024: {total_count}")

#View the number of rows and columns in the dataset
print("\nShape of the dataset (rows, columns):")
print(df.shape)

