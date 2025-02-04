import matplotlib.pyplot as plt
import requests
import numpy as np

url = "https://financialmodelingprep.com/api/v3/income-statement/MSFT"
params = {
    "period": "quarter",
    "apikey": <YOUR_API_KEY>
}

# Send the GET request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
else:
    print(f"Failed to retrieve data: {response.status_code}")
    data = []

# Extract data
dates = [item['date'] for item in data][::-1]
revenues = np.array([item['revenue'] for item in data][::-1])
total_costs = np.array([item['costAndExpenses'] for item in data][::-1])

# Plot revenue and total cost lines
plt.figure(figsize=(10, 6))
plt.plot(dates, revenues, label='Revenue', marker='o', markersize=3, color='blue')
plt.plot(dates, total_costs, label='Total Cost', marker='o', markersize=3, color='orange')

# Fill the area between the lines
plt.fill_between(dates, revenues, total_costs,
                 where=(revenues > total_costs),
                 interpolate=True, color='lightgreen', alpha=0.5, label='Profit Area')

plt.fill_between(dates, revenues, total_costs,
                 where=(revenues < total_costs),
                 interpolate=True, color='lightcoral', alpha=0.5, label='Loss Area')

# Mark the first crossing point
for i in range(len(dates)):
    if revenues[i] > total_costs[i]:
        plt.scatter(dates[i], revenues[i], color='red', label='Operating Leverage Point')
        break

plt.xlabel('Date')
plt.ylabel('Amount (USD)')
plt.title('Revenue and Total Cost Over Time')
plt.legend()
plt.grid(False)
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()
