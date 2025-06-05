import pandas as pd
import plotly.express as px
import re

#add list of stopwords 
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
    "just", "don", "should", "now", "al", "says"
])

# Load CSV and combine year/month/day into one column 
df = pd.read_csv("FASDH25-portfolio3/data/dataframes/title/title.csv")
df = df.dropna(subset=["title", "year", "month", "day"])
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

rows = []

# Loop through each title with date, tokenize words and filter stopwords
for date, title in zip(df['date'], df['title']):
    tokens = re.findall(r'\b\w+\b', title.lower())
    for word in tokens:
        if word in ["palestinian", "palestinians"]:
            word = "palestinians"  # normalize to one form
        if word in ["attack", "attacks"]:
            word = "attacks"
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

#bar graph to show the frequency of the top 10 words in all the article titles
# Total counts for each word 
total_word_counts = word_counts_per_date.groupby('word')['count'].sum().reset_index()

# Keep only the top 10 words
top_word_counts_bar = total_word_counts[total_word_counts['word'].isin(top_words)]

# Sort for better visualization
top_word_counts_bar = top_word_counts_bar.sort_values(by='count', ascending=False)

# Create bar chart
fig_bar = px.bar(
    top_word_counts_bar,
    x='word',
    y='count',
    title='Top 10 Most Frequent Words in Article Titles',
    labels={'word': 'Word', 'count': 'Total Frequency'},
    text='count'
)

# Improve bar chart layout
fig_bar.show()

#most used words in article titles that were published after october 7th 2023
filtered_words_df = words_df[words_df['date'] > pd.Timestamp("2023-10-07")]

#recalculate word counts
filtered_counts = filtered_words_df.groupby(['date', 'word']).size().reset_index(name='count')

#find top 10 most frequent words after Oct 7
top_filtered_words = filtered_counts.groupby('word')['count'].sum().sort_values(ascending=False).head(10).index

# Filter to only top words
top_filtered_word_counts = filtered_counts[filtered_counts['word'].isin(top_filtered_words)]

# Plot line graph for filtered range
fig2 = px.line(
    top_filtered_word_counts,
    x='date',
    y='count',
    color='word',
    title="Top 10 Most Frequent Words in Article Titles After October 7, 2023",
    labels={'count': 'Frequency', 'date': 'Date', 'word': 'Word'},
    markers=True
)

fig2.update_layout(xaxis_tickangle=45)
fig2.show()

#total frequency of the top 10 words after october 7th
# Sum total counts per word
total_word_counts = filtered_counts.groupby('word')['count'].sum().reset_index()

# Keep only the top 10
top_bar_words = total_word_counts.sort_values(by='count', ascending=False).head(10)

# Plot bar chart
fig_bar2 = px.bar(
    top_bar_words,
    x='word',
    y='count',
    title='Top 10 Most Frequent Words in Article Titles After October 7, 2023',
    labels={'word': 'Word', 'count': 'Total Frequency'},
    text='count'
)

fig_bar2.show()
