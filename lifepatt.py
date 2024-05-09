import csv
from datetime import datetime, timedelta
from typing import Dict, List, Union


def generate_empty_datetimes(
    ttb_start: datetime, ttb_end: datetime, ttb_unit_delta: timedelta
):
    eventlist = []
    current_date = ttb_start
    while current_date < ttb_end:
        eventlist.append([current_date, None])
        current_date += ttb_unit_delta

    return eventlist


def create_eventlist():
    ttb_year = int(input("Start of Timetable (Year): "))
    ttb_month = int(input("Start of Timetable (Month): "))
    ttb_day = int(input("Start of Timetable (Day): "))
    ttb_hour = int(input("Start of Timetable (Hour): "))
    ttb_min = int(input("Start of Timetable (Minute): "))
    ttb_sec = int(input("Start of Timetable (Second): "))
    ttb_start = datetime(ttb_year, ttb_month, ttb_day, ttb_hour, ttb_min, ttb_sec)

    mode = 0
    while mode not in [1, 2]:
        mode = int(
            input("(1) Specify the Length of Timetable; (2) Specify the End Datetime: ")
        )

        if mode == 1:
            ttb_len = int(input("Enter the Length of Timetable (Days): "))
            ttb_end = ttb_start + timedelta(days=ttb_len)
        elif mode == 2:
            ttb_year_end = int(input("End of Timetable (Year): "))
            ttb_month_end = int(input("End of Timetable (Month): "))
            ttb_day_end = int(input("End of Timetable (Day): "))
            ttb_hour_end = int(input("End of Timetable (Hour): "))
            ttb_min_end = int(input("End of Timetable (Minute): "))
            ttb_sec_end = int(input("End of Timetable (Second): "))
            ttb_end = datetime(
                ttb_year_end,
                ttb_month_end,
                ttb_day_end,
                ttb_hour_end,
                ttb_min_end,
                ttb_sec_end,
            )
        else:
            print("Invalid Mode: Please Enter 1 or 2.")

    ttb_unit = int(input("Enter the Unit of Event Duration (Minutes): "))
    ttb_unit_delta = timedelta(minutes=ttb_unit)

    eventlist = generate_empty_datetimes(ttb_start, ttb_end, ttb_unit_delta)

    return eventlist


def schedule_events(
    eventlist: List[List[Union[datetime, None]]], idx2lbl: Dict[int, str]
):
    print(f"--------------------------------------------------------------")

    i = 0

    while i < len(eventlist):
        print(f"Available Events: {idx2lbl}")
        print(f"-----New Event-----")
        event_start = eventlist[i][0]
        print(f"Event Start Datetime: {event_start}")
        event_idx = int(input("Enter the Index of Event (0, 1, 2, 3, 4): "))
        event_hours = int(input("Enter the Length of Event (Hours): "))
        event_minutes = int(input("Enter the Length of Event (Minutes): "))
        event_end = event_start + timedelta(hours=event_hours, minutes=event_minutes)

        while i < len(eventlist) and eventlist[i][0] < event_end:
            eventlist[i] = (eventlist[i][0], idx2lbl[event_idx])
            print(f"Datetime: {eventlist[i][0]}; Event: {eventlist[i][1]}")
            i += 1

        print(f"Event End Datetime: {event_end}")
        print(f"--------------------------------------------------------------")

    return eventlist


def write_dataset(
    eventlist: List[List[Union[datetime, None]]], csv_path: str, columns: List[str]
):
    with open(csv_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)

        for row in eventlist:
            timestamp, event = row
            writer.writerow([timestamp.strftime("%Y-%m-%d %H:%M:%S"), event])


def read_dataset(csv_path: str):
    eventlist = []
    with open(csv_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  ## Skip the header row
        for row in reader:
            timestamp = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            event = row[1]
            eventlist.append([timestamp, event])
    return eventlist


def is_same_csv(csv_path_1, csv_path_2):
    try:
        with open(csv_path_1, "r") as csv_1, open(csv_path_2, "r") as csv_2:
            csv_path_1 = list(csv.reader(csv_1))
            csv_path_2 = list(csv.reader(csv_2))

            if len(csv_path_1) != len(csv_path_2):
                return False

            for row_1, row_2 in zip(csv_path_1, csv_path_2):
                if row_1 != row_2:
                    return False

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


def show_dataset_info(
    csv_path: str = None, message: str = "Timetable Info:", return_info: bool = False
):
    if csv_path is None:
        csv_path = input("Enter the Path to the CSV: ")

    eventlist = read_dataset(csv_path)

    ttb_start = eventlist[0][0]
    ttb_end = eventlist[-1][0]
    ttb_unit_delta = ttb_end - eventlist[-2][0]

    print(f"--------------------------------------------------------------")
    print(f"{message}")
    print(f"Start of Timetable: {ttb_start}")
    print(f"End of Timetable: {ttb_end}")
    print(f"Length of Timetable: {ttb_end - ttb_start + ttb_unit_delta}")
    print(f"Unit of Event Duration: {ttb_unit_delta.seconds / 60} Minutes")
    print(f"--------------------------------------------------------------")

    if return_info:
        return eventlist, ttb_start, ttb_end, ttb_unit_delta


def extend_eventlist():
    csv_path_prev = input("Enter the Path to the Original CSV: ")

    eventlist_prev, ttb_start_prev, ttb_end_prev, ttb_unit_delta = show_dataset_info(
        csv_path=csv_path_prev,
        message="Original Timetable Info:",
        return_info=True,
    )

    ttb_start = ttb_end_prev + ttb_unit_delta

    mode = 0
    while mode not in [1, 2]:
        mode = int(
            input(
                "(1) Specify the Number of Days to Add; (2) Specify the End Datetime: "
            )
        )

        if mode == 1:
            ttb_len = int(input("Enter the Number of Days to Add (Days): "))
            ttb_end = ttb_start + timedelta(days=ttb_len)
        elif mode == 2:
            ttb_year_end = int(input("End of Timetable (Year): "))
            ttb_month_end = int(input("End of Timetable (Month): "))
            ttb_day_end = int(input("End of Timetable (Day): "))
            ttb_hour_end = int(input("End of Timetable (Hour): "))
            ttb_min_end = int(input("End of Timetable (Minute): "))
            ttb_sec_end = int(input("End of Timetable (Second): "))
            ttb_end = datetime(
                ttb_year_end,
                ttb_month_end,
                ttb_day_end,
                ttb_hour_end,
                ttb_min_end,
                ttb_sec_end,
            )
        else:
            print("Invalid Mode: Please Enter 1 or 2.")

    idx_empty = len(eventlist_prev)

    eventlist = eventlist_prev + generate_empty_datetimes(
        ttb_start, ttb_end, ttb_unit_delta
    )

    return eventlist, idx_empty


def duplicate_events(eventlist: List[List[Union[datetime, None]]], idx_empty: int):
    idx_current = 0
    idx_empty

    while idx_empty < len(eventlist):
        eventlist[idx_empty][1] = eventlist[idx_current][1]
        idx_current += 1
        idx_empty += 1

    return eventlist
