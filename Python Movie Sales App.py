from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime

engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1/athletetoathletedb")

def getValidDate():
    while True:
        start_date = datetime.strptime("11-08-2024", "%m-%d-%Y")
        end_date = datetime.strptime("11-10-2024", "%m-%d-%Y")
        
        date = input("Please enter a date from 11-8-2024 to 11-10-2024 to check which theater in the Northwest group had the highest sales: ")

        try:
            parsed_date = datetime.strptime(date, "%m-%d-%Y")

            if start_date <= parsed_date <= end_date:
                formatted_date = parsed_date.strftime("%Y-%m-%d")
                return formatted_date
            else:
                print("The given date is outside the date range. Please enter a date from 11-8-2024 to 11-10-2024.")

        except ValueError:
            print("Invalid date format. Please enter the date in MM-DD-YYYY format.")


def run():
    print("Hello and welcome to the Northwest Theater sales tracking system!")

    query = """
        SELECT s.theater_id, t.name AS theater_name, SUM(s.total_sales) AS total_sales
        FROM sales s
        INNER JOIN theaters t ON s.theater_id = t.id
        WHERE s.sales_date = :sales_date
        GROUP BY s.theater_id, t.name
        ORDER BY total_sales DESC
        LIMIT 1
    """

    with engine.connect() as connection:
        df = pd.read_sql(text(query), con=connection, params={"sales_date": getValidDate()})
    
    print(df)


if __name__ == "__main__":
    run()
