/**
 * Profile Page JavaScript
 * Handles interactive elements and animations
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeProfilePage();
});

function initializeProfilePage() {
    // Initialize all components
    setupScrollAnimations();
    setupImageLazyLoading();
    setupSocialLinkTracking();
    setupPrintFunctionality();
    setupShareFunctionality();
    setupAccessibility();
    
    // Add any special effects for featured profiles
    if (document.querySelector('.featured-hero')) {
        initializeFeaturedEffects();
    }
}

/**
 * Setup scroll-triggered animations
 */
function setupScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe all content cards and sidebar cards
    document.querySelectorAll('.content-card, .sidebar-card').forEach(card => {
        card.classList.add('animate-ready');
        observer.observe(card);
    });
}

/**
 * Setup lazy loading for images
 */
function setupImageLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for browsers without IntersectionObserver
        images.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
        });
    }
}

/**
 * Track social link clicks for analytics
 */
function setupSocialLinkTracking() {
    document.querySelectorAll('.social-link').forEach(link => {
        link.addEventListener('click', function(e) {
            const platform = this.querySelector('i').className;
            const url = this.href;
            
            // Track with Google Analytics if available
            if (typeof gtag !== 'undefined') {
                gtag('event', 'social_click', {
                    'social_platform': platform,
                    'social_url': url
                });
            }
            
            // Add visual feedback
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });
}

/**
 * Setup print functionality
 */
function setupPrintFunctionality() {
    // Add print button if it doesn't exist
    const heroContent = document.querySelector('.hero-content');
    if (heroContent && !document.querySelector('.print-btn')) {
        const printBtn = document.createElement('button');
        printBtn.className = 'btn btn-outline-light print-btn mt-3';
        printBtn.innerHTML = '<i class="fas fa-print"></i> Print Profile';
        printBtn.addEventListener('click', function() {
            window.print();
        });
        heroContent.appendChild(printBtn);
    }

    // Optimize for printing
    window.addEventListener('beforeprint', function() {
        document.body.classList.add('printing');
    });

    window.addEventListener('afterprint', function() {
        document.body.classList.remove('printing');
    });
}

/**
 * Setup share functionality
 */
function setupShareFunctionality() {
    if (navigator.share) {
        // Use native Web Share API if available
        const shareBtn = document.createElement('button');
        shareBtn.className = 'btn btn-outline-light share-btn mt-3 ms-2';
        shareBtn.innerHTML = '<i class="fas fa-share"></i> Share';
        shareBtn.addEventListener('click', async function() {
            try {
                await navigator.share({
                    title: document.title,
                    text: document.querySelector('meta[name="description"]').content,
                    url: window.location.href
                });
            } catch (err) {
                console.log('Error sharing:', err);
            }
        });

        const heroContent = document.querySelector('.hero-content');
        if (heroContent) {
            heroContent.appendChild(shareBtn);
        }
    }
}

/**
 * Setup accessibility features
 */
function setupAccessibility() {
    // Add skip links
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.className = 'skip-link';
    skipLink.textContent = 'Skip to main content';
    document.body.insertBefore(skipLink, document.body.firstChild);

    // Add focus indicators for keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-nav');
        }
    });

    document.addEventListener('mousedown', function() {
        document.body.classList.remove('keyboard-nav');
    });

    // Improve screen reader experience
    const profileImage = document.querySelector('.profile-image');
    if (profileImage && !profileImage.alt) {
        const name = document.querySelector('.hero-title').textContent;
        profileImage.alt = `Profile photo of ${name}`;
    }
}

/**
 * Initialize special effects for featured profiles
 */
function initializeFeaturedEffects() {
    // Add particle effect to featured hero
    createParticleEffect();
    
    // Enhance featured achievements with hover effects
    document.querySelectorAll('.achievement-item.featured-achievement').forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(10px) scale(1.02)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });

    // Add typing effect to featured badge
    const featuredBadge = document.querySelector('.featured-badge');
    if (featuredBadge) {
        typeWriter(featuredBadge);
    }
}

/**
 * Create particle effect for featured profiles
 */
function createParticleEffect() {
    const hero = document.querySelector('.hero-section.featured-hero');
    if (!hero) return;

    const canvas = document.createElement('canvas');
    canvas.style.position = 'absolute';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '1';
    hero.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    const particles = [];

    function resizeCanvas() {
        canvas.width = hero.offsetWidth;
        canvas.height = hero.offsetHeight;
    }

    function createParticle() {
        return {
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5,
            size: Math.random() * 2 + 1,
            alpha: Math.random() * 0.5 + 0.2
        };
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        particles.forEach((particle, index) => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            if (particle.x < 0 || particle.x > canvas.width) particle.vx *= -1;
            if (particle.y < 0 || particle.y > canvas.height) particle.vy *= -1;
            
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 255, 255, ${particle.alpha})`;
            ctx.fill();
        });
        
        requestAnimationFrame(animate);
    }

    // Initialize
    resizeCanvas();
    for (let i = 0; i < 50; i++) {
        particles.push(createParticle());
    }
    animate();

    window.addEventListener('resize', resizeCanvas);
}

/**
 * Typing effect for featured badge
 */
function typeWriter(element) {
    const text = element.textContent;
    element.textContent = '';
    element.style.opacity = '1';
    
    let i = 0;
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, 100);
        }
    }
    
    setTimeout(type, 1000);
}

/**
 * Smooth scrolling for anchor links
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

/**
 * Add CSS for animations
 */
const style = document.createElement('style');
style.textContent = `
    .animate-ready {
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.6s ease, transform 0.6s ease;
    }
    
    .animate-in {
        opacity: 1;
        transform: translateY(0);
    }
    
    .skip-link {
        position: absolute;
        top: -40px;
        left: 6px;
        background: var(--primary-color);
        color: white;
        padding: 8px;
        text-decoration: none;
        border-radius: 4px;
        z-index: 9999;
        transition: top 0.3s;
    }
    
    .skip-link:focus {
        top: 6px;
    }
    
    .keyboard-nav *:focus {
        outline: 2px solid var(--secondary-color);
        outline-offset: 2px;
    }
    
    .lazy {
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .printing .hero-section {
        background: none !important;
        color: black !important;
    }
    
    .printing .navbar,
    .printing .footer,
    .printing .print-btn,
    .printing .share-btn {
        display: none !important;
    }
    
    @media (prefers-reduced-motion: reduce) {
        .animate-ready,
        .animate-in {
            transition: none;
        }
        
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
`;
document.head.appendChild(style);
