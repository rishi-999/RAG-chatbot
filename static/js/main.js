document.addEventListener('DOMContentLoaded', () => {
    const loadingSpinner = document.getElementById('loading-indicator');
    const messageForm = document.getElementById('message-form');

    messageForm.addEventListener('submit', () => {
        // Show the loading spinner when the form is submitted
        loadingSpinner.style.display = 'inline-block'; // Make it visible
    });
});
