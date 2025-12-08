import express, { Request, Response } from 'express';
import crypto from 'crypto';

const router = express.Router();

// Webhook secret for signature verification
const WEBHOOK_SECRET = process.env.WC_WEBHOOK_SECRET || '';

/**
 * Verify WooCommerce webhook signature
 */
function verifyWebhookSignature(req: Request): boolean {
  if (!WEBHOOK_SECRET) {
    console.warn('WC_WEBHOOK_SECRET not set - skipping signature verification');
    return true;
  }

  const signature = req.headers['x-wc-webhook-signature'] as string;
  if (!signature) {
    return false;
  }

  const payload = JSON.stringify(req.body);
  const hash = crypto
    .createHmac('sha256', WEBHOOK_SECRET)
    .update(payload)
    .digest('base64');

  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(hash));
}

/**
 * Log event to Grafana/Prometheus
 */
async function logToGrafana(event: string, data: any) {
  // Track subscription metrics
  const metrics = {
    subscription_created: 1,
    subscription_renewed: 1,
    subscription_cancelled: 1,
    subscription_expired: 1,
    subscription_trial_ended: 1
  };

  // In production, send to Prometheus pushgateway or Grafana Faro
  console.log(`[Grafana] ${event}:`, {
    subscription_id: data.id,
    customer_id: data.customer_id,
    plan: data.line_items?.[0]?.name,
    status: data.status,
    total: data.total,
    timestamp: new Date().toISOString()
  });

  // Send to Grafana Faro (if configured)
  if (process.env.GRAFANA_FARO_URL) {
    try {
      await fetch(`${process.env.GRAFANA_FARO_URL}/events`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          event: event,
          attributes: {
            subscription_id: data.id,
            customer_id: data.customer_id,
            plan: data.line_items?.[0]?.name,
            status: data.status,
            value: parseFloat(data.total)
          }
        })
      });
    } catch (error) {
      console.error('Failed to send to Grafana:', error);
    }
  }
}

/**
 * Update user entitlements in database
 */
async function updateEntitlements(customerId: number, subscription: any) {
  const planName = subscription.line_items?.[0]?.name || 'Unknown';
  const status = subscription.status;

  // Determine entitlements based on plan
  const entitlements = {
    'Kids Bible Monthly': ['kids-coloring-packs', 'episode-early-access', 'member-designs'],
    'Homeschool Monthly': ['homeschool-curriculum', 'lesson-videos', 'teacher-community'],
    'Wedding Planning Monthly': ['wedding-planners', 'vendor-checklists', 'budget-trackers'],
    'Premium Coloring Club': ['premium-coloring', 'exclusive-designs', 'monthly-packs'],
    'Activity Pack Subscription': ['activity-packs', 'printables', 'worksheets']
  };

  const userEntitlements = entitlements[planName as keyof typeof entitlements] || [];

  // Update database (pseudo-code - replace with actual DB logic)
  console.log(`[Entitlements] Updating customer ${customerId}:`, {
    plan: planName,
    status: status,
    entitlements: userEntitlements,
    active: ['active', 'trialling'].includes(status)
  });

  // In production, update your database:
  // await db.users.update({
  //   where: { woocommerce_customer_id: customerId },
  //   data: {
  //     subscription_status: status,
  //     subscription_plan: planName,
  //     entitlements: userEntitlements,
  //     subscription_active: ['active', 'trialling'].includes(status)
  //   }
  // });
}

/**
 * Send push notification to customer
 */
async function sendPushNotification(customerId: number, event: string, data: any) {
  const notifications = {
    subscription_created: {
      title: '🎉 Welcome to CodexDominion!',
      body: `Your ${data.line_items?.[0]?.name} subscription is now active!`,
      action: 'View Your Membership'
    },
    subscription_renewed: {
      title: '✅ Subscription Renewed',
      body: `Your ${data.line_items?.[0]?.name} has been renewed successfully!`,
      action: 'Download New Content'
    },
    subscription_cancelled: {
      title: '😢 Subscription Cancelled',
      body: 'We\'re sad to see you go. Your access will continue until the end of your billing period.',
      action: 'View Benefits'
    },
    subscription_expired: {
      title: '⏰ Subscription Expired',
      body: 'Your subscription has ended. Renew now to regain access!',
      action: 'Renew Subscription'
    },
    subscription_trial_ended: {
      title: '🔔 Trial Ended',
      body: 'Your free trial has ended. Subscribe now to continue enjoying premium content!',
      action: 'Subscribe Now'
    }
  };

  const notification = notifications[event as keyof typeof notifications];
  if (!notification) return;

  console.log(`[Push Notification] Customer ${customerId}:`, notification);

  // In production, send via Firebase Cloud Messaging, OneSignal, etc:
  // await pushService.send({
  //   userId: customerId,
  //   title: notification.title,
  //   body: notification.body,
  //   data: { action: notification.action, subscription_id: data.id }
  // });
}

/**
 * Send email notification
 */
async function sendEmailNotification(customer: any, event: string, data: any) {
  const emails = {
    subscription_created: {
      subject: '🎉 Welcome to Your Subscription!',
      template: 'subscription-welcome',
      data: {
        plan_name: data.line_items?.[0]?.name,
        first_payment: data.total,
        billing_period: data.billing_period,
        trial_end: data.trial_end_date
      }
    },
    subscription_renewed: {
      subject: '✅ Your Subscription Has Been Renewed',
      template: 'subscription-renewed',
      data: {
        plan_name: data.line_items?.[0]?.name,
        amount: data.total,
        next_payment: data.next_payment_date
      }
    },
    subscription_cancelled: {
      subject: 'Your Subscription Has Been Cancelled',
      template: 'subscription-cancelled',
      data: {
        plan_name: data.line_items?.[0]?.name,
        end_date: data.end_date,
        reactivate_link: `${process.env.SITE_URL}/my-account/subscriptions`
      }
    }
  };

  const emailConfig = emails[event as keyof typeof emails];
  if (!emailConfig) return;

  console.log(`[Email] Sending to ${customer.email}:`, emailConfig.subject);

  // In production, send via SendGrid, Mailgun, etc:
  // await emailService.send({
  //   to: customer.email,
  //   subject: emailConfig.subject,
  //   template: emailConfig.template,
  //   data: emailConfig.data
  // });
}

/**
 * Handle subscription webhook events
 */
router.post('/wc/subscription', async (req: Request, res: Response) => {
  try {
    // Verify webhook signature
    if (!verifyWebhookSignature(req)) {
      console.error('[Webhook] Invalid signature');
      return res.status(401).json({ error: 'Invalid signature' });
    }

    const { event, data } = req.body;
    const customerId = data.customer_id;

    console.log(`[Webhook] Received: ${event} for subscription ${data.id}`);

    // Handle different subscription events
    switch (event) {
      case 'subscription_created':
        await updateEntitlements(customerId, data);
        await sendPushNotification(customerId, event, data);
        await sendEmailNotification(data.billing, event, data);
        await logToGrafana('subscription_created', data);
        break;

      case 'subscription_renewed':
        await updateEntitlements(customerId, data);
        await sendPushNotification(customerId, event, data);
        await sendEmailNotification(data.billing, event, data);
        await logToGrafana('subscription_renewed', data);
        break;

      case 'subscription_cancelled':
        await updateEntitlements(customerId, data);
        await sendPushNotification(customerId, event, data);
        await sendEmailNotification(data.billing, event, data);
        await logToGrafana('subscription_cancelled', data);
        break;

      case 'subscription_expired':
        await updateEntitlements(customerId, data);
        await sendPushNotification(customerId, event, data);
        await logToGrafana('subscription_expired', data);
        break;

      case 'subscription_trial_ended':
        await sendPushNotification(customerId, event, data);
        await logToGrafana('subscription_trial_ended', data);
        break;

      case 'subscription_status_changed':
        // Handle status changes (active, on-hold, pending-cancel, etc.)
        await updateEntitlements(customerId, data);
        await logToGrafana('subscription_status_changed', data);
        break;

      case 'subscription_payment_failed':
        console.error(`[Webhook] Payment failed for subscription ${data.id}`);
        await logToGrafana('subscription_payment_failed', data);
        // Send payment failure notification
        break;

      default:
        console.log(`[Webhook] Unhandled event: ${event}`);
    }

    // Return 200 to acknowledge receipt
    res.status(200).json({
      success: true,
      event: event,
      subscription_id: data.id
    });

  } catch (error) {
    console.error('[Webhook] Error processing subscription webhook:', error);

    // Still return 200 to prevent WooCommerce from retrying
    // Log the error for investigation
    res.status(200).json({
      success: false,
      error: 'Internal processing error'
    });
  }
});

/**
 * Handle order webhook events (for one-time purchases)
 */
router.post('/wc/order', async (req: Request, res: Response) => {
  try {
    if (!verifyWebhookSignature(req)) {
      return res.status(401).json({ error: 'Invalid signature' });
    }

    const { event, data } = req.body;

    console.log(`[Webhook] Order event: ${event} for order ${data.id}`);

    switch (event) {
      case 'order_completed':
        await logToGrafana('order_completed', {
          order_id: data.id,
          customer_id: data.customer_id,
          total: data.total,
          items: data.line_items?.length
        });
        break;

      case 'order_refunded':
        await logToGrafana('order_refunded', {
          order_id: data.id,
          refund_amount: data.refund_amount
        });
        break;
    }

    res.status(200).json({ success: true, event: event, order_id: data.id });

  } catch (error) {
    console.error('[Webhook] Error processing order webhook:', error);
    res.status(200).json({ success: false });
  }
});

/**
 * Health check endpoint
 */
router.get('/health', (req: Request, res: Response) => {
  res.json({
    status: 'ok',
    service: 'woocommerce-webhooks',
    timestamp: new Date().toISOString()
  });
});

export default router;
