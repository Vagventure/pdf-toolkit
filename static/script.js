window.addEventListener('DOMContentLoaded', () => {
    const span = document.querySelector('.instructions span');
    const ol = document.querySelector('.instructions ol');
    if (span) {
        span.classList.add('font-bold', 'text-lg', 'underline'); // or 'text-xl' for larger size
    }
    if (ol) {
        ol.classList.add('list-decimal', 'pl-5');
    }
});



const slider = document.getElementById('slider')
const kids = slider.children;
let current = 0;

setInterval(() => {
    current = (current + 1) % kids.length;
    let ScrollX = current * slider.clientWidth;
    slider.scrollTo({
        left: ScrollX,
        behavior: 'smooth'
    })
}, 5000)

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
            const fname = m ? m[1] : "Input_pdf.pdf";

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

function checkAndSubmitOrder() {
    const fileInput = document.getElementById('file-upload');
    const progressBar = document.getElementById('upload-progress');

    const files = fileInput.files;
    if (!files || files.length === 0) return;

    const xhr = new XMLHttpRequest();
    const formData = new FormData();

    for (let i = 0; i < files.length; i++) {
        formData.append('files[]', files[i]);
    }

    xhr.open('POST', `/tools/${op}`, true);
    xhr.responseType = 'blob';

    progressBar.classList.remove('hidden');

    xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
            const percent = (e.loaded / e.total) * 100;
            progressBar.value = percent;

            document.querySelector(".blinker")?.classList.toggle('hidden');
        }
    };

    xhr.onload = () => {
        if (xhr.status === 200) {
            // Save PDF file or whatever was returned
            const blob = xhr.response;
            const cd = xhr.getResponseHeader("Content-Disposition") || "";
            const m = /filename="?(.+)"?/.exec(cd);
            const fname = m ? m[1] : "output.pdf";

            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = fname;
            a.click();
            URL.revokeObjectURL(url);

            // Update progress
            progressBar.value = 100;
            document.querySelector(".blinker2")?.classList.remove('hidden');
            document.querySelector(".blinker")?.classList.add('hidden');

            // Fetch previews
            fetch('/previews')
                .then(res => res.json())
                .then(images => {
                    const previewContainer = document.getElementById('preview-container');
                    previewContainer.innerHTML = '';

                    images.forEach((img, i) => {
                        const imgElem = document.createElement('img');
                        imgElem.src = `/previews/${img}?t=${Date.now()}`; // cache-busting
                        imgElem.alt = `Preview ${i + 1}`;
                        imgElem.className = 'w-14 h-14 object-cover rounded border';
                        previewContainer.appendChild(imgElem);
                    });
                })
                .catch(err => {
                    console.error('Error fetching previews:', err);
                });
        } else {
            alert("Upload failed");
        }
    };

    xhr.onerror = () => {
        alert("Upload error occurred.");
    };

    xhr.send(formData);
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

    case "Pdf Decryptor":
        let box3 = document.querySelector(".option")
        box3.innerHTML = `
                                     <label for="file-upload" class="p-1 rounded-lg bg-orange-300 font-bold text-white cursor-pointer">
                                     Upload File
                                     </label>
                                     <div class="flex flex-col items-center">
                                         <input id="file-upload" class="hidden" type="file" name="files[]" onChange= checkAndSubmitEncrypt() multiple />
                                         
                                        <div class="options w-auto mx-auto mt-3 items-center justify-center flex gap-7 h-auto"> <input
                                                 class="bg-white outline-1 text-center text-black w-32 font-medium" id="pass" type="text" placeholder="Current Password"
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
                                     <div class="flex flex-col items-center justify-center">
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

    case "Pdf Rotator":
        let box4 = document.querySelector(".option")
        box4.innerHTML = `
                                     <label for="file-upload" class="p-1 rounded-lg bg-orange-300 font-bold text-white cursor-pointer">
                                     Upload File
                                     </label>
                                     <div class="flex flex-col items-center justify-center">
                                         <input id="file-upload" class="hidden" type="file" name="files[]" onChange= checkAndSubmitCompress() multiple />
                                         
                                        <div class="options w-auto mx-auto mt-3 items-center justify-center flex gap-7 h-auto"> <select class="border-2 bg-white text-black" name="value" id="quality" onChange= checkAndSubmitCompress()>
                                        <option value="90">Rotate 90°</option>
                                        <option value="180">Rotate 180°</option>
                                        <option value="270">Rotate 270°</option>
                                         </select> 
                                         </div>
                                         <progress id="upload-progress" value="0" max="100" class="w-1/3 mt-3"></progress>
                                     </div>
                                     `

        document.querySelector(".img1").classList.add("p-2")


        break;

    case "Pdf Watermarker":
        let box5 = document.querySelector(".option")
        box5.innerHTML = `
                                     <label for="file-upload" class="p-1 rounded-lg bg-orange-300 font-bold text-white cursor-pointer">
                                     Upload File
                                     </label>
                                     <div class="flex flex-col items-center">
                                         <input id="file-upload" class="hidden" type="file" name="files[]" onChange= checkAndSubmitEncrypt() multiple />
                                         
                                        <div class="options w-auto mx-auto mt-3 items-center justify-center flex gap-7 h-auto"> <input
                                                 class="bg-white outline-1 text-center text-black w-32 font-medium" id="pass" type="text" placeholder="Watermark"
                                                 name="code" onChange= checkAndSubmitEncrypt()>
                                         </div>
                                         <progress id="upload-progress" value="0" max="100" class="w-1/3 mt-3"></progress>
                                     </div>
                                     
                                     `
        break;

    case "Pdf Reorderer":
        let box6 = document.querySelector(".option")
        box6.innerHTML = `
                                     <label for="file-upload" class="p-1 rounded-lg bg-orange-300 font-bold text-white cursor-pointer">
                                     Upload File
                                     </label>
                                     <div class="flex flex-col items-center gap-1">
                                         <input id="file-upload" class="hidden" type="file" name="files[]" onChange= checkAndSubmitOrder() multiple />
                                         
                                        <div id="preview-container" class="options w-full h-32 mx-auto mt-3 border-2 items-center justify-center flex flex-wrap gap-1"> 
                                        <div class="h-14 w-14 flex items-center justify-center outline-1">Hello</div>
                                      
                                        </div>

                                      <button class="w-auto h-auto p-1 rounded-lg bg-orange-300 font-bold text-white cursor-pointer">Download</button>
                                      <progress id="upload-progress" value="0" max="100" class="w-1/3 mt-1"></progress>
                                     </div>
                                     
                                     `
        break;

}


function loadPreviews() {
    fetch('/preview-list')
        .then(res => res.json())
        .then(images => {
            const container = document.getElementById('preview-container');
            container.innerHTML = ""; // clear old content

            images.forEach(filename => {
                const img = document.createElement('img');
                img.src = `/previews/${filename}`;
                img.className = "h-20 w-20 object-contain border";
                img.setAttribute("draggable", true);
                container.appendChild(img);
            });
        });
}

document.querySelector(".burger").addEventListener('click', () => {
    ham = document.querySelector('.ham')
    ham.classList.toggle('hidden')
})


document.querySelectorAll(".quick-tool, .Reco-tool").forEach(e => {
    e.addEventListener('click', (p) => {
        let text = p.target.innerText.trim();
        let opr = text.replace(/\s+/g, "-")
        console.log(opr);
        let form = document.querySelector(".formsubmit");

        switch (text) {
            case "Pdf Merger":
                form.classList.add(opr)
                form.action = `/tools/${encodeURIComponent(text)}`
                form.innerHTML = `
                <input type="hidden" name="img1"
         value="https://st5.depositphotos.com/20980838/64706/v/450/depositphotos_647060022-stock-illustration-pdf-icon-vector-illustration-flat.jpg">
        <input type="hidden" name="caption1" value="Original Pdf">

        <input type="hidden" name="img2"
          value="https://st5.depositphotos.com/20980838/64706/v/450/depositphotos_647060022-stock-illustration-pdf-icon-vector-illustration-flat.jpg">
        <input type="hidden" name="caption2" value="Merged Pdf">

        <input type="hidden" name="description" value="Easily combine multiple PDF files into a single, well-structured document
          while preserving layout and quality.">

                `
                break

            case "Images to Pdf":
                form.classList.add(opr)
                form.action = `/tools/${encodeURIComponent(text)}`
                form.innerHTML = `
                <input type="hidden" name="img1"
          value="https://cdn3.iconfinder.com/data/icons/file-formats-part-1/1000/PNG-512.png">
        <input type="hidden" name="caption1" value="Images">

        <input type="hidden" name="img2"
          value="https://st5.depositphotos.com/20980838/64706/v/450/depositphotos_647060022-stock-illustration-pdf-icon-vector-illustration-flat.jpg">
        <input type="hidden" name="caption2" value="Pdf">

        <input type="hidden" name="description" value="Quickly merge multiple images into a single PDF while keeping their quality
          and layout intact—ideal for sharing or archiving.">

                `
                break

            case "Pdf Splitter":
                form.classList.add(opr)
                form.action = `/tools/${encodeURIComponent(text)}`
                form.innerHTML = `
                 <input type="hidden" name="img1"
          value="https://st5.depositphotos.com/20980838/64706/v/450/depositphotos_647060022-stock-illustration-pdf-icon-vector-illustration-flat.jpg">
        <input type="hidden" name="caption1" value="Original Pdf">

        <input type="hidden" name="img2"
          value="https://st5.depositphotos.com/20980838/64706/v/450/depositphotos_647060022-stock-illustration-pdf-icon-vector-illustration-flat.jpg">
        <input type="hidden" name="caption2" value="Splitted Pdf">

        <input type="hidden" name="description" value="Split large PDFs into smaller files or extract specific pages with full
          control and fast processing.">
                `
                break

            case "Pdf Compresser":
                form.classList.add(opr)
                form.action = `/tools/${encodeURIComponent(text)}`
                form.innerHTML = `
                        <input type="hidden" name="img1"
          value="https://st5.depositphotos.com/20980838/64706/v/450/depositphotos_647060022-stock-illustration-pdf-icon-vector-illustration-flat.jpg">
        <input type="hidden" name="caption1" value="Original Pdf">

        <input type="hidden" name="img2"
          value="https://st5.depositphotos.com/20980838/64706/v/450/depositphotos_647060022-stock-illustration-pdf-icon-vector-illustration-flat.jpg">
        <input type="hidden" name="caption2" value="Compressed Pdf">

        <input type="hidden" name="description" value="Reduce your PDF file size without losing quality—perfect for faster uploads,
          sharing, and saving storage space.">

                `
                break

            case "Pdf to PNG":
                form.classList.add(opr)
                form.action = `/tools/${encodeURIComponent(text)}`
                form.innerHTML = `
                <input type="hidden" name="img1"
          value="https://st5.depositphotos.com/20980838/64706/v/450/depositphotos_647060022-stock-illustration-pdf-icon-vector-illustration-flat.jpg">
        <input type="hidden" name="caption1" value="Original Pdf">

        <input type="hidden" name="img2"
          value="https://st2.depositphotos.com/47577860/46963/v/600/depositphotos_469635890-stock-illustration-file-format-png-icon.jpg">
        <input type="hidden" name="caption2" value="PNGs">

        <input type="hidden" name="description" value="Turn PDFs into crystal-clear PNG images, ideal for designs, transparency, and
          digital use.">
                `
                break

            case "Pdf to JPG":
                form.classList.add(opr)
                form.action = `/tools/${encodeURIComponent(text)}`
                form.innerHTML = `
                <input type="hidden" name="img1"
          value="https://st5.depositphotos.com/20980838/64706/v/450/depositphotos_647060022-stock-illustration-pdf-icon-vector-illustration-flat.jpg">
        <input type="hidden" name="caption1" value="Original Pdf">

        <input type="hidden" name="img2"
          value="https://st.depositphotos.com/57803962/56363/v/600/depositphotos_563637420-stock-illustration-file-format-icon-vector-illustration.jpg">
        <input type="hidden" name="caption2" value="JPGs">

        <input type="hidden" name="description" value="Convert PDF pages to sharp, high-resolution JPG images suitable for sharing,
          previews, or web use.">
                `
                break

            case "Pdf to TIFF":
                form.classList.add(opr)
                form.action = `/tools/${encodeURIComponent(text)}`
                form.innerHTML = `
                        <input type="hidden" name="img1"
          value="https://st5.depositphotos.com/20980838/64706/v/450/depositphotos_647060022-stock-illustration-pdf-icon-vector-illustration-flat.jpg">
        <input type="hidden" name="caption1" value="Original Pdf">

        <input type="hidden" name="img2"
          value="https://st4.depositphotos.com/1000507/23793/v/600/depositphotos_237931072-stock-illustration-tagged-image-file-format.jpg">
        <input type="hidden" name="caption2" value="TIFFs">

        <input type="hidden" name="description" value="Generate high-quality TIFF images from your PDFs, perfect for printing,
          scanning, or archiving.">

                `
                break

            case "Pdf Encryptor":
                form.classList.add(opr)
                form.action = `/tools/${encodeURIComponent(text)}`
                form.innerHTML = `
                
                        <input type="hidden" name="img1"
          value="https://st5.depositphotos.com/20980838/64706/v/450/depositphotos_647060022-stock-illustration-pdf-icon-vector-illustration-flat.jpg">
        <input type="hidden" name="caption1" value="Original Pdf">

        <input type="hidden" name="img2"
          value="https://st2.depositphotos.com/42596756/44437/v/600/depositphotos_444376980-stock-illustration-file-folders-vector-icon.jpg">
        <input type="hidden" name="caption2" value="Locked Pdf">

        <input type="hidden" name="description" value="Add strong password protection to your PDFs to prevent unauthorized access,
          copying, or editing.">`
                break


        }

        form.target = "_blank";
        form.submit();

    })

})
