import pandas as pd
import plotly.express as px
import re

custom_stopwords = set([
       "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
    "you", "your", "yours", "yourself", "yourselves", "he", "him",
    "his", "himself", "she", "her", "hers", "herself", "it", "its",
    "itself","the", "they", "them", "their", "theirs", "themselves", "what",
    "which", "who", "whom", "this", "that", "these", "those", "am", "is",
    "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "having", "do", "does", "did", "day", "doing", "a", "an", "the", "and", "but",
    "if", "in", "or", "because", "as", "until", "while", "of", "at", "by", "for",
    "with", "about", "against", "between", "into", "through", "during",
    "before", "after", "above", "below", "to", "from", "up", "down", "in",
    "out", "on", "off", "over", "under", "again", "further", "then", "once",
    "here", "there", "when", "where", "why", "how", "all", "any", "both",
    "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not",
    "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will",
    "just", "don", "should", "now", "al"
])

# Load CSV and combine year/month/day into datetime
df = pd.read_csv("FASDH25-portfolio3/data/dataframes/title/title.csv")
df = df.dropna(subset=["title", "year", "month", "day"])
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

rows = []

# Loop through each title with date, tokenize words and filter stopwords
for date, title in zip(df['date'], df['title']):
    tokens = re.findall(r'\b\w+\b', title.lower())
    for word in tokens:
        if word not in custom_stopwords:
            rows.append((date, word))

words_df = pd.DataFrame(rows, columns=['date', 'word'])

# Count word occurrences by date
word_counts_per_date = words_df.groupby(['date', 'word']).size().reset_index(name='count')

# Find top 10 most frequent words overall
top_words = word_counts_per_date.groupby('word')['count'].sum().sort_values(ascending=False).head(10).index

# Filter counts to only top words
top_word_counts = word_counts_per_date[word_counts_per_date['word'].isin(top_words)]

# Plot line graph of word frequency over time
fig = px.line(
    top_word_counts,
    x='date',
    y='count',
    color='word',
    title="Top 10 Most Frequent Words in Article Titles Over Time",
    labels={'count': 'Frequency', 'date': 'Date', 'word': 'Word'},
    markers=True
)

# Improve x-axis labels for readability
fig.update_layout(xaxis_tickangle=45)
fig.show()
