from bs4 import BeautifulSoup
import pandas as pd
import os

# Directory containing the TXT files
directory = "data"  # Update this to your directory containing the TXT files
all_data = []

# Loop through each TXT file in the directory
for file_name in os.listdir(directory):
    if file_name.endswith('.txt'):
        category_name = os.path.splitext(file_name)[0]  # Get category from file name
        
        # Open and parse the HTML file
        with open(os.path.join(directory, file_name), "r", encoding="utf-8") as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')

            # Extract product names
            product_name_divs = soup.find_all('div', class_='whitespace-normal line-clamp-2 break-words min-h-[2.5rem] text-sm')
            product_names = [div.get_text(strip=True) for div in product_name_divs]

            # Extract prices
            #price_spans = soup.find_all('span', class_='font-medium text-base/5 truncate')
            #prices = [span.get_text(strip=True) for span in price_spans]
            price_spans = soup.find_all('span', class_='font-medium text-base/5 truncate')
            prices = []
            for span in price_spans:
                price_text = span.get_text(strip=True)
                price_text_cleaned = price_text.replace("RM", "").replace(",", "").strip()  # Remove RM and commas
                prices.append(price_text_cleaned)

            # Extract sold numbers
            sold_divs = soup.find_all('div', class_='truncate text-shopee-black87 text-xs min-h-4')
            numbers_sold = [div.get_text(strip=True).split()[0] if div.get_text(strip=True) else "0" for div in sold_divs]

            # Combine the data for this file
            max_length = max(len(product_names), len(prices), len(numbers_sold))
            product_names += ["N/A"] * (max_length - len(product_names))
            prices += [0] * (max_length - len(prices))  # Use 0 as default for prices
            numbers_sold += ["0"] * (max_length - len(numbers_sold))

            for i in range(max_length):
                all_data.append({
                    'Product Name': product_names[i],
                    'Price': prices[i],
                    'Sold': numbers_sold[i],
                    'Category': category_name
                })

# Create a DataFrame with all collected data
df = pd.DataFrame(all_data)

# Save the DataFrame to a CSV file
df.to_csv('product_data.csv', index=False)

print("Data saved to product_data.csv")
