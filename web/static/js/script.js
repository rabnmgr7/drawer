function uploadFile() {
    let formData = new FormData();
    formData.append("file", document.getElementById("fileInput").files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        alert(data.message); // Show upload success message
        loadFileList(); // Reload file list
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function loadFileList() {
    fetch('/files')
    .then(response => response.json())
    .then(data => {
        const fileList = document.getElementById("fileList");
        fileList.innerHTML = ''; // Clear existing list

        data.forEach(file => {
            const li = document.createElement('li');
            const link = document.createElement('a');
            link.href = `/download/${file.id}`;
            link.textContent = file.name;
            li.appendChild(link);
            fileList.appendChild(li);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
