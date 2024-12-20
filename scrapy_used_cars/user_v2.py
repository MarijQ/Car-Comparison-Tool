import tkinter as tk
from tkinter import ttk
import psycopg2

# Database connection parameters
DB_NAME = "car_listings"
DB_USER = "marij"
DB_PASS = "marij"
DB_HOST = "localhost"


class CarFilterApp:
    def __init__(self, master):
        self.master = master
        master.title("Car Search")

        # Frame for filters (left side)
        self.filter_frame = tk.Frame(master, padx=10, pady=10)
        self.filter_frame.grid(row=0, column=0, sticky="n")

        # Frame for results (right side)
        self.result_frame = tk.Frame(master, padx=10, pady=10)
        self.result_frame.grid(row=0, column=1, sticky="n")

        # Fields to filter on
        # For simplicity, include a small subset. Add or remove fields as needed.
        # We will assume the following fields:
        # text fields: make, model, fuel_type, body_style, transmission
        # numeric fields: price, mileage, year, n_doors, previous_owners
        # We'll also allow filtering on engine_size (numeric, treated as cc or liters)
        # If unsure about a field, you can treat as text or numeric accordingly.
        self.fields = {
            "make": "text",
            "model": "text",
            "fuel_type": "text",
            "body_style": "text",
            "transmission": "text",
            "price": "numeric",
            "mileage": "numeric",
            "year": "numeric",
            "n_doors": "numeric",
            "previous_owners": "numeric",
            "engine_size": "numeric",
        }

        self.entries = {}
        row_count = 0
        for field_name, field_type in self.fields.items():
            label = tk.Label(self.filter_frame, text=f"{field_name.capitalize()}:")
            label.grid(row=row_count, column=0, sticky="e", pady=2)
            entry = tk.Entry(self.filter_frame, width=20)
            entry.grid(row=row_count, column=1, pady=2)
            self.entries[field_name] = entry
            row_count += 1

        # Add a search button
        self.search_button = tk.Button(self.filter_frame, text="Search", command=self.run_search)
        self.search_button.grid(row=row_count, column=0, columnspan=2, pady=10)

        # Results table (top right)
        self.table_label = tk.Label(self.result_frame, text="Top 5 Matches", font=("Arial", 14, "bold"))
        self.table_label.grid(row=0, column=0, sticky="w")

        self.tree = ttk.Treeview(self.result_frame, columns=("make", "model", "price", "mileage", "year"), show='headings')
        self.tree.heading("make", text="Make")
        self.tree.heading("model", text="Model")
        self.tree.heading("price", text="Price")
        self.tree.heading("mileage", text="Mileage")
        self.tree.heading("year", text="Year")
        self.tree.grid(row=1, column=0, sticky="nsew")

        # Average price label (bottom right)
        self.avg_label = tk.Label(self.result_frame, text="Average Price: N/A")
        self.avg_label.grid(row=2, column=0, sticky="w", pady=10)

        # Make the columns stretch
        self.result_frame.grid_rowconfigure(1, weight=1)
        self.result_frame.grid_columnconfigure(0, weight=1)

    def run_search(self):
        filters = []
        values = []
        
        # Construct dynamic query
        # We will apply filters only if user provides input.
        # For text fields: exact match (e.g., make = 'Toyota')
        # For numeric fields: value between val*0.8 and val*1.2
        for field_name, field_type in self.fields.items():
            val = self.entries[field_name].get().strip()
            if val:  # If user provided a value
                if field_type == "text":
                    # exact match case-insensitive
                    filters.append(f"LOWER({field_name}) = LOWER(%s)")
                    values.append(val)
                else:
                    # numeric
                    try:
                        num_val = float(val)
                        low = num_val * 0.8
                        high = num_val * 1.2
                        filters.append(f"{field_name} BETWEEN %s AND %s")
                        values.append(low)
                        values.append(high)
                    except ValueError:
                        # If not numeric, skip or treat as no filter.
                        pass

        where_clause = ""
        if filters:
            where_clause = "WHERE " + " AND ".join(filters)

        # We retrieve top 5 matched cars ordered by price ascending
        query = f"""
            SELECT make, model, price, mileage, year
            FROM cargiant
            {where_clause}
            ORDER BY price ASC
            LIMIT 5;
        """

        # Also retrieve average price over all matched cars
        avg_query = f"""
            SELECT AVG(price), COUNT(*)
            FROM cargiant
            {where_clause};
        """

        try:
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
            cur = conn.cursor()

            cur.execute(query, tuple(values))
            rows = cur.fetchall()

            # Clear existing rows in Treeview
            for i in self.tree.get_children():
                self.tree.delete(i)

            # Insert new rows
            for r in rows:
                self.tree.insert("", tk.END, values=r)

            # Compute average price
            cur.execute(avg_query, tuple(values))
            avg_res = cur.fetchone()
            avg_price, count = avg_res[0], avg_res[1]

            if avg_price is not None:
                self.avg_label.config(text=f"Average Price: {round(avg_price, 2)} (based on {count} cars)")
            else:
                self.avg_label.config(text="Average Price: N/A (no matches)")

            conn.close()

        except Exception as e:
            print(f"Database error: {e}")
            self.avg_label.config(text="Error fetching data.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CarFilterApp(root)
    root.mainloop()
