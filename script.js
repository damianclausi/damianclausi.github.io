/**
 * Terminal Portfolio - JavaScript
 * Minimal, performance-focused interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize typing effect for header
    initTypingEffect();

    // Smooth scroll for navigation links
    initSmoothScroll();

    // Add terminal boot sequence (optional visual flair)
    initBootSequence();
});

/**
 * Creates a typing effect for the title
 */
function initTypingEffect() {
    const title = document.querySelector('.terminal-title');
    if (!title) return;

    const text = title.textContent.replace('_', '');
    const cursor = '<span class="cursor">_</span>';

    title.innerHTML = cursor;

    let index = 0;
    const typeInterval = setInterval(() => {
        if (index < text.length) {
            title.innerHTML = text.substring(0, index + 1) + cursor;
            index++;
        } else {
            clearInterval(typeInterval);
        }
    }, 80);
}

/**
 * Initializes smooth scrolling for anchor links
 */
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href === '#') return;

            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });

                // Update URL without jumping
                history.pushState(null, '', href);
            }
        });
    });
}

/**
 * Simulates a terminal boot sequence effect
 */
function initBootSequence() {
    const sections = document.querySelectorAll('.terminal-section');

    sections.forEach((section, index) => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(10px)';
        section.style.transition = 'opacity 0.4s ease, transform 0.4s ease';

        setTimeout(() => {
            section.style.opacity = '1';
            section.style.transform = 'translateY(0)';
        }, 200 + (index * 150));
    });
}

/**
 * Console Easter Egg
 */
console.log('%c> Welcome to Damian Clausi\'s Terminal', 'color: #00ff00; font-family: monospace; font-size: 14px;');
console.log('%c> Type "help" for available commands...', 'color: #888888; font-family: monospace; font-size: 12px;');
console.log('%c> Just kidding, this is a portfolio, not a real terminal 😄', 'color: #555555; font-family: monospace; font-size: 10px;');
