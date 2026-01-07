// Auto-dismiss messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.alert-message');

    messages.forEach(function(message) {
        // Start fading out after 5 seconds
        setTimeout(function() {
            message.style.transition = 'opacity 0.5s ease-out';
            message.style.opacity = '0';

            // Remove from DOM after fade completes
            setTimeout(function() {
                message.remove();
            }, 500);
        }, 5000);
    });
});