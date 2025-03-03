import { createClient } from  "https://esm.sh/@supabase/supabase-js"



let url = "https://wwvtvsapleldrdrblnka.supabase.co"
let key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind3dnR2c2FwbGVsZHJkcmJsbmthIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQ5MjYxMjQsImV4cCI6MjA1MDUwMjEyNH0.R2XNRCLYW32M1nKKCM8-30lROLODMtwhNB3Xh3h4c7E"

const supabase = createClient(url, key)
let login = false

const homePage = "home.html"
const loginPage = "login.html"
const createAccountPage = "createaccount.html"
const baseApi = "http://127.0.0.1:8000/"
const baseSocket = "http://127.0.0.1:8000/detections"
const loginApi = `${baseApi}login`
const createAccountApi = `${baseApi}new-user`
const cameraApi = `${baseApi}add-camera`
const loadCameraApi = `${baseApi}load-camera`
const deleteCameraApi = `${baseApi}delete-camera`
const baseButtonApi = `${baseApi}buttons`
const savePhotoApi = `${baseApi}save-photo`
const createModelApi = `${baseApi}upload-photos`
const detectionSocket = `${baseApi}detections`

document.addEventListener("DOMContentLoaded", () => {

    if (localStorage.getItem("login") === null || localStorage.getItem("login") === "false"){
        fetch(loginPage)
        .then(response => response.text())
        .then(data => {
            let parser = new DOMParser();
            let doc = parser.parseFromString(data, "text/html");
            let newBody = doc.body.innerHTML;
            let body = document.querySelector("body")
            body.innerHTML = newBody;
            body.style.visibility = "visible"
            
            addUser()
            let loginButton = document.querySelector("#login");
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
                    
                    if (data === 0) {
                        loadHomeState(username)
                        localStorage.setItem("login", "true");
                        localStorage.setItem("username", username);
                    } else if (data === 1) {
                        login = false;
                        message.innerText = "Invalid password";
                    }
                    else{
                        message.innerText = "User does not exist"
                    }
                })
                .catch(error => {
                    console.error("Error:", error);
                });
            });
            
        })
        .catch(error => {
            console.error("Error loading login.html:", error);
        });
    }
else{
    loadHomeState()
}
})


function addUser(){
    let addAccountButton = document.querySelector("#createaccount")    
    addAccountButton.addEventListener("click", () => {
        fetch(createAccountPage)
        .then(response => response.text())
        .then(data => {
            let parser = new DOMParser();
            let doc = parser.parseFromString(data, "text/html");
            let body = doc.body.innerHTML;
            document.querySelector("body").innerHTML = body;

            let backButton = document.querySelector("#back-button")
            backButton.addEventListener("click", () => {
                location.reload()
            })

            document.querySelector("#add-account").addEventListener("click", () => {
                let newUsername = document.querySelector("#add-username").value
                let newPassword = document.querySelector("#add-password").value
                let message = document.querySelector("#message")
                if (newUsername.length > 1 && newPassword.length > 1){
                    fetch(createAccountApi, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ username: newUsername, password: newPassword })
                        }).then(response => response.json())
                    .then(data => {
                        if (data === 1){
                            message.innerText = "username already exists"
                        }
                        else{
                            loadHomeState()    
                            localStorage.setItem("login", "true");
                            localStorage.setItem("username", newUsername);
                        }
                    })
                }
                else{
                    document.querySelector("#message").innerText = "Please enter a username and password"
                }
            })
        })
    })

    
}




function buttons(){
    function press_button(button){
        button.addEventListener("click", () => {
            fetch(baseButtonApi, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({username: localStorage.getItem("username"),button_pressed:  button.innerText, camera_name: localStorage.getItem("active-camera")})
            })
        })
    }

    press_button(document.querySelector("#black-and-white"))
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
            inputIP.type = "text"
            inputIP.placeholder = "Camera ip address"
            
            let inputPORT = document.createElement("input")
            inputPORT.type = "text"
            inputPORT.placeholder = "Camera Port"
            
            let inputUsername = document.createElement("input")
            inputUsername.type = "text"
            inputUsername.placeholder = "Camera Username"
            
            let inputPassword = document.createElement("input")
            inputPassword.type = "text"
            inputPassword.placeholder = "Camera Password"
            
            let inputCameraName = document.createElement("input")
            inputCameraName.type = "text"
            inputCameraName.placeholder = "Camera Name"
            
            let inputButton = document.createElement("button")
            inputButton.innerText = "Submit"
            inputButton.addEventListener("click", () => {
                if(inputIP.value.length < 1 && inputCameraName.value.length < 1){
                    alert("Please provide a name and ip address for the camera")
                    return
                }
                    let cameraButton = document.createElement("button")
                    cameraButton.innerText = inputCameraName
                    document.querySelector(".input").removeChild(inputSection)

                    let CameraPort = inputPORT.value === null? "80" : inputPORT.value 

                    fetch(cameraApi, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ username: localStorage.getItem("username"), ip_address: inputIP.value, name: inputCameraName.value, port: CameraPort})
                    })
                    location.reload()
                    
                

            })
            
            let cancelButton = document.createElement("button")
            cancelButton.innerText = "Cancel"
            cancelButton.addEventListener("click", () => {
                document.querySelector(".input").removeChild(inputSection)
                menuOpen = false
                
            })
            
            let requiredHeading = document.createElement('h3')
            requiredHeading.innerText = "Required"
            
            let otherHeading = document.createElement('h4')
            otherHeading.innerText = "Custom"
            
            let buttons = document.createElement('div')
            buttons.appendChild(inputButton)
            buttons.appendChild(cancelButton)
            
            let inputDiv = document.createElement("div")
            inputDiv.className = "input-text-boxes"
            inputDiv.appendChild(inputIP)
            inputDiv.appendChild(inputCameraName)
            inputDiv.appendChild(inputPORT)
            
            
            let inputSection = document.createElement('div')
            inputSection.className = 'inputSection'
            inputSection.appendChild(inputDiv)
            inputSection.appendChild(buttons)
            
            document.querySelector(".input").appendChild(inputSection)
            

        }

    })
}



function loadCamera(){
    fetch(loadCameraApi + `/${localStorage.getItem("username")}`)
    .then(response => response.json())
    .then(data => {
        let userCameras = data
        localStorage.setItem("cameras", userCameras)
        userCameras.forEach(camera => {
            
            let cameraName = camera["name"]
            let buttonInfo = camera["Black and White"]
            let buttonDiv = document.createElement("div")
            buttonDiv.className = "camera-button"
            buttonDiv.id = cameraName + "-results-div"
            let button = document.createElement("button")
            button.innerText = cameraName
            
            
            let resultsHeader = document.createElement("h2")
            resultsHeader.id = cameraName + "-results"
            resultsHeader.className = "camera-results"
            buttonDiv.appendChild(button)
            buttonDiv.appendChild(resultsHeader)
            document.querySelector(".camera-buttons").appendChild(buttonDiv)
            let img = document.querySelector("#img")
            FaceRecResults(cameraName)
            button.addEventListener("click", () => {
                img.src = baseApi + "camera/" + `${localStorage.getItem("username")}/` + `${cameraName}`
                localStorage.setItem("active-camera", cameraName)
                document.querySelector('.frame-showed').innerText = cameraName
                document.querySelector(".on-screen").innerText = resultsHeader.innerText
                
                
            })

        })

        
        
            
        })
        
}

function deleteCamera(){
    let deleteButtonDiv = document.querySelector(".delete-button-div")
    
    let deleteButton = document.querySelector('.delete-camera')
    let deleteMode = false
    let doneButton = document.createElement('button')
    doneButton.innerText = "Done"
    
    
    let buttonDiv = document.querySelector('.camera-buttons')
    deleteButton.addEventListener("click", () => {
        deleteMode = true
        deleteButtonDiv.removeChild(deleteButton)
        deleteButtonDiv.appendChild(doneButton)
        
        let buttons = buttonDiv.querySelectorAll('button')

        buttons.forEach(button => {
            button.addEventListener("click", () => {
                if (deleteMode){
                    button.style.backgroundColor = "black"
                }
            })
        })
        
    })
    doneButton.addEventListener("click", () =>{
        let buttons = buttonDiv.querySelectorAll('button')
        deleteMode = false
        buttons.forEach(button => {
            if (button.style.backgroundColor === "black"){
                let removeable = document.querySelector("#" + button.innerText + "-results-div")
                console.log(button.innerText);
                
                buttonDiv.removeChild(removeable)
                fetch(deleteCameraApi + `/${localStorage.getItem("username")}`+`/${button.innerText}`)
            }
        })
        deleteButtonDiv.removeChild(doneButton)
        deleteButtonDiv.appendChild(deleteButton)
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
    let addAFaceButton = document.createElement('button')
    let videoButtons = document.querySelector('.video-buttons')
    let input = document.createElement('input')
    let submitFaceNameButton = document.createElement('button')
    let bwButton = document.querySelector("#black-and-white")

    mainGalleryButton.innerText = "Save"
    cancelButton.innerText = "cancel"
    addAFaceButton.innerText = "Add a Face to Remember"
    submitFaceNameButton.innerText = `Submit ${input.value}`
    

    snapButton.addEventListener("click", async () => {
        try{
            const response = await fetch(
                baseApi + "snap/" + `${localStorage.getItem("username")}/` + localStorage.getItem("active-camera")
            );
        
            if (!response.ok) {
                document.querySelector(".frame-showed").innerText = response.statusText;
                return;  // Exit the function early
            }
        
            document.querySelector("#img").src = response.url
        }
        catch(err){
            document.querySelector(".frame-showed").innerText = "Error"
            
        }
        removeAllChildElements(videoButtons)
        videoButtons.appendChild(cancelButton)
        videoButtons.appendChild(mainGalleryButton)
        console.log("people: " + localStorage.getItem("people"));
        
        cancelButton.addEventListener("click", () => {
            removeAllChildElements(videoButtons)
            videoButtons.appendChild(snapButton)
            videoButtons.appendChild(bwButton)

            snapButton.innerText = "Snap Picture"
            img.src = baseApi + "camera/" + `${localStorage.getItem("username")}/` + `${localStorage.getItem("active-camera")}`
        })
        
        
        mainGalleryButton.addEventListener("click", () => {
            removeAllChildElements(videoButtons)
            videoButtons.appendChild(snapButton)
            videoButtons.appendChild(bwButton)
            userMessage.innerText = ""
            fetch(savePhotoApi + `/${localStorage.getItem("username")}`)
        })

        
    })

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

async function populateGallery(){
    async function delete_picture(name){
        const { data, error } = await supabase
        .storage
        .from('Images')
        .remove([`${localStorage.getItem("username")}/name`])
        
    }
    
    const { data: files, error } = await supabase
    .storage
    .from('Images') // Replace with your bucket name
    .list(localStorage.getItem("username") + "/"); // Replace with your folder path and desired limit
    
    if (error){
        console.error(error)
    }

    for (let file of files) {
        // console.log(file);
        
        const { data, error: downloadError } = await supabase
        .storage
        .from('Images') 
        .download(localStorage.getItem("username")+ "/" + file.name);

        let photoDiv = document.createElement('div')
        let photoFooterDiv = document.createElement('div')
        let img = document.createElement('img')
        let deleteButton = document.createElement('button')
        let downloadButton = document.createElement('button')
        
        
        photoDiv.className = "picture"
        photoFooterDiv.className = "photo-footer"
        
        deleteButton.innerText = "Delete"
        downloadButton.innerText = "Download"
        
        
        photoFooterDiv.appendChild(deleteButton)
        photoFooterDiv.appendChild(downloadButton)
        photoDiv.appendChild(photoFooterDiv)
        photoDiv.appendChild(img)
        
        deleteButton.addEventListener("click", () => {
            delete_picture(file.name)
        })

        downloadButton.addEventListener("click", () => {

        })

        const blob = new Blob([data], { type: 'image/jpeg' });
        const imageUrl = URL.createObjectURL(blob);
        
        
    
        img.src = imageUrl
        document.querySelector("#main-gallery").appendChild(photoDiv)
    }




    
}

function addAPerson(){
    let faceRecDiv = document.querySelector(".add-person")
    
    let form = document.createElement("form")
    form.className = "add-person-form"
    form.multiple = true

    let buttonDiv = document.createElement("div")
    buttonDiv.className = "face-rec-button-div"

    let addPersonButton = document.querySelector("#add-person")

    
    let nameInput = document.createElement("input")
    nameInput.placeholder = "Name"
    form.appendChild(nameInput)
    
    
    
    
    let fileInput = document.createElement("input")
    fileInput.className = "inputFiles"
    fileInput.type = "file"
    fileInput.accept = "image/*"
    fileInput.multiple = true
    form.appendChild(fileInput)
    
    
    let submitButton = document.createElement("button")
    submitButton.innerText = "Submit"
    submitButton.type = "submit"
    buttonDiv.appendChild(submitButton)


    let files = [];
    
    fileInput.addEventListener("change", (event) => {
        files = [...files, ...event.target.files];
        console.log(files);
        
    })

    submitButton.addEventListener("click", (event) => {
        event.preventDefault();
        let formData = new FormData();
        
        // console.log(files.length);
        

        if (files.length < 1 || nameInput.value.length < 1){
            alert("fill out all fields");
            return; 
        }
        
        for (let file of files){
            formData.append("files", file);
        }
        
        
        fetch(createModelApi + "/" + localStorage.getItem("username") + "/" + nameInput.value, {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            
        })
        .catch(err => {
            console.log(err);
            
        });


        
        
        
    })
    
    let cancel = document.createElement("button")
    cancel.innerText = 'Cancel'
    buttonDiv.appendChild(cancel)

    form.appendChild(buttonDiv)

    addPersonButton.addEventListener("click", () => {
        faceRecDiv.removeChild(addPersonButton)
        faceRecDiv.appendChild(form)



    })
}

async function FaceRecResults(cameraName) {
    function sleep(seconds){
        let time = seconds * 1000
        return new Promise(resolve => setTimeout(resolve, time));
    }
    while (true){
        let detectionSocketFull = new WebSocket(baseSocket + "/" +localStorage.getItem("username") + "/" + cameraName)
        detectionSocketFull.onmessage = (event) => {
            // console.log("event.data: " + event.data);
            
            let onScreen = document.querySelector("#" + cameraName + "-results")
            onScreen.style.color = event.data === "unknown"?"red":"green"
            document.querySelector("#" + cameraName + "-results").innerText = "on screen: " +  event.data
            
        }

        await sleep(5)
        
    }
    
}



function loadHomeState(username){
    fetch("home.html")
        .then(response => response.text())
        .then(page => {

            
            let parser = new DOMParser()
            let doc = parser.parseFromString(page, "text/html")
            let newBody = doc.body.innerHTML
            let body = document.querySelector("body")
            body.innerHTML = newBody
            body.style.visibility = "visible"

            let notifs = document.querySelector(".notifs")
            document.querySelector(".notif-drop").addEventListener("click", () => {
                if (notifs.style.visibility === "hidden"){
                    notifs.style.visibility = "visible"
                }
                else{
                    notifs.style.visibility = "hidden"
                }
            
            })
        
            
            buttons()
            addCamera()
            loadCamera(username)
            deleteCamera()
            
            snapPicture()
            loadGallery()
            populateGallery()



            addAPerson()
            document.querySelector('.logout').addEventListener('click', () => {
                localStorage.setItem("login", false)
                location.reload()
            })
        })
    }






