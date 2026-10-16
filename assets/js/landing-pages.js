document.addEventListener('DOMContentLoaded', () => {
    const faqItems = document.querySelectorAll('.cro-faq-list details');
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

});
