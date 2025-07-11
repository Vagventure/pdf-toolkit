
function checkAndSubmit() {
    const start = document.getElementById("start").value.trim();
    const end = document.getElementById("end").value.trim();
    const fileInput = document.getElementById("file-upload");
    const progressBar = document.getElementById('upload-progress');
    const file = fileInput.files[0];

    if (!(start && end && file)) return;

    const formData = new FormData();
    formData.append("start-page", start);
    formData.append("end-page", end);
    formData.append("files[]", file);

    const xhr = new XMLHttpRequest();
    const endpoint = `/tools/${encodeURIComponent(op)}`;

    xhr.open("POST", endpoint, true)
    xhr.responseType = "blob"

    progressBar.classList.remove('hidden')

    xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
            document.getElementById("upload-progress").value = (e.loaded / e.total) * 100;
        }
    };


    xhr.onload = () => {
        if (xhr.status === 200) {
            // now xhr.response is a Blob
            const blob = xhr.response;
            const cd = xhr.getResponseHeader("Content-Disposition") || "";
            const m = /filename="?(.+)"?/.exec(cd);
            const fname = m ? m[1] : "splitted.pdf";

            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = fname;
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);
            alert("Upload complete")
            progressBar.value = 100
            sig2 = document.querySelector(".blinker2")
            sig2.classList.remove('hidden')
            sig.classList.add('hidden')

        } else {
            alert("Encryption failed: " + xhr.statusText);
        }
    };

    xhr.send(formData);

    setInterval(() => {
        sig = document.querySelector(".blinker")
        sig.classList.toggle('hidden')

    }, 500);


}

function checkAndSubmitEncrypt() {
    const lock = document.getElementById("pass").value.trim();
    const fileInput = document.getElementById("file-upload");
    const progressBar = document.getElementById('upload-progress');
    const file = fileInput.files[0];
    if (!lock || !file) return;

    const formData = new FormData();
    formData.append("code", lock);
    formData.append("files[]", file);

    const xhr = new XMLHttpRequest();
    const endpoint = `/tools/${encodeURIComponent(op)}`;
    xhr.open("POST", endpoint, true);

    // ← THIS is the missing piece
    xhr.responseType = "blob";

    xhr.upload.onprogress = e => {
        if (e.lengthComputable) {
            document.getElementById("upload-progress").value =
                (e.loaded / e.total) * 100;
        }
    };

    xhr.onload = () => {
        if (xhr.status === 200) {
            // now xhr.response is a Blob
            const blob = xhr.response;
            const cd = xhr.getResponseHeader("Content-Disposition") || "";
            const m = /filename="?(.+)"?/.exec(cd);
            const fname = m ? m[1] : "locked.pdf";

            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = fname;
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);
            progressBar.value = 100
            sig2 = document.querySelector(".blinker2")
            sig2.classList.remove('hidden')
            sig.classList.add('hidden')

        } else {
            alert("Encryption failed: " + xhr.statusText);
        }
    };

    xhr.onerror = () => {
        alert("Network error trying to encrypt.");
    };

    xhr.send(formData);

    setInterval(() => {
        sig = document.querySelector(".blinker")
        sig.classList.toggle('hidden')

    }, 500);
}


function checkAndSubmitCompress() {
    const val = document.getElementById("quality");
    const fileInput = document.getElementById("file-upload");
    const progressBar = document.getElementById('upload-progress');
    const file = fileInput.files[0];
    if (!val || !file) return;

    const formData = new FormData();
    formData.append("value", val.value);
    formData.append("files[]", file);

    const xhr = new XMLHttpRequest();
    const endpoint = `/tools/${encodeURIComponent(op)}`;
    xhr.open("POST", endpoint, true);

    // ← THIS is the missing piece
    xhr.responseType = "blob";

    xhr.upload.onprogress = e => {

        if (e.lengthComputable) {
            document.getElementById("upload-progress").value =
                (e.loaded / e.total) * 100;
            setInterval(() => {
                sig = document.querySelector(".blinker")
                sig.classList.toggle('hidden')

            }, 500);
        }
    };

    xhr.onload = () => {
        if (xhr.status === 200) {
            // now xhr.response is a Blob
            const blob = xhr.response;
            const cd = xhr.getResponseHeader("Content-Disposition") || "";
            const m = /filename="?(.+)"?/.exec(cd);
            const fname = m ? m[1] : "Compressed.pdf";

            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = fname;
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);
            progressBar.value = 100
            sig2 = document.querySelector(".blinker2")
            sig2.classList.remove('hidden')
            sig.classList.add('hidden')

        } else {
            alert("Compression failed: " + xhr.statusText);
        }
    };

    xhr.onerror = () => {
        alert("Network error trying to encrypt.");
    };

    xhr.send(formData);


}



function checkAndSubmitNormal() {
    // const form = document.getElementById('upload-form')
    const fileInput = document.getElementById('file-upload');
    const progressBar = document.getElementById('upload-progress');

    const files = fileInput.files;
    if (!files) return;


    const xhr = new XMLHttpRequest()
    const formData = new FormData()

    for (let i = 0; i < files.length; i++) {
        formData.append('files[]', files[i])
    }


    xhr.open('POST', `/tools/${op}`, true)

    xhr.responseType = 'blob'

    progressBar.classList.remove('hidden')

    xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
            setInterval(() => {
                sig = document.querySelector(".blinker")
                sig.classList.toggle('hidden')

            }, 500);
            const percent = (e.loaded / e.total) * 100
            progressBar.value = percent
        }
    }

    xhr.onload = () => {
        if (xhr.status === 200) {
            const blob = xhr.response;
            const cd = xhr.getResponseHeader("Content-Disposition") || "";
            const m = /filename="?(.+)"?/.exec(cd);
            const fname = m ? m[1] : "merged.pdf";

            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = fname;
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);
            progressBar.value = 100
            sig2 = document.querySelector(".blinker2")
            sig2.classList.remove('hidden')
            sig.classList.add('hidden')


        } else {
            alert("Upload failed")
        }
    }

    xhr.send(formData)
}


op = document.title
console.log(op)

switch (op) {
    case "Pdf Splitter":
        let box = document.querySelector(".option")
        box.innerHTML = `
                                     <label for="file-upload" class="p-1 rounded-lg bg-orange-300 font-bold text-white cursor-pointer">
                                     Upload File
                                     </label>
                                     <div class="flex flex-col items-center">
                                         <input id="file-upload" class="hidden" type="file" name="files[]" onChange= checkAndSubmit() multiple/>
                                         
                                        <div class="options w-auto mx-auto mt-3 items-center justify-center flex gap-7 h-auto"> <input
                                                 class="outline-1 text-center text-black w-32 font-medium " id="start" type="text" placeholder="Start Page"
                                                 name="start-page" onChange= checkAndSubmit()>
                                             <input class="outline-1 text-center text-black w-32 font-medium " id="end" type="text" placeholder="End Page"
                                                 name="end-page" onChange= checkAndSubmit()>
                                         </div>
                                         <progress id="upload-progress" value="0" max="100" class="w-1/3 mt-3"></progress>
                                     </div>
                                     `

        break;

    case "Pdf Encryptor":
        let box1 = document.querySelector(".option")
        box1.innerHTML = `
                                     <label for="file-upload" class="p-1 rounded-lg bg-orange-300 font-bold text-white cursor-pointer">
                                     Upload File
                                     </label>
                                     <div class="flex flex-col items-center">
                                         <input id="file-upload" class="hidden" type="file" name="files[]" onChange= checkAndSubmitEncrypt() multiple />
                                         
                                        <div class="options w-auto mx-auto mt-3 items-center justify-center flex gap-7 h-auto"> <input
                                                 class="bg-white outline-1 text-center text-black w-32 font-medium" id="pass" type="text" placeholder="Password"
                                                 name="code" onChange= checkAndSubmitEncrypt()>
                                         </div>
                                         <progress id="upload-progress" value="0" max="100" class="w-1/3 mt-3"></progress>
                                     </div>
                                     `

        break;

    case "Pdf Compresser":
        let box2 = document.querySelector(".option")
        box2.innerHTML = `
                                     <label for="file-upload" class="p-1 rounded-lg bg-orange-300 font-bold text-white cursor-pointer">
                                     Upload File
                                     </label>
                                     <div class="flex flex-col items-center">
                                         <input id="file-upload" class="hidden" type="file" name="files[]" onChange= checkAndSubmitCompress() multiple />
                                         
                                        <div class="options w-auto mx-auto mt-3 items-center justify-center flex gap-7 h-auto"> <select class="border-2 bg-white text-black" name="value" id="quality" onChange= checkAndSubmitCompress()>
                                         <option value="/prepress"> High Quality(Best for Printing)</option>
                                         <option value="/default"> Standard Quality(Best for Most Uses) </option>
                                         <option value="/ebook"> Small File(Fastest to Load) </option>
                                         <option value="/screen"> Ultra Compressed(For Screen Only) </option>
                                         </select> 
                                         </div>
                                         <progress id="upload-progress" value="0" max="100" class="w-1/3 mt-3"></progress>
                                     </div>
                                     `
        break;


}
