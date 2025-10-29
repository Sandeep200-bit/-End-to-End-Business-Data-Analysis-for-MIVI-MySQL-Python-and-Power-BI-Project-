


pip install mysql-connector-python pandas numpy matplotlib seaborn

pip install pymysql sqlalchemy pandas

import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
from mysql.connector import Error
import pandas as pd
from sqlalchemy import create_engine


# MySQL connection details
connection = pymysql.connect(
    host="localhost",        
    user="root",             
    password="Sandeep@1234", 
    database="Mivi_Internship_Task"  
)

# Fetch supply_chain_issues data
supply_chain_issues = "SELECT * FROM supply_chain_issues;"
supply_chain_issues_df = pd.read_sql(supply_chain_issues, connection)


# Fetch after_sales_defects data
after_sales_defects = "SELECT * FROM after_sales_defects;"
after_sales_defects_df = pd.read_sql(after_sales_defects, connection)


# Fetch marketing_brand_awareness data
marketing_brand_awareness = "SELECT * FROM marketing_brand_awareness;"
marketing_brand_awareness_df = pd.read_sql(marketing_brand_awareness, connection)


# Close the connection
connection.close()


marketing_brand_awareness_df

supply_chain_issues_df

after_sales_defects_df






# -------- Robust Date Cleaning Function --------
def robust_date_parse(df, col):
    formats = ['%d-%m-%Y', '%d/%m/%Y', '%b %d, %Y', '%Y-%m-%d', '%d-%b-%Y']
    # Try to parse each format, keep best
    parsed_col = pd.Series([pd.NaT]*len(df), dtype='datetime64[ns]')
    for fmt in formats:
        # Only apply to rows yet unparsed
        temp = pd.to_datetime(df[col], format=fmt, errors='coerce')
        parsed_col = parsed_col.combine_first(temp)
    # As last resort, use pandas general parse on missing
    parsed_col = parsed_col.combine_first(pd.to_datetime(df[col], errors='coerce'))
    df[col+'_parsed'] = parsed_col
    # Optional: drop original or keep for reference
    return df

# -------- After Sales Defects Cleaning --------
for col in ['Sale_Date', 'Complaint_Logged_Date']:
    after_sales_defects_df = robust_date_parse(after_sales_defects_df, col)

after_sales_defects_df = after_sales_defects_df.drop_duplicates()
after_sales_defects_df['Product_Type'] = after_sales_defects_df['Product_Type'].str.strip().str.title()
after_sales_defects_df['Region'] = after_sales_defects_df['Region'].str.strip().str.title()
after_sales_defects_df['Status'] = after_sales_defects_df['Status'].str.strip().str.capitalize()
after_sales_defects_df['Complaint_Type'] = after_sales_defects_df['Complaint_Type'].str.strip().str.title()
after_sales_defects_df['Resolution_Time_Days'] = pd.to_numeric(after_sales_defects_df['Resolution_Time_Days'], errors='coerce')
after_sales_defects_df['Resolution_Time_Days'].fillna(after_sales_defects_df['Resolution_Time_Days'].median(), inplace=True)

# -------- Marketing Brand Cleaning --------
for col in ['Start_Date', 'End_Date']:
    marketing_brand_awareness_df = robust_date_parse(marketing_brand_awareness_df, col)

marketing_brand_awareness_df = marketing_brand_awareness_df.drop_duplicates()
marketing_brand_awareness_df['Platform'] = marketing_brand_awareness_df['Platform'].str.strip().str.title()
marketing_brand_awareness_df['Campaign_Name'] = marketing_brand_awareness_df['Campaign_Name'].str.strip().str.title()
marketing_brand_awareness_df['Target_Audience'] = marketing_brand_awareness_df['Target_Audience'].str.strip().str.title()
marketing_brand_awareness_df['Budget_Spent'] = pd.to_numeric(marketing_brand_awareness_df['Budget_Spent'], errors='coerce')
marketing_brand_awareness_df['Budget_Spent'].fillna(marketing_brand_awareness_df['Budget_Spent'].median(), inplace=True)
marketing_brand_awareness_df['Impressions'] = pd.to_numeric(marketing_brand_awareness_df['Impressions'], errors='coerce')
marketing_brand_awareness_df['Clicks'] = pd.to_numeric(marketing_brand_awareness_df['Clicks'], errors='coerce')
marketing_brand_awareness_df['Engagement_Rate'] = pd.to_numeric(marketing_brand_awareness_df['Engagement_Rate'], errors='coerce')

# -------- Supply Chain Issues Cleaning --------
supply_chain_issues_df = robust_date_parse(supply_chain_issues_df, 'Date')
supply_chain_issues_df = supply_chain_issues_df.drop_duplicates()
for col in ['Cost_Per_Unit', 'Wastage_Percentage', 'Quantity_Produced']:
    supply_chain_issues_df[col] = pd.to_numeric(supply_chain_issues_df[col], errors='coerce')
    supply_chain_issues_df[col].fillna(supply_chain_issues_df[col].median(), inplace=True)
supply_chain_issues_df['Part'] = supply_chain_issues_df['Part'].str.strip().str.title()
supply_chain_issues_df['Supplier'] = supply_chain_issues_df['Supplier'].str.strip().str.title()
supply_chain_issues_df['Production_Line'] = supply_chain_issues_df['Production_Line'].str.strip().str.title()
supply_chain_issues_df['Inspection_Status'] = supply_chain_issues_df['Inspection_Status'].str.strip().str.capitalize()

# ----- Sample EDA with Plots -----

# EDA 1: After-Sales Complaints by Product
plt.figure(figsize=(8,5))
sns.countplot(data=after_sales_defects_df, x='Product_Type')
plt.title('Complaints Count by Product Type')
plt.xticks(rotation=45)
plt.show()

# EDA 2: Marketing - Engagement Rate by Platform
plt.figure(figsize=(7,5))
sns.barplot(x='Platform', y='Engagement_Rate', data=marketing_brand_awareness_df, estimator=np.mean)
plt.title('Average Engagement Rate by Platform')
plt.xticks(rotation=45)
plt.show()

# EDA 3: Supply Chain - Cost vs Wastage
plt.figure(figsize=(7,5))
sns.scatterplot(data=supply_chain_issues_df, x='Cost_Per_Unit', y='Wastage_Percentage', hue='Part')
plt.title('Cost vs Wastage (%) by Part')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
plt.show()

# EDA 4: After Sales - Resolution Time Distribution
plt.figure(figsize=(7,4))
sns.histplot(after_sales_defects_df['Resolution_Time_Days'], bins=15, kde=True)
plt.title('Distribution of Resolution Time')
plt.xlabel('Days')
plt.show()

# EDA 5: Marketing - Budget vs Impressions
plt.figure(figsize=(7,5))
sns.scatterplot(data=marketing_brand_awareness_df, x='Budget_Spent', y='Impressions', hue='Platform')
plt.title('Budget Spent vs Impressions')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
plt.show()

# EDA 6: Supply Chain - Quantity Produced Over Time
plt.figure(figsize=(10,4))
daily_prod = supply_chain_issues_df.groupby('Date_parsed')['Quantity_Produced'].sum().reset_index()
sns.lineplot(data=daily_prod, x='Date_parsed', y='Quantity_Produced')
plt.title('Production Volume Over Time')
plt.xticks(rotation=30)
plt.show()


marketing_brand_awareness_df

supply_chain_issues_df

after_sales_defects_df


supply_chain_issues_df.to_csv('supply_chain_issues_df.csv', index=False)

marketing_brand_awareness_df.to_csv('marketing_brand_awareness_df.csv', index=False)

after_sales_defects_df.to_csv('after_sales_defects_df.csv', index=False)








































