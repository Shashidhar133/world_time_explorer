import tkinter as tk
import math


class AnalogClock:
    def __init__(self, parent):
        self.parent = parent

        self.width = 320
        self.height = 320
        self.radius = 125

        self.canvas = tk.Canvas(
            parent,
            width=self.width,
            height=self.height,
            bg="#081421",
            highlightthickness=0
        )

        self.canvas.pack(
            expand=True
        )

    # =====================================================
    # DRAW CLOCK
    # =====================================================

    def draw(self, current_time):

        if current_time is None:
            return

        self.canvas.delete("all")

        center_x = self.width / 2
        center_y = self.height / 2
        radius = self.radius

        # =================================================
        # OUTER GLOW RINGS
        # =================================================

        self.canvas.create_oval(
            center_x - radius - 14,
            center_y - radius - 14,
            center_x + radius + 14,
            center_y + radius + 14,
            outline="#09253a",
            width=5
        )

        self.canvas.create_oval(
            center_x - radius - 7,
            center_y - radius - 7,
            center_x + radius + 7,
            center_y + radius + 7,
            outline="#00bcd4",
            width=2
        )

        # =================================================
        # CLOCK FACE
        # =================================================

        self.canvas.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            fill="#06111c",
            outline="#1d526b",
            width=3
        )

        # =================================================
        # DAY / NIGHT ARC
        # =================================================

        hour24 = current_time.hour

        if 6 <= hour24 < 18:

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

        # =================================================
        # HOUR MARKERS
        # =================================================

        for hour in range(1, 13):

            angle = math.radians(
                hour * 30 - 90
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
                text=str(hour),
                fill="#d9f8ff",
                font=(
                    "Segoe UI",
                    10,
                    "bold"
                )
            )

        # =================================================
        # MINUTE MARKERS
        # =================================================

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

        # =================================================
        # CURRENT TIME
        # =================================================

        hour = current_time.hour % 12
        minute = current_time.minute
        second = current_time.second
        microsecond = current_time.microsecond

        # Smooth second
        second_float = (
            second
            + microsecond / 1_000_000
        )

        # =================================================
        # HOUR HAND
        # =================================================

        hour_angle = math.radians(
            (
                hour
                + minute / 60
                + second / 3600
            ) * 30 - 90
        )

        self.draw_hand(
            center_x,
            center_y,
            hour_angle,
            65,
            "#ffffff",
            7
        )

        # =================================================
        # MINUTE HAND
        # =================================================

        minute_angle = math.radians(
            (
                minute
                + second / 60
            ) * 6 - 90
        )

        self.draw_hand(
            center_x,
            center_y,
            minute_angle,
            95,
            "#00e5ff",
            5
        )

        # =================================================
        # SECOND HAND
        # =================================================

        second_angle = math.radians(
            second_float * 6 - 90
        )

        self.draw_hand(
            center_x,
            center_y,
            second_angle,
            110,
            "#ff4081",
            2
        )

        # =================================================
        # SECOND HAND COUNTERWEIGHT
        # =================================================

        back_x = (
            center_x
            - math.cos(second_angle)
            * 16
        )

        back_y = (
            center_y
            - math.sin(second_angle)
            * 16
        )

        self.canvas.create_line(
            center_x,
            center_y,
            back_x,
            back_y,
            fill="#ff4081",
            width=2
        )

        # =================================================
        # CENTER HUB
        # =================================================

        self.canvas.create_oval(
            center_x - 10,
            center_y - 10,
            center_x + 10,
            center_y + 10,
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

    # =====================================================
    # HAND
    # =====================================================

    def draw_hand(
        self,
        center_x,
        center_y,
        angle,
        length,
        color,
        width
    ):

        x = (
            center_x
            + math.cos(angle)
            * length
        )

        y = (
            center_y
            + math.sin(angle)
            * length
        )

        self.canvas.create_line(
            center_x,
            center_y,
            x,
            y,
            fill=color,
            width=width,
            capstyle=tk.ROUND
        )