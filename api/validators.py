from datetime import datetime, timedelta

def validate_reserve_datetime(
    new_reserve_start_datetime: datetime,
    new_reserve_duration: timedelta,
    existing_reserve_start_datetime: datetime,
    existing_reserve_duration: duration
    ):

    # 3 validations:
    # 1 - new reserve starts earlier, but ends in time of existing reserve
    if existing_reserve_start_datetime < new_reserve_start_datetime + new_reserve_duration and \
       new_reserve_start_datetime + new_reserve_duration < existing_reserve_start_datetime + existing_reserve_duration:
       return Exception("New reserve starts in time of existing reserve time")
    #
#    elif existing
