let login = false

const homePage = "home.html"
const loginPage = "login.html"
const createAccountPage = "createaccount.html"
const loginApi = "http://127.0.0.1:8000/login"
const createAccountApi = "http://127.0.0.1:8000/new-user"
const cameraApi = "http://127.0.0.1:8000/add-camera"
const loadCameraApi = "http://127.0.0.1:8000/load-camera"


if (localStorage.getItem("login") === null || localStorage.getItem("login") === "false"){
    fetch(loginPage)
        .then(response => response.text())
        .then(data => {
            let parser = new DOMParser();
            let doc = parser.parseFromString(data, "text/html");
            let body = doc.body.innerHTML;
            document.querySelector("body").innerHTML = body;

            addUser()
            let loginButton = document.querySelector("#login");
            if (loginButton) {
                loginButton.addEventListener("click", () => {
                    let username = document.querySelector("#username").value;
                    let password = document.querySelector("#password").value;
                    let message = document.querySelector("#message");

                    if (username.length < 1 || password.length < 1) {
                        message.innerText = "You must enter a username and password";
                        return;
                    }

                    fetch(loginApi, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ username: username, password: password })
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);
                        
                        if (data.message === "Login successful!") {
                            loadHomeState(username)
                            localStorage.setItem("login", "true");
                            localStorage.setItem("username", username);
                        } else if (data.message === "Login failed!") {
                            login = false;
                            message.innerText = "Invalid username or password";
                        }
                    })
                    .catch(error => {
                        console.error("Error:", error);
                    });
                });
            } else {
                console.error("Login button not found in the loaded content.");
            }
        })
        .catch(error => {
            console.error("Error loading login.html:", error);
        });
}
else{
    loadHomeState()
}


function addUser(){
    let addAccountButton = document.querySelector("#createaccount")
    if (addAccountButton){
        
        addAccountButton.addEventListener("click", () => {
            fetch(createAccountPage)
            .then(response => response.text())
            .then(data => {
                let parser = new DOMParser();
                let doc = parser.parseFromString(data, "text/html");
                let body = doc.body.innerHTML;
                document.querySelector("body").innerHTML = body;
                document.querySelector("#add-account").addEventListener("click", () => {
                    let newUsername = document.querySelector("#add-username").value
                    let newPassword = document.querySelector("#add-password").value
                    if (newUsername.length > 1 && newPassword.length > 1){
                        fetch(createAccountApi, {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({ username: newUsername, password: newPassword })
                        })
                        loadHomeState()    
                        localStorage.setItem("login", "true");
                        localStorage.setItem("username", newUsername);
                    }
                    else{
                        document.querySelector("#message").innerText = "Please enter a username and password"
                    }
                })
            })
        })
    }
    else{
        console.error("Add account button not found in the loaded content.")
    }
}





function press_button(button, status_button, switch_name){
    if (localStorage.getItem(switch_name) === null){
        localStorage.setItem(switch_name, "OFF")
    }
    status_button.innerText = localStorage.getItem(switch_name)
    status_button.style.color = status_button.innerText === "ON"? "green":"red"
    button.addEventListener("click", () => {
        if (status_button.innerText === "OFF"){
            localStorage.setItem(switch_name, "ON")
            status_button.innerText = "ON"
        }
        else{
            localStorage.setItem(switch_name, "OFF")
            status_button.innerText = "OFF"
        }
        status_button.style.color = status_button.innerText === "ON"? "green":"red"

        fetch(buttonApi, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username: localStorage.getItem("username"), password: newPassword })
        })
    })
}

function facial_recogntion(notif_status){
    if (notif_status.innerText === "ON"){
        document.querySelector(".peeps").innerText = `${peopleOnScreen}`
        
    }
}

function addNumber(){
    let input = document.createElement("#number")
    let submit = document.createElement("#submit-number")
    submit.addEventListener("click", () => {
        if (input.value.length > 10){
            fetch(numberApi, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ username: localStorage.getItem("username"), phone_number: input.value })
            })
            localStorage.setItem("phone-number", input.value)

        }
    })
}

function addCamera(username){
    let add_camera_button = document.querySelector(".add-camera")
    let cameras = {

    }
    console.log(cameras.length);
    
    add_camera_button.addEventListener("click", () => {
        let inputDiv = document.createElement("div")
        let inputIP = document.createElement("input")
        let inputCameraName = document.createElement("input")
        let inputButton = document.createElement("button")
        let cancelButton = document.createElement("button")
        
        cancelButton.innerText = "Cancel"
        inputButton.innerText = "Submit"
        
        inputIP.setAttribute("type", "text")
        inputIP.setAttribute("placeholder", "Camera ip address")
        inputCameraName.setAttribute("type", "text")
        inputCameraName.setAttribute("placeholder", "Camera Name")
        inputDiv.appendChild(inputIP)
        document.querySelector(".input-ip").appendChild(inputDiv)
        document.querySelector(".input-ip").appendChild(inputCameraName)
        document.querySelector(".input-ip").appendChild(inputButton)
        document.querySelector(".input-ip").appendChild(cancelButton)
        
        

        cancelButton.addEventListener("click", () => {
            document.querySelector(".input-ip").removeChild(inputDiv)
            document.querySelector(".input-ip").removeChild(inputButton)
            document.querySelector(".input-ip").removeChild(cancelButton)
            document.querySelector(".input-ip").removeChild(inputCameraName)
        })


        inputButton.addEventListener("click", () => {
            if(inputIP.value.length > 1 && inputCameraName.value.length > 1){
                let cameraButton = document.createElement("button")
                cameraButton.innerText = inputCameraName
    
                
                document.querySelector(".camera-buttons").appendChild(cameraButton)
                document.querySelector(".input-ip").removeChild(inputDiv)
                document.querySelector(".input-ip").removeChild(inputButton)
                document.querySelector(".input-ip").removeChild(cancelButton)

                fetch(cameraApi, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ username: localStorage.getItem("username"), camera: [inputIP.value, inputCameraName.value]})
                })
                location.reload()
                
            }
            else{
                alert("Please provide a name and ip address for the camera")
            }

        })


    })
}



function loadCamera(username){
    fetch(loadCameraApi)
    .then(response => response.json())
    .then(data => {
        let userCameras = data[localStorage.getItem("username")]
        console.log(userCameras);
        let camera_names = Object.keys(userCameras)
        camera_names.forEach(camera => {
            let button = document.createElement("button")
            button.innerText = camera
            document.querySelector(".camera-buttons").appendChild(button)

        })

        
        
            
        })
        
}


function loadHomeState(username){
    fetch("home.html")
        .then(response => response.text())
        .then(page => {

            
            let parser = new DOMParser()
            let doc = parser.parseFromString(page, "text/html")
            let body = doc.body.innerHTML
            document.querySelector("body").innerHTML = body
            
            let notifs = document.querySelector(".notifs")
            document.querySelector(".notif-drop").addEventListener("click", () => {
                if (notifs.style.visibility === "hidden"){
                    notifs.style.visibility = "visible"
                }
                else{
                    notifs.style.visibility = "hidden"
                }
            
            })
        
            let fr_button = document.querySelector("#facial-rec")
            let fr_status = document.querySelector("#facial-status")
            let fr_switch = "fr switch"
            
            let notif_button = document.querySelector("#notif")
            let notif_status = document.querySelector("#notif-status")
            let notif_switch = "notif switch"

            let bw_button = document.querySelector("#black-and-white")
            let bw_status = document.querySelector("#black-and-white-status")
            let bw_switch = "refresh"

        
            press_button(fr_button, fr_status, fr_switch)
            press_button(notif_button, notif_status, notif_switch)
            press_button(bw_button, bw_status, bw_switch)

            addCamera()
            loadCamera(username)


            fetch("http://127.0.0.1:8000/notifs")
            .then(response => response.json())
            .then(notificationsAndTimeOfNotfications => {
                notifications = notificationsAndTimeOfNotfications[0]
                timeOfNotifications = notificationsAndTimeOfNotfications[1]
                
                let notif = document.createElement("p")
                let timeOfNotificationElement = document.createElement("p")
                let fullNotif = document.createElement("div")
                notif.classList.add("notif")
                timeOfNotificationElement.classList.add("time")
                fullNotif.classList.add("full-notif")
                
                timeOfNotifications.forEach(time => {
                    timeOfNotificationElement.innerText = time
                    fullNotif.appendChild(timeOfNotificationElement)
                })
                notifications.forEach(notification => {
                    notif.innerText = notification
                    fullNotif.appendChild(notif)
                })
                
                
                document.querySelector(".notifs").appendChild(fullNotif)
            })


            document.querySelector('.logout').addEventListener('click', () => {
                localStorage.setItem("login", false)
            })
        })
    }



