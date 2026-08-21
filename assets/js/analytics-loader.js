(() => {
  const loadGoogleAds = () => {
    if (document.querySelector('script[data-google-ads-loader]')) return;

    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=AW-18128635569';
    script.dataset.googleAdsLoader = 'true';
    document.head.appendChild(script);
  };

  const schedule = () => {
    if ('requestIdleCallback' in window) {
      window.requestIdleCallback(loadGoogleAds, { timeout: 2500 });
    } else {
      window.setTimeout(loadGoogleAds, 1500);
    }
  };

  if (document.readyState === 'complete') {
    schedule();
  } else {
    window.addEventListener('load', schedule, { once: true, passive: true });
  }
})();
