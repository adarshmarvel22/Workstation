// Auto-dismiss messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        // Add close button
        const closeBtn = document.createElement('button');
        closeBtn.className = 'close-btn';
        closeBtn.innerHTML = '×';
        closeBtn.addEventListener('click', () => {
            alert.classList.add('fade-out');
            setTimeout(() => alert.remove(), 500);
        });
        alert.appendChild(closeBtn);

        // Auto-hide after 5 seconds
        setTimeout(() => {
            alert.classList.add('fade-out');
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});