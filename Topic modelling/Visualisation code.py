# Importing required libraries such as pandas used to work with DataFrames
import pandas as pd

# importing plotly which is used to make interactive graphs 
import plotly.express as px


# Load the dataset 
df = pd.read_csv(r"C:\Users\batoo\Downloads\FASDH25-portfolio3\data\dataframes\topic-model\topic-model.csv")

# Create a new column called date from year, month and day columns 
df["date"] = pd.to_datetime(df[["year", "month", "day"]])

#filter out unassigned topics (Topic = -1)
# It keeps only those rows where a topic is assigned and creates a new copy of the filtered data
df = df[df["Topic"] != -1].copy()

# Remove Stop Words as they don't add much meaning
# Copied from NLTK website
stop_words = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 
    'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 
    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 
    'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 
    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 
    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
}

# Go through each of the 4 topic keyword columns and remove stop words using a normal loop

# Loop through each topic column
for col in ["topic_1", "topic_2", "topic_3", "topic_4"]:
    cleaned_words = []  # to store the cleaned column

    for word in df[col]:
        if word in stop_words:
            cleaned_words.append("")
        else:
            cleaned_words.append(word)

    # Assign the cleaned list back to the column in df
    df[col] = cleaned_words
    

# Combine the 4 topic keywords into a single label per topic
# It adds all the words in the 4 separate columns into one column and names it Topic Label
df["Topic_Label"] = df[["topic_1", "topic_2", "topic_3", "topic_4"]].agg(", ".join, axis=1)


# Get the top 5 most common topics by the total number of articles they appear in
# It counts the articles for each topic and selects the 5 with the highest count
my_chosen_topics = [1, 5, 11, 15, 17]

# Creates a new table that only includes rows from the 5 topics 
df_top_topics = df[df["Topic"].isin(my_chosen_topics)].copy()

#Find the Daily topic trends by counting the number of times articles are written per day for each topic label
daily_trend = df_top_topics.groupby(["date", "Topic_Label"]).size().reset_index(name="Article Count")

# Create a line chart to show how article counts changed on daily basis for each top topic
fig_daily_facet = px.line(
    daily_trend,
    x = "date",
    y = "Article Count",
    color = "Topic_Label",  # Different color for each topic
    facet_col = "Topic_Label",   # Separate chart for each topic
    facet_col_wrap = 2,    # Wrap the chart into 2 columns
    title = "Daily Topic Trend Over Time for Top 5 Topics"
)

fig_daily_facet.show()

# Create a column with year and month to help while we group them as month later
# It converts the year and month to strings, adds a dash and makes sure that month is of two digits
df["year_month"] = df ["year"].astype(str) + "-" + df ["month"].astype(str).str.zfill(2)

# Filters the data to only include rows with the top 5 topics
df_monthly_top = df[df["Topic"].isin(my_chosen_topics)].copy()

# Counts how many articles exist of each topic label for each year and month 
monthly_trend = df_monthly_top.groupby(["year_month", "Topic_Label"]).size().reset_index(name="Article Count")


# Make a bar graph to show topic trends by month
fig_monthly = px.bar(
    monthly_trend,
    x ="year_month",
    y = "Article Count",
    color = "Topic_Label",
    barmode = "group",    # Bars are grouped side by side for each topic per month
    facet_col = "Topic_Label",
    facet_col_wrap = 2,
    title = "Monthly Topic Trends for Top 5 Topics",
    text_auto = True,
    height = 600
)

fig_monthly.update_layout(xaxis_tickangle=45) # Rotates the x-axis labels to make them easier to read
fig_monthly.show()


# Finding the most used words per topic
# This selects the five columns, Topic label - the human readable name and the four topic columns associated with the articles 
# It uses melt function so that each has only one keyword and the topic label is repeated for each word

keyword_df = df[["Topic_Label", "topic_1", "topic_2", "topic_3", "topic_4"]].melt(
    id_vars="Topic_Label",  # Keeps the topic label the same
    value_name="Keyword"   # creates one column for all keywords from the four keyword columns
)


# Count how often each keyword appears in each topic
# Groups both topic and keywords and counts how many times each keyword appears 
top_words_by_topic = keyword_df.groupby(["Topic_Label", "Keyword"]).size().reset_index(name='Frequency')

# Sorts keywords by topic and within each topic in order of how frequent they are
top_words_by_topic = top_words_by_topic.sort_values(["Topic_Label", "Frequency"], ascending=[True, False])

# Get top 5 most used keyword for each topic

# Create an empty list 
top_keywords_list = []

# Go through each unique label one by one 
for topic in top_words_by_topic["Topic_Label"].unique():

    #From the sorted data above take the top 5 keywords for the particular topic
    top5 = top_words_by_topic[top_words_by_topic["Topic_Label"] == topic].head(5)

    #Add these top 5 rows to the list 
    top_keywords_list.append(top5)


# Combine the top 5 keywords from all the topics into a single table 
top5_keywords_df = pd.concat(top_keywords_list)


# Limit to top 5 topics for visualization

# Get a list of Topic Label names that are part of the most discussed topics 
top_topic_labels = df[df["Topic"].isin(my_chosen_topics)]["Topic_Label"].unique()

# Filter the top 5 keyowrd data to keep only keywords from those top topics 
filtered_keywords_df = top5_keywords_df[top5_keywords_df["Topic_Label"].isin(top_topic_labels)]


#Calculate the average word count per article for each topic

# Group the data by topic and calculate the average number of words used in articles under each topic
average_count = df.groupby("Topic_Label")["Count"].mean().reset_index(name="Average_Word_Count")

# Create a bar graph showing average word count per topic
fig_average_count = px.bar(
    average_count,          # Use the table with average word counts
    x="Topic_Label",
    y="Average_Word_Count",
    title="Average Word Count per Topic",
    text_auto = True,
    height = 600
)
fig_average_count.show()

# Group only the chosen topics and count articles per topic per year
grouped = (
    df[df["Topic"].isin([1, 5, 11, 15, 17])]
    .groupby(["Topic_Label", "year"])
    .size()
    .reset_index(name="Article_Count")
)

#Create the Bar chart 
fig = px.bar(
    grouped,
    x='year',
    y='Article_Count',
    color='Topic_Label',
    barmode='group',
    title='Article Counts by Topic and Year',
    labels={'Topic_Label': 'Topic', 'Article_Count': 'Number of Articles', 'year': 'Year'},
    text_auto = True,
    height = 500
)

fig.show()

# Count how many times hamas and israel is mentioned in the article titles

# Filter the dataset to only keep the articles that beling to the top 10 topics

filtered_df = df[df["Topic_Label"].isin(my_chosen_topics)].copy()

# Check if 'hamas' or 'israel' appear in any of the 4 topic keyword columns
filtered_df["hamas_mention"] = (
    (filtered_df["topic_1"].str.contains("hamas", case=False, na=False)) |
    (filtered_df["topic_2"].str.contains("hamas", case=False, na=False)) |
    (filtered_df["topic_3"].str.contains("hamas", case=False, na=False)) |
    (filtered_df["topic_4"].str.contains("hamas", case=False, na=False))
).astype(int)

filtered_df["israel_mention"] = (
    (filtered_df["topic_1"].str.contains("israel", case=False, na=False)) |
    (filtered_df["topic_2"].str.contains("israel", case=False, na=False)) |
    (filtered_df["topic_3"].str.contains("israel", case=False, na=False)) |
    (filtered_df["topic_4"].str.contains("israel", case=False, na=False))
).astype(int)

# Count mentions per year
mentions_per_month = filtered_df.groupby("month")[["hamas_mention", "israel_mention"]].sum().reset_index()

#Create line chart for hamas
fig = px.line(
    mentions_per_month,
    x="month",
    y="hamas_mention",
    markers=True,
    labels={"hamas_mention": "Mentions", "month": "Month"},
)

# Add second line for israel using add_scatter
fig.add_scatter(
    x=mentions_per_month["month"],
    y=mentions_per_month["israel_mention"],
    mode='lines+markers',
    name='israel_mention'
)

# Update title and layout
fig.update_layout(
    title="Mentions of 'hamas' and 'israel' in article titles per month",
    xaxis=dict(dtick=1),
    yaxis_title="Number of Mentions"
)

fig.show()
