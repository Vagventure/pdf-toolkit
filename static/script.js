document.querySelectorAll(".tools").forEach(e => {
    e.addEventListener('click', () => {
        window.open('/tools', '_blank')
    })
});

const form = document.getElementById('upload-form')
const fileInput = document.getElementById('file-upload');
const progressBar = document.getElementById('upload-progress');

fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (!file) return;


    const xhr = new XMLHttpRequest()
    const formData = new FormData()

    formData.append('file', file)

    xhr.open('POST', '/tools', true)

    progressBar.classList.remove('hidden')

    xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
            const percent = (e.loaded / e.total) * 100
            progressBar.value = percent
        }
    }

    xhr.onload = () => {
        if (xhr.status === 200) {
            alert("Upload complete")
            progressBar.value = 100
        } else {
            alert("Upload failed")
        }
    }

    xhr.send(formData)
})

setInterval(() => {
    sig = document.querySelector(".blinker")
    sig.classList.toggle('hidden')
    
}, 500);