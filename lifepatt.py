import csv
import math
import os
from datetime import datetime, timedelta
from typing import Dict, List, Union

import pandas as pd


def getDatetime(message: str = "Start of Timetable") -> datetime:
    year = int(input(f"{message} (Year): "))
    month = int(input(f"{message} (Month): "))
    day = int(input(f"{message} (Day): "))
    hour = int(input(f"{message} (Hour): "))
    min = int(input(f"{message} (Minute): "))
    sec = int(input(f"{message} (Second): "))

    return datetime(year, month, day, hour, min, sec)


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
    ttb_start = getDatetime(message="Start of Timetable")

    mode = 0
    while mode not in [1, 2]:
        mode = int(
            input("(1) Specify the Length of Timetable; (2) Specify the End Datetime: ")
        )

        if mode == 1:
            ttb_len = int(input("Enter the Length of Timetable (Days): "))
            ttb_end = ttb_start + timedelta(days=ttb_len)
        elif mode == 2:
            ttb_end = getDatetime(message="End of Timetable")
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
        idx_event = int(input("Enter the Index of Event (0, 1, 2, 3, 4): "))
        event_hours = int(input("Enter the Length of Event (Hours): "))
        event_minutes = int(input("Enter the Length of Event (Minutes): "))
        event_end = event_start + timedelta(hours=event_hours, minutes=event_minutes)

        while i < len(eventlist) and eventlist[i][0] < event_end:
            eventlist[i] = (eventlist[i][0], idx2lbl[idx_event])
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


def lbl2idx_eventlist(
    eventlist: List[List[Union[datetime, None]]], lbl2idx: Dict[str, int]
):
    for event in eventlist:
        event[1] = lbl2idx[event[1]]
    return eventlist


def idx2lbl_eventlist(
    eventlist: List[List[Union[datetime, None]]], idx2lbl: Dict[int, str]
):
    for event in eventlist:
        event[1] = idx2lbl[event[1]]
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
            ttb_end = getDatetime(message="End of Timetable")
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


def get_closest_date_idx(
    eventlist: List[List[Union[datetime, None]]],
    target_date: datetime,
    condition: str = "none",
) -> int:
    if condition == "earlier":
        earlier_dates = [
            (i, date) for i, (date, _) in enumerate(eventlist) if date <= target_date
        ]

        if earlier_dates:
            return max(earlier_dates, key=lambda x: x[1])[0]
        else:
            print("No Earlier Date")
            return -1

    elif condition == "later":
        later_dates = [
            (i, date) for i, (date, _) in enumerate(eventlist) if date >= target_date
        ]

        if later_dates:
            return min(later_dates, key=lambda x: x[1])[0]
        else:
            print("No Later Date")
            return -1

    else:
        date_diffs = [
            (i, date, abs(date - target_date)) for i, (date, _) in enumerate(eventlist)
        ]
        sorted_date_diffs = sorted(date_diffs, key=lambda x: x[2])

        if sorted_date_diffs:
            return sorted_date_diffs[0][0]
        else:
            print("Empty Eventlist")
            return -1


def get_train_test_idx(
    eventlist: List[List[Union[datetime, None]]],
    ttb_unit_delta: timedelta,
    stage: str,
    test_start: datetime = None,
):
    if stage not in ["train", "test"]:
        raise ValueError("Invalid stage. Use 'train' or 'test'.")

    print(f"Splitting the {stage.capitalize()} Set:")

    idx_start = None
    mode = 0
    while mode not in [1, 2, 3]:
        mode = int(
            input(
                f"(1) Specify the Ratio of the {stage.capitalize()} Set; (2) Specify the Start Datetime of the {stage.capitalize()} Set; (3) Specify the Size of {stage.capitalize()} Set (Days): "
            )
        )
        if mode == 1:
            ratio = float(
                input(f"Enter the Ratio of the {stage.capitalize()} Set (0-1): ")
            )
            print(f"Specified Ratio of {stage.capitalize()} Set: {ratio}")
            idx_start = len(eventlist) - math.ceil(len(eventlist) * ratio)

        elif mode == 2:
            start_target = getDatetime(message=f"Start of {stage.capitalize()} Set")
            print(f"Specified Start of {stage.capitalize()} Set: {start_target}")
            idx_start = get_closest_date_idx(
                eventlist=eventlist,
                target_date=start_target,
                condition="earlier",
            )
        elif mode == 3:
            set_len = int(input(f"Enter the Size of {stage.capitalize()} Set (Days): "))

            if stage == "test":
                start_target = (
                    eventlist[-1][0] - timedelta(days=set_len) + ttb_unit_delta
                )
            elif stage == "train":
                start_target = test_start - timedelta(days=set_len)

            print(f"Specified Start of {stage.capitalize()} Set: {start_target}")
            idx_start = get_closest_date_idx(
                eventlist=eventlist,
                target_date=start_target,
                condition="earlier",
            )
        else:
            print("Invalid Mode: Please Enter 1, 2, or 3.")

    return idx_start


def split_dataset():
    csv_path_prev = input("Enter the Path to the Original CSV: ")
    eventlist_prev, ttb_start_prev, ttb_end_prev, ttb_unit_delta = show_dataset_info(
        csv_path=csv_path_prev,
        message="Original Timetable Info:",
        return_info=True,
    )

    idx_start_test = get_train_test_idx(
        eventlist=eventlist_prev,
        ttb_unit_delta=ttb_unit_delta,
        stage="test",
        test_start=None,
    )

    eventlist_test = eventlist_prev[idx_start_test:]

    csv_path_test = str(input("Enter the Path to Save the Test Set: "))
    write_dataset(
        eventlist=eventlist_test,
        csv_path=csv_path_test,
        columns=["timestamp", "event"],
    )

    show_dataset_info(
        csv_path=csv_path_test,
        message="Test Set Info:",
        return_info=False,
    )

    eventlist_remain = eventlist_prev[:idx_start_test]

    split_train = True
    while split_train:
        idx_start_train = get_train_test_idx(
            eventlist=eventlist_remain,
            ttb_unit_delta=ttb_unit_delta,
            stage="train",
            test_start=eventlist_test[0][0],
        )
        eventlist_train = eventlist_remain[idx_start_train:]

        csv_path_train = str(input("Enter the Path to Save the Train Set: "))
        write_dataset(
            eventlist=eventlist_train,
            csv_path=csv_path_train,
            columns=["timestamp", "event"],
        )

        show_dataset_info(
            csv_path=csv_path_train,
            message="Train Set Info:",
            return_info=False,
        )

        split_train = bool(input("Continue to split the Train Set? (y/n): ") == "y")


def lbl2oh_dataset():
    csv_path_prev = input("Enter the Path to the Original CSV: ")
    out_dir_path = str(input("Enter the Path to the New Directory: "))

    os.makedirs(out_dir_path, exist_ok=True)

    eventlist_prev, ttb_start_prev, ttb_end_prev, ttb_unit_delta = show_dataset_info(
        csv_path=csv_path_prev,
        message="Original Timetable Info:",
        return_info=True,
    )

    df = pd.DataFrame(eventlist_prev, columns=["timestamp", "event"])
    one_hot = pd.get_dummies(df["event"], prefix="event", dtype=float)
    df = df.drop("event", axis=1)
    df = df.join(one_hot)
    df.to_csv(f"{out_dir_path}/all_events.csv", index=False)

    for column in one_hot.columns:
        csv_path_oh = f"{out_dir_path}/{column}.csv"
        df_oh = df[["timestamp", column]]
        df_oh.to_csv(csv_path_oh, index=False)
