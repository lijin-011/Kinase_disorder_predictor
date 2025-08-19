window.addEventListener('scroll', function() {
    document.querySelectorAll('.fade-in').forEach(function(el) {
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight - 50) {
            el.style.animationPlayState = 'running';
        }
    });
});