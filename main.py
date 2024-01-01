import statistics
import matplotlib.pyplot as plt

stock = 'SHEL' # Stock name, used to open file and to give graph a title

with open(f'{stock}.csv', 'r') as f:
    database = []
    for line in f.readlines():
        if line[0] != 'D':
            date, op, hi, lo, cl, adj_cl, vol = line.split(',')
            database.append((date, float(op), float(hi), float(lo), float(cl), float(adj_cl), int(vol)))

# Fetch prices from the database
def generate_price_data(database):
    # Extracting 'Close' prices from the database
    return [row[4] for row in database]

# Calculate mean reversion
def calculate_mean_reversion(prices):
    prices = prices[-200:] # Use 200 day moving window to calculate data
    mean = statistics.mean(prices)
    deviation = [price - mean for price in prices]
    std_deviation = statistics.stdev(prices)
    z_scores = [dev / std_deviation if std_deviation != 0 else 0 for dev in deviation]
    return z_scores

# Define thresholds for overvalued and undervalued
overvalued_threshold = 0.75
undervalued_threshold = -0.75

# Use the provided database to get prices
prices = generate_price_data(database)

# Calculate mean reversion
z_scores = calculate_mean_reversion(prices)

# Store number of days ago
days = []

# Determine trading signals based on thresholds
for i, z_score in enumerate(z_scores):
    days.append(i)
    if z_score > overvalued_threshold:
        print(f"Date: {database[i][0]}, Price: {prices[i]} is overvalued (Z-Score: {z_score}) - Consider selling")
    elif z_score < undervalued_threshold:
        print(f"Date: {database[i][0]}, Price: {prices[i]} is undervalued (Z-Score: {z_score}) - Consider buying")
    else:
        print(f"Date: {database[i][0]}, Price: {prices[i]} is within the normal range (Z-Score: {z_score}) - Hold")

# Plot price vs days on top graph, and Z-value vs days on bottom graph
fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle(f'{stock} Mean Reversion - Nola')
ax1.plot(days[-50:], prices[-50:]) # Zoom in on only past 50 days
ax2.plot(days[-50:], z_scores[-50:]) # Zoom in on only past 50 days
plt.show()
