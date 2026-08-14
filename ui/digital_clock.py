import tkinter as tk

from core.clock import (
    get_time_string,
    get_date_string,
    get_day,
    get_month,
    get_year,
    is_daytime
)


class DigitalClock:
    def __init__(self, parent):
        self.parent = parent

        self.create_ui()

    # =====================================================
    # UI
    # =====================================================

    def create_ui(self):

        tk.Label(
            self.parent,
            text="CURRENT TIME",
            font=("Segoe UI", 11, "bold"),
            fg="#66859e",
            bg="#081421"
        ).pack(
            pady=(50, 5)
        )

        self.time_label = tk.Label(
            self.parent,
            text="00:00:00",
            font=("Consolas", 44, "bold"),
            fg="#00e5ff",
            bg="#081421"
        )

        self.time_label.pack(
            pady=8
        )

        self.date_label = tk.Label(
            self.parent,
            text="",
            font=("Segoe UI", 17),
            fg="#dcecf5",
            bg="#081421"
        )

        self.date_label.pack(
            pady=10
        )

        # =================================================
        # DATE BOXES
        # =================================================

        date_frame = tk.Frame(
            self.parent,
            bg="#081421"
        )

        date_frame.pack(
            pady=25
        )

        self.day_frame, self.day_box = (
            self.create_date_box(
                date_frame,
                "DAY"
            )
        )

        self.month_frame, self.month_box = (
            self.create_date_box(
                date_frame,
                "MONTH"
            )
        )

        self.year_frame, self.year_box = (
            self.create_date_box(
                date_frame,
                "YEAR"
            )
        )

        # =================================================
        # LIVE STATUS
        # =================================================

        self.status_label = tk.Label(
            self.parent,
            text="● LIVE",
            font=("Segoe UI", 12, "bold"),
            fg="#00ff9d",
            bg="#081421"
        )

        self.status_label.pack(
            pady=15
        )

        # =================================================
        # DAY / NIGHT
        # =================================================

        self.period_label = tk.Label(
            self.parent,
            text="",
            font=("Segoe UI", 12, "bold"),
            fg="#ffd166",
            bg="#081421"
        )

        self.period_label.pack(
            pady=5
        )

        # =================================================
        # SYNC
        # =================================================

        self.sync_label = tk.Label(
            self.parent,
            text="● CLOCK SYNCHRONIZED",
            font=("Segoe UI", 9, "bold"),
            fg="#31566c",
            bg="#081421"
        )

        self.sync_label.pack(
            pady=(18, 0)
        )

    # =====================================================
    # DATE BOX
    # =====================================================

    def create_date_box(self, parent, title):

        frame = tk.Frame(
            parent,
            bg="#102438",
            width=105,
            height=75
        )

        frame.pack(
            side="left",
            padx=7
        )

        frame.pack_propagate(False)

        value = tk.Label(
            frame,
            text="--",
            font=("Consolas", 19, "bold"),
            fg="#00e5ff",
            bg="#102438"
        )

        value.pack(
            pady=(8, 0)
        )

        tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 8, "bold"),
            fg="#66859e",
            bg="#102438"
        ).pack()

        return frame, value

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, current_time):

        if current_time is None:
            return

        # Digital time
        self.time_label.config(
            text=get_time_string(
                current_time
            )
        )

        # Full date
        self.date_label.config(
            text=get_date_string(
                current_time
            )
        )

        # Day
        self.day_box.config(
            text=get_day(
                current_time
            )
        )

        # Month
        self.month_box.config(
            text=get_month(
                current_time
            )
        )

        # Year
        self.year_box.config(
            text=get_year(
                current_time
            )
        )

        # Day / Night
        if is_daytime(current_time):

            self.period_label.config(
                text="☀ DAY TIME",
                fg="#ffd166"
            )

        else:

            self.period_label.config(
                text="🌙 NIGHT TIME",
                fg="#a8b9ff"
            )