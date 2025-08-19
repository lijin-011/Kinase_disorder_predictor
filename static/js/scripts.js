document.addEventListener('DOMContentLoaded', function() {
    // Button ripple effect
    document.querySelectorAll('.btn-animated').forEach(btn => {
        btn.addEventListener('mouseenter', function(e) {
            btn.style.boxShadow = '0 4px 16px #2ca02c88';
        });
        btn.addEventListener('mouseleave', function(e) {
            btn.style.boxShadow = '0 2px 8px #2ca02c33';
        });
    });
});