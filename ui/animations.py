import tkinter as tk
import math
import random
from datetime import datetime
from zoneinfo import ZoneInfo

from config.countries import COUNTRIES


class BackgroundAnimation:
    def __init__(self, parent, get_selected_country):
        self.parent = parent
        self.get_selected_country = get_selected_country

        self.canvas = tk.Canvas(
            parent,
            bg="#030712",
            highlightthickness=0
        )

        self.canvas.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        self.stars = []

        self.sun_position = 0
        self.moon_position = 0

        self.twinkle_offset = 0
        self.animation_offset = 0

        self.create_stars()

    # =====================================================
    # STARS
    # =====================================================

    def create_stars(self):

        width = self.parent.winfo_width() or 1250
        height = self.parent.winfo_height() or 760

        self.stars.clear()

        for _ in range(140):

            self.stars.append([
                random.randint(0, width),
                random.randint(0, height),
                random.choice(
                    [1, 1, 1, 2, 2, 3]
                ),
                random.uniform(
                    0.1,
                    0.5
                )
            ])

    # =====================================================
    # BACKGROUND ANIMATION
    # =====================================================

    def animate(self):

        self.canvas.delete("all")

        width = (
            self.parent.winfo_width()
            or 1250
        )

        height = (
            self.parent.winfo_height()
            or 760
        )

        try:

            country = self.get_selected_country()

            timezone = COUNTRIES[
                country
            ]["timezone"]

            current_time = datetime.now(
                ZoneInfo(timezone)
            )

            hour = current_time.hour
            minute = current_time.minute

        except Exception:

            hour = 12
            minute = 0

        # =================================================
        # DAY / NIGHT
        # =================================================

        self.is_day = (
            6 <= hour < 18
        )

        # =================================================
        # SPACE GRID / AURORA LINES
        # =================================================

        for i in range(7):

            y = 90 + i * 85

            drift = math.sin(
                self.animation_offset
                * 0.012
                + i
            ) * 18

            self.canvas.create_arc(
                -250 + drift,
                y,
                width + 250 + drift,
                y + 180,
                start=190,
                extent=160,
                outline="#071b2b",
                width=1
            )

        # =================================================
        # STARS
        # =================================================

        for index, star in enumerate(
            self.stars
        ):

            x, y, size, speed = star

            star[0] -= speed

            if star[0] < -5:

                star[0] = width + 5

                star[1] = random.randint(
                    0,
                    height
                )

            twinkle = (
                math.sin(
                    self.twinkle_offset
                    * 0.08
                    + index
                ) + 1
            ) / 2

            if self.is_day:

                star_size = max(
                    1,
                    int(size * 0.35)
                )

            else:

                star_size = max(
                    1,
                    int(
                        size
                        + twinkle * 2
                    )
                )

            self.canvas.create_oval(
                x,
                y,
                x + star_size,
                y + star_size,
                fill="#9cc7dc",
                outline=""
            )

        # =================================================
        # SUN / MOON
        # =================================================

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

            # Sun glow

            for radius in range(
                95,
                20,
                -10
            ):

                self.canvas.create_oval(
                    sun_x - radius,
                    sun_y - radius,
                    sun_x + radius,
                    sun_y + radius,
                    outline="#163a4c"
                )

            # Sun

            self.canvas.create_oval(
                sun_x - 30,
                sun_y - 30,
                sun_x + 30,
                sun_y + 30,
                fill="#ffd166",
                outline=""
            )

            self.canvas.create_oval(
                sun_x - 21,
                sun_y - 21,
                sun_x + 21,
                sun_y + 21,
                fill="#ffe8a3",
                outline=""
            )

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

            # Moon glow

            for radius in range(
                80,
                20,
                -10
            ):

                self.canvas.create_oval(
                    moon_x - radius,
                    moon_y - radius,
                    moon_x + radius,
                    moon_y + radius,
                    outline="#141c3b"
                )

            # Moon

            self.canvas.create_oval(
                moon_x - 28,
                moon_y - 28,
                moon_x + 28,
                moon_y + 28,
                fill="#e8edf7",
                outline=""
            )

            # Crescent cutout

            self.canvas.create_oval(
                moon_x - 13,
                moon_y - 30,
                moon_x + 20,
                moon_y + 12,
                fill="#030712",
                outline=""
            )

        # =================================================
        # LOWER FLOATING GLOW
        # =================================================

        cx = width - 80
        cy = height - 80

        for radius in range(
            180,
            20,
            -20
        ):

            self.canvas.create_oval(
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
                outline="#0a2336"
            )

        self.animation_offset += 1
        self.twinkle_offset += 1

        self.parent.after(
            40,
            self.animate
        )

    # =====================================================
    # RESET COUNTRY SCENE
    # =====================================================

    def reset_scene(self):

        self.sun_position = 0
        self.moon_position = 0


class UIAnimation:
    def __init__(
        self,
        status_label,
        sync_label
    ):

        self.status_label = status_label
        self.sync_label = sync_label

        self.clock_pulse = 0

    # =====================================================
    # LIVE INDICATOR
    # =====================================================

    def animate(self):

        pulse = (
            math.sin(
                self.clock_pulse
                * 0.08
            ) + 1
        ) / 2

        if pulse > 0.55:

            self.status_label.config(
                fg="#00ff9d"
            )

            self.sync_label.config(
                fg="#246078"
            )

        else:

            self.status_label.config(
                fg="#00c982"
            )

            self.sync_label.config(
                fg="#31566c"
            )

        self.clock_pulse += 1

        self.status_label.after(
            50,
            self.animate
        )