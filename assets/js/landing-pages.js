document.addEventListener('DOMContentLoaded', () => {
    const header = document.getElementById('lpHeader');
    const form = document.getElementById('contactForm');
    const faqItems = document.querySelectorAll('.lp-faq-list details');
    const whatsappNumber = '5547988670233';

    const updateHeader = () => {
        if (header) header.classList.toggle('is-scrolled', window.scrollY > 8);
    };

    updateHeader();
    window.addEventListener('scroll', updateHeader, { passive: true });

    faqItems.forEach((item) => {
        item.addEventListener('toggle', () => {
            if (!item.open) return;
            faqItems.forEach((otherItem) => {
                if (otherItem !== item) otherItem.open = false;
            });
        });
    });

    form?.addEventListener('submit', (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const pageName = form.dataset.pageName || document.body.dataset.landingPage || document.title.split('|')[0];
        const name = String(formData.get('nome') || '').trim();
        const situation = String(formData.get('situacao') || '').trim();
        const message = String(formData.get('mensagem') || '').trim();
        const parts = [
            `Olá! Vim da página de ${pageName} e gostaria de falar com um advogado.`,
            name ? `Meu nome é ${name}.` : '',
            situation ? `Minha situação se aproxima de: ${situation}.` : '',
            message ? `Resumo: ${message}` : '',
        ].filter(Boolean);

        const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(parts.join(' '))}`;
        window.open(whatsappUrl, '_blank', 'noopener,noreferrer');
    });
});
