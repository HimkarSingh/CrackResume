document.addEventListener('DOMContentLoaded', function() {
    // File upload functionality
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('resume_file');
    const uploadForm = document.getElementById('uploadForm');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const removeFileBtn = document.getElementById('removeFile');
    
    // Drag and drop functionality
    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    fileInput.addEventListener('change', handleFileSelect);
    removeFileBtn.addEventListener('click', clearFileSelection);
    uploadForm.addEventListener('submit', handleFormSubmit);

    function handleDragOver(e) {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    }

    function handleDragLeave(e) {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
    }

    function handleDrop(e) {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            if (isValidFile(file)) {
                fileInput.files = files;
                displaySelectedFile(file);
            } else {
                showAlert('Invalid file type. Please upload PDF, DOC, or DOCX files only.', 'danger');
            }
        }
    }

    function handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            if (isValidFile(file)) {
                displaySelectedFile(file);
            } else {
                showAlert('Invalid file type. Please upload PDF, DOC, or DOCX files only.', 'danger');
                fileInput.value = '';
            }
        }
    }

    function isValidFile(file) {
        const allowedTypes = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ];
        return allowedTypes.includes(file.type);
    }

    function displaySelectedFile(file) {
        const uploadContent = uploadArea.querySelector('.upload-content');
        const fileSelected = uploadArea.querySelector('.file-selected');
        const fileName = fileSelected.querySelector('.file-name');
        
        uploadContent.classList.add('d-none');
        fileSelected.classList.remove('d-none');
        fileName.textContent = file.name;
        
        // Change upload area styling
        uploadArea.style.borderStyle = 'solid';
        uploadArea.style.borderColor = '#057642';
        uploadArea.style.backgroundColor = '#e8f5e8';
    }

    function clearFileSelection() {
        const uploadContent = uploadArea.querySelector('.upload-content');
        const fileSelected = uploadArea.querySelector('.file-selected');
        
        fileSelected.classList.add('d-none');
        uploadContent.classList.remove('d-none');
        fileInput.value = '';
        
        // Reset upload area styling
        uploadArea.style.borderStyle = 'dashed';
        uploadArea.style.borderColor = '#ddd';
        uploadArea.style.backgroundColor = '#fafafa';
    }

    function handleFormSubmit(e) {
        // Show loading modal
        const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
        loadingModal.show();
        
        // Disable submit button
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
    }

    function showAlert(message, type) {
        // Create alert element
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insert alert at the top of the container
        const container = document.querySelector('.container');
        const firstElement = container.querySelector('.row');
        container.insertBefore(alertDiv, firstElement);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const alert = bootstrap.Alert.getOrCreateInstance(alertDiv);
            alert.close();
        }, 5000);
    }

    // File size validation
    fileInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const maxSize = 16 * 1024 * 1024; // 16MB
            if (file.size > maxSize) {
                showAlert('File size exceeds 16MB limit. Please choose a smaller file.', 'danger');
                this.value = '';
                clearFileSelection();
            }
        }
    });

    // Form validation
    uploadForm.addEventListener('submit', function(e) {
        const jobPosition = document.getElementById('job_position').value.trim();
        const file = fileInput.files[0];
        
        if (!jobPosition) {
            e.preventDefault();
            showAlert('Please specify a target job position.', 'danger');
            return;
        }
        
        if (!file) {
            e.preventDefault();
            showAlert('Please select a resume file to upload.', 'danger');
            return;
        }
    });

    // Auto-focus on job position input
    const jobPositionInput = document.getElementById('job_position');
    if (jobPositionInput) {
        jobPositionInput.focus();
    }

    // Add smooth scrolling to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Initialize tooltips if Bootstrap tooltips are used
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
