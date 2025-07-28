// Cover Lettered Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    init();
});

function init() {
    // Set active navigation item
    setActiveNavItem();
    
    // Add smooth scrolling for internal links
    addSmoothScrolling();
    
    console.log('Cover Lettered app initialized');
}

function setActiveNavItem() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

function addSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Utility functions for future use
function showNotification(message, type = 'info') {
    // Future implementation for user notifications
    console.log(`${type.toUpperCase()}: ${message}`);
}

function toggleElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = element.style.display === 'none' ? 'block' : 'none';
    }
}

// Export functions for potential module use
window.CoverLettered = {
    showNotification,
    toggleElement,
    setActiveNavItem
};