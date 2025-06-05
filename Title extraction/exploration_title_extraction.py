import pandas as pd
import plotly.express as px
import re

# Load data
df = pd.read_csv("FASDH25-portfolio3/data/dataframes/title/title.csv")

# Drop rows with missing title or date
df = df.dropna(subset=["title", "year", "month", "day"])

# Combine year, month, day into single date column
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

# Show basic structure
print(df.head())
print(df.columns)

# Add a column for title word count
def count_words(text):
    return len(re.findall(r'\b\w+\b', text.lower()))

df['title_length'] = df['title'].apply(count_words)

title_length_counts = df['title_length'].value_counts().reset_index()
title_length_counts.columns = ['title_length', 'count']

fig = px.bar(title_length_counts, x='title_length', y='count',
              title='Title Length Distribution',
              labels={'title_length': 'Number of Words in Article Titles',
                      'count': 'Number of Titles'},
              text='count',
            color= 'count')

fig.show()
