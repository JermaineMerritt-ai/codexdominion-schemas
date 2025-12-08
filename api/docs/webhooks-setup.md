# WooCommerce Webhook Configuration

## Setup Instructions

### 1. Configure Webhook Secret
Add to your `.env` file:
```env
WC_WEBHOOK_SECRET=your_webhook_secret_here
GRAFANA_FARO_URL=https://your-grafana-faro-endpoint
SITE_URL=https://codexdominion.app
```

### 2. Create Webhooks in WooCommerce

Go to **WooCommerce → Settings → Advanced → Webhooks** and create:

#### Subscription Created
- **Name**: Subscription Created
- **Status**: Active
- **Topic**: Subscription created
- **Delivery URL**: `https://api.codexdominion.app/webhooks/wc/subscription`
- **Secret**: [Copy from .env WC_WEBHOOK_SECRET]
- **API Version**: WP REST API Integration v3

#### Subscription Renewed
- **Name**: Subscription Renewed
- **Topic**: Subscription renewed
- **Delivery URL**: `https://api.codexdominion.app/webhooks/wc/subscription`

#### Subscription Cancelled
- **Name**: Subscription Cancelled
- **Topic**: Subscription cancelled
- **Delivery URL**: `https://api.codexdominion.app/webhooks/wc/subscription`

#### Subscription Expired
- **Name**: Subscription Expired
- **Topic**: Subscription expired
- **Delivery URL**: `https://api.codexdominion.app/webhooks/wc/subscription`

#### Subscription Status Changed
- **Name**: Subscription Status Changed
- **Topic**: Subscription updated
- **Delivery URL**: `https://api.codexdominion.app/webhooks/wc/subscription`

#### Order Completed
- **Name**: Order Completed
- **Topic**: Order completed
- **Delivery URL**: `https://api.codexdominion.app/webhooks/wc/order`

#### Order Refunded
- **Name**: Order Refunded
- **Topic**: Order refunded
- **Delivery URL**: `https://api.codexdominion.app/webhooks/wc/order`

### 3. Test Webhooks

Send test webhook from WooCommerce:
1. Go to webhook settings
2. Click "Edit" on a webhook
3. Scroll to bottom and click "Deliver"
4. Check response in logs

### 4. Monitor Webhook Logs

Check API logs:
```bash
docker logs codex-api --tail 100 -f | grep Webhook
```

### 5. Entitlements Mapping

| Subscription Plan | Entitlements |
|-------------------|--------------|
| Kids Bible Monthly | kids-coloring-packs, episode-early-access, member-designs |
| Homeschool Monthly | homeschool-curriculum, lesson-videos, teacher-community |
| Wedding Planning Monthly | wedding-planners, vendor-checklists, budget-trackers |
| Premium Coloring Club | premium-coloring, exclusive-designs, monthly-packs |
| Activity Pack Subscription | activity-packs, printables, worksheets |

### 6. Webhook Events Handled

- `subscription_created` - New subscription starts
- `subscription_renewed` - Recurring payment successful
- `subscription_cancelled` - Customer cancels subscription
- `subscription_expired` - Subscription period ended
- `subscription_trial_ended` - Trial period completed
- `subscription_status_changed` - Status update (on-hold, pending-cancel, etc.)
- `subscription_payment_failed` - Payment processing failed
- `order_completed` - One-time purchase completed
- `order_refunded` - Order refunded

### 7. Grafana Metrics Tracked

- Subscription creation count
- Renewal count
- Cancellation count
- Churn rate
- Revenue per subscription
- Customer lifetime value
- Payment failure rate

### 8. Security Notes

- Always verify webhook signature using HMAC SHA256
- Use HTTPS for webhook URLs
- Keep webhook secret secure
- Log all webhook events for audit trail
- Return 200 even on errors to prevent retries
