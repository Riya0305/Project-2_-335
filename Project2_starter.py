import json
from datetime import datetime, timedelta

def time_to_minutes(time_str):
    t = datetime.strptime(time_str, "%H:%M")
    return t.hour * 60 + t.minute

def minutes_to_time(minutes):
    return (datetime.min + timedelta(minutes=minutes)).strftime("%H:%M")

def find_common_free_intervals(busy_schedules, active_periods, meeting_duration):
    # Initialize the common free interval based on the first person's active period
    start_common = max(time_to_minutes(active_period[0]) for active_period in active_periods)
    end_common = min(time_to_minutes(active_period[1]) for active_period in active_periods)

    if start_common >= end_common:
        return []  # No common time available
    
    # Track all busy times directly
    for i in range(len(busy_schedules)):
        for busy_start, busy_end in busy_schedules[i]:
            start_busy = time_to_minutes(busy_start)
            end_busy = time_to_minutes(busy_end)
            
            # Adjust common interval by excluding busy times within it
            if start_busy <= start_common < end_busy:
                start_common = end_busy
            if start_busy < end_common <= end_busy:
                end_common = start_busy

            # If at any point there’s no valid time left
            if start_common >= end_common:
                return []  # No available common slot

    # Check if the final common interval meets the meeting duration requirement
    if end_common - start_common >= meeting_duration:
        return [[minutes_to_time(start_common), minutes_to_time(end_common)]]
    else:
        return []  # No slot long enough for the meeting

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

        available_slots = find_common_free_intervals(busy_schedules, active_periods, meeting_duration)
        
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
