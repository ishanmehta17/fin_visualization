import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import requests
import mplcursors
import webbrowser

symbol = 'MSFT'
api_key = '<api_key>'

# Fetch price target data
price_target_url = "https://financialmodelingprep.com/api/v4/price-target?symbol=" + symbol + "&apikey=" + api_key
response = requests.get(price_target_url)
price_target_data = response.json()

# Fetch historical data
historical_url = "https://financialmodelingprep.com/api/v3/historical-price-full/" + symbol + "?apikey=" + api_key
response = requests.get(historical_url)
historical_data = response.json()

# Parse price target data
target_dates = [datetime.fromisoformat(item["publishedDate"].replace("Z", "")) for item in price_target_data]
prices_start = [item["priceWhenPosted"] for item in price_target_data]
prices_end = [item["adjPriceTarget"] for item in price_target_data]
titles = [item["newsTitle"] for item in price_target_data]
urls = [item["newsURL"] for item in price_target_data]
analysts = [item["analystName"] for item in price_target_data]
publishers = [item["newsPublisher"] for item in price_target_data]
companies = [item["analystCompany"] for item in price_target_data]

# Parse historical data
historical = historical_data["historical"]
historical_dates = [datetime.strptime(item["date"], "%Y-%m-%d") for item in historical]
adj_close_prices = [item["adjClose"] for item in historical]

# Filter historical data to match the minimum date in price target data
min_date = min(target_dates)
historical_dates_filtered = [date for date in historical_dates if date >= min_date]
adj_close_prices_filtered = adj_close_prices[:len(historical_dates_filtered)]

# Plotting
fig, ax = plt.subplots(figsize=(14, 7))

# Dictionary to map artist (dot) to URL
dot_to_url = {}

# Plot price target arrows and dots
yellow_dots = []  # Store yellow dots for hover interaction
for date, start, end, title, url, analyst, publisher, company in zip(
        target_dates, prices_start, prices_end, titles, urls, analysts, publishers, companies
):
    # Plot only the arrow for the price target data (Price When Posted -> Price Target)
    arrow_color = "dodgerblue" if end > start else "blue"
    ax.annotate(
        "",
        xy=(date, end),
        xytext=(date, start),
        arrowprops=dict(arrowstyle="->", color=arrow_color, lw=1)
    )
    # Yellow dot for price when posted
    scatter_start = ax.scatter(
        date, start, color="yellow", label="Price When Posted" if date == target_dates[0] else ""
    )
    scatter_start.set_gid(
        f"Title: {title}\nURL: {url}\nAnalyst: {analyst}\nPublisher: {publisher}\nAnalyst Company: {company}")
    dot_to_url[scatter_start] = url  # Map the dot to its URL
    yellow_dots.append(scatter_start)  # Store yellow dot for hover
    # Green or red dot for price target
    dot_color = "green" if end > start else "red"
    ax.scatter(date, end, color=dot_color, label="Price Target" if date == target_dates[0] else "")

# Plot historical adjClose prices without arrows
ax.plot(historical_dates_filtered, adj_close_prices_filtered, label="Adj Close Price", color="lightblue",
        linestyle="--")

# Format x-axis to show year, month, and day
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%b-%d"))
plt.xticks(rotation=45)

# Labels and title
plt.xlabel("Date")
plt.ylabel("Price")
plt.title(f"Price Target with Historical Adj Close Prices for {symbol}")
plt.grid(True, linestyle="--", alpha=0.5)

# Add legend
plt.legend()

# Set axis limits for better visibility
plt.ylim(min(prices_start + prices_end + adj_close_prices_filtered) - 1,
         max(prices_start + prices_end + adj_close_prices_filtered) + 1)
plt.tight_layout()

# Add hover interactivity with mplcursors (only on yellow dots)
cursor = mplcursors.cursor(yellow_dots, hover=True)  # Only interact with yellow dots


@cursor.connect("add")
def on_add(sel):
    sel.annotation.set_text(sel.artist.get_gid())
    sel.annotation.set_fontsize(10)
    sel.annotation.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='gray'))


# Make yellow dots clickable to open URL
def on_click(event):
    for artist, url in dot_to_url.items():
        if artist.contains(event)[0]:  # Check if the clicked area is the artist
            webbrowser.open(url)  # Open the corresponding URL
            break


fig.canvas.mpl_connect("button_press_event", on_click)

# Show plot
plt.show()
