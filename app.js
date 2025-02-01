let login = false

const homePage = "home.html"
const loginPage = "login.html"
const createAccountPage = "createaccount.html"
const baseApi = "http://127.0.0.1:8000/"
const loginApi = `${baseApi}login`
const createAccountApi = `${baseApi}new-user`
const cameraApi = `${baseApi}add-camera`
const loadCameraApi = `${baseApi}load-camera`
const deleteCameraApi = `${baseApi}delete-camera`
const snapPictureApi = `${baseApi}snap`
const imagesApi = `${baseApi}gallery-photos`
const peoplePhotosApi = `${baseApi}people-photos`
const baseButtonApi = `${baseApi}buttons`
const savePhotoApi = `${baseApi}save-photo`
const getPeopleApi = `${baseApi}people`
const deletePhotoApi = `${baseApi}delete-photo`



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
    button.addEventListener("click", () => {
        fetch(baseButtonApi, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username: localStorage.getItem("username"),button_pressed:  button.innerText, camera_name: localStorage.getItem("active-camera")})
        })
        status_button.innerText = status_button.innerText === "ON"? "OFF": "ON"
        status_button.style.color = status_button.innerText === "ON"? "green": "red"
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

function addCamera(){
    let menuOpen = false
    let add_camera_button = document.querySelector(".add-camera")
    let cameras = {

    }
    console.log(cameras.length);
    
    add_camera_button.addEventListener("click", () => {
        if (menuOpen === false){
            menuOpen = true
        
            let inputIP = document.createElement("input")
            let inputPORT = document.createElement("input")
            let inputUsername = document.createElement("input")
            let inputPassword = document.createElement("input")
            let inputCameraName = document.createElement("input")
            let inputButton = document.createElement("button")
            let cancelButton = document.createElement("button")
            let message1 = document.createElement('p')
            let message2 = document.createElement('p')
            let requiredHeading = document.createElement('h3')
            let otherHeading = document.createElement('h4')
            let buttons = document.createElement('div')
            let inputDiv = document.createElement("div")
            let inputSection = document.createElement('div')


            requiredHeading.innerText = "Required"
            otherHeading.innerText = "Custom"
            message1.innerText = "Fill out only what applies to your camera"
            message2.innerHTML = "Don't know what your camera has? Ask <a href='https://chatgpt.com/'>ChatGPT</a> "
            
            cancelButton.innerText = "Cancel"
            inputButton.innerText = "Submit"
            inputDiv.className = "input-text-boxes"
            inputSection.className = 'inputSection'
            inputIP.setAttribute("type", "text")
            inputIP.setAttribute("placeholder", "Camera ip address")
            inputCameraName.setAttribute("type", "text")
            inputCameraName.setAttribute("placeholder", "Camera Name")
            inputPORT.setAttribute("type", "text")
            inputPORT.setAttribute("placeholder", "Camera Port")
            inputUsername.setAttribute("type", "text")
            inputUsername.setAttribute("placeholder", "Camera Username")
            inputPassword.setAttribute("type", "text")
            inputPassword.setAttribute("placeholder", "Camera Password")
            

            inputDiv.appendChild(inputIP)
            inputDiv.appendChild(inputCameraName)
            inputDiv.appendChild(inputPORT)
            
            buttons.appendChild(inputButton)
            buttons.appendChild(cancelButton)
            
            inputSection.appendChild(inputDiv)
            inputSection.appendChild(buttons)
            document.querySelector(".input").appendChild(inputSection)
            
            

            cancelButton.addEventListener("click", () => {
                document.querySelector(".input").removeChild(inputSection)
                menuOpen = false
                
            })


            inputButton.addEventListener("click", () => {
                if(inputIP.value.length > 1 && inputCameraName.value.length > 1){
                    let cameraButton = document.createElement("button")
                    cameraButton.innerText = inputCameraName
                    document.querySelector(".input").removeChild(inputSection)

                    fetch(cameraApi, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ username: localStorage.getItem("username"), ip_address: inputIP.value, name: inputCameraName.value, port: inputPORT.value})
                    })
                    location.reload()
                    
                }
                else{
                    alert("Please provide a name and ip address for the camera")
                }

            })
        }

    })
}



function loadCamera(){
    fetch(loadCameraApi + `/${localStorage.getItem("username")}`)
    .then(response => response.json())
    .then(data => {
        let userCameras = data
        console.log(userCameras);
        userCameras.forEach(camera => {
            console.log(camera);
            
            let cameraName = camera["name"]
            let buttonInfo = camera["Black and White"]
            let button = document.createElement("button")
            
            button.innerText = cameraName
            let bwStatus = document.querySelector("#black-and-white-status")
            bwStatus.innerText = buttonInfo === true? "ON":"OFF"
            document.querySelector(".camera-buttons").appendChild(button)
            let img = document.querySelector("#img")

            button.addEventListener("click", () => {
                img.src = baseApi + "camera/" + `${localStorage.getItem("username")}/` + `${cameraName}`
                localStorage.setItem("active-camera", cameraName)
                document.querySelector('.frame-showed').innerText = cameraName
                
                
            })
        })

        
        
            
        })
        
}

function deleteCamera(){
    let deleteButton = document.querySelector('.delete-camera')
    deleteMode = true
    deleteButton.addEventListener("click", () => {
        let doneButton = document.createElement('button')
        doneButton.innerText = "Done"
        let buttonDiv = document.querySelector('.camera-buttons')
        let buttons = buttonDiv.querySelectorAll('button')
        
        document.querySelector('.buttons-controls').appendChild(doneButton)

        buttons.forEach(button => {
            button.addEventListener("click", () => {
                if (deleteMode){

                    button.style.backgroundColor = "black"
                }
            })
        })
        doneButton.addEventListener("click", () =>{
            
            buttons.forEach(button => {
                if (button.style.backgroundColor ==="black"){
                    buttonDiv.removeChild(button)
                    fetch(deleteCameraApi + `/${localStorage.getItem("username")}`+`/${button.innerText}`)
                }
            })
            document.querySelector('.buttons-controls').removeChild(doneButton) 
            deleteMode = false
        })
        
    })
}

function snapPicture(){
    function removeAllChildElements(parent) {
        while (parent.firstChild) {
            parent.removeChild(parent.firstChild);
        }
    }
    let snapButton = document.querySelector('#snap')
    let cancelButton= document.createElement('button')
    let mainGalleryButton = document.createElement('button')
    let userMessage = document.querySelector('.message-to-user')
    let videoButtons = document.querySelector('.video-buttons')


    snapButton.addEventListener("click", () => {
        document.querySelector("#img").src = baseApi + "snap/" + `${localStorage.getItem("username")}/` + localStorage.getItem("active-camera")
        mainGalleryButton.innerText = "Main Gallery"
        cancelButton.innerText = "cancel"
        userMessage.innerText = "Where would you like to save this picture?"
        videoButtons.appendChild(cancelButton)
        videoButtons.appendChild(mainGalleryButton)
        videoButtons.removeChild(snapButton)
        console.log("people: " + localStorage.getItem("people"));
        
        cancelButton.addEventListener("click", () => {
            removeAllChildElements(videoButtons)
            videoButtons.appendChild(snapButton)
            snapButton.innerText = "Snap Picture"
            userMessage.innerText = ""
            img.src = baseApi + "camera/" + `${localStorage.getItem("username")}/` + `${localStorage.getItem("active-camera")}`
            // snapPicture()
        })
        
        
        mainGalleryButton.addEventListener("click", () => {
            removeAllChildElements(videoButtons)
            videoButtons.appendChild(snapButton)
            userMessage.innerText = ""
            fetch(savePhotoApi + `/${localStorage.getItem("username")}/gallery`)
        })
        
        
        people = localStorage.getItem("people")
        people = JSON.parse(people)
        
        if (people.length >  1){
            people.forEach(person => {
                let personButton = document.createElement('button')
                personButton.innerText = person
                videoButtons.appendChild(personButton)
                personButton.addEventListener("click", () => {
                    removeAllChildElements(videoButtons)
                    videoButtons.appendChild(snapButton)
                    userMessage.innerText = ""
                    fetch(locationApi + `/${localStorage.getItem("username")}/` + person)
                    
                })
            })
        }
        else{
            let personButton = document.createElement('button')
            personButton.innerText = people
            videoButtons.appendChild(personButton)
            personButton.addEventListener("click", () => {
                removeAllChildElements(videoButtons)
                videoButtons.appendChild(snapButton)

                userMessage.innerText = ""
                fetch(savePhotoApi + `/${localStorage.getItem("username")}/` + people)
        })}
    })

}

function savePicture(){

}

function loadGallery(){
    let galleryButton = document.querySelector(".gallery-button");
    let gallery = document.querySelector(".gallery");
    let galleryheader = document.querySelector("#main-gallery-heading");
    let galleryContents = document.querySelector("#main-gallery");
    
    
    galleryButton.addEventListener("click", () => {
        if (gallery.style.display === "none") {
            gallery.style.display = "flex";
        } else {
            gallery.style.display = "none";
            galleryContents.style.display = "none";

        }
    });  

    galleryheader.addEventListener("click", () => {
        if (galleryContents.style.display === "none") {
            galleryContents.style.display = "flex";
        } else {
            galleryContents.style.display = "none";
        }
    })
}

function populateGallery(){
    
    fetch(imagesApi + `/${localStorage.getItem("username")}`)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        data.forEach((image, n) => {
            let [encodedImage, timeStamp, cameraName] = image
            
            let photoDiv = document.createElement('div')
            let photoInfoDiv = document.createElement('div')
            let photoFooterDiv = document.createElement('div')
            let img = document.createElement('img')
            let date = document.createElement('p')
            let camera = document.createElement('h4')
            let deleteButton = document.createElement('button')
            let downloadButton = document.createElement('button')
            
            
            photoDiv.className = "picture"
            photoInfoDiv.className = "photo-info"
            photoFooterDiv.className = "photo-footer"
            camera.className = "camera-name"
            date.className = "date-time"
            
            deleteButton.innerText = "Delete"
            downloadButton.innerText = "Download"
            
            
            photoInfoDiv.appendChild(camera)
            photoInfoDiv.appendChild(date)
            photoFooterDiv.appendChild(deleteButton)
            photoFooterDiv.appendChild(photoInfoDiv)
            photoFooterDiv.appendChild(downloadButton)
            photoDiv.appendChild(img)
            photoDiv.appendChild(photoFooterDiv)
            
            deleteButton.addEventListener("click", () => {
                fetch(deletePhotoApi + `/${localStorage.getItem("username")}/gallery/${n}`)
                
            })

            img.src = `data:image/jpeg;base64,${encodedImage}`
            camera.innerText = cameraName
            date.innerText = timeStamp
            document.querySelector("#main-gallery").appendChild(photoDiv)

        })
    }) 
    
    fetch(peoplePhotosApi + `/${localStorage.getItem("username")}`)
    .then(response => response.json())
    .then(data => {
        let keys = Object.keys(data)
        let values = Object.values(data)
        localStorage.setItem("people", JSON.stringify(keys))
        console.log("data: " + keys);
        console.log("values: " + values);
        
        
        values.forEach((person, index) => {
            let [encodedImage, timeStamp, cameraName] = person
            let personHeading = document.createElement('h2')


            personHeading.innerText = keys[index]
            personHeading.style.cursor = "pointer"
            let photoDiv = document.createElement('div')
            let photoInfoDiv = document.createElement('div')
            let photoFooterDiv = document.createElement('div')
            let img = document.createElement('img')
            let date = document.createElement('p')
            let camera = document.createElement('h4')
            let deleteButton = document.createElement('button')
            let downloadButton = document.createElement('button')
            let galleryContents = document.createElement("div")
            
            let gallery = document.querySelector(".gallery")
            gallery.appendChild(personHeading)
            
            personHeading.addEventListener("click", () => {
                if (galleryContents.style.visibility === "hidden") {
                    galleryContents.style.visibility = "visible";
                } else {
                    galleryContents.style.visibility = "hidden";
                }
            })
            galleryContents.id = `${keys[index]}-gallery`
            galleryContents.className = "gallery-section"
            photoDiv.className = "picture"
            photoInfoDiv.className = "photo-info"
            photoFooterDiv.className = "photo-footer"
            camera.className = "camera-name"
            date.className = "date-time"

            deleteButton.innerText = "Delete"
            downloadButton.innerText = "Download"
        
            
            photoInfoDiv.appendChild(camera)
            photoInfoDiv.appendChild(date)
            photoFooterDiv.appendChild(deleteButton)
            photoFooterDiv.appendChild(photoInfoDiv)
            photoFooterDiv.appendChild(downloadButton)
            photoDiv.appendChild(img)
            photoDiv.appendChild(photoFooterDiv)
            galleryContents.appendChild(photoDiv)
            
            img.src = `data:image/jpeg;base64,${encodedImage}`
            camera.innerText = cameraName
            date.innerText = timeStamp
            gallery.appendChild(galleryContents)
            deleteButton.addEventListener("click", () => {
                fetch(deletePhotoApi + `/${localStorage.getItem("username")}/${keys[index]}/${index}`)
            })
        })


    })
}

function savePhoto(){

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
            deleteCamera()
            
            snapPicture()
            loadGallery()
            populateGallery()

            document.querySelector('.logout').addEventListener('click', () => {
                localStorage.setItem("login", false)
            })
        })
    }






