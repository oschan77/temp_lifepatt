import lifepatt

if __name__ == "__main__":
    csv_path = input("Enter the Path to the CSV: ")

    lifepatt.show_dataset_info(
        csv_path=csv_path,
        message="Timetable Info:",
        return_info=False,
    )
