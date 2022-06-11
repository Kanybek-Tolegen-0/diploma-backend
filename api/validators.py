from datetime import datetime, timedelta, time

def validate_reserve_datetime(
    new_reserve_start_datetime: datetime,
    new_reserve_duration: timedelta,
    existing_reserve_start_datetime: datetime,
    existing_reserve_duration: timedelta
    ):

    # 3 validations:
    # 1 - new reserve starts earlier, but ends in time of existing reserve
    if existing_reserve_start_datetime < new_reserve_start_datetime + new_reserve_duration and \
        new_reserve_start_datetime + new_reserve_duration < existing_reserve_start_datetime + existing_reserve_duration:
        raise Exception("New reserve starts in time of existing reserve time")
    # 2 - new reserve starts in time of existing reserve
    elif new_reserve_start_datetime >= existing_reserve_start_datetime and \
        new_reserve_start_datetime < existing_reserve_start_datetime + existing_reserve_duration:
        raise Exception("New reserve starts in time of existing reserve time")
    elif new_reserve_start_datetime < existing_reserve_start_datetime and \
        new_reserve_start_datetime + new_reserve_duration > existing_reserve_start_datetime + existing_reserve_duration:
        raise Exception("New reserve starts in time of existing reserve time")
    return True


def validate_passed_datetime(new_reserve_start_datetime: datetime):
    tzone = new_reserve_start_datetime.tzinfo
    if new_reserve_start_datetime < datetime.now(tzone):
        raise Exception("Cannot reserve passed time")
    return True


def validated_by_cafe_working_hours(
    new_reserve_start_datetime: datetime,
    new_reserve_duration: timedelta,
    cafe_start_time: time,
    cafe_end_time: time
    ):
    new_reserve_end_datetime = new_reserve_start_datetime + new_reserve_duration
    if new_reserve_start_datetime.time() < cafe_start_time:
        raise Exception("Too early for cafe start time")
    elif new_reserve_end_datetime.time() > cafe_end_time:
        raise Exception("Too late for cafe end time")
    return True
