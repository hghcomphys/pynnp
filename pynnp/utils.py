from datetime import datetime


def get_time_and_date():
    return datetime.now().strftime("%H:%M:%S %d/%m/%Y")
