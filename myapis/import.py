import csv
import mysql.connector

from utils import convert_date

# Connect to your MySQL database
conn = mysql.connector.connect(
    host='127.0.0.1', 
    user='root', 
    password='shengyi2020', 
    database='mysqlDB'
)
cursor = conn.cursor()

# Path to the CSV file
csv_file_path = '/Users/shengyi/Desktop/Demo_Project/stock-data.csv'

# Open the CSV file and read its content
with open(csv_file_path, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row
    for row in reader:
        row[2] = convert_date(row[2])
        cursor.execute("""
            INSERT INTO investment_data (id,name, asof, volume, close_usd, sector_level1, sector_level2)
            VALUES (%s,%s, %s, %s, %s, %s, %s)
        """, row)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()