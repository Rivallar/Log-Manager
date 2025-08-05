// Main JavaScript file for Log Manager

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add active class to current nav item
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });

    // Console log for debugging
    console.log('Log Manager JavaScript loaded successfully');
});

// Shared utility functions for loading and error handling
function showLoading() {
    const loadingSection = document.getElementById('loadingSection');
    if (loadingSection) loadingSection.style.display = 'block';
}

function hideLoading() {
    const loadingSection = document.getElementById('loadingSection');
    if (loadingSection) loadingSection.style.display = 'none';
}

function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    const errorSection = document.getElementById('errorSection');
    if (errorMessage) errorMessage.textContent = message;
    if (errorSection) errorSection.style.display = 'block';
}

function hideError() {
    const errorSection = document.getElementById('errorSection');
    if (errorSection) errorSection.style.display = 'none';
} 

// Shared utility function to clear a form and optionally hide results and errors
function clearForm(formId, resultsSectionId) {
    const form = document.getElementById(formId);
    if (form) form.reset();
    if (resultsSectionId) {
        const resultsSection = document.getElementById(resultsSectionId);
        if (resultsSection) resultsSection.style.display = 'none';
    }
    hideError();
}

// Shared utility function to format date/time strings
function formatDateTime(dateTimeString) {
    const date = new Date(dateTimeString);
    return date.toLocaleString();
} 