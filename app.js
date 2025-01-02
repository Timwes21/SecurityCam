let login = false



if (localStorage.getItem("login") === null || localStorage.getItem("login") === "false"){
    fetch("login.html")
        .then(response => response.text())
        .then(data => {
            let parser = new DOMParser();
            let doc = parser.parseFromString(data, "text/html");
            let body = doc.body.innerHTML;
            document.querySelector("body").innerHTML = body;


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

                    fetch("http://127.0.0.1:8000/login", {
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
                            loadHomeState()
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
    })
}

function facial_recogntion(notif_status){
    if (notif_status.innerText === "ON"){
        document.querySelector(".peeps").innerText = `${peopleOnScreen}`
        
    }
}

function addCamera(){
    let add_camera_button = document.querySelector(".add-camera")
    let cameras = {

    }
    console.log(cameras.length);
    
    add_camera_button.addEventListener("click", () => {
        let inputDiv = document.createElement("div")
        let input = document.createElement("input")
        let inputButton = document.createElement("button")
        let cancelButton = document.createElement("button")
        cancelButton.innerText = "Cancel"

        input.setAttribute("type", "text")
        input.setAttribute("placeholder", "Enter camera ip address")
        inputButton.innerText = "Submit"
        inputDiv.appendChild(input)
        document.querySelector(".input-ip").appendChild(inputDiv)
        document.querySelector(".input-ip").appendChild(inputButton)
        document.querySelector(".input-ip").appendChild(cancelButton)
        

        cancelButton.addEventListener("click", () => {
            document.querySelector(".input-ip").removeChild(inputDiv)
            document.querySelector(".input-ip").removeChild(inputButton)
            document.querySelector(".input-ip").removeChild(cancelButton)
        })


        inputButton.addEventListener("click", () => {
            if(input.value.length > 1){
                let cameraButton = document.createElement("button")
                cameras = JSON.parse(localStorage.getItem("cameras")) || {}
                let cameraNumber = Object.keys(cameras).length+1
                cameraButton.innerText = `Cameraa ${cameraNumber}` 
                cameraButton.id = `camera-${cameraNumber}`
                cameras[cameraButton.id] = input.value
                localStorage.setItem("cameras", JSON.stringify(cameras))
                console.log(localStorage.getItem("cameras"));
                
                document.querySelector(".camera-buttons").appendChild(cameraButton)
                document.querySelector(".input-ip").removeChild(inputDiv)
                document.querySelector(".input-ip").removeChild(inputButton)
            }
            else{
                alert("Please enter an ip address")
            }

        })
    })
}

function loadCameraButtons(){
    let cameras = JSON.parse(localStorage.getItem("cameras"))
    let cameraButtons = document.querySelector(".camera-buttons")
    let n = 1
    Object.keys(cameras).forEach(camera => {
        let cameraButton = document.createElement("button")
        cameraButton.innerText = `camera ${n}`
        cameraButton.id = camera
        cameraButtons.appendChild(cameraButton)
        n++
    })
}

function loadCameraFeed(){
    let videoImg = document.querySelector("#img")    

    let cameras = JSON.parse(localStorage.getItem("cameras"))
    Object.keys(cameras).forEach(camera => {
        let cameraButton = document.querySelector(`#${camera}`)
        cameraButton.addEventListener("click", () => {
            localStorage.setItem("videoURL", cameras[camera])
        })
    })
    
    videoImg.src = localStorage.getItem("videoURL")
}


function loadHomeState(){
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
            let bw_switch = "bw switch"

        
            press_button(fr_button, fr_status, fr_switch)
            press_button(notif_button, notif_status, notif_switch)
            press_button(bw_button, bw_status, bw_switch)

            addCamera()
            loadCameraButtons()
            loadCameraFeed()


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



