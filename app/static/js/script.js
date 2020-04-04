const show_page = (page, id_content) => {
    let content = document.getElementById(id_content);

    fetch(page, {method: "GET"})
    .then(function(response) {
        if (response.ok) {
            return response.text();
        } else {
            alert("Error " + response.status + ": " + response.statusText);
            return null;
        }
    })
    .then(function(text) {
        if (text != null) {
            content.innerHTML = text;
        }
    })
    .catch(error => console.error("Error: " + error.message));
};

const register_user = (form) => {
    const username = form.username.value;
    const passwd = form.password.value;
    const passwd_confirm = form.confirm_password.value;
    const json = JSON.stringify({"username": username, "password": passwd});
    const my_headers = new Headers({"Content-Type": "application/json;charset=utf-8"});

    if (passwd.length < 8) {
        alert("Your password must have at least 8 characters");
        return;
    }
    if (passwd.localeCompare(passwd_confirm) != 0) {
        alert("The two passwords don't match !");
        return;
    }
    fetch("/register", {method: "POST", headers: my_headers, body: json})
    .then(function(response) {
        if (response.ok) {
            return response.json();
        } else {
            alert("Error " + response.status + ": " + response.statusText);
            return null;
        }
    })
    .then(function(json) {
        if (json != null) {
            if (json.hasOwnProperty("result")) {
                alert(json["result"]);
                show_page("/login_page", "content");
            } else {
                alert("Error: " + json["error"]);
            }
        }
    })
    .catch(error => console.error("Error: " + error.message));
};

const signin_user = (form) => {
    const username = form.username.value;
    const passwd = form.password.value;
    const json = JSON.stringify({"username": username, "password": passwd});
    const my_headers = new Headers({"Content-Type": "application/json;charset=utf-8"});

    fetch("/signin", {method: "POST", headers: my_headers, body: json})
    .then(function(response) {
        if (response.ok) {
            return response.json();
        } else {
            alert("Error " + response.status + ": " + response.statusText);
            return null;
        }
    })
    .then(function(json) {
        if (json != null) {
            if (json.hasOwnProperty("result")) {
                location.reload();
            } else {
                alert("Error: " + json["error"]);
            }
        }
    })
    .catch(error => console.error("Error: " + error.message));
};

const signout_user = () => {
    fetch("/signout", {method: "POST"})
    .then(function(response) {
        if (response.ok) {
            return response.json();
        } else {
            alert("Error " + response.status + ": " + response.statusText);
            return null;
        }
    })
    .then(function(json) {
        if (json != null) {
            location.reload();
        }
    })
    .catch(error => console.error("Error: " + error.message));
};

const add_task = (form) => {
    const title = form.title.value;
    const json = JSON.stringify({"title": title});
    const my_headers = new Headers({"Content-Type": "application/json;charset=utf-8"});

    fetch("/user/task/add", {method: "POST", headers: my_headers, body: json})
    .then(function(response) {
        if (response.ok) {
            return response.json();
        } else {
            alert("Error " + response.status + ": " + response.statusText);
            return null;
        }
    })
    .then(function(json) {
        if (json != null) {
            if (json.hasOwnProperty("result")) {
                alert(json["result"]);
                location.reload();
            } else {
                alert("Error: " + json["error"]);
            }
        }
    })
    .catch(error => console.error("Error: " + error.message));
};

const get_all_tasks = () => {
    let task_table = document.getElementById("task_table");

    fetch("/user/task", {method: "GET"})
    .then(function(response) {
        if (response.ok) {
            return response.json();
        } else {
            alert("Error " + response.status + ": " + response.statusText);
            return null;
        }
    })
    .then(function(json) {
        if (json != null) {
            if (json.hasOwnProperty("result")) {
                task_table.innerHTML = create_task_table_from_json(json);
            } else {
                alert("Error: " + json["error"]);
            }
        }
    })
    .catch(error => console.error("Error: " + error.message));
};

const create_task_table_from_json = (json) => {
    const tasks = json["result"]["tasks"];
    let output = "";

    if (tasks.length == 0) {
        return "<p class='section_title'>You don't have tasks yet</p>";
    }
    output += "<table class='table task_table'>";
    output += "<tr>";
    output += "<th>Title</th>";
    output += "</tr>";
    for (const task of tasks) {
        for (const id in task) {
            output += "<tr task_id='" + id + "' onclick='select_task(this);event.cancelBubble=true;'>";
            const infos = task[id];
            output += "<td>" + infos["title"] + "</td>";
            output += "</tr>";
        }
    }
    output += "</table>";
    return output;
};

const select_task = (row) => {
    let id = row.getAttribute("task_id");
    let result = document.getElementById("result_section");
    let remove_button = document.getElementById("remove_task");

    remove_button.disabled = false;
    remove_button.setAttribute("task_id", id);
    fetch("/user/task/" + id, {method: "GET"})
    .then(function(response) {
        if (response.ok) {
            return response.json();
        } else {
            alert("Error " + response.status + ": " + response.statusText);
            return null;
        }
    })
    .then(function(json) {
        if (json != null) {
            if (json.hasOwnProperty("result")) {
                result.innerHTML = create_infos_table_from_json(json);
                result.innerHTML += "<button class='button' onclick='show_task_modification()'>Modify</button>";
            } else {
                alert("Error: " + json["error"]);
            }
        }
    })
    .catch(error => console.error("Error: " + error.message));
};

const create_infos_table_from_json = (json) => {
    const task = json["result"];
    let output = "";

    output += "<table class='table' id='task_infos'>";
    output += "<caption>Task selected</caption>";
    output += "<tr>";
    output += "<th>Title</th>";
    output += "<td>" + task["title"] + "</td>";
    output += "</tr>";
    output += "<tr>";
    output += "<th>Begin</th>";
    output += "<td>" + task["begin"] + "</td>";
    output += "</tr>";
    output += "<tr>";
    output += "<th>End</th>";
    if (task["end"] == null) {
        output += "<td>" + task["begin"] + "</td>";
    } else {
        output += "<td>" + task["end"] + "</td>";
    }
    output += "</tr>";
    output += "<tr>";
    output += "<th>Status</th>";
    output += "<td>" + task["status"].charAt(0).toUpperCase() + task["status"].slice(1) + "</td>";
    output += "</tr>";
    output += "</table>";
    return output;
};

const delete_task = (button) => {
    let task_id = button.getAttribute("task_id");

    if (!confirm("Do you really want to remove this task ?")) {
        return;
    }
    fetch("/user/task/del/" + task_id, {method: "POST"})
    .then(function(response) {
        if (response.ok) {
            return response.json();
        } else {
            alert("Error " + response.status + ": " + response.statusText);
            return null;
        }
    })
    .then(function(json) {
        if (json != null) {
            if (json.hasOwnProperty("result")) {
                alert(json["result"]);
                location.reload();
            } else {
                alert("Error: " + json["error"]);
            }
        }
    })
    .catch(error => console.error("Error: " + error.message));
};

const show_task_modification = () => {
    const task_table = document.getElementById("task_table");

    for (const i = 0; i < task_table.rows.length; i++) {
        const row = task_table.rows[i]
        const content = row.cells[1].innerHTML;
        row.cells[1].innerHTML = "<input type='text' value='" + content + "' />"
    }
}