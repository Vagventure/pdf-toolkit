let selectedToolSlug = null;

document.querySelectorAll(".tools").forEach(e => {
    e.addEventListener('click', () => {
        selectedToolSlug = e.innerText.trim();
        console.log("Selected tool:", selectedToolSlug);
        window.open(`/tools/${encodeURIComponent(selectedToolSlug)}`, '_blank');
    });
});

fileInput.addEventListener('change', () => {
    if (!selectedToolSlug) {
        alert("Please select a tool first.");
        return;
    }

    const file = fileInput.files[0];
    if (!file) return;

    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    formData.append('file', file);

    xhr.open('POST', `/tools/${encodeURIComponent(selectedToolSlug)}`, true);

    progressBar.classList.remove('hidden');

    xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
            progressBar.value = (e.loaded / e.total) * 100;
        }
    };

    xhr.onload = () => {
        if (xhr.status === 200) {
            alert("Upload complete");
            progressBar.value = 100;
        } else {
            alert("Upload failed");
        }
    };

    xhr.send(formData);
});
