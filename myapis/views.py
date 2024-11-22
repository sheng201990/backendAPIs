import mysql.connector
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework import status
from datetime import datetime
from mysql.connector import Error

#def hello_world(request):
#   return HttpResponse("Hello, World!")

def db_connection():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',  # e.g., 'localhost'
            user='root',
            password='shengyi2020',
            database='mysqlDB'
        )
        if conn.is_connected():
            print("Connected to the database!")
            return conn
    except Error as e:
        print(f"Error: {e}")
        return None
    
class ListAllCompany(APIView):
    def get(self, request, *args, **kwargs):
        conn = db_connection()
        cursor = conn.cursor()

        # Execute a query to get all stock data
        cursor.execute("SELECT * FROM company")
        stock_data = cursor.fetchall()
        cursor.close()

        # Prepare data to return
        data = []
        for row in stock_data:
            data.append({
                "id": row[0],
                "name": row[1],
                "sector_level1": row[2],
                "sector_level2": row[3],
            })

        # Return the data as a response
        return Response(data, status=status.HTTP_200_OK)

class ListAllStockData(APIView):
    def get(self, request, *args, **kwargs):
        conn = db_connection()
        cursor = conn.cursor()

        # Execute a query to get all stock data
        cursor.execute("SELECT * FROM stock_data")
        stock_data = cursor.fetchall()

        # Close the cursor (not the connection)
        cursor.close()

        # Prepare data to return
        data = []
        for row in stock_data:
            data.append({
                "company_id": row[1],
                "asof": row[2],
                "volume": row[3],
                "close_usd": row[4],
            })

        # Return the data as a response
        return Response(data, status=status.HTTP_200_OK)

class RetrieveStockDataByCompanyName(APIView):
    def get(self, request, company_id, *args, **kwargs):
        conn = db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM stock_data WHERE company_id = %s", [company_id])
        stock_data = cursor.fetchall()
        cursor.close()

        if not stock_data:
            return Response({"error": "No data found for the given company."}, status=status.HTTP_404_NOT_FOUND)

        # Prepare data for response
        data = []
        for row in stock_data:
            data.append({
                "company_id": row[1],
                "asof": row[2],
                "volume": row[3],
                "close_usd": row[4],
            })

        return Response(data, status=status.HTTP_200_OK)
    
class CalculateCumulativeReturns(APIView):
     def post(self, request, *args, **kwargs):
        company_id = request.data.get("company_id")
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        conn = db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT asof, close_usd FROM stock_data
            WHERE company_id = %s AND asof BETWEEN %s AND %s
            ORDER BY asof ASC
        """, [company_id, start_date, end_date])

        stock_data = cursor.fetchall()
        cursor.close()

        if not stock_data:
            return Response({"error": "No data found for the given period."}, status=status.HTTP_404_NOT_FOUND)

        initial_price = stock_data[0][1]
        final_price = stock_data[-1][1]
        cumulative_return = (final_price - initial_price) / initial_price * 100  # as a percentage

        return Response({
            "cumulative_return": cumulative_return
        }, status=status.HTTP_200_OK)