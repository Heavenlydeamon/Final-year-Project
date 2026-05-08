/**
 * Bento Topics — Interactive Enhancements
 * Shared by: environment_topics, heritage_topics, cultural_topics
 */
'use strict';

document.addEventListener('DOMContentLoaded', () => {

    /* ── Scroll-reveal ─────────────────────────────────────── */
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, i) => {
            if (entry.isIntersecting) {
                // Stagger cards within the same batch
                const delay = parseInt(entry.target.dataset.delay || 0);
                setTimeout(() => entry.target.classList.add('visible'), delay);
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.bt-reveal').forEach((el, i) => {
        el.dataset.delay = (i % 4) * 90; // stagger every card in groups of 4
        revealObserver.observe(el);
    });

    /* ── Full-card click navigation ────────────────────────── */
    document.querySelectorAll('.bt-card').forEach(card => {
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'article');

        card.addEventListener('click', (e) => {
            // Don't intercept button/link clicks
            if (e.target.closest('a, button')) return;
            const primaryLink = card.querySelector('.bt-btn--primary');
            if (primaryLink?.href) window.location.href = primaryLink.href;
        });

        card.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const primaryLink = card.querySelector('.bt-btn--primary');
                if (primaryLink?.href) window.location.href = primaryLink.href;
            }
        });
    });

    /* ── Mouse parallax on hero card ───────────────────────── */
    const heroCard = document.querySelector('.bt-card--hero');
    if (heroCard && window.matchMedia('(pointer: fine)').matches) {
        const heroImg = heroCard.querySelector('.bt-card__img');
        heroCard.addEventListener('mousemove', (e) => {
            const rect = heroCard.getBoundingClientRect();
            const xPct = ((e.clientX - rect.left) / rect.width  - 0.5) * 2;
            const yPct = ((e.clientY - rect.top)  / rect.height - 0.5) * 2;
            heroImg.style.transform = `scale(1.08) translate(${xPct * 6}px, ${yPct * 4}px)`;
        });
        heroCard.addEventListener('mouseleave', () => {
            heroImg.style.transform = '';
        });
    }

    /* ── Lazy-load images ──────────────────────────────────── */
    if ('loading' in HTMLImageElement.prototype) {
        // Native lazy loading already set via attribute — nothing extra needed
    } else if ('IntersectionObserver' in window) {
        const imgObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) img.src = img.dataset.src;
                    imgObserver.unobserve(img);
                }
            });
        });
        document.querySelectorAll('.bt-card__img[data-src]').forEach(img => {
            imgObserver.observe(img);
        });
    }

    /* ── Update stats counter in header ───────────────────── */
    const countEl = document.querySelector('[data-topic-count]');
    if (countEl) {
        const total = document.querySelectorAll('.bt-card').length;
        countEl.textContent = total;
    }

});
