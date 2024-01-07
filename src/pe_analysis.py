from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import pandas as pd
import requests
from scipy.stats import norm

# Fetching data from the API
symbol = 'AAPL'
api_key = 'dummy'

# Fetch key metrics data
url_key_metrics = f'https://financialmodelingprep.com/api/v3/key-metrics/{symbol}?period=quarter&limit=400&apikey={api_key}'
response_key_metrics = requests.get(url_key_metrics)
data_key_metrics = response_key_metrics.json()

# Extract PE ratios
pe_ratios = [item.get('peRatio') for item in data_key_metrics][::-1]

# Create DataFrame
df = pd.DataFrame({'pe_ratios': pe_ratios})

# Display summary statistics
stats = df.describe()

# Extract relevant statistics
min_value = stats.loc['min'].mean()
mean = stats.loc['mean'].mean()
std = stats.loc['std'].mean()
q25 = stats.loc['25%'].mean()
q75 = stats.loc['75%'].mean()
mu = stats.loc['50%'].mean()
max_value = stats.loc['max'].mean()

# Create two separate figure windows
fig1 = plt.figure(figsize=(5, 5))
fig2 = plt.figure(figsize=(10, 6))

# Plot the data on each figure
ax1 = fig1.add_subplot(111)
ax2 = fig2.add_subplot(111)

x = np.linspace(min_value, max_value, 1000)

# Generate the normal distribution based on mean (mu) and standard deviation (std)
pdf = norm.pdf(x, mu, std)

# Plot the PDF curve
ax1.plot(x, pdf, label='Normal Distribution', color='blue')

# Plot vertical lines for quartiles and mean
ax1.axvline(q25, color='blue', linestyle='--', label='25% Quartile')
ax1.axvline(mu, color='green', linestyle='--', label='Median (50%)')
ax1.axvline(q75, color='purple', linestyle='--', label='75% Quartile')
ax1.axvline(mean, color='red', linestyle='--', label='Mean')

# Customize the plot
ax1.set_title('Normalized Distribution Curve')
ax1.set_xlabel('Values')
ax1.set_ylabel('Probability Density')
ax1.xaxis.set_major_locator(MultipleLocator(25))
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90)

# Customize the plot
ax2.set_title('Histogram')
ax2.set_xlabel('P/E values')
ax2.set_ylabel('Counts')
ax2.xaxis.set_major_locator(MultipleLocator(25))
ax2.set_xticklabels(ax1.get_xticklabels(), rotation=90)

ax1.legend()
ax2.legend()

# Histograms [ One with density = True to show the normal distribution curve and one without to show actual values]
counts1, bins1, _ = ax1.hist(pe_ratios, bins=30, edgecolor='black', alpha=0.3, density=True)
counts2, bins2, _ = ax2.hist(pe_ratios, bins=30, edgecolor='black', alpha=0.5)

# Fetch real-time stock price
url_stock_price = f'https://financialmodelingprep.com/api/v3/stock/real-time-price/{symbol}?apikey={api_key}'
response_stock_price = requests.get(url_stock_price)
data_stock_price = response_stock_price.json()

current_stock_price = data_stock_price['companiesPriceList'][0]['price']

# Fetch analyst estimates
url_analyst_estimates = f'https://financialmodelingprep.com/api/v3/analyst-estimates/{symbol}?limit=400&apikey={api_key}'
response_analyst_estimates = requests.get(url_analyst_estimates)
data_analyst_estimates = response_analyst_estimates.json()

# Get current date
current_date = datetime.today()

# Filter data for future date estimates
filtered_data = [
    entry for entry in data_analyst_estimates
    if datetime.strptime(entry["date"], "%Y-%m-%d") > current_date
]

# Calculate EPS ratio and reverse the result to get ascending dates order
result = [(current_stock_price / entry["estimatedEpsAvg"], entry["date"]) for entry in filtered_data][::-1]

# Annotate bars with specific values and average EPS estimates
for data in result:
    estimated_eps = data[0]
    bin_index = np.digitize(estimated_eps, bins1) - 1
    ax1.annotate(text=f"{estimated_eps:.2f} : Avg EPS Estimate {data[1]}",
                 xy=(estimated_eps, counts1[bin_index]),
                 ha="center", va="bottom", rotation=90, fontsize=6,
                 xytext=(0, 15), textcoords="offset points", arrowprops=dict(arrowstyle='->', lw=1.5, color='red'))

for data in result:
    estimated_eps = data[0]
    bin_index = np.digitize(estimated_eps, bins2) - 1
    ax2.annotate(text=f"{estimated_eps:.2f} : Avg EPS Estimate {data[1]}",
                 xy=(estimated_eps, counts2[bin_index]),
                 ha="center", va="bottom", rotation=90, fontsize=7.5,
                 xytext=(0, 15), textcoords="offset points", arrowprops=dict(arrowstyle='->', lw=1.5, color='red'))

plt.show()
