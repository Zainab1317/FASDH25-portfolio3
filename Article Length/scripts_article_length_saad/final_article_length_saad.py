#Load libraries
import pandas as pd
import plotly.express as px

# Load datasets
articles_df = pd.read_csv("data/dataframes/length/length.csv") # Article-level data
monthly_df = pd.read_csv("data/dataframes/length/length-year-month.csv") # monthly data

# Filter articles with length >= 50 (homework)
articles_df = articles_df[articles_df['length'] >= 50]

# Create 'date' column for articles_df by combining year, month, day (homework 14.1)
articles_df['date'] = pd.to_datetime(articles_df[['year', 'month', 'day']])

# Convert year, month to datetime for monthly_df (homework 14.1)
monthly_df['date'] = pd.to_datetime(monthly_df[['year', 'month']].assign(day=1))

# Filter data from Sep 2023 onwards (homework)
cutoff_date = pd.to_datetime("2023-08-01")
articles_df = articles_df[articles_df['date'] >= cutoff_date]
monthly_df = monthly_df[monthly_df['date'] >= cutoff_date]

# Group articles for the same date and count frequency (homework and chatgpt#1)
daily_counts = articles_df.groupby('date').size().reset_index(name='article_count') 
#Extract the name of the day (e.g., Monday, Tuesday) from the 'date' column and store it in a new column 'day'
daily_counts['day_name'] = daily_counts['date'].dt.day_name() 
# Create a formatted date label for cleaner display on x-axis in plots
daily_counts['date_label'] = daily_counts['date'].dt.strftime('%b %d, %Y')

#Plot: Number of Articles Per Day
fig_daily = px.bar(
    daily_counts,x='date_label',y='article_count',title='Number of Articles Per Day',
    labels={'date_label': 'Date', 'article_count': 'Number of Articles'},
    color='article_count',
    color_continuous_scale='Inferno'

)


fig_daily.show()
fig_daily.write_html("number_of_articles_per_day_saad.html")


# Articles per weekday (chatgpt#2)

articles_df['weekday'] = articles_df['date'].dt.day_name()

# Define order of weekdays
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Count articles per weekday
weekday_counts = (
    articles_df.groupby('weekday').size().reindex(weekday_order).fillna(0)
    .reset_index(name='article_count')
)


# Plot: Articles Published Per Weekday
fig_weekday = px.bar(
     weekday_counts,
    x='weekday',
    y='article_count',
    title='Articles Published Per Day of the Week',
    labels={'weekday_name': 'Weekday', 'article_count': 'Number of Articles'},
    color='article_count',
    color_continuous_scale='Cividis'
)
fig_weekday.show()
fig_weekday.write_html("articles_per_weekday_saad.html") 

# Monthly article length sums (chatgpt#3)
monthly_df = monthly_df.sort_values('date') #homework
monthly_df['month'] = monthly_df['date'].dt.strftime('%b %Y') # taken from chatgpt#1

# Plot: Total Article Length by Month
fig_monthly_length = px.bar(
    monthly_df,
    x='month',
    y='length-sum',
    title='Total Article Length by Month (After Sep 2023)',
    labels={'month_label': 'Month', 'length-sum': 'Total Article Length (words)'},
    color='length-sum',
    color_continuous_scale='Plasma'
)
fig_monthly_length.show()
fig_monthly_length.write_html("total_article_length_by_month_saad.html")

# Cumulative Articles Over Time (chatgpt#4)
daily_counts = daily_counts.sort_values('date')
# an empty list to store cumulative values
cumulative = []

# Variable to keep running total
running_total = 0

# Loop through the article counts row by row and calculate cumulative
for count in daily_counts['article_count']:
    running_total += count
    cumulative.append(running_total)

# Assign the cumulative list as a new column
daily_counts['cumulative_count'] = cumulative


fig_cumulative = px.line(
    daily_counts,
    x='date',
    y='cumulative_count',
    title='Cumulative Number of Articles Over Time',
    labels={'date': 'Date', 'cumulative_count': 'Cumulative Articles'}
)

fig_cumulative.show()
fig_cumulative.write_html("cumulative_articles_over_time_saad.html")

#Facet Grids for the first graph - number of articles per day (chatgpt#5)

# Create 'month_label' for facets and 'day_of_month' for x-axis
daily_counts['month_label'] = daily_counts['date'].dt.strftime('%b %Y') 
daily_counts['day_of_month'] = daily_counts['date'].dt.day              



# Create faceted bar chart by month (x-axis = day of month)
fig_facet_month = px.bar(
    daily_counts,
    x='day_of_month',
    y='article_count',
    facet_col='month_label', facet_col_wrap=3,
    title='Daily Article Counts Faceted by Month',
    labels={'day_of_month': 'Day of Month', 'article_count': 'Number of Articles'},
    
    height=400,
    width=1200
)


fig_facet_month.update_layout(
    height=600,
    showlegend=False
)
fig_facet_month.show()
fig_facet_month.write_html("daily_article_counts_faceted_by_month_saad.html") 

# Plot: Distribution of Article Lengths
fig_length_distribution = px.histogram(
    articles_df,
    x='length',
    title='Distribution of Article Lengths',
    labels={'length': 'Article Length (words)', 'count': 'Count'},
   
)

# Add average line (covered in class)
mean_length=articles_df['length'].mean()
fig_length_distribution.add_vline(
    mean_length, 
    line_dash="dash", 
    line_color="black",
    annotation_text=f"Average: {articles_df['length'].mean():} words" 
)

fig_length_distribution.show()
fig_length_distribution.write_html("distribution_of_article_lengths_saad.html")

#(chatgpt#6)
print("Publishing Statistics") 
print(f"Total articles analyzed: {len(articles_df)}")
print(f"Date range: {articles_df['date'].min().strftime('%B %d, %Y')} to {articles_df['date'].max().strftime('%B %d, %Y')}")
print(f"Average article length: {articles_df['length'].mean():} words")
print(f"Most productive day: {articles_df['date'].dt.day_name().mode()[0]}")
print(f"Average articles per day: {len(articles_df) / len(daily_counts):}")
