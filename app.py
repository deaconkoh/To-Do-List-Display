from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# In-memory storage for tasks (for demonstration purposes)
todo_list = []

@app.route('/')
def index():
    return render_template('index.html')  # Serves your HTML file for the web interface

@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': todo_list})

@app.route('/save_tasks', methods=['POST'])
def save_tasks():
    global todo_list
    data = request.json
    tasks = data.get('tasks', [])
    todo_list = tasks  # Replace the current list with the new one
    print(f"Tasks updated. Current todo_list: {todo_list}")
    socketio.emit('update', {'tasks': todo_list})
    return jsonify({'status': 'success', 'message': 'Tasks saved successfully'}), 200

if __name__ == "__main__":
    socketio.run(app, host='127.0.0.1', port="Any port number that is not in used") #change 127.0.0.1 to 0.0.0.0 if u want to connect to local devices
