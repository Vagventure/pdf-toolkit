// let text = null

document.addEventListener("DOMContentLoaded", async function () {
    document.querySelectorAll(".tools").forEach(e => {
        e.addEventListener('click', (p) => {
            let text = p.target.innerText.trim();  // or e.innerText
            console.log(text);
            window.open(`/tools/${encodeURIComponent(text)}`, '_blank')

            const form = document.getElementById('upload-form')
            const fileInput = document.getElementById('file-upload');
            const progressBar = document.getElementById('upload-progress');
            fileInput.addEventListener('change', () => {
                const files = fileInput.files;
                if (!files) return;
    
    
                const xhr = new XMLHttpRequest()
                const formData = new FormData()
                
                for (let i = 0; i < files.length; i++) {
                    formData.append('files[]', files[i])
                }
    
                xhr.open('POST', `/tools/${text}`, true)
    
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
        });
        });

});
