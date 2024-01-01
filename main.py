import statistics

# Fetch prices from the database
def generate_price_data(database):
    # Extracting 'Close' prices from the database
    return [row[4] for row in database]

# Calculate mean reversion
def calculate_mean_reversion(prices):
    mean = statistics.mean(prices)
    deviation = [price - mean for price in prices]
    std_deviation = statistics.stdev(prices)
    z_scores = [dev / std_deviation if std_deviation != 0 else 0 for dev in deviation]
    return z_scores

# Define thresholds for overvalued and undervalued
overvalued_threshold = 1.5
undervalued_threshold = -1.5

# Use the provided database to get prices
prices = generate_price_data(database)

# Calculate mean reversion
z_scores = calculate_mean_reversion(prices)

# Determine trading signals based on thresholds
for i, z_score in enumerate(z_scores):
    if z_score > overvalued_threshold:
        print(f"Date: {database[i][0]}, Price: {prices[i]} is overvalued (Z-Score: {z_score}) - Consider selling")
    elif z_score < undervalued_threshold:
        print(f"Date: {database[i][0]}, Price: {prices[i]} is undervalued (Z-Score: {z_score}) - Consider buying")
    else:
        print(f"Date: {database[i][0]}, Price: {prices[i]} is within the normal range (Z-Score: {z_score}) - Hold")
