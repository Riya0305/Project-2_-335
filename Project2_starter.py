import json
from datetime import datetime, timedelta

def time_to_minutes(time_str):
    t = datetime.strptime(time_str, "%H:%M")
    return t.hour * 60 + t.minute

def minutes_to_time(minutes):
    return (datetime.min + timedelta(minutes=minutes)).strftime("%H:%M")

def get_free_intervals(busy_schedule, active_period):
    login, logout = time_to_minutes(active_period[0]), time_to_minutes(active_period[1])
    busy_intervals = [[time_to_minutes(start), time_to_minutes(end)] for start, end in busy_schedule]
    free_intervals = []
    start = login

    # Sort busy intervals to process in order
    busy_intervals.sort()

    # Find gaps between busy intervals as free intervals
    for busy_start, busy_end in busy_intervals:
        if start < busy_start:
            free_intervals.append([start, busy_start])
        start = max(start, busy_end)

    # If there's free time after the last busy period until logout
    if start < logout:
        free_intervals.append([start, logout])

    return free_intervals

def merge_intervals(intervals, meeting_duration):
    # Sort intervals to prepare for merging
    intervals.sort()
    merged_intervals = []
    current_start, current_end = intervals[0]

    for start, end in intervals[1:]:
        # If intervals overlap or touch, merge them
        if start <= current_end:
            current_end = max(current_end, end)
        else:
            # Save the merged interval if it meets the meeting duration
            if current_end - current_start >= meeting_duration:
                merged_intervals.append([current_start, current_end])
            # Start a new interval
            current_start, current_end = start, end

    # Append the last interval if it meets the duration
    if current_end - current_start >= meeting_duration:
        merged_intervals.append([current_start, current_end])

    # Convert intervals back to time format
    return [[minutes_to_time(start), minutes_to_time(end)] for start, end in merged_intervals]

def find_available_slots(busy_schedules, active_periods, meeting_duration):
    all_free_intervals = []
    for i in range(len(busy_schedules)):
        # Get free intervals for each person's schedule and active period
        free_intervals = get_free_intervals(busy_schedules[i], active_periods[i])
        all_free_intervals.extend(free_intervals)
    
    # Merge all intervals and filter by the meeting duration
    return merge_intervals(all_free_intervals, meeting_duration)

def main():
    try:
        # Reading input from Input.txt
        with open("Input.txt", "r") as file:
            lines = file.readlines()
        
        busy_schedules = []
        active_periods = []
        meeting_duration = int(lines[-1].strip())  # Last line is the meeting duration

        for i in range(0, len(lines) - 1, 2):
            busy_schedule = json.loads(lines[i].strip().replace("‘", "\"").replace("’", "\""))
            active_period = json.loads(lines[i + 1].strip().replace("‘", "\"").replace("’", "\""))
            busy_schedules.append(busy_schedule)
            active_periods.append(active_period)

        available_slots = find_available_slots(busy_schedules, active_periods, meeting_duration)
        
        # Writing output to Output.txt
        with open("Output.txt", "w") as file:
            file.write(str(available_slots) + "\n")
        print("Available slots saved to Output.txt:", available_slots)

    except FileNotFoundError:
        print("Error: Input.txt file not found.")
    except ValueError as e:
        print("Error in processing file content:", e)
    except Exception as e:
        print("Unexpected error:", e)

if __name__ == "__main__":
    main()
