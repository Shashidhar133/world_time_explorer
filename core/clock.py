from datetime import datetime


def get_time_string(current_time):
    return current_time.strftime("%H:%M:%S")


def get_date_string(current_time):
    return current_time.strftime("%A, %d %B %Y")


def get_day(current_time):
    return current_time.strftime("%d")


def get_month(current_time):
    return current_time.strftime("%B")


def get_year(current_time):
    return current_time.strftime("%Y")


def is_daytime(current_time):
    return 6 <= current_time.hour < 18