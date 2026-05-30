import tkinter as tk
from tkinter import ttk, messagebox
import requests
import design_config as cfg


class CurrencyConverterApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Currency Exchange")
        self.root.geometry("300x400")

        self.rates_data = {}


        self.create_widgets()


        self.fetch_live_data()

    def create_widgets(self):
        # Title (Doesn't need self, we never change it)
        title_text = tk.Label(self.root, text=cfg.TITLE_TEXT, font=cfg.FONT_FOR_TITLE)
        title_text.grid(row=0, column=0, columnspan=2, pady=20)

        """Labels - User Input"""
        # Amount
        amount_label = tk.Label(self.root, text="Amount:", font=cfg.FONT_LABELS)
        amount_label.grid(row=1, column=0, pady=5)

        # ADDED SELF HERE so the math engine can read what the user types
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1, pady=5)

        # From
        from_currency_label = tk.Label(self.root, text="From:", font=cfg.FONT_LABELS)
        from_currency_label.grid(row=2, column=0, pady=5)

        # ADDED SELF HERE so the math engine knows what currency is selected
        self.from_currency_box = ttk.Combobox(self.root)
        self.from_currency_box.grid(row=2, column=1, pady=5)

        # To
        to_currency_label = tk.Label(self.root, text="To:", font=cfg.FONT_LABELS)
        to_currency_label.grid(row=3, column=0, pady=5)

        self.to_currency_box = ttk.Combobox(self.root)
        self.to_currency_box.grid(row=3, column=1)

        # Result
        result_exchange_label = tk.Label(self.root, text="Result:", font=cfg.FONT_LABELS)
        result_exchange_label.grid(row=4, column=0, pady=10)

        self.result_exchange_output = tk.Label(self.root, text="--", font=cfg.FONT_LABELS)
        self.result_exchange_output.grid(row=4, column=1)

        # Button - Convert (Added command=self.convert_currency to link them!)
        self.convert_button = ttk.Button(self.root, text="Convert", command=self.convert_currency)
        self.convert_button.grid(row=5, column=0, columnspan=2, pady=20)

    def fetch_live_data(self):
        response = requests.get("https://open.er-api.com/v6/latest/USD")

        if response.status_code == 200:
            data_dictionary = response.json()

            self.rates_data = data_dictionary["rates"]

            currency_codes = list(self.rates_data.keys())
            self.from_currency_box['values'] = currency_codes
            self.to_currency_box['values'] = currency_codes

            print("Data saved to class memory successfully!")

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            from_curr = self.from_currency_box.get()
            to_curr = self.to_currency_box.get()

            rate_from = self.rates_data[from_curr]
            rate_to = self.rates_data[to_curr]

            final_value = amount * (rate_to / rate_from)

            self.result_exchange_output.config(text=f"{final_value:.2f} {to_curr}")

        except KeyError:
            messagebox.showwarning(title="Error", message="Select valid currency")
        except ValueError:
            messagebox.showwarning(title="Error", message="Enter a number please.")



root = tk.Tk()
app = CurrencyConverterApp(root)
root.mainloop()