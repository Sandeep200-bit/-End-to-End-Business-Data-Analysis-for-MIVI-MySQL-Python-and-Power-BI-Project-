
!pip install faker
pip install faker


import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker()

# Dataset 1: Supply Chain Issues
np.random.seed(42)
parts = ['Speaker', 'Battery', 'Chipset', 'Microphone', 'Cable', 'Earbud Housing', 'PCB', 'Wire', 'Connector', 'Charger']
costs = np.round(np.random.uniform(10, 100, 600), 2)
wastage = np.random.randint(0, 5, 600)
qty_produced = np.random.randint(100, 1000, 600)
date_list = pd.date_range(start='2023-01-01', periods=600, freq='D').to_series()
date_formats = [lambda x: x.strftime('%Y-%m-%d'),
                lambda x: x.strftime('%d/%m/%Y'),
                lambda x: x.strftime('%b %d, %Y')]
dates_messy = [random.choice(date_formats)(date) for date in date_list]

supply_chain_df = pd.DataFrame({
    'Part': np.random.choice(parts, 600),
    'Cost_Per_Unit': costs,
    'Wastage_Percentage': wastage,
    'Quantity_Produced': qty_produced,
    'Date': dates_messy,
    'Supplier': [fake.company() for _ in range(600)],
    'Batch_Number': np.random.randint(1000, 2000, 600).astype(str),
    # Messy columns
    'Notes': [random.choice([fake.sentence(), None, '']) for _ in range(600)],
    'Production_Line': np.random.choice(['Line A', 'Line B ', 'Line C', 'LiNe D', np.nan], 600),
    'Inspection_Status': np.random.choice(['Passed', 'Failed', 'Passed ', 'Failded', None], 600)
})

# Introduce duplicates and missing deliberately
supply_chain_df.loc[5] = supply_chain_df.loc[4]
supply_chain_df.loc[50, 'Cost_Per_Unit'] = None
supply_chain_df.loc[100, 'Date'] = '2023/15/05'  # Invalid date format
supply_chain_df.loc[150, 'Batch_Number'] = ''


# Dataset 2: After-Sales Service and Defect Management
product_types = ['Earbuds', 'Headphones', 'Bluetooth Speaker', 'Soundbar', 'Charging Cable']
regions = ['North', 'South', 'East', 'West', 'Central']
status = ['Resolved', 'Pending', 'In Progress', 'Closed']
area_codes = ['A1', 'B2', 'C3', 'D4', 'E5']

date_list2 = pd.date_range(start='2023-01-01', periods=700, freq='D').to_series()
dates_messy2 = [random.choice(date_formats)(date) for date in date_list2]

after_sales_df = pd.DataFrame({
    'Sale_ID': np.arange(1000, 1700),
    'Product_Type': np.random.choice(product_types, 700),
    'Region': np.random.choice(regions, 700),
    'Sale_Date': dates_messy2,
    'Customer_Area_Code': np.random.choice(area_codes, 700),
    'Complaint_Logged_Date': dates_messy2,
    'Complaint_Type': np.random.choice(['Defect', 'Late Delivery', 'Non-Functioning', 'Warranty Issue'], 700),
    'Status': np.random.choice(status, 700),
    'Resolution_Time_Days': np.random.choice([np.nan, 1, 3, 5, 7, 10], 700),
    'Comments': [random.choice([fake.text(max_nb_chars=30), None, '']) for _ in range(700)]
})

after_sales_df.loc[10] = after_sales_df.loc[9]
after_sales_df.loc[100, 'Sale_Date'] = '15-2023-03'  # Invalid date
after_sales_df.loc[145, 'Complaint_Type'] = ''
after_sales_df.loc[200, 'Resolution_Time_Days'] = None


# Dataset 3: Marketing and Brand Awareness
social_platforms = ['Facebook', 'Instagram', 'Twitter', 'LinkedIn', 'YouTube']
paid_campaigns = ['New Launch', 'Sale Promo', 'Festival Discount', 'Brand Awareness', 'Product Spotlight']

date_list3 = pd.date_range(start='2023-01-01', periods=600, freq='W').to_series()
dates_messy3 = [random.choice(date_formats)(date) for date in date_list3]

marketing_df = pd.DataFrame({
    'Campaign_ID': np.arange(5000, 5600),
    'Platform': np.random.choice(social_platforms, 600),
    'Campaign_Name': np.random.choice(paid_campaigns, 600),
    'Start_Date': dates_messy3,
    'End_Date': dates_messy3,
    'Budget_Spent': np.round(np.random.uniform(5000, 50000, 600), 2),
    'Impressions': np.random.randint(10000, 1000000, 600),
    'Clicks': np.random.randint(500, 50000, 600),
    'Engagement_Rate': np.round(np.random.uniform(0.1, 10, 600), 2),
    'Notes': [random.choice([fake.sentence(), None, '']) for _ in range(600)],
    'Target_Audience': np.random.choice(['Youth', 'Adults', 'Tech Enthusiasts', 'General Public'], 600)
})

marketing_df.loc[20] = marketing_df.loc[19]
marketing_df.loc[70, 'End_Date'] = ''
marketing_df.loc[150, 'Budget_Spent'] = None

# Save to CSV for further use or inspection
supply_chain_df.to_csv('supply_chain_issues.csv', index=False)
after_sales_df.to_csv('after_sales_defects.csv', index=False)
marketing_df.to_csv('marketing_brand_awareness.csv', index=False)

print("Datasets created with messiness for cleaning practice.")

































