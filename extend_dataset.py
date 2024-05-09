import lifepatt

if __name__ == "__main__":
    eventlist, idx_empty = lifepatt.extend_eventlist()
    eventlist = lifepatt.duplicate_events(eventlist, idx_empty)

    csv_path = str(input("Enter the Path to Save the New CSV: "))

    lifepatt.write_dataset(
        eventlist=eventlist,
        csv_path=csv_path,
        columns=["timestamp", "event"],
    )
