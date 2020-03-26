function show_page(page) {
    var content = document.getElementById("content");
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                content.innerHTML = this.responseText;
            }
            if (this.status === 404) {
                content.innerHTML = "Page not found.";
            }
        }
    };
    xhr.open("GET", page);
    xhr.send();
}

function register_user(form) {
    var username = form.username.value;
    var passwd = form.password.value;
    var passwd_confirm = form.confirm_password.value;
    var json = {"username": username, "password": passwd};
    var xhr = new XMLHttpRequest();

    if (passwd.length < 8) {
        alert("Your password must have at least 8 characters");
        return;
    }
    if (passwd.localeCompare(passwd_confirm) != 0) {
        alert("The two password doesn't match !");
        return;
    }
    xhr.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            var json = JSON.parse(this.responseText);
            if (json.hasOwnProperty("result")) {
                alert(json["result"]);
                show_page("login_page");
            } else {
                alert("Error: " + json["error"]);
            }
        }
    };
    xhr.open("POST", "/register");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(json));
}

function signin_user(form) {
    var username = form.username.value;
    var passwd = form.password.value;
    var json = {"username": username, "password": passwd};
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            var json = JSON.parse(this.responseText);
            if (json.hasOwnProperty("result")) {
                location.reload();
            } else {
                alert("Error: " + json["error"]);
            }
        }
    };
    xhr.open("POST", "/signin");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(json));
}

function signout_user() {
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            var json = JSON.parse(this.responseText);
            if (json.hasOwnProperty("result")) {
                location.reload();
            } else {
                alert("Error: " + json["error"]);
            }
        }
    };
    xhr.open("POST", "/signout");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send();
}