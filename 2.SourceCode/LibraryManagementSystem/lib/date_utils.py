from datetime import datetime, timedelta


def format_date_mmddyyyy(date_obj):
    return date_obj.strftime("%m-%d-%Y") 

def format_date_yyyy(date_obj):
    return date_obj.strftime("%Y") 


def is_valid_return_date(return_date: datetime) -> bool:
    today = datetime.now().date()
    min_valid_date = today + timedelta(days=1)
    return return_date.date() >= min_valid_date