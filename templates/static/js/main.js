(function () {
    'use strict';

    // Dark Mode Toggle
    const THEME_KEY = 'petconnect-theme';
    const htmlEl = document.documentElement;
    const toggle = document.getElementById('themeToggle');

    function applyTheme(theme) {
        htmlEl.setAttribute('data-bs-theme', theme);
        if (toggle) {
            const icon = toggle.querySelector('i');
            if (icon) {
                icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
            }
        }
    }

    const saved = localStorage.getItem(THEME_KEY);
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    applyTheme(saved || (systemPrefersDark ? 'dark' : 'light'));

    if (toggle) {
        toggle.addEventListener('click', function () {
            const current = htmlEl.getAttribute('data-bs-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            applyTheme(next);
            localStorage.setItem(THEME_KEY, next);
        });
    }

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar-petconnect');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 20) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }, { passive: true });
    }

    // Auto-dismiss flash messages
    document.querySelectorAll('.alert-dismissible').forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 6000);
    });

    // Reveal on scroll
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in-up');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('[data-reveal]').forEach(function (el) {
            observer.observe(el);
        });
    }

})();