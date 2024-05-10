import lifepatt

if __name__ == "__main__":
    idx2lbl = {
        0: "not_at_home",
        1: "bedroom",
        2: "kitchen",
        3: "bathroom",
        4: "living_room",
    }
    lbl2idx = {v: k for k, v in idx2lbl.items()}

    csv_path = str(input("Enter the Path to the Original CSV: "))
    eventlist = lifepatt.read_dataset(csv_path=csv_path)
    idx_eventlist = lifepatt.lbl2idx_eventlist(
        eventlist=eventlist,
        lbl2idx=lbl2idx,
    )
    idx_csv_path = str(input("Enter the Path to the New CSV: "))
    lifepatt.write_dataset(
        eventlist=idx_eventlist,
        csv_path=idx_csv_path,
        columns=["timestamp", "event"],
    )
