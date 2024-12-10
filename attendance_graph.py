import matplotlib.pyplot as plt

def read_attendance_data(file_path):
    """Reads attendance interval data from a text file."""
    data = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                interval, count = line.split(':')
                data[interval.strip()] = int(count.split()[0])  # Extracts the numeric count
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except ValueError as e:
        print(f"Error while processing the file: {e}")
    return data

def plot_attendance_graph(file_path):
    """Plots the attendance intervals distribution graph."""
    data = read_attendance_data(file_path)
    if not data:
        print("No data to plot.")
        return

    intervals = list(data.keys())
    event_counts = list(data.values())

    # Creating the bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(intervals, event_counts)

    # Adding title and labels
    plt.title("Attendance Intervals Distribution")
    plt.xlabel("Attendance Intervals")
    plt.ylabel("Number of Events")

    # Display the plot
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Replace with the actual path to attendance_intervals.txt
    plot_attendance_graph("attendance_intervals.txt")

