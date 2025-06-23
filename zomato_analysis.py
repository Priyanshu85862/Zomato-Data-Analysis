import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('zomato.csv')
print("Original Data:\n", df.head())

# Drop unnecessary columns (safely)
columns_to_drop = ['url', 'address', 'phone', 'dish_liked', 'reviews_list', 'menu_item']
df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

# Drop missing values
df.dropna(inplace=True)

# Remove duplicates
df.drop_duplicates(inplace=True)

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Clean 'rate' column if exists
if 'rate' in df.columns:
    # Convert to string and strip whitespace
    df['rate'] = df['rate'].astype(str).str.strip()

    # Remove "/5", 'NEW', '-', empty strings, etc.
    df['rate'] = df['rate'].str.replace('/5', '', regex=False)
    df['rate'] = df['rate'].replace(['NEW', '-', 'nan', '', ' '], np.nan)

    # Remove any rows that contain non-numeric junk
    df = df[df['rate'].str.match(r'^\d+\.?\d*$', na=False)]

    # Finally, convert to float
    df['rate'] = df['rate'].astype(float)


# Show cleaned data info
print("\nCleaned Data Info:")
print(df.info())
print(df.head())
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
plt.style.use('ggplot')
sns.set_theme(style="whitegrid")

# Top 10 Restaurant Types
plt.figure(figsize=(12, 6))
rest_type = df['rest_type'].value_counts()[:10]
sns.barplot(x=rest_type.values, y=rest_type.index, palette='viridis')
plt.title('Top 10 Restaurant Types')
plt.xlabel('Number of Restaurants')
plt.ylabel('Restaurant Type')
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6))
sns.boxplot(x='online_order', y='rate', data=df, palette='Set2')
plt.title('Online Order vs Rating')
plt.xlabel('Online Order Available')
plt.ylabel('Rating')
plt.tight_layout()
plt.show()

# Clean approx_cost column (remove commas and convert to float)
df['approx_cost(for_two_people)'] = df['approx_cost(for_two_people)'].str.replace(',', '')
df['approx_cost(for_two_people)'] = df['approx_cost(for_two_people)'].astype(float)

# Cost for Two vs Rating
plt.figure(figsize=(10, 6))
sns.scatterplot(x='approx_cost(for_two_people)', y='rate', data=df, hue='online_order', alpha=0.7)
plt.title('Cost vs Rating')
plt.xlabel('Approx Cost for Two')
plt.ylabel('Rating')
plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 6))
top_locations = df['location'].value_counts()[:10]
sns.barplot(x=top_locations.index, y=top_locations.values, palette='magma')
plt.title('Top 10 Locations with Most Restaurants')
plt.xticks(rotation=45)
plt.ylabel('Number of Restaurants')
plt.tight_layout()
plt.show()

# Top Cuisines (Split and count)
from collections import Counter

# Flatten all cuisines into a list
cuisine_list = df['cuisines'].dropna().apply(lambda x: x.split(', '))
flat_list = [item for sublist in cuisine_list for item in sublist]

# Count top 10
top_cuisines = Counter(flat_list).most_common(10)

# Convert to DataFrame for plotting
top_cuisines_df = pd.DataFrame(top_cuisines, columns=['Cuisine', 'Count'])

# Plot
plt.figure(figsize=(12, 6))
sns.barplot(x='Count', y='Cuisine', data=top_cuisines_df, palette='coolwarm')
plt.title('Top 10 Cuisines Offered')
plt.xlabel('Number of Restaurants')
plt.ylabel('Cuisine')
plt.tight_layout()
plt.show()


