document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('contactForm');
    const faqItems = document.querySelectorAll('.cro-faq-list details');
    const whatsappNumber = '5547988670233';
    const conversionSendTo = 'AW-18128635569/1bouCJi_h-UcELGNtMRD';
    const pageName = document.body.dataset.landingPage || document.title.split('|')[0].trim();

    const trackLeadConversion = (eventLabel) => {
        if (typeof window.gtag !== 'function') return;

        window.gtag('event', 'conversion', {
            send_to: conversionSendTo,
            event_category: 'lead',
            event_label: `${pageName}:${eventLabel}`,
        });
    };

    const trackWhatsappClick = (link) => {
        if (typeof window.gtag !== 'function') return;

        window.gtag('event', 'whatsapp_click', {
            event_category: 'engagement',
            event_label: `${pageName}:whatsapp_click`,
            link_url: link.href,
            page_location: window.location.href,
            transport_type: 'beacon',
        });
    };

    faqItems.forEach((item) => {
        item.addEventListener('toggle', () => {
            if (!item.open) return;
            faqItems.forEach((otherItem) => {
                if (otherItem !== item) otherItem.open = false;
            });
        });
    });

    document.querySelectorAll('a[href*="wa.me"], a[href*="api.whatsapp.com"], a[href^="tel:"]').forEach((link) => {
        link.addEventListener('click', () => {
            const href = link.getAttribute('href') || '';
            const isPhoneClick = href.startsWith('tel:');
            if (!isPhoneClick) trackWhatsappClick(link);
            trackLeadConversion(isPhoneClick ? 'phone_click' : 'whatsapp_click');
        });
    });

    form?.addEventListener('submit', (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const formPageName = form.dataset.pageName || pageName;
        const name = String(formData.get('nome') || '').trim();
        const situation = String(formData.get('situacao') || '').trim();
        const whatsapp = String(formData.get('whatsapp') || '').trim();
        const message = String(formData.get('mensagem') || '').trim();
        const parts = [
            `Olá! Vim da página de ${formPageName} e gostaria de falar com um advogado.`,
            name ? `Meu nome é ${name}.` : '',
            whatsapp ? `Meu WhatsApp é ${whatsapp}.` : '',
            situation ? `Minha situação se aproxima de: ${situation}.` : '',
            message ? `Resumo: ${message}` : '',
        ].filter(Boolean);

        // A ação automática do Google Ads cobre a URL explícita /index.html.
        // Nas demais páginas, o evento direto garante a mensuração do formulário.
        if (!window.location.pathname.endsWith('/index.html')) {
            trackLeadConversion('form_submit');
        }

        const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(parts.join(' '))}`;
        window.open(whatsappUrl, '_blank', 'noopener,noreferrer');
    });
});
