from datetime import datetime, timedelta

def time_to_minutes(time_str):
    # Convert a time string 'HH:MM' to minutes since midnight
    t = datetime.strptime(time_str, "%H:%M")
    return t.hour * 60 + t.minute

def minutes_to_time(minutes):
    # Convert minutes since midnight to a time string 'HH:MM'
    return (datetime.min + timedelta(minutes=minutes)).strftime("%H:%M")

def get_free_times(busy_schedule, active_period, meeting_duration):
    # Generate free intervals for a person based on their busy schedule and active period.
    login, logout = time_to_minutes(active_period[0]), time_to_minutes(active_period[1])
    busy_schedule = [[time_to_minutes(start), time_to_minutes(end)] for start, end in busy_schedule]

    # Initialize free intervals
    free_times = []
    start = login

    # Go through busy intervals to create free times
    for interval in busy_schedule:
        if start + meeting_duration <= interval[0]:  # There is enough time before the busy interval
            free_times.append([start, interval[0]])
        start = max(start, interval[1])  # Update start to the end of the current busy interval

    # Check if there's time after the last busy period until logout
    if start + meeting_duration <= logout:
        free_times.append([start, logout])

    return free_times
