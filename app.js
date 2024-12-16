const canvas = document.getElementById("video")
const cvt = canvas.getContext('2d')

async function fetchStream() {
    const response = await fetch("http://127.0.0.1:8000/video")
    const reader = response.body.getReader()

    let imageBuffer = ''
    while (true){
        const { value, done} = await reader.read()
        if (done) break

        imageBuffer += new TextDecoder().decode(value)
        const boundary = imageBuffer.indexOf("--frame")
        if (boundary !== -1){
            const imageBlob = new Blob([imageBuffer.slice(0, boundary)], { type: "image/jpeg"})
            const img = new Image()

            img.onload = () => {
                canvas.width = img.width
                canvas.height = img.height
                cvt.drawImage(img, 0, 0)
            }
            img.src = URL.createObjectURL(imageBlob)
            imageBuffer = imageBuffer.slice(boundary + "--frame".length)
        }
    }
    
}

fetchStream()