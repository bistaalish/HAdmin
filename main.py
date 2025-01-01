import csv
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def load_olt_info(filepath):
    """Load OLT info from a CSV file."""
    olt_info = {}
    try:
        with open(filepath, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                olt_info[row["olt"]] = row["ip"]  # Store OLT name as key and IP as value
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
    return olt_info

def update_ip_display(olt_name, olt_info, ip_label):
    """Update the IP label when an OLT is selected."""
    if olt_name in olt_info:
        ip_label.config(text=f"IP: {olt_info[olt_name]}")

def main():
    # Load OLT info from CSV
    olt_file = "csv/devices.csv"
    olt_info = load_olt_info(olt_file)
    olt_options = list(olt_info.keys())  # List of OLT names

    # Create the main application window
    root = ttk.Window(themename="darkly")  # Choose your preferred theme
    root.title("Huawei OLT Manager")
    window_width = 800
    window_height = 800

    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate position for center
    x_cord = int((screen_width / 2) - (window_width / 2))
    y_cord = int((screen_height / 2) - (window_height / 2))

    # Set window size and position
    root.geometry(f"{window_width}x{window_height}+{x_cord}+{y_cord}")

    # Ensure the window is always on top
    root.attributes("-topmost", True)

    # Create a label with the welcome message
    welcome_label = ttk.Label(
        root, 
        text="Welcome to Huawei OLT Manager", 
        font=("Helvetica", 16),
        bootstyle=INFO
    )
    welcome_label.pack(pady=10)  # Add padding above and below

    # Create a frame to hold the OLT label, dropdown, and IP label
    info_frame = ttk.Frame(root)
    info_frame.pack(pady=20, fill=X)

    # Create a frame inside the info_frame to organize OLT dropdown and IP label
    center_frame = ttk.Frame(info_frame)
    center_frame.pack(side=TOP, fill=X, padx=150)

    # Add a label for the dropdown (OLT)
    olt_label = ttk.Label(
        center_frame, 
        text="OLT:", 
        font=("Helvetica", 12),
        bootstyle=INFO
    )
    olt_label.pack(side=LEFT, padx=10)

    # Add a dropdown (combobox) for OLT selection
    olt_dropdown = ttk.Combobox(
        center_frame, 
        values=olt_options, 
        font=("Helvetica", 12), 
        bootstyle=INFO
    )
    olt_dropdown.pack(side=LEFT, padx=10)  # Add padding to the left of the dropdown
    olt_dropdown.current(0)  # Set the default selected option

    # Add a label for the IP display
    ip_label = ttk.Label(
        center_frame, 
        text="IP:", 
        font=("Helvetica", 12),
        bootstyle=INFO
    )
    ip_label.pack(side=LEFT, padx=20)  # Margin between dropdown and IP label

    # Add the IP text (will be updated based on the OLT selection)
    ip_text = ttk.Label(center_frame, text="", font=("Helvetica", 12))
    ip_text.pack(side=LEFT, padx=10)  # Add padding for spacing

    # Update the IP label when the dropdown selection changes
    olt_dropdown.bind("<<ComboboxSelected>>", lambda event: update_ip_display(olt_dropdown.get(), olt_info, ip_text))

    # Initial IP display
    update_ip_display(olt_dropdown.get(), olt_info, ip_text)

    # Create a new frame for action buttons
    action_frame = ttk.Frame(root)
    action_frame.pack(pady=20,padx=300, fill=X)

    # Autofind Button
    autofind_button = ttk.Button(
        action_frame, 
        text="Autofind", 
        bootstyle=PRIMARY
    )
    autofind_button.pack(side=LEFT, padx=20)

    # Add Button (disabled by default)
    add_button = ttk.Button(
        action_frame, 
        text="Add", 
        bootstyle=SUCCESS,
        state=DISABLED  # Set the Add button as disabled initially
    )
    add_button.pack(side=LEFT, padx=20)

    # Create a frame for search components (Search Input, Search Button, Search Options)
    search_frame = ttk.Frame(root)
    search_frame.pack(pady=20,padx=150, fill=X)

    # Search Input Field
    search_entry = ttk.Entry(
        search_frame,
        font=("Helvetica", 12)
    )
    search_entry.pack(side=LEFT, padx=10)

    # Search Button
    search_button = ttk.Button(
        search_frame, 
        text="Search", 
        bootstyle=INFO
    )
    search_button.pack(side=LEFT, padx=10)

    # Create a frame for the search options (Search by SN, Search by Desc)
    search_options_frame = ttk.Frame(search_frame)
    search_options_frame.pack(side=LEFT, padx=20)

    # Variable to control mutual exclusivity
    search_option = ttk.IntVar()

    # Search by SN radiobutton
    search_by_sn = ttk.Radiobutton(
        search_options_frame, 
        text="SN", 
        variable=search_option,
        value=1,
        bootstyle=INFO
    )
    search_by_sn.pack(side=LEFT, padx=10)

    # Search by Desc radiobutton
    search_by_desc = ttk.Radiobutton(
        search_options_frame, 
        text="Desc", 
        variable=search_option,
        value=2,
        bootstyle=INFO
    )
    search_by_desc.pack(side=LEFT, padx=10)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
