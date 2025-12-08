'use client';

import { useEffect } from 'react';

export function Analytics() {
  useEffect(() => {
    // Track pageviews
    const handleRouteChange = (url: string) => {
      if ((window as any).gtag) {
        (window as any).gtag('config', process.env.NEXT_PUBLIC_GA_ID, {
          page_path: url,
        });
      }
    };

    // Listen to route changes
    window.addEventListener('popstate', () => handleRouteChange(window.location.pathname));

    return () => {
      window.removeEventListener('popstate', () => handleRouteChange(window.location.pathname));
    };
  }, []);

  return (
    <>
      {/* Google Analytics */}
      {process.env.NEXT_PUBLIC_GA_ID && (
        <>
          <script
            async
            src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_ID}`}
          />
          <script
            dangerouslySetInnerHTML={{
              __html: `
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag('js', new Date());
                gtag('config', '${process.env.NEXT_PUBLIC_GA_ID}', {
                  page_path: window.location.pathname,
                });
              `,
            }}
          />
        </>
      )}

      {/* Grafana Faro RUM */}
      {process.env.NEXT_PUBLIC_GRAFANA_FARO_URL && (
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function() {
                var script = document.createElement('script');
                script.src = 'https://unpkg.com/@grafana/faro-web-sdk@latest/dist/bundle/faro-web-sdk.iife.js';
                script.onload = function() {
                  window.GrafanaFaro.initializeFaro({
                    url: '${process.env.NEXT_PUBLIC_GRAFANA_FARO_URL}',
                    app: {
                      name: 'codexdominion-web',
                      version: '2.0.0',
                      environment: '${process.env.NODE_ENV}'
                    },
                    instrumentations: [...window.GrafanaFaro.getWebInstrumentations()],
                  });
                };
                document.head.appendChild(script);
              })();
            `,
          }}
        />
      )}
    </>
  );
}

// Track custom events
export function trackEvent(eventName: string, params?: Record<string, any>) {
  // Google Analytics
  if (typeof window !== 'undefined' && (window as any).gtag) {
    (window as any).gtag('event', eventName, params);
  }

  // Grafana Faro
  if (typeof window !== 'undefined' && (window as any).GrafanaFaro) {
    (window as any).GrafanaFaro.api.pushEvent(eventName, params);
  }

  // Console log in development
  if (process.env.NODE_ENV === 'development') {
    console.log('[Analytics Event]', eventName, params);
  }
}

// E-commerce tracking helpers
export const trackAddToCart = (product: any, quantity: number = 1) => {
  trackEvent('add_to_cart', {
    event_category: 'ecommerce',
    event_label: product.name,
    value: parseFloat(product.price) * quantity,
    items: [{
      item_id: product.id,
      item_name: product.name,
      item_category: product.categories?.[0]?.name,
      price: parseFloat(product.price),
      quantity
    }]
  });
};

export const trackSubscribe = (plan: string, price: string) => {
  trackEvent('subscribe', {
    event_category: 'conversion',
    event_label: plan,
    value: parseFloat(price)
  });
};

export const trackDownloadLeadMagnet = (magnetId: string, email: string) => {
  trackEvent('download_lead_magnet', {
    event_category: 'engagement',
    event_label: magnetId,
    value: email
  });
};

export const trackNicheView = (niche: string) => {
  trackEvent('view_niche', {
    event_category: 'engagement',
    event_label: niche
  });
};

export const trackFunnelStep = (funnel: string, step: string) => {
  trackEvent('funnel_step', {
    event_category: 'funnel',
    event_label: `${funnel}_${step}`
  });
};
