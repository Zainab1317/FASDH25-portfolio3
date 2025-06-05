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



# Remove Stop Words 
# This was copied from NLTK website
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

#Loop through each column in the list
for col in ["topic_1", "topic_2", "topic_3", "topic_4"]:
    #Go through each word in the column and use lambda to replace stop words with empty string 
    df[col] = df[col].apply(lambda word: "" if word in stop_words else word) #took the code from slides 14.1 and modified it using chatgpt to add "lambda" (entry 1 in AI doc)
    
#Combines the four topic keyword columns into a single column called "Topic Label."
df["Topic_Label"] = df[["topic_1", "topic_2", "topic_3", "topic_4"]].agg(", ".join, axis=1) #this was taken from homework 14.2 (topicmodelling-bar)







#Calculate the mean word count per article for each topic
# Group the data by topic and calculate the mean number of words used in articles under each topic
mean_count = df.groupby("Topic_Label")["Count"].mean().reset_index(name="Mean_Word_Count")

# Create a bar graph showing mean word count per topic
fig_mean_count = px.bar(
    mean_count,          
    x="Topic_Label",
    y="Mean_Word_Count",
    title="Mean Word Count for all Topics",
    text_auto = True,
    height = 600  # Chart height in pixels
)
fig_mean_count.show()

#save html file in the folder
fig_mean_count.write_html("mean_wordcount_for_all_topics_zainab.html")






# Get the topics by the total number of articles they appear in
# It counts the articles for each topic and then i have selected topics that i think are relavent 
my_chosen_topics = [1, 5, 11, 15, 17]

# Creates a new table that only includes rows from the 5 chosen topics 
df_top_topics = df[df["Topic"].isin(my_chosen_topics)].copy()

#Find the Daily topic trends by counting the number of times articles are written per day for each topic label
daily_trend = df_top_topics.groupby(["date", "Topic_Label"]).size().reset_index(name="Article Count")

# Create a line chart to show how article counts changed on daily basis for each top topic
fig_daily_facet = px.line(
    daily_trend,
    x = "date", #x-axis will have date
    y = "Article Count", #y-axis will have Article_counts
    color = "Topic_Label",  # Different color for each topic
    facet_col = "Topic_Label",   # Separate chart for each topic #asked chatgpt what would be the best way to make multiple graphs (entry 2 in AI doc)
    facet_col_wrap = 2,    # Arrange the facets in 2 columns per row
    title = "Daily Topic Trend Over Time for best 5 Topics"
)

fig_daily_facet.show()

#save html file in the folder
fig_daily_facet.write_html("Daily_topic_trend_overtime_for_best5_topics_zainab")

    




# Creates a column combining year and two-digit month as a string for monthly grouping
df["month_year_name"] = df ["year"].astype(str) + "-" + df ["month"].astype(str).str.zfill(2) #took help from chatgpt to understand what ".zfill(2)" does it basically helps in consisten formatting(entry 3 in AI doc)

# Filters the data to only include rows with the chosen 5 topics
df_monthly_top = df[df["Topic"].isin(my_chosen_topics)].copy()

# Counts the number of articles per topic label for each year-month combination
monthly_trend = df_monthly_top.groupby(["month_year_name", "Topic_Label"]).size().reset_index(name="Article Count")

# Make a bar graph to show topic trends by month
fig_monthly = px.bar(
    monthly_trend,
    x ="month_year_name",
    y = "Article Count",
    color = "Topic_Label",
    barmode = "group",    
    facet_col = "Topic_Label",
    facet_col_wrap = 2,
    title = "Monthly Topic Trends for best 5 Topics",
    text_auto = True,
    height = 600  # Chart height in pixels
)

fig_monthly.update_layout(xaxis_tickangle=60) # used chatgpt this isnt that necessary its only there so that reader can easily read the graph at an angle(entry 4 in AI doc)
fig_monthly.show()

#save html file in the folder
fig_monthly.write_html("monthly_topic_trends_for_best5_topics_zainab.html")








# Group only the chosen topics and count articles per topic per year
grouped = (
    df[df["Topic"].isin([1, 5, 11, 15, 17])]
    .groupby(["Topic_Label", "year"]) # Group by topic label and year
    .size()
    .reset_index(name="Article_Count") #Convert the group count to a DataFrame and rename the column to 'Article_Count'
)

#Create the Bar chart showing article counts by year for the 5 chosen topics
fig = px.bar(
    grouped,
    x='year',
    y='Article_Count',
    color='Topic_Label',
    barmode='group',
    title= 'Article counts of best 5 topics by years',
    labels={'Topic_Label': 'Topic', 'Article_Count': 'Number of Articles', 'year': 'Year'},
    text_auto = True,  # Show article count on top of each bar
    height = 500  # Chart height in pixels
)

fig.show()

#save html file in the folder
fig.write_html("article_countsof_best5topics_by_year_zainab.html")



