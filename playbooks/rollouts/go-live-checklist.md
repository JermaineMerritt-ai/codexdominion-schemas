# Go-Live Checklist - Codex Dominion Production Launch

## Pre-Launch (1 Week Before)

### Infrastructure Setup
- [ ] Server provisioned (IONOS VPS 74.208.123.158)
- [ ] DNS A records configured
  - [ ] codexdominion.app → 74.208.123.158
  - [ ] api.codexdominion.app → 74.208.123.158
  - [ ] www.codexdominion.app → 74.208.123.158
- [ ] SSL certificates installed and valid
  - [ ] Run: `certbot --nginx -d codexdominion.app -d www.codexdominion.app -d api.codexdominion.app`
  - [ ] Verify expiry: `certbot certificates` (should show 90 days)
- [ ] Firewall configured
  - [ ] Allow ports: 80, 443, 22
  - [ ] Block unnecessary ports
  - [ ] Rate limiting enabled

### Application Configuration

**WordPress:**
- [ ] WordPress installed at http://localhost:8080 or production domain
- [ ] WooCommerce plugin installed and activated
- [ ] Custom plugins activated:
  - [ ] Codex Auto Bundles
  - [ ] Codex Subscription Seeder
  - [ ] Codex Schema Markup
- [ ] Run Subscription Seeder to create 5 subscription products
- [ ] Verify 10 bundles auto-created by Auto Bundles plugin
- [ ] Taxonomy configured (15 categories, 14 tags)
- [ ] Test product created and visible
- [ ] Payment gateway configured (Stripe/PayPal)
  - [ ] Test mode successful
  - [ ] Live keys entered
  - [ ] Test transaction completed

**WooCommerce Settings:**
- [ ] Store address and currency set
- [ ] Shipping zones configured
- [ ] Tax rates entered (if applicable)
- [ ] Email notifications working
- [ ] Permalink structure: Post name
- [ ] REST API keys generated
  - [ ] Consumer Key copied to `web/.env.local`
  - [ ] Consumer Secret copied to `web/.env.local`

**Webhooks Configured:**
- [ ] subscription_created → https://api.codexdominion.app/webhooks/wc/subscription
- [ ] subscription_renewed → https://api.codexdominion.app/webhooks/wc/subscription
- [ ] subscription_cancelled → https://api.codexdominion.app/webhooks/wc/subscription
- [ ] subscription_expired → https://api.codexdominion.app/webhooks/wc/subscription
- [ ] subscription_updated → https://api.codexdominion.app/webhooks/wc/subscription
- [ ] order_completed → https://api.codexdominion.app/webhooks/wc/order
- [ ] order_refunded → https://api.codexdominion.app/webhooks/wc/order
- [ ] Webhook secret matches `api/.env` WC_WEBHOOK_SECRET
- [ ] Test delivery successful (check logs: `docker logs codex-api | grep Webhook`)

**Next.js Frontend:**
- [ ] Environment variables configured in `web/.env.local`
  - [ ] WC_CONSUMER_KEY set
  - [ ] WC_CONSUMER_SECRET set
  - [ ] WC_API_URL set to production WordPress
  - [ ] NEXT_PUBLIC_SITE_URL set to https://codexdominion.app
  - [ ] NEXT_PUBLIC_GA_MEASUREMENT_ID set
  - [ ] NEXT_PUBLIC_GRAFANA_FARO_URL set
- [ ] Build successful: `npm run build`
- [ ] No TypeScript errors
- [ ] Lighthouse score > 90 (Performance, Accessibility, Best Practices, SEO)
- [ ] All images optimized (WebP/AVIF)
- [ ] Open Graph tags present (test with https://www.opengraph.xyz/)
- [ ] Twitter Card tags present

**API Backend:**
- [ ] Environment variables configured in `api/.env`
  - [ ] WC_WEBHOOK_SECRET matches WooCommerce
  - [ ] GRAFANA_FARO_URL set
  - [ ] SITE_URL set to https://api.codexdominion.app
  - [ ] DATABASE_URL set to production database
  - [ ] SMTP credentials configured
- [ ] Health check endpoint working: `curl https://api.codexdominion.app/health`
- [ ] Webhook endpoint working: `curl https://api.codexdominion.app/webhooks/health`
- [ ] Database connection successful
- [ ] Email notifications sending

### Content & Products

**Products:**
- [ ] At least 10 products uploaded with:
  - [ ] High-quality images (min 1000x1000px)
  - [ ] Complete descriptions
  - [ ] Pricing
  - [ ] Categories and tags
  - [ ] Stock status
- [ ] 5 subscription products created by Subscription Seeder plugin
- [ ] 10 bundle products auto-created by Auto Bundles plugin
- [ ] Featured products selected

**Pages:**
- [ ] Homepage live and styled
- [ ] About/Charter page created
- [ ] Shop page showing products
- [ ] Subscriptions page showing 5 plans
- [ ] Contact page with form
- [ ] Privacy Policy
- [ ] Terms of Service
- [ ] Refund Policy

**Lead Magnets:**
- [ ] Christian Wedding Checklist (8-page PDF) created and uploaded
- [ ] Christmas Coloring Pack created
- [ ] Homeschool Guide created
- [ ] Memory Verse Cards created
- [ ] Landing pages for each lead magnet
- [ ] Email sequences configured in email service (Mailchimp/ConvertKit)

**Media Assets:**
- [ ] Logo uploaded (PNG with transparency)
- [ ] Favicon configured
- [ ] Social media images (1200x630px for Open Graph)
- [ ] Product photography complete
- [ ] Instagram carousel images for lead magnets

### Analytics & Monitoring

**Grafana:**
- [ ] Dashboard accessible at https://codexdominion.app/grafana
- [ ] E-commerce dashboard configured (10 panels)
- [ ] Data flowing from Prometheus
- [ ] Admin password changed from default
- [ ] Alert rules configured:
  - [ ] Error rate > 5%
  - [ ] Response time > 2 seconds
  - [ ] Database connections > 80% of max

**Prometheus:**
- [ ] Scraping all targets successfully
  - [ ] web (Next.js)
  - [ ] api (Express)
  - [ ] wordpress
  - [ ] nginx
  - [ ] mysql
  - [ ] redis
- [ ] Retention period configured (30 days)
- [ ] Storage sufficient for metrics

**Google Analytics 4:**
- [ ] GA4 property created
- [ ] Measurement ID added to Next.js
- [ ] E-commerce tracking configured
- [ ] Conversion events defined:
  - [ ] add_to_cart
  - [ ] begin_checkout
  - [ ] purchase
  - [ ] subscribe
  - [ ] download_lead_magnet

**Social Media:**
- [ ] Instagram business account created and linked
- [ ] Facebook Page created
- [ ] Pinterest business account created
- [ ] YouTube channel created
- [ ] TikTok business account created
- [ ] UTM tracking configured in all social links

### Testing

**Functional Tests:**
- [ ] User can register account
- [ ] User can log in
- [ ] User can browse products by category
- [ ] User can search products
- [ ] User can add product to cart
- [ ] User can proceed to checkout
- [ ] User can complete purchase (test payment)
- [ ] User receives order confirmation email
- [ ] User can subscribe to monthly plan
- [ ] User receives subscription confirmation email
- [ ] User can download lead magnet
- [ ] User receives lead magnet email sequence
- [ ] User can access downloads after purchase
- [ ] Admin can view orders in WooCommerce

**Performance Tests:**
- [ ] Homepage loads in < 2 seconds
- [ ] Product pages load in < 2 seconds
- [ ] Checkout completes in < 3 seconds
- [ ] API responds in < 500ms (p95)
- [ ] No memory leaks (monitor over 1 hour)
- [ ] Load test with 100 concurrent users successful

**Security Tests:**
- [ ] SQL injection test passed
- [ ] XSS test passed
- [ ] CSRF protection enabled
- [ ] HTTPS enforced (no HTTP)
- [ ] Security headers configured (CSP, X-Frame-Options, etc.)
- [ ] WooCommerce webhook signature verification working
- [ ] Admin area password protected
- [ ] Database not accessible from public internet

**Mobile Tests:**
- [ ] Site responsive on iPhone (Safari)
- [ ] Site responsive on Android (Chrome)
- [ ] Touch targets at least 44x44px
- [ ] Text readable without zoom
- [ ] Forms usable on mobile
- [ ] Checkout works on mobile

### Backups & Recovery

**Backup System:**
- [ ] Automated backup script configured: `infra/docker/backup.sh`
- [ ] Backup cron job scheduled (daily at 2am)
  - [ ] Add to crontab: `0 2 * * * /root/codex-dominion/infra/docker/backup.sh`
- [ ] Backup storage configured (minimum 30 days retention)
- [ ] Test backup restoration successful
- [ ] Off-site backup configured (S3, Backblaze, etc.)

**Disaster Recovery:**
- [ ] Rollback procedure documented
- [ ] Database restore tested successfully
- [ ] Time to recover < 30 minutes
- [ ] Incident response playbook ready

### Legal & Compliance

- [ ] Privacy Policy published and linked in footer
- [ ] Terms of Service published and linked in footer
- [ ] Refund Policy published
- [ ] Cookie consent banner implemented (if targeting EU)
- [ ] GDPR compliance verified (if targeting EU)
- [ ] PCI DSS compliance (payment processor handles)
- [ ] Copyright notices on all content
- [ ] Domain registered for minimum 1 year

## Launch Day

### Morning (9am)

- [ ] **Final backup:** `cd infra/docker && ./backup.sh`
- [ ] **Verify all services healthy:**
  ```bash
  ssh root@74.208.123.158
  docker-compose ps  # All should be "Up"
  curl https://codexdominion.app
  curl https://api.codexdominion.app/health
  ```
- [ ] **Check SSL expiry:** `certbot certificates`
- [ ] **Review monitoring dashboards:** Grafana, Prometheus
- [ ] **Enable maintenance mode (if transitioning from old site)**

### Deployment (10am)

- [ ] **Deploy production code:**
  ```bash
  cd /root/codex-dominion
  git pull origin main
  docker-compose build --no-cache
  docker-compose up -d
  ```
- [ ] **Verify deployment:**
  ```bash
  docker-compose ps
  docker logs codex-web --tail 50
  docker logs codex-api --tail 50
  ```
- [ ] **Run smoke tests:** Test checkout, subscription, lead magnet
- [ ] **Disable maintenance mode**

### Post-Launch (11am)

- [ ] **Monitor metrics for 1 hour:**
  - [ ] Error rate < 1%
  - [ ] Response times normal
  - [ ] No memory/CPU spikes
  - [ ] Database connections healthy
- [ ] **Test from multiple locations:** Use VPN to test from different countries
- [ ] **Cross-browser testing:** Chrome, Firefox, Safari, Edge
- [ ] **Test on real mobile devices**

### Announcement (12pm)

- [ ] **Social media announcements:**
  - [ ] Instagram post: "🎉 We're LIVE! Shop our Christian printables..."
  - [ ] Facebook post with link
  - [ ] Pinterest pin linking to homepage
  - [ ] YouTube Community post
  - [ ] TikTok video announcement
- [ ] **Email announcement:** Send to mailing list (if exists)
- [ ] **Update website header:** Add "NEW!" badge or launch banner
- [ ] **Submit to search engines:**
  - [ ] Google Search Console: Submit sitemap
  - [ ] Bing Webmaster Tools: Submit sitemap

## Post-Launch (First Week)

### Day 1-3: Intensive Monitoring
- [ ] Monitor Grafana hourly
- [ ] Review error logs twice daily
- [ ] Check webhook delivery success rate
- [ ] Monitor conversion funnel daily
- [ ] Respond to customer issues within 1 hour

### Day 4-7: Optimization
- [ ] Review Google Analytics data
- [ ] Identify high bounce rate pages and optimize
- [ ] A/B test CTAs on homepage
- [ ] Optimize product images further if needed
- [ ] Add more lead magnet content based on performance

### Week 2: Content & Marketing
- [ ] Publish 5 Instagram posts
- [ ] Publish 20 Pinterest pins
- [ ] Upload 2 YouTube videos
- [ ] Send follow-up email sequence to subscribers
- [ ] Start paid ads ($50/day budget)

### Week 3: Feature Additions
- [ ] Add customer reviews/testimonials
- [ ] Launch affiliate program
- [ ] Add more subscription tiers based on demand
- [ ] Implement customer loyalty program

### Week 4: Analysis & Iteration
- [ ] Review month 1 metrics:
  - [ ] Total revenue
  - [ ] Conversion rate
  - [ ] Average order value
  - [ ] Customer LTV
  - [ ] Churn rate
  - [ ] Lead magnet conversion rate
- [ ] Identify top-performing products
- [ ] Double down on winning niches
- [ ] Plan month 2 content calendar

## Success Metrics

**Week 1 Goals:**
- [ ] 100 unique visitors
- [ ] 10 transactions
- [ ] $500 revenue
- [ ] 50 lead magnet downloads
- [ ] 5 subscriptions

**Month 1 Goals:**
- [ ] 1,000 unique visitors
- [ ] 50 transactions
- [ ] $2,500 revenue
- [ ] 300 lead magnet downloads
- [ ] 20 active subscriptions
- [ ] 500 email subscribers

**Quarter 1 Goals:**
- [ ] 5,000 unique visitors/month
- [ ] 200 transactions/month
- [ ] $10,000 revenue/month
- [ ] 1,000 lead magnet downloads
- [ ] 100 active subscriptions
- [ ] 2,000 email subscribers

## Rollback Trigger

**Abort launch if:**
- Critical functionality broken (checkout, payment processing)
- Security vulnerability discovered
- Major performance issue (site loading > 5 seconds)
- Data loss or corruption
- Legal/compliance issue identified

**Rollback procedure:** See `playbooks/runbooks/deployment.md`

---

**Launch Date:** [To Be Determined]
**Launch Manager:** [Name]
**On-Call Engineer:** [Name]
**Incident Commander:** [Name]

**Emergency Contacts:**
- DevOps Lead: [Phone]
- Business Owner: [Phone]
- Payment Processor Support: [Phone]
- Hosting Provider Support: [Phone]

---

**Last Updated:** December 6, 2025
**Status:** Ready for launch pending WordPress setup
