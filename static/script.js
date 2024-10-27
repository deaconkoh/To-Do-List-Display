const inputBox = document.getElementById("input-box");
const listContainer = document.getElementById("list-container");

function addTask(){
    if(inputBox.value === ""){
        alert("Error! You must write something.");
    } else {
        let li = document.createElement("li");
        li.innerHTML = inputBox.value;
        listContainer.appendChild(li);
        let span = document.createElement("span");
        span.innerHTML = "\u00d7";
        li.appendChild(span);
        inputBox.value = "";
        saveData();  // Save the new task to the backend
    }
}

listContainer.addEventListener("click", function(e){
    if(e.target.tagName === "LI"){
        e.target.classList.toggle("checked");
        saveData();  // Save the updated status to the backend
    }
    else if(e.target.tagName === "SPAN"){
        e.target.parentElement.remove();
        saveData();  // Update the backend after removal
    }
}, false);

function saveData(){
    const tasks = [];
    listContainer.querySelectorAll("li").forEach(li => {
        tasks.push({
            text: li.firstChild.textContent,
            completed: li.classList.contains("checked")
        });
    });
    // Send the tasks to the Flask backend as JSON
    fetch('/save_tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tasks })
    }).then(response => response.json())
      .then(data => {
          console.log(data.message);
      });
}

function showTask(){
    fetch('/get_tasks')
        .then(response => response.json())
        .then(data => {
            listContainer.innerHTML = "";
            data.tasks.forEach(task => {
                let li = document.createElement("li");
                li.textContent = task.text;
                if (task.completed) {
                    li.classList.add("checked");
                }
                let span = document.createElement("span");
                span.innerHTML = "\u00d7";
                li.appendChild(span);
                listContainer.appendChild(li);
            });
        });
}

// Load tasks when the page loads
showTask();
