import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Initialize variables
ticker = "PLTR"
base_url = "https://financialmodelingprep.com/api/v3/stock_news"
page = 0
max_pages = 1000  # Number of pages to fetch
news_data = []
api_key = "<your_api_key>"

# Loop to fetch articles from multiple pages
while page < max_pages:
    response = requests.get(f"{base_url}?tickers={ticker}&page={page}&apikey={api_key}")
    if response.status_code == 200:
        news_data.extend(response.json())
        page += 1
        print(page)
    else:
        break

# Create a DataFrame from the fetched news data
df = pd.DataFrame(news_data)

# Convert 'publishedDate' to datetime and extract year and month
df['publishedDate'] = pd.to_datetime(df['publishedDate'])
df['YearMonth'] = df['publishedDate'].dt.to_period('M')

# Count the number of articles per month
article_counts = df['YearMonth'].value_counts().sort_index()

# Generate colors based on the number of articles
norm = plt.Normalize(article_counts.min(), article_counts.max())
colors = plt.cm.viridis(norm(article_counts.values))

# Plotting the bubble chart
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(article_counts.index.astype(str), article_counts, s=article_counts * 100, c=colors, alpha=0.6,
                     cmap='viridis')

# Add a color bar
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Number of Articles')

# Add annotations to display the number of articles when hovering over the bubbles
annot = ax.annotate("", xy=(0, 0), xytext=(20, 20),
                    textcoords="offset points", bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)


def update_annot(ind):
    pos = scatter.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = f"{article_counts.index[ind['ind'][0]]}: {article_counts.iloc[ind['ind'][0]]} articles"
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor('white')
    annot.get_bbox_patch().set_alpha(0.6)


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = scatter.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()


fig.canvas.mpl_connect("motion_notify_event", hover)

plt.xlabel('Year-Month')
plt.ylabel('Number of Articles')
plt.title('Number of Articles per Month for ' + ticker)
plt.xticks(rotation=45)
plt.show()
