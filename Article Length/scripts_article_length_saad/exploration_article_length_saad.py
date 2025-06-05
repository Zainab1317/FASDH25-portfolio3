import pandas as pd
import plotly.express as px

# Load data
articles_df = pd.read_csv("data/dataframes/length/length.csv")
monthly_df = pd.read_csv("data/dataframes/length/length-year-month.csv")

print("Articles Dataframe columns:", articles_df.columns)
print("Monthly Dataframe columns:", monthly_df.columns)

print("Articles Dataframe rows:")
print(articles_df.head())

print("Monthly Dataframe rows:")
print(monthly_df.head())

# Try filtering articles by length >= 50
filtered_articles = articles_df[articles_df['length'] >= 50]
print(f"Number of articles with length >= 50: {len(filtered_articles)}")

# Create 'date' from year, month, day for articles_df
articles_df['date'] = pd.to_datetime(articles_df[['year', 'month', 'day']])

# Create 'date' from year, month for monthly_df
monthly_df['date'] = pd.to_datetime(monthly_df[['year', 'month']].assign(day=1))

# Filter data from Sep 2023 onwards
cutoff = pd.to_datetime("2023-09-01")
articles_recent = articles_df[articles_df['date'] >= cutoff]
monthly_recent = monthly_df[monthly_df['date'] >= cutoff]

print(f"Number of recent articles (from Sep 2023): {len(articles_recent)}")
print(f"Number of recent months (from Sep 2023): {len(monthly_recent)}")

# Try grouping by date to count articles per day
daily_counts = articles_recent.groupby('date').size().reset_index(name='count')
print("Daily article counts sample:")
print(daily_counts.head())

# Check day names from dates
daily_counts['day_name'] = daily_counts['date'].dt.day_name()

#articles per day (test)
fig = px.bar(daily_counts, x='date', y='count', title="Test: Articles per day")
fig.show()

# Test monthly aggregation (sum of length)
monthly_recent_sorted = monthly_recent.sort_values('date')
fig3 = px.bar(monthly_recent_sorted, x='date', y='length-sum', title='Test: Monthly total article length')
fig3.show()


# Sort daily counts by date
daily_counts = daily_counts.sort_values('date')

# An empty list to store cumulative values
cumulative = []

# Variable to keep running total
running_total = 0

# Loop through the article counts row by row and calculate cumulative
for count in daily_counts['count']:
    running_total += count
    cumulative.append(running_total)

# Assign the cumulative list as a new column
daily_counts['cumulative_count'] = cumulative

# Display first few rows to inspect cumulative count
print("\nDaily counts with manually calculated cumulative count:")
print(daily_counts.head())
daily_counts_sorted = daily_counts.sort_values('date')

# An empty list to store cumulative values
cumulative = []

# Variable to keep running total
running_total = 0

# Loop through the article counts row by row and calculate cumulative
for count in daily_counts['count']:
    running_total += count
    cumulative.append(running_total)

# Assign the cumulative list as a new column
daily_counts_sorted['cumulative_count'] = cumulative

fig4 = px.line(daily_counts_sorted, x='date', y='cumulative_count', title="Test: Cumulative articles over time")
fig4.show()


