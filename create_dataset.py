import lifepatt

if __name__ == "__main__":
    idx2lbl = {
        0: "not_at_home",
        1: "bedroom",
        2: "kitchen",
        3: "bathroom",
        4: "living_room",
    }

    eventlist = lifepatt.create_eventlist()
    eventlist = lifepatt.schedule_events(eventlist, idx2lbl)

    csv_path = str(input("Enter the Path to Save the CSV: "))

    lifepatt.write_dataset(
        eventlist=eventlist,
        csv_path=csv_path,
        columns=["timestamp", "event"],
    )
