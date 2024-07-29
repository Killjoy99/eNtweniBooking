from datetime import datetime, timedelta


async def calculate_minutes(check_in: datetime, check_out: datetime):
    minutes: int = (check_out - check_in).seconds / 60 
    return minutes

async def calculate_hours(check_in: datetime, check_out: datetime):
    hours: int = await calculate_minutes(check_in, check_out)
    return hours

async def calculate_days(check_in: datetime, check_out: datetime):
    days: int = (check_out - check_in).days()
    return days

async def calculate_months(check_in: datetime, check_out: datetime):
    months: int = (check_out.year - check_in.year) * 12 + (check_out.month - check_in.month)
    return months