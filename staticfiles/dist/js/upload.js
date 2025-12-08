
  const dropZone = document.getElementById('dropZone');
  const fileInput = document.getElementById('fileInput');
  const fileList = document.getElementById('fileList');
  const uploadForm = document.getElementById('uploadForm');
  const progressContainer = document.getElementById('progressContainer');
  const progressBar = document.getElementById('progressBar');
  const progressText = document.getElementById('progressText');
  const uploadedFiles = document.getElementById('uploadedFiles');

  const allowedTypes = [
    'application/pdf',
    'text/html', 'text/css', 'text/javascript',
    'image/png', 'image/jpeg', 'image/gif', 'image/svg+xml'
  ];

  // Drag & Drop
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
  });

  dropZone.addEventListener('drop', handleDrop, false);

  function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
  }

  fileInput.addEventListener('change', () => {
    handleFiles(fileInput.files);
  });

  function handleFiles(files) {
    fileList.innerHTML = '';
    [...files].forEach(file => {
      if (file.size > 10 * 1024 * 1024) { // 10MB limit
        alert(`File ${file.name} is too large (>10MB)`);
        return;
      }
      if (!allowedTypes.includes(file.type) && !file.name.match(/\.(html|css|js|pdf)$/i)) {
        alert(`File type not allowed: ${file.name}`);
        return;
      }

      const div = document.createElement('div');
      div.className = 'd-flex justify-content-between align-items-center file-item';

      const name = document.createElement('span');
      name.textContent = file.name;

      const size = document.createElement('small');
      size.className = 'text-muted';
      size.textContent = formatBytes(file.size);

      const removeBtn = document.createElement('button');
      removeBtn.className = 'btn btn-sm btn-danger';
      removeBtn.textContent = '×';
      removeBtn.onclick = () => div.remove();

      div.appendChild(name);
      div.appendChild(size);
      div.appendChild(removeBtn);
      fileList.appendChild(div);

      // Preview for images and PDFs
      if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = e => {
          const img = document.createElement('img');
          img.src = e.target.result;
          img.className = 'preview';
          div.appendChild(img);
        };
        reader.readAsDataURL(file);
      }
    });
  }

  function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  }

  // Upload with Progress
  uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const files = fileInput.files;
    if (files.length === 0) {
      alert('Please select files first');
      return;
    }

    const formData = new FormData();
    for (let file of files) {
      formData.append('files[]', file);
    }

    progressContainer.style.display = 'block';
    progressBar.style.width = '0%';
    progressText.textContent = 'Starting upload...';

    try {
      const xhr = new XMLHttpRequest();

      xhr.upload.onprogress = (event) => {
        if (event.lengthComputable) {
          const percent = (event.loaded / event.total) * 100;
          progressBar.style.width = percent + '%';
          progressText.textContent = `Uploading... ${Math.round(percent)}%`;
        }
      };

      xhr.onload = () => {
        if (xhr.status === 200) {
          progressText.textContent = 'Upload complete!';
          displayUploadedFiles(JSON.parse(xhr.responseText));
          fileList.innerHTML = '';
          fileInput.value = '';
        } else {
          alert('Upload failed: ' + xhr.status);
        }
      };

      xhr.open('POST', 'upload.php'); // Change to your backend
      xhr.send(formData);

    } catch (err) {
      alert('Error: ' + err.message);
    }
  });

  function displayUploadedFiles(files) {
    uploadedFiles.innerHTML = '<h5 class="mt-4">Uploaded Files:</h5>';
    const ul = document.createElement('ul');
    ul.className = 'list-group';
    files.forEach(file => {
      const li = document.createElement('li');
      li.className = 'list-group-item d-flex justify-content-between align-items-center';
      li.innerHTML = `
        <span>
          <strong>${file.name}</strong> 
          <small class="text-muted">(${file.size})</small>
        </span>
        <a href="${file.url}" target="_blank" class="btn btn-sm btn-primary">View</a>
      `;
      ul.appendChild(li);
    });
    uploadedFiles.appendChild(ul);
  }