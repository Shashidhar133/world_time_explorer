import tkinter as tk
import math
import random
from datetime import datetime
from zoneinfo import ZoneInfo

from config.countries import COUNTRIES


class WorldTimeExplorer(tk.Tk):

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self):
        super().__init__()

        self.title("🌍 World Time Explorer")
        self.geometry("1250x760")
        self.minsize(1000, 650)

        self.configure(bg="#030712")

        # -----------------------------------------------------
        # SELECTED COUNTRY
        # -----------------------------------------------------

        self.selected_country = "India"

        # -----------------------------------------------------
        # SEARCH
        # -----------------------------------------------------

        self.search_results = []

        # -----------------------------------------------------
        # ANIMATION VARIABLES
        # -----------------------------------------------------

        self.stars = []

        self.animation_offset = 0
        self.sun_position = 0
        self.moon_position = 0
        self.twinkle_offset = 0

        self.is_day = True

        # -----------------------------------------------------
        # CREATE UI
        # -----------------------------------------------------

        self.create_ui()

        # -----------------------------------------------------
        # CREATE STARS
        # -----------------------------------------------------

        self.create_stars()

        # -----------------------------------------------------
        # INITIAL CLOCK UPDATE
        # -----------------------------------------------------

        self.update_clock()

        # -----------------------------------------------------
        # BACKGROUND ANIMATION
        # -----------------------------------------------------

        self.animate_background()

    # =========================================================
    # MAIN UI
    # =========================================================

    def create_ui(self):

        # =====================================================
        # BACKGROUND
        # =====================================================

        self.background_canvas = tk.Canvas(
            self,
            bg="#030712",
            highlightthickness=0
        )

        self.background_canvas.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        # =====================================================
        # MAIN FRAME
        # =====================================================

        self.main_frame = tk.Frame(
            self,
            bg="#030712"
        )

        self.main_frame.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        # =====================================================
        # HEADER
        # =====================================================

        title = tk.Label(
            self.main_frame,
            text="🌍 WORLD TIME EXPLORER",
            font=("Segoe UI", 30, "bold"),
            fg="#00e5ff",
            bg="#030712"
        )

        title.pack(pady=(22, 2))

        subtitle = tk.Label(
            self.main_frame,
            text="Explore the current time across the world",
            font=("Segoe UI", 12),
            fg="#7190a8",
            bg="#030712"
        )

        subtitle.pack()

        # =====================================================
        # SEARCH
        # =====================================================

        search_container = tk.Frame(
            self.main_frame,
            bg="#0b1726",
            highlightbackground="#16415b",
            highlightthickness=1
        )

        search_container.pack(
            pady=15,
            ipadx=8,
            ipady=6
        )

        tk.Label(
            search_container,
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
            search_container,
            textvariable=self.search_var,
            font=("Segoe UI", 13),
            fg="white",
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
            self.clear_search_placeholder
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_country
        )

        self.search_entry.bind(
            "<Return>",
            self.select_first_result
        )

        # =====================================================
        # CLEAR BUTTON
        # =====================================================

        tk.Button(
            search_container,
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
        # CONTENT
        # =====================================================

        content = tk.Frame(
            self.main_frame,
            bg="#030712"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=(5, 30)
        )

        # =====================================================
        # LEFT CLOCK CARD
        # =====================================================

        self.clock_card = tk.Frame(
            content,
            bg="#081421",
            highlightbackground="#123e56",
            highlightthickness=2
        )

        self.clock_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 15)
        )

        # =====================================================
        # FLAG
        # =====================================================

        self.flag_label = tk.Label(
            self.clock_card,
            text="🇮🇳",
            font=("Segoe UI Emoji", 32),
            bg="#081421"
        )

        self.flag_label.pack(
            pady=(12, 0)
        )

        # =====================================================
        # COUNTRY
        # =====================================================

        self.country_label = tk.Label(
            self.clock_card,
            text="India",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#081421"
        )

        self.country_label.pack()

        # =====================================================
        # TIMEZONE
        # =====================================================

        self.location_label = tk.Label(
            self.clock_card,
            text="Asia/Kolkata",
            font=("Segoe UI", 10),
            fg="#66859e",
            bg="#081421"
        )

        self.location_label.pack(
            pady=(0, 5)
        )

        # =====================================================
        # CLOCK CONTAINER
        # =====================================================

        clock_container = tk.Frame(
            self.clock_card,
            bg="#081421"
        )

        clock_container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(5, 25)
        )

        # =====================================================
        # ANALOG CLOCK
        # =====================================================

        self.canvas = tk.Canvas(
            clock_container,
            width=320,
            height=320,
            bg="#081421",
            highlightthickness=0
        )

        self.canvas.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # =====================================================
        # RIGHT INFORMATION CARD
        # =====================================================

        info_card = tk.Frame(
            content,
            bg="#081421",
            highlightbackground="#123e56",
            highlightthickness=2
        )

        info_card.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(15, 0)
        )

        # =====================================================
        # CURRENT TIME
        # =====================================================

        tk.Label(
            info_card,
            text="CURRENT TIME",
            font=("Segoe UI", 11, "bold"),
            fg="#66859e",
            bg="#081421"
        ).pack(
            pady=(50, 5)
        )

        # =====================================================
        # DIGITAL CLOCK
        # =====================================================

        self.time_label = tk.Label(
            info_card,
            text="00:00:00",
            font=("Consolas", 44, "bold"),
            fg="#00e5ff",
            bg="#081421"
        )

        self.time_label.pack(
            pady=8
        )

        # =====================================================
        # DATE
        # =====================================================

        self.date_label = tk.Label(
            info_card,
            text="",
            font=("Segoe UI", 17),
            fg="#dcecf5",
            bg="#081421"
        )

        self.date_label.pack(
            pady=10
        )

        # =====================================================
        # DATE BOXES
        # =====================================================

        date_frame = tk.Frame(
            info_card,
            bg="#081421"
        )

        date_frame.pack(
            pady=25
        )

        self.day_box = self.create_date_box(
            date_frame,
            "DAY"
        )

        self.month_box = self.create_date_box(
            date_frame,
            "MONTH"
        )

        self.year_box = self.create_date_box(
            date_frame,
            "YEAR"
        )

        # =====================================================
        # LIVE
        # =====================================================

        self.status_label = tk.Label(
            info_card,
            text="● LIVE",
            font=("Segoe UI", 12, "bold"),
            fg="#00ff9d",
            bg="#081421"
        )

        self.status_label.pack(
            pady=15
        )

        # =====================================================
        # DAY / NIGHT
        # =====================================================

        self.period_label = tk.Label(
            info_card,
            text="",
            font=("Segoe UI", 13, "bold"),
            fg="#ffd166",
            bg="#081421"
        )

        self.period_label.pack(
            pady=5
        )

    # =========================================================
    # SEARCH PLACEHOLDER
    # =========================================================

    def clear_search_placeholder(self, event=None):

        if self.search_entry.get() == "Search country...":

            self.search_entry.delete(
                0,
                tk.END
            )

            self.search_entry.config(
                fg="white"
            )

    # =========================================================
    # SEARCH COUNTRY
    # =========================================================

    def search_country(self, event=None):

        query = self.search_var.get().strip().lower()

        if (
            not query
            or query == "search country..."
        ):

            self.search_results = []

            self.hide_search_results()

            return

        self.search_results = [
            country
            for country in COUNTRIES
            if query in country.lower()
        ][:8]

        self.show_search_results()

    # =========================================================
    # SHOW SEARCH RESULTS
    # =========================================================

    def show_search_results(self):

        self.hide_search_results()

        if not self.search_results:
            return

        self.results_frame = tk.Frame(
            self.main_frame,
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

            tk.Button(
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
                command=lambda c=country: self.select_country(c)
            ).pack(
                fill="x",
                padx=3,
                pady=1
            )

    # =========================================================
    # HIDE RESULTS
    # =========================================================

    def hide_search_results(self):

        if hasattr(self, "results_frame"):

            try:
                self.results_frame.destroy()

            except tk.TclError:
                pass

    # =========================================================
    # SELECT COUNTRY
    # =========================================================

    def select_country(self, country):

        if country not in COUNTRIES:
            return

        self.selected_country = country

        data = COUNTRIES[country]

        self.country_label.config(
            text=country
        )

        self.flag_label.config(
            text=data["flag"]
        )

        self.location_label.config(
            text=data["timezone"]
        )

        self.search_var.set(
            country
        )

        self.search_entry.config(
            fg="white"
        )

        self.hide_search_results()

        # -----------------------------------------------------
        # RESET ANIMATIONS
        # -----------------------------------------------------

        self.sun_position = 0
        self.moon_position = 0

        # -----------------------------------------------------
        # IMPORTANT:
        # UPDATE IMMEDIATELY AFTER COUNTRY CHANGE
        # -----------------------------------------------------

        self.update_clock()

    # =========================================================
    # SELECT FIRST RESULT
    # =========================================================

    def select_first_result(self, event=None):

        if self.search_results:

            self.select_country(
                self.search_results[0]
            )

    # =========================================================
    # CLEAR SEARCH
    # =========================================================

    def clear_search(self):

        self.search_var.set("")

        self.search_results = []

        self.hide_search_results()

        self.search_entry.focus_set()

    # =========================================================
    # DATE BOX
    # =========================================================

    def create_date_box(
        self,
        parent,
        title
    ):

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

        return value

    # =========================================================
    # CREATE STARS
    # =========================================================

    def create_stars(self):

        width = self.winfo_width()

        if width < 100:
            width = 1250

        height = self.winfo_height()

        if height < 100:
            height = 760

        self.stars.clear()

        for _ in range(120):

            self.stars.append([
                random.randint(0, width),
                random.randint(0, height),
                random.choice([1, 1, 1, 2, 2, 3]),
                random.uniform(0.1, 0.5)
            ])

    # =========================================================
    # BACKGROUND ANIMATION
    # =========================================================

    def animate_background(self):

        self.background_canvas.delete("all")

        width = self.winfo_width()

        if width < 100:
            width = 1250

        height = self.winfo_height()

        if height < 100:
            height = 760

        # =====================================================
        # GET CURRENT COUNTRY TIME
        # =====================================================

        try:

            timezone = COUNTRIES[
                self.selected_country
            ]["timezone"]

            current_time = datetime.now(
                ZoneInfo(timezone)
            )

            hour = current_time.hour

            minute = current_time.minute

            # -------------------------------------------------
            # MORE ACCURATE DAY/NIGHT CALCULATION
            # -------------------------------------------------

            total_minutes = (
                hour * 60
                + minute
            )

            self.is_day = (
                6 * 60
                <= total_minutes
                <
                18 * 60
            )

        except Exception:

            self.is_day = True

        # =====================================================
        # STARS
        # =====================================================

        for index, star in enumerate(self.stars):

            x, y, size, speed = star

            star[0] -= speed

            if star[0] < 0:

                star[0] = width

                star[1] = random.randint(
                    0,
                    height
                )

            twinkle = (
                math.sin(
                    self.twinkle_offset * 0.08
                    + index
                ) + 1
            ) / 2

            if self.is_day:

                star_size = max(
                    1,
                    int(size * 0.4)
                )

            else:

                star_size = max(
                    1,
                    int(size + twinkle * 2)
                )

            self.background_canvas.create_oval(
                x,
                y,
                x + star_size,
                y + star_size,
                fill="#9cc7dc",
                outline=""
            )

        # =====================================================
        # SUN
        # =====================================================

        if self.is_day:

            self.sun_position += 0.8

            sun_x = (
                width - 180
                + math.sin(
                    math.radians(
                        self.sun_position
                    )
                ) * 35
            )

            sun_y = (
                130
                + math.cos(
                    math.radians(
                        self.sun_position
                    )
                ) * 20
            )

            for radius in range(
                90,
                20,
                -10
            ):

                self.background_canvas.create_oval(
                    sun_x - radius,
                    sun_y - radius,
                    sun_x + radius,
                    sun_y + radius,
                    outline="#163a4c"
                )

            self.background_canvas.create_oval(
                sun_x - 28,
                sun_y - 28,
                sun_x + 28,
                sun_y + 28,
                fill="#ffd166",
                outline=""
            )

            self.background_canvas.create_oval(
                sun_x - 20,
                sun_y - 20,
                sun_x + 20,
                sun_y + 20,
                fill="#ffe8a3",
                outline=""
            )

        # =====================================================
        # MOON
        # =====================================================

        else:

            self.moon_position += 0.35

            moon_x = (
                width - 180
                + math.sin(
                    math.radians(
                        self.moon_position
                    )
                ) * 45
            )

            moon_y = (
                130
                + math.cos(
                    math.radians(
                        self.moon_position
                    )
                ) * 25
            )

            for radius in range(
                75,
                20,
                -10
            ):

                self.background_canvas.create_oval(
                    moon_x - radius,
                    moon_y - radius,
                    moon_x + radius,
                    moon_y + radius,
                    outline="#141c3b"
                )

            self.background_canvas.create_oval(
                moon_x - 27,
                moon_y - 27,
                moon_x + 27,
                moon_y + 27,
                fill="#e8edf7",
                outline=""
            )

            self.background_canvas.create_oval(
                moon_x - 14,
                moon_y - 28,
                moon_x + 18,
                moon_y + 10,
                fill="#030712",
                outline=""
            )

        # =====================================================
        # BACKGROUND GLOW
        # =====================================================

        center_x = width - 80
        center_y = height - 80

        for radius in range(
            170,
            30,
            -20
        ):

            self.background_canvas.create_oval(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                outline="#0a2336"
            )

        # =====================================================
        # COUNTERS
        # =====================================================

        self.animation_offset += 1
        self.twinkle_offset += 1

        self.after(
            40,
            self.animate_background
        )

    # =========================================================
    # ANALOG CLOCK
    # =========================================================

    def draw_clock(
        self,
        current_time
    ):

        self.canvas.delete("all")

        width = 320
        height = 320

        center_x = width / 2
        center_y = height / 2

        radius = 125

        # =====================================================
        # OUTER GLOW
        # =====================================================

        self.canvas.create_oval(
            center_x - radius - 12,
            center_y - radius - 12,
            center_x + radius + 12,
            center_y + radius + 12,
            outline="#0c2d42",
            width=4
        )

        self.canvas.create_oval(
            center_x - radius - 6,
            center_y - radius - 6,
            center_x + radius + 6,
            center_y + radius + 6,
            outline="#00bcd4",
            width=2
        )

        # =====================================================
        # CLOCK FACE
        # =====================================================

        self.canvas.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            fill="#06111c",
            outline="#1d526b",
            width=3
        )

        # =====================================================
        # DAY / NIGHT ARC
        # =====================================================

        if self.is_day:

            self.canvas.create_arc(
                center_x - radius + 8,
                center_y - radius + 8,
                center_x + radius - 8,
                center_y + radius - 8,
                start=0,
                extent=180,
                outline="#1e6b8b",
                width=5
            )

        else:

            self.canvas.create_arc(
                center_x - radius + 8,
                center_y - radius + 8,
                center_x + radius - 8,
                center_y + radius - 8,
                start=180,
                extent=180,
                outline="#30285c",
                width=5
            )

        # =====================================================
        # HOUR MARKERS
        # =====================================================

        for h in range(1, 13):

            angle = math.radians(
                h * 30 - 90
            )

            x1 = (
                center_x
                + math.cos(angle)
                * (radius - 9)
            )

            y1 = (
                center_y
                + math.sin(angle)
                * (radius - 9)
            )

            x2 = (
                center_x
                + math.cos(angle)
                * (radius - 21)
            )

            y2 = (
                center_y
                + math.sin(angle)
                * (radius - 21)
            )

            self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill="#8ed8e8",
                width=3
            )

            number_x = (
                center_x
                + math.cos(angle)
                * (radius - 38)
            )

            number_y = (
                center_y
                + math.sin(angle)
                * (radius - 38)
            )

            self.canvas.create_text(
                number_x,
                number_y,
                text=str(h),
                fill="#d9f8ff",
                font=(
                    "Segoe UI",
                    10,
                    "bold"
                )
            )

        # =====================================================
        # MINUTE MARKERS
        # =====================================================

        for minute in range(60):

            if minute % 5 == 0:
                continue

            angle = math.radians(
                minute * 6 - 90
            )

            x1 = (
                center_x
                + math.cos(angle)
                * (radius - 10)
            )

            y1 = (
                center_y
                + math.sin(angle)
                * (radius - 10)
            )

            x2 = (
                center_x
                + math.cos(angle)
                * (radius - 15)
            )

            y2 = (
                center_y
                + math.sin(angle)
                * (radius - 15)
            )

            self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill="#31566c",
                width=1
            )

        # =====================================================
        # TIME
        # =====================================================

        hour = current_time.hour % 12
        minute = current_time.minute
        second = current_time.second

        # =====================================================
        # HOUR HAND
        # =====================================================

        hour_angle = math.radians(
            (hour + minute / 60) * 30 - 90
        )

        hour_x = (
            center_x
            + math.cos(hour_angle)
            * 65
        )

        hour_y = (
            center_y
            + math.sin(hour_angle)
            * 65
        )

        self.canvas.create_line(
            center_x,
            center_y,
            hour_x,
            hour_y,
            fill="#ffffff",
            width=7,
            capstyle=tk.ROUND
        )

        # =====================================================
        # MINUTE HAND
        # =====================================================

        minute_angle = math.radians(
            (minute + second / 60) * 6 - 90
        )

        minute_x = (
            center_x
            + math.cos(minute_angle)
            * 95
        )

        minute_y = (
            center_y
            + math.sin(minute_angle)
            * 95
        )

        self.canvas.create_line(
            center_x,
            center_y,
            minute_x,
            minute_y,
            fill="#00e5ff",
            width=5,
            capstyle=tk.ROUND
        )

        # =====================================================
        # SECOND HAND
        # =====================================================

        second_angle = math.radians(
            second * 6 - 90
        )

        second_x = (
            center_x
            + math.cos(second_angle)
            * 110
        )

        second_y = (
            center_y
            + math.sin(second_angle)
            * 110
        )

        self.canvas.create_line(
            center_x,
            center_y,
            second_x,
            second_y,
            fill="#ff4081",
            width=2,
            capstyle=tk.ROUND
        )

        # =====================================================
        # CENTER HUB
        # =====================================================

        self.canvas.create_oval(
            center_x - 9,
            center_y - 9,
            center_x + 9,
            center_y + 9,
            fill="#00bcd4",
            outline=""
        )

        self.canvas.create_oval(
            center_x - 3,
            center_y - 3,
            center_x + 3,
            center_y + 3,
            fill="#ffffff",
            outline=""
        )

    # =========================================================
    # UPDATE CLOCK
    # =========================================================

    def update_clock(self):

        try:

            # =================================================
            # COUNTRY
            # =================================================

            data = COUNTRIES[
                self.selected_country
            ]

            timezone = data["timezone"]

            # =================================================
            # COUNTRY LOCAL TIME
            # =================================================

            current_time = datetime.now(
                ZoneInfo(timezone)
            )

            # =================================================
            # DIGITAL TIME
            # =================================================

            self.time_label.config(
                text=current_time.strftime(
                    "%H:%M:%S"
                )
            )

            # =================================================
            # FULL DATE
            # =================================================

            self.date_label.config(
                text=current_time.strftime(
                    "%A, %d %B %Y"
                )
            )

            # =================================================
            # DAY
            # =================================================

            self.day_box.config(
                text=current_time.strftime("%d")
            )

            # =================================================
            # MONTH
            # =================================================

            self.month_box.config(
                text=current_time.strftime("%B")
            )

            # =================================================
            # YEAR
            # =================================================

            self.year_box.config(
                text=current_time.strftime("%Y")
            )

            # =================================================
            # DAY / NIGHT
            # =================================================

            hour = current_time.hour
            minute = current_time.minute

            total_minutes = (
                hour * 60
                + minute
            )

            # -------------------------------------------------
            # DAY = 06:00 - 17:59
            # NIGHT = 18:00 - 05:59
            # -------------------------------------------------

            if (
                6 * 60
                <= total_minutes
                <
                18 * 60
            ):

                self.is_day = True

                self.period_label.config(
                    text="☀ DAY TIME",
                    fg="#ffd166"
                )

            else:

                self.is_day = False

                self.period_label.config(
                    text="🌙 NIGHT TIME",
                    fg="#a8b9ff"
                )

            # =================================================
            # DRAW ANALOG CLOCK
            # =================================================

            self.draw_clock(
                current_time
            )

        except Exception as error:

            print(
                "Clock error:",
                error
            )

        # =====================================================
        # RUN AGAIN AFTER 1 SECOND
        # =====================================================

        self.after(
            1000,
            self.update_clock
        )


# =============================================================
# APPLICATION START
# =============================================================

if __name__ == "__main__":

    app = WorldTimeExplorer()

    app.mainloop()