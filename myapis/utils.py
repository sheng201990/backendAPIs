from datetime import datetime
def convert_date(date_str):
    # Parse the date string in MM/DD/YYYY format
    date_obj = datetime.strptime(date_str, '%m/%d/%Y')
    # Convert to YYYY-MM-DD format for MySQL
    return date_obj.strftime('%Y-%m-%d')