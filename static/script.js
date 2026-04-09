// Intersection Observer for scroll animations
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.fade-in').forEach(el => {
    observer.observe(el);
});

// Form Submission handling
document.getElementById('contact-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const statusEl = document.getElementById('form-status');
    const submitBtn = e.target.querySelector('button[type="submit"]');
    
    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending...';
    statusEl.textContent = '';
    statusEl.className = 'form-status';

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/api/contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            statusEl.textContent = 'Message sent successfully! David will get back to you soon.';
            statusEl.classList.add('status-success');
            e.target.reset();
        } else {
            statusEl.textContent = 'Failed to send message. Please try again.';
            statusEl.classList.add('status-error');
        }
    } catch (error) {
        statusEl.textContent = 'An error occurred. Please check your connection.';
        statusEl.classList.add('status-error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send Message';
    }
});
