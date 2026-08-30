document.addEventListener("DOMContentLoaded", () => {
    // File upload logic to show selected filename
    const fileInput = document.querySelector('.file-input');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const fileName = this.value.split('\\').pop();
            const textBox = this.parentElement.querySelector('.file-upload-box span');
            if (fileName) {
                textBox.textContent = fileName;
                textBox.style.color = 'var(--text-primary)';
            } else {
                textBox.textContent = 'Click to browse';
                textBox.style.color = '';
            }
        });
    }

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        }, 5000);
    });
});
