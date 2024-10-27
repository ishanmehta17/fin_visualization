import requests
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import datetime
import webbrowser
import mplcursors  # To enable hover and tooltips

# URL and API Key
symbol = 'META'
url = "https://financialmodelingprep.com/api/v4/upgrades-downgrades?symbol=" + symbol + "&apikey=<your_api_key>"

# Fetch the data
response = requests.get(url)
if response.status_code != 200:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    exit()

# Parse the JSON data
data = response.json()

# Grade classification
strong_sell = {'Strong Sell'}
sell = {'Sell', 'Underweight', 'Underperform', 'Underperformer', 'Negative', 'Sector Underperform', 'Below Average',
        'Market Underperform', 'Reduce'}
hold = {'Hold', 'Hold Neutral', 'Neutral', 'In-Line', 'Market Perform', 'Sector Perform', 'Cautious', 'Mixed',
        'Peer Perform', 'Perform', 'Sector Weight', 'Equal-Weight'}
buy = {'Buy', 'Positive', 'Above Average', 'Accumulate', 'Overweight', 'Outperform', 'Market Outperform',
       'Sector Outperform', 'Speculative Buy', 'Sector Overweight'}
strong_buy = {'Strong Buy', 'Conviction Buy', 'Top Pick', 'Action List Buy'}

# Setup for visualization
timestamps = []
new_grades = []
previous_grades = []
y_values = []
urls = []
titles = []
publishers = []


# Prepare data for plotting
for entry in data:
    published_date = datetime.datetime.strptime(entry["publishedDate"], "%Y-%m-%dT%H:%M:%S.%fZ")
    new_grade = entry.get("newGrade")
    previous_grade = entry.get("previousGrade")

    if new_grade:
        timestamps.append(published_date)
        new_grades.append(new_grade)
        previous_grades.append(previous_grade)
        urls.append(entry.get("newsURL"))
        titles.append(entry.get("newsTitle"))
        publishers.append(entry.get("newsPublisher"))

        # Determine the y-value based on the grade classification
        if new_grade in strong_sell:
            y_values.append(-2)  # Strong Sell at y = -2
        elif new_grade in sell:
            y_values.append(-1)  # Sell at y = -1
        elif new_grade in hold:
            y_values.append(0)  # Hold at y = 0
        elif new_grade in buy:
            y_values.append(1)  # Buy at y = 1
        elif new_grade in strong_buy:
            y_values.append(2)  # Strong Buy at y = 2
        else:
            y_values.append(0)  # Default to Hold if not classified

# Create figure and axes
plt.style.use('seaborn-v0_8-darkgrid')
# Define shades for each category
color_map = {
    'Strong Sell': '#8B0000',  # Dark Red
    'Sell': '#FF6347',         # Tomato Red
    'Hold': '#FFD700',         # Gold
    'Buy': '#3CB371',          # Medium Sea Green
    'Strong Buy': '#006400'    # Dark Green
}
fig, ax = plt.subplots()
scatter_points = []
# Plot each grade with a specific color based on classification
for i, new_grade in enumerate(new_grades):
    if new_grade in strong_sell:
        color = color_map['Strong Sell']
    elif new_grade in sell:
        color = color_map['Sell']
    elif new_grade in hold:
        color = color_map['Hold']
    elif new_grade in buy:
        color = color_map['Buy']
    elif new_grade in strong_buy:
        color = color_map['Strong Buy']
    else:
        color = color_map['Hold']  # Default for unknown grades

    # Plot the new grade as a circle at the appropriate y-value
    point = ax.scatter(timestamps[i], y_values[i], color=color, s=100, label=new_grade)
    scatter_points.append(point)

    # Draw arrow if there's a change in grade
    if previous_grades[i] and previous_grades[i] != new_grades[i]:
        # Determine y-value for the previous grade
        if previous_grades[i] in strong_sell:
            prev_y = -2
        elif previous_grades[i] in sell:
            prev_y = -1
        elif previous_grades[i] in hold:
            prev_y = 0
        elif previous_grades[i] in buy:
            prev_y = 1
        elif previous_grades[i] in strong_buy:
            prev_y = 2
        else:
            prev_y = 0  # Default to Hold if not classified

            # Offset positions for arrow to start and end at circle edges
            arrow_start_y = prev_y + (y_values[i] - prev_y) * (1 - circle_radius / 100)
            arrow_end_y = y_values[i] - (y_values[i] - prev_y) * (1 - circle_radius / 100)

        # If previous grade is different, draw an arrow
        ax.annotate('', xy=(timestamps[i], y_values[i]), xytext=(timestamps[i], prev_y),
                    arrowprops=dict(facecolor='#A9A9A9', edgecolor='black', linewidth=0.05,  width=2.5))

# Format the x-axis with dates
ax.xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(dates.MonthLocator())
fig.autofmt_xdate()

# Title and labels
plt.title(symbol + ' Stock Grades Over Time')
plt.xlabel('Date')

# Y-axis tick marks labels (remove grade display)
y_ticks = [-2, -1, 0, 1, 2]
y_labels = ['Strong Sell', 'Sell', 'Hold', 'Buy', 'Strong Buy']
plt.yticks(y_ticks, y_labels)  # Set custom labels for y-axis

# Add hover functionality with tooltips
cursor = mplcursors.cursor(scatter_points, hover=True)


# Tooltip to show title, publisher, and URL on hover
@cursor.connect("add")
def on_add(sel):
    ind = scatter_points.index(sel.artist)
    sel.annotation.set(text=f"{titles[ind]}\n{publishers[ind]}\n{urls[ind]}")


# Function to handle mouse click events on circles
def onpick(event):
    # Find the index of the clicked point
    for i, scatter_point in enumerate(scatter_points):
        if scatter_point.contains(event)[0]:
            webbrowser.open(urls[i])  # Open the URL in the default web browser
            break


# Connect click event to the figure to make URLs clickable
fig.canvas.mpl_connect('button_press_event', onpick)

# Show the plot without the legend or labels
plt.show()
