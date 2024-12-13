import psycopg2
import sys

def run_query():
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            dbname="used_cars",
            user="marij",
            password="marij", 
            host="localhost"
        )
        cursor = connection.cursor()

        print("Connected to the database. Type your SQL query below:")
        query = input("SQL> ")  # Input a SQL query from the user

        cursor.execute(query)  # Execute the user's query
        if cursor.description:  # Check if the query returned rows (e.g., SELECT)
            results = cursor.fetchall()  # Fetch all results
            print("\nResults:")
            for row in results:
                print(row)
        else:
            connection.commit()  # Commit changes for non-SELECT queries (e.g., INSERT/UPDATE)
            print(f"Query executed successfully: {cursor.rowcount} rows affected.")

    except Exception as e:
        print(f"Error: {e}")  # Print any errors encountered
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the database connection

if __name__ == "__main__":
    run_query()
