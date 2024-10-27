import tkinter as tk
import requests
import json
import os
import socketio
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates



# Replace with the IP address of your Flask server
FLASK_SERVER_URL = "http://<your-server-ip>:<port>/get_tasks"
LOCAL_FILE = "todo_list.json"  # File to store the last known to-do list
SOCKET_SERVER_URL = "http://<your-server-ip>:<port>"

# Create a Tkinter window
root = tk.Tk()
root.title("To-Do List")
root.geometry("900x800")
root.configure(bg="white")  # White background for high contrast

# Create a frame for the title
title_label = tk.Label(
    root,
    text="To-Do List",
    font=("Helvetica", 18, "bold"),
    bg="white",
    fg="black"
)
title_label.pack(pady=5)

# Create a frame to display tasks in a grid
task_frame = tk.Frame(root, bg="white", bd=2, relief="solid")
task_frame.pack(pady=10)

# Create a frame for the stock chart
chart_frame = tk.Frame(root, bg="white")
chart_frame.pack(pady=10)

# Initialize SocketIO client
sio = socketio.Client()

# Predefine a grid for tasks
columns = 8
max_rows = 5
task_labels = [[None for _ in range(columns)] for _ in range(max_rows)]

def setup_task_grid():
    """Set up an empty grid with placeholder labels."""
    for row in range(max_rows):
        for col in range(columns):
            label = tk.Label(
                task_frame,
                text="",  # Initially empty
                font=("Helvetica", 15, "bold"),
                bg="white",
                fg="black",
                anchor="w",
                justify="left",
                wraplength=200
            )
            label.grid(row=row, column=col, sticky="w", padx=10, pady=5)
            task_labels[row][col] = label

def update_task_display():
    """Update the task display in the predefined grid."""
    # Flatten the task labels into a single list for easy indexing
    flat_task_labels = [label for row in task_labels for label in row]

    # Clear the text of all labels
    for label in flat_task_labels:
        label.config(text="")

    # Populate the labels with tasks
    for i, task in enumerate(tasks):
        if i < len(flat_task_labels):
            text = f"• {task['text']}"
            if task.get('completed'):
                text += " (completed)"
            flat_task_labels[i].config(text=text)

def fetch_tasks():
    global tasks
    try:
        # Send a GET request to the Flask server to retrieve tasks
        response = requests.get(FLASK_SERVER_URL)
        response.raise_for_status()  # Raise an error if the server is unreachable

        data = response.json()
        tasks = data['tasks']

        # Save the tasks locally
        with open(LOCAL_FILE, 'w') as f:
            json.dump(tasks, f)

        print("Tasks fetched from server and saved locally.")

    except requests.exceptions.RequestException as e:
        print("Error fetching tasks:", e)

        # Load tasks from the local file if it exists
        if os.path.exists(LOCAL_FILE):
            with open(LOCAL_FILE, 'r') as f:
                tasks = json.load(f)
            print("Loaded tasks from local file.")
        else:
            tasks = []  # If no local file exists, set to an empty list
            print("No local file found, starting with an empty list.")

    # Update the display with the tasks
    update_task_display()

def fetch_and_plot_stock_data(stock_symbol="CSPX.L"):
    # Download stock data
    stock_data = yf.download(stock_symbol, period="5d", interval="1d")

    # Check if stock data is empty or not
    if stock_data.empty:
        print(f"No data available for {stock_symbol}.")
        return

    # Create a new figure for the stock data line chart
    fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
    ax.plot(stock_data.index, stock_data['Close'], marker='o', linestyle='-', color='black', linewidth=1, markersize=1.5)
    ax.set_title(f"{stock_symbol} Stock Price", fontsize=7)
    ax.set_xlabel("Date", fontsize=5)
    ax.set_ylabel("Closing Price", fontsize=5)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.tick_params(axis='x', rotation=45, labelsize=4)  # Rotate x-axis labels for readability
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
    ax.tick_params(axis='y', rotation=45, labelsize=4)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)
    
    # Clear any existing canvas and add the new one
    for widget in chart_frame.winfo_children():
        widget.destroy()
    
    # Add the new chart to the Tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

@sio.event
def connect():
    print("Connected to the Flask server.")

@sio.on('update')
def on_update(data):
    print("Received update from server:", data)
    # Fetch the latest tasks when an update is received
    fetch_tasks()

@sio.event
def disconnect():
    print("Disconnected from the server.")

# Connect to the Flask server's WebSocket
sio.connect(SOCKET_SERVER_URL)

setup_task_grid()
fetch_tasks()

def refresh_stock_data():
    fetch_and_plot_stock_data("CSPX.L")
    root.after(3600000, refresh_stock_data)

refresh_stock_data()
# Start the Tkinter main loop
root.mainloop()
