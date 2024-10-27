# To-Do List and Stock Data Display with Raspberry Pi

This project creates a simple To-Do List management system with real-time updates and stock price visualization. It utilizes Flask for the server-side logic, SocketIO for real-time communication, and a Tkinter-based client designed for Raspberry Pi, allowing you to manage and display tasks from any device on the same local network.

## Project Overview

- **Frontend**: A web interface built with HTML, CSS, and JavaScript that allows users to manage a to-do list.
- **Backend**: A Flask server that handles task management and real-time updates using SocketIO.
- **Client**: A Tkinter-based application designed for Raspberry Pi to display tasks and stock data charts.
- **Stock Data**: The Tkinter client fetches stock data using `yfinance` and updates the display every hour.

## How It Works

- The Flask server acts as a central hub, managing tasks and providing real-time updates to connected clients.
- Users can interact with the To-Do List through a web interface (`index.html`), adding, updating, or deleting tasks.
- The web client sends tasks to the Flask server, which updates the task list and broadcasts changes to all connected clients.
- The Raspberry Pi runs the Tkinter client (`main.py`), which displays the latest tasks and a stock price chart that updates every hour.
- Stock prices are fetched from Yahoo Finance (`yfinance`) and displayed using `matplotlib` charts within the Tkinter window.

## Features

- **Real-Time Task Updates**: Add, complete, or delete tasks from any device connected to the same local network. Changes reflect instantly on the Raspberry Pi display.
- **Stock Price Visualization**: The Raspberry Pi client displays a stock chart that updates every hour, showing the closing prices for a specified stock symbol.
- **Cross-Device Synchronization**: The system allows you to manage tasks from your computer while the Raspberry Pi serves as a dynamic display board.


## Notes

- In-Memory Storage: The tasks are stored in memory on the server. For production, consider using a database like SQLite.
- Security: This setup does not include authentication. Ensure that your network is secure when deploying this system.
- Local Network Only: The Flask server and the Tkinter client must be on the same local network for real-time updates.

## Usage Example

1. Start the Flask server on your main computer.
2. Access the To-Do List web interface from any browser on the same local network.
3. Add or update tasks using the web interface.
4. The Raspberry Pi client will automatically update the task list display and stock price chart every hour.
