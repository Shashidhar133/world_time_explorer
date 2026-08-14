import tkinter as tk

from config.countries import COUNTRIES
from utils.helpers import search_countries


class CountrySelector:
    def __init__(self, parent, on_country_selected):
        self.parent = parent
        self.on_country_selected = on_country_selected

        self.search_results = []

        self.create_ui()

    def create_ui(self):
        self.search_container = tk.Frame(
            self.parent,
            bg="#0b1726",
            highlightbackground="#16415b",
            highlightthickness=1
        )
        self.search_container.pack(
            pady=15,
            ipadx=8,
            ipady=6
        )

        tk.Label(
            self.search_container,
            text="🔍",
            font=("Segoe UI Emoji", 16),
            fg="#00e5ff",
            bg="#0b1726"
        ).pack(
            side="left",
            padx=(12, 5)
        )

        self.search_var = tk.StringVar()

        self.search_entry = tk.Entry(
            self.search_container,
            textvariable=self.search_var,
            font=("Segoe UI", 13),
            fg="#7190a8",
            bg="#14283d",
            insertbackground="#00e5ff",
            relief="flat",
            width=30
        )

        self.search_entry.pack(
            side="left",
            ipady=8,
            padx=5
        )

        self.search_entry.insert(
            0,
            "Search country..."
        )

        self.search_entry.bind(
            "<FocusIn>",
            self.clear_placeholder
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_country
        )

        self.search_entry.bind(
            "<Return>",
            self.select_first_result
        )

        tk.Button(
            self.search_container,
            text="✕",
            font=("Segoe UI", 12, "bold"),
            fg="#8aa5b8",
            bg="#0b1726",
            activebackground="#0b1726",
            activeforeground="#ff4081",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.clear_search
        ).pack(
            side="left",
            padx=8
        )

    # =====================================================
    # SEARCH
    # =====================================================

    def clear_placeholder(self, event=None):
        if self.search_entry.get() == "Search country...":
            self.search_entry.delete(
                0,
                tk.END
            )

            self.search_entry.config(
                fg="white"
            )

    def search_country(self, event=None):
        query = self.search_var.get().strip().lower()

        if (
            not query
            or query == "search country..."
        ):
            self.search_results = []
            self.hide_search_results()
            return

        self.search_results = search_countries(
            query,
            COUNTRIES
        )

        self.show_search_results()

    # =====================================================
    # RESULTS
    # =====================================================

    def show_search_results(self):
        self.hide_search_results()

        if not self.search_results:
            return

        self.results_frame = tk.Frame(
            self.parent,
            bg="#102438",
            highlightbackground="#16415b",
            highlightthickness=1
        )

        self.results_frame.place(
            relx=0.5,
            y=160,
            anchor="n"
        )

        for country in self.search_results:

            data = COUNTRIES[country]

            button = tk.Button(
                self.results_frame,
                text=f"{data['flag']}  {country}",
                font=("Segoe UI", 11),
                fg="white",
                bg="#102438",
                activebackground="#00bcd4",
                activeforeground="white",
                anchor="w",
                relief="flat",
                borderwidth=0,
                width=35,
                cursor="hand2",
                command=lambda c=country:
                    self.select_country(c)
            )

            button.pack(
                fill="x",
                padx=3,
                pady=1
            )

    def hide_search_results(self):

        if hasattr(
            self,
            "results_frame"
        ):

            try:
                self.results_frame.destroy()

            except tk.TclError:
                pass

    # =====================================================
    # COUNTRY SELECTION
    # =====================================================

    def select_country(self, country):

        if country not in COUNTRIES:
            return

        self.search_var.set(country)

        self.search_entry.config(
            fg="white"
        )

        self.hide_search_results()

        self.on_country_selected(
            country
        )

    def select_first_result(self, event=None):

        if self.search_results:
            self.select_country(
                self.search_results[0]
            )

    def clear_search(self):

        self.search_var.set("")

        self.search_results = []

        self.hide_search_results()

        self.search_entry.focus_set()