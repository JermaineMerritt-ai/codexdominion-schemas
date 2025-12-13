# Stripe Integration Guide for CodexDominion.app

## Quick Start (30 minutes)

### Step 1: Create Stripe Account (5 minutes)
1. Go to https://stripe.com
2. Sign up with your business email
3. Complete business verification
4. Navigate to Developers → API Keys

### Step 2: Get API Keys (2 minutes)
You'll need two keys:
- **Test Mode (for development):**
  - Publishable key: `pk_test_...`
  - Secret key: `sk_test_...`

- **Live Mode (for production):**
  - Publishable key: `pk_live_...`
  - Secret key: `sk_live_...`

### Step 3: Add Environment Variables (3 minutes)
Create `frontend/.env.local`:

```env
# Stripe Keys (use test keys first)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
STRIPE_SECRET_KEY=sk_test_your_key_here

# Site URL
NEXT_PUBLIC_SITE_URL=http://localhost:3001
```

For production, create `frontend/.env.production`:
```env
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_your_key_here
STRIPE_SECRET_KEY=sk_live_your_key_here
NEXT_PUBLIC_SITE_URL=https://www.codexdominion.app
```

**⚠️ IMPORTANT:** Never commit `.env.local` or `.env.production` to Git!

### Step 4: Install Stripe SDK (2 minutes)
```bash
cd frontend
npm install @stripe/stripe-js stripe
```

### Step 5: Create Products in Stripe Dashboard (15 minutes)

#### For Each Product:
1. Go to Stripe Dashboard → Products → Add Product
2. Enter details:
   - **Name:** The Daily Flame: 365 Days of Eternal Light
   - **Description:** A year-long journey of daily reflections...
   - **Price:** $27.00 USD (one-time payment)
   - **Tax Code:** Digital goods (if applicable)
3. Click **Save Product**
4. Copy the **Product ID** (e.g., `prod_ABC123`)
5. Copy the **Price ID** (e.g., `price_XYZ789`)

#### Update products.json:
Open `frontend/data/products.json` and add IDs:
```json
{
  "id": "dev-001",
  "title": "The Daily Flame: 365 Days of Eternal Light",
  "stripeProductId": "prod_ABC123",
  "stripePriceId": "price_XYZ789",
  ...
}
```

**Repeat for all 8 products.**

### Step 6: Update Product Detail Page (5 minutes)
Open `frontend/pages/products/[slug].tsx` and replace the "Buy Now" button section:

```tsx
import { loadStripe } from '@stripe/stripe-js';

// At the top of the component
const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);

// Replace the Buy Now button with:
const handlePurchase = async () => {
  const stripe = await stripePromise;

  const response = await fetch('/api/create-checkout-session', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      productId: product.slug,
      priceId: product.stripePriceId,
      productName: product.title,
      productPrice: displayPrice
    })
  });

  const { sessionId } = await response.json();
  await stripe?.redirectToCheckout({ sessionId });
};

// Update the button:
<button
  onClick={handlePurchase}
  className="w-full py-5 bg-gradient-to-r from-gold-500 to-amber-500 hover:from-gold-600 hover:to-amber-600 rounded-xl font-bold text-xl transition-all duration-300 shadow-2xl transform hover:scale-105"
>
  🛒 Buy Now - Instant Access
</button>
```

### Step 7: Test the Checkout Flow (3 minutes)
1. Start development server:
   ```bash
   cd frontend
   npm run dev
   ```
2. Visit http://localhost:3001
3. Navigate to a product page
4. Click "Buy Now"
5. Use Stripe test card:
   - **Card Number:** 4242 4242 4242 4242
   - **Expiry:** Any future date (e.g., 12/25)
   - **CVC:** Any 3 digits (e.g., 123)
   - **ZIP:** Any 5 digits (e.g., 12345)
6. Complete checkout
7. Verify redirect to `/order/success`

---

## Production Deployment Checklist

### Before Going Live:
- [ ] Switch to live Stripe keys in `.env.production`
- [ ] Test all 8 products with live keys
- [ ] Set up Stripe webhooks for order notifications
- [ ] Configure tax settings in Stripe Dashboard
- [ ] Enable email receipts in Stripe settings
- [ ] Test full purchase flow on mobile & desktop
- [ ] Verify SSL certificate on www.codexdominion.app

### Stripe Dashboard Settings:
1. **Business Settings**
   - Add business name and logo
   - Set support email and phone
   - Configure refund policy

2. **Email Receipts**
   - Enable automatic receipts
   - Customize email template with brand colors

3. **Webhooks** (for advanced features)
   - Endpoint: `https://www.codexdominion.app/api/stripe-webhook`
   - Events to listen for:
     - `checkout.session.completed`
     - `payment_intent.succeeded`
     - `charge.refunded`

---

## Test Cards for Development

Use these cards in **test mode** only:

| Scenario | Card Number | Expiry | CVC | ZIP |
|----------|-------------|--------|-----|-----|
| Success | 4242 4242 4242 4242 | 12/25 | 123 | 12345 |
| Decline | 4000 0000 0000 0002 | 12/25 | 123 | 12345 |
| Insufficient Funds | 4000 0000 0000 9995 | 12/25 | 123 | 12345 |
| 3D Secure (authentication) | 4000 0025 0000 3155 | 12/25 | 123 | 12345 |

---

## Revenue Tracking

### Stripe Dashboard
- View real-time sales
- Track revenue by product
- Monitor conversion rates
- Export transaction data

### Key Metrics to Watch:
- **Gross Revenue:** Total sales before fees
- **Net Revenue:** After Stripe fees (2.9% + $0.30 per transaction)
- **Conversion Rate:** Purchases / Checkout Sessions
- **Average Order Value:** Total Revenue / Number of Orders

---

## Customer Support

### Common Questions:

**Q: Customer didn't receive download link**
**A:** Check Stripe Dashboard → Payments → Find order → Resend receipt

**Q: Customer wants refund**
**A:** Stripe Dashboard → Payments → Find order → Refund

**Q: Card declined**
**A:** Ask customer to contact their bank or try different card

---

## Next Steps After Stripe

1. **Set up automated emails:**
   - Order confirmation with download links
   - 24-hour follow-up ("How's your experience?")
   - 7-day check-in with upsell offer

2. **Create customer account system:**
   - Allow login to view order history
   - Download products anytime
   - Track purchase history

3. **Add affiliate program:**
   - Pay 20% commission to affiliates
   - Track referrals via UTM parameters
   - Automate payouts

---

## Troubleshooting

### Error: "No such price: price_123"
- **Cause:** Wrong Price ID in products.json
- **Fix:** Copy correct Price ID from Stripe Dashboard

### Error: "API key invalid"
- **Cause:** Using test key in production or vice versa
- **Fix:** Check `.env.production` has live keys

### Checkout redirects to cancel page
- **Cause:** User clicked back button or closed checkout
- **Fix:** Normal behavior, no action needed

### Payment succeeded but no email
- **Cause:** Email receipts disabled in Stripe
- **Fix:** Stripe Dashboard → Settings → Emails → Enable receipts

---

## Support

**Stripe Support:** https://support.stripe.com
**Stripe Docs:** https://stripe.com/docs/checkout/quickstart
**CodexDominion Support:** support@codexdominion.app

---

**Estimated Setup Time:** 30-45 minutes
**Cost:** 2.9% + $0.30 per successful transaction
**Payout Schedule:** Rolling 2-day (customizable)
