# UX COPY & MICRO-STATE SPECIFICATIONS
**CodexDominion Design System**  
**Version 1.0.0** | December 23, 2025

---

## 📖 COPY TONE & VOICE GUIDELINES

### Brand Voice
- **Empowering**: "Your Culture. Your Creators. Your Digital Economy."
- **Community-Focused**: Emphasize collaboration, Caribbean pride
- **Action-Oriented**: Use verbs like "Create", "Earn", "Rise", "Share"
- **Inclusive**: Always say "You" and "Your", never exclusive language

### Writing Principles
1. **Clarity First**: Short, direct sentences
2. **Celebrate Progress**: Every action is a step toward sovereignty
3. **Caribbean Pride**: References to culture, community, heritage
4. **Youth-Friendly**: Modern, energetic, emoji-enhanced (🔥, 🎉, 👑, 💰)

---

## 🎯 CORE USER FLOWS

---

## 1️⃣ SIGN UP FLOW

### Screen: Create Account

**Headline:**
```
Welcome to CodexDominion 👑
```

**Subheadline:**
```
Your digital journey starts here. Join thousands of Caribbean creators earning daily.
```

**Form Fields:**

1. **Full Name**
   - Label: "Your Name"
   - Placeholder: "e.g., Marcus Thompson"
   - Helper Text: "The name you want creators to see"

2. **Email Address**
   - Label: "Email Address"
   - Placeholder: "you@example.com"
   - Helper Text: "We'll never share your email"

3. **Password**
   - Label: "Create Password"
   - Placeholder: "8+ characters, mix of letters & numbers"
   - Helper Text: "Use a strong password to keep your account secure"

4. **Country**
   - Label: "Country"
   - Placeholder: "Select your country"
   - Options: [All Caribbean nations]

**Primary Button:**
```
Create Account 🔥
```

**Secondary Link:**
```
Already have an account? Sign In
```

---

### Micro-States: Sign Up

| State | UI Change | Message | Duration |
|-------|-----------|---------|----------|
| **Empty Field** | Red border on field | "This field is required" | Persistent |
| **Invalid Email** | Red border, error icon | "Please enter a valid email address" | Persistent |
| **Weak Password** | Yellow border, warning icon | "Try a stronger password (8+ characters)" | Persistent |
| **Creating Account** | Spinner on button, disabled | "Creating your account..." | 1-3s |
| **Success** | Green checkmark animation | "Welcome! Redirecting to your dashboard..." | 1s then redirect |
| **Error (Network)** | Red alert banner | "Connection error. Please try again." | Persistent |
| **Error (Email Taken)** | Red border on email field | "This email is already in use. Try signing in?" | Persistent |

**Success Animation:**
- Green checkmark fades in (200ms)
- Confetti burst (500ms)
- Redirect to dashboard (1s delay)

---

## 2️⃣ UPLOAD PRODUCT FLOW

### Screen: Upload Product

**Headline:**
```
Turn your creativity into income 💰
```

**Subheadline:**
```
Upload your digital product in minutes. Start earning immediately.
```

**Form Fields:**

1. **Product Title**
   - Label: "Product Name"
   - Placeholder: "e.g., Caribbean Wedding Planner Bundle"
   - Character Limit: 80 characters
   - Helper Text: "Make it clear and descriptive"

2. **Description**
   - Label: "Description"
   - Placeholder: "Describe what makes your product special..."
   - Character Limit: 500 characters
   - Helper Text: "Share what's included and who it's for"

3. **Price**
   - Label: "Price (USD)"
   - Placeholder: "9.99"
   - Helper Text: "Your take-home: 85% after fees"

4. **Category**
   - Label: "Category"
   - Options: [Kids Bible Stories, Homeschool, Wedding, Memory Verse, Seasonal, Digital Downloads]

5. **File Upload**
   - Label: "Upload Files"
   - Accepted: PDF, PNG, JPG, ZIP (max 50MB)
   - Helper Text: "Upload your product files (PDF, images, or ZIP)"

**Primary Button:**
```
Publish Product 🚀
```

**Secondary Button:**
```
Save as Draft
```

---

### Micro-States: Upload Product

| State | UI Change | Message | Duration |
|-------|-----------|---------|----------|
| **Empty Title** | Red border on title field | "Your product needs a name" | Persistent |
| **File Uploading** | Progress bar (0-100%) | "Uploading... 45%" | Real-time |
| **Processing File** | Spinner animation | "Processing your file... Almost there!" | 2-5s |
| **File Too Large** | Red alert, file rejected | "File is too large (max 50MB). Try compressing it." | Persistent |
| **Invalid File Type** | Red alert, file rejected | "This file type isn't supported. Try PDF, PNG, JPG, or ZIP." | Persistent |
| **Success** | Green checkmark, confetti | "Product published! 🎉 View your listing." | 3s auto-dismiss |
| **Error** | Red alert banner | "Upload failed. Please check your connection and try again." | Persistent |
| **Saved as Draft** | Blue notification | "Draft saved! You can finish later." | 3s auto-dismiss |

**Upload Progress Animation:**
```
1. File selected → Shows filename with progress bar
2. Progress bar fills left-to-right (blue)
3. On complete → Checkmark appears, "File uploaded ✅"
4. Processing state → Spinner appears, "Processing..."
5. Success → Green banner, confetti burst
```

---

## 3️⃣ SHARE LINK FLOW

### Screen: Promote Your Product

**Headline:**
```
Your link is ready! Start earning today 🔗
```

**Subheadline:**
```
Share your product with your audience. Every sale puts money in your pocket.
```

**Shareable Link (Copy Box):**
```
https://codexdominion.app/p/your-product-id
```

**Copy Button:**
```
Copy Link 📋
```

**Social Share Buttons:**

1. **WhatsApp**
   - Icon: WhatsApp green
   - Label: "Share on WhatsApp"
   - Pre-filled message: "Check out my new product on CodexDominion! [link]"

2. **Instagram**
   - Icon: Instagram gradient
   - Label: "Share on Instagram"
   - Action: Opens Instagram app with link in bio prompt

3. **TikTok**
   - Icon: TikTok black/blue
   - Label: "Share on TikTok"
   - Action: Opens TikTok app with link in bio prompt

4. **Facebook**
   - Icon: Facebook blue
   - Label: "Share on Facebook"
   - Action: Opens Facebook share dialog with link

**Secondary Button:**
```
View Product Page
```

---

### Micro-States: Share Link

| State | UI Change | Message | Duration |
|-------|-----------|---------|----------|
| **Link Copied** | Green checkmark on button | "Link copied! ✅ Paste it anywhere." | 2s auto-dismiss |
| **Share Success** | Green toast notification | "Shared successfully! 🎉" | 3s auto-dismiss |
| **Share Error** | Red alert | "Couldn't share. Try copying the link instead." | Persistent |

**Copy Button Animation:**
```
1. Click → Button text changes to "Copied! ✅"
2. Button turns green (200ms transition)
3. After 2s → Button returns to "Copy Link 📋"
```

---

## 4️⃣ PURCHASE FLOW

### Screen: Checkout

**Headline:**
```
Support a Caribbean creator 💙
```

**Subheadline:**
```
Secure checkout powered by Stripe. Your purchase helps creators thrive.
```

**Order Summary (Card):**
- Product Title
- Creator Name
- Price: **$9.99**
- Platform Fee: **$1.50**
- **Total: $11.49**

**Payment Form:**

1. **Email**
   - Label: "Email for receipt"
   - Placeholder: "you@example.com"

2. **Card Details** (Stripe Element)
   - Label: "Card Information"
   - Fields: Card number, Expiry, CVC

**Primary Button:**
```
Complete Purchase 💳
```

**Trust Badges (Below Button):**
- 🔒 Secure checkout
- ⚡ Instant delivery
- 💯 100% satisfaction

---

### Micro-States: Purchase Flow

| State | UI Change | Message | Duration |
|-------|-----------|---------|----------|
| **Processing Payment** | Spinner on button, disabled | "Processing your payment... 💳" | 2-5s |
| **Payment Success** | Green screen, confetti | "Success! Check your email for download link 🎉" | 3s then redirect |
| **Payment Failed** | Red alert banner | "Payment declined. Please check your card details and try again." | Persistent |
| **Network Error** | Red alert banner | "Connection error. Your card was not charged. Please try again." | Persistent |

**Success Animation:**
```
1. Green checkmark fades in (300ms)
2. Confetti burst from center (600ms)
3. Message: "Success! Downloading now..."
4. Auto-redirect to download page (2s)
```

---

## 5️⃣ PAYOUT FLOW

### Screen: Request Payout

**Headline:**
```
Your earnings are ready 💰
```

**Subheadline:**
```
Withdraw your earnings instantly. Payments processed within 24 hours.
```

**Earnings Summary (Card):**
- **Available Balance:** $247.50
- **Pending:** $32.00
- **Total Earned (All-Time):** $1,823.00

**Payout Form:**

1. **Payout Method**
   - Options: PayPal, Bank Transfer, Mobile Money
   
2. **Amount**
   - Label: "Amount to withdraw"
   - Placeholder: "$247.50"
   - Min: $10
   - Helper Text: "Minimum withdrawal: $10"

3. **PayPal Email** (if PayPal selected)
   - Label: "PayPal Email"
   - Placeholder: "your-paypal@example.com"

**Primary Button:**
```
Request Payout 🚀
```

**Secondary Link:**
```
View Payout History
```

---

### Micro-States: Payout Flow

| State | UI Change | Message | Duration |
|-------|-----------|---------|----------|
| **Below Minimum** | Red border on amount | "Minimum withdrawal is $10" | Persistent |
| **Processing Request** | Spinner on button, disabled | "Processing your request... 💰" | 1-3s |
| **Request Submitted** | Green notification | "Payout requested! Funds will arrive in 24-48 hours." | 5s auto-dismiss |
| **Error** | Red alert banner | "Request failed. Please check your details and try again." | Persistent |
| **Success** | Green confetti animation | "Payout on the way! Check your email for confirmation 🎉" | 3s auto-dismiss |

---

## 6️⃣ LEADERBOARD FLOW

### Screen: Creator Leaderboard

**Headline:**
```
Rise with the community 👑
```

**Subheadline:**
```
Top-earning creators this week. Keep creating to climb the ranks!
```

**Your Rank Card (Highlighted):**
```
🔥 You're Rank #47 this week!
Move up 3 spots to unlock "Rising Star" badge
```

**Leaderboard Table:**
- **Columns:** Rank | Creator | Earnings | Badges
- **Your Row:** Highlighted in gold border

**Filter Tabs:**
- This Week (default)
- This Month
- All-Time

**Micro-Label (Bottom):**
```
🔄 Leaderboard resets every Monday at midnight
```

---

### Micro-States: Leaderboard

| State | UI Change | Message | Duration |
|-------|-----------|---------|----------|
| **Rank-Up** | Row slides up, glow effect | Toast: "You just moved up! 🎉 Now #45" | 3s auto-dismiss |
| **Near Top 10** | Blue notification banner | "You're just 3 spots away from Top 10! Keep going 💪" | Persistent (dismissible) |
| **New Badge Unlocked** | Badge icon appears, scale animation | Modal: "Badge Unlocked! 🏆 Rising Star" | 5s auto-dismiss |
| **Weekly Reset** | Gray banner at top | "Leaderboard reset! New week, new opportunities 🔥" | Persistent for 24h |

**Rank-Up Animation:**
```
1. User's row slides upward (20px, 300ms ease-out)
2. Gold pulse glow behind row (400ms, loops 2x)
3. Toast notification slides from bottom center
4. Confetti burst (optional, 500ms)
```

---

## 📝 FORM VALIDATION MESSAGES

### General Errors
```
❌ This field is required
❌ Please enter a valid email address
❌ Passwords must be at least 8 characters
❌ Passwords don't match
❌ Please select an option
```

### Success Messages
```
✅ Saved successfully!
✅ Changes applied
✅ Email verified
✅ Payment received
✅ Account updated
```

### Loading States
```
⏳ Loading...
⏳ Saving changes...
⏳ Processing payment...
⏳ Uploading files...
⏳ Sending email...
```

---

## 🎨 EMPTY STATES

### No Products Yet
```
📦 No products yet

Ready to start earning? Upload your first product and share it with the world.

[Upload Product] button
```

### No Sales Yet
```
💰 No sales yet

Your products are live! Share your links to start making sales.

[Share Links] button
```

### No Notifications
```
🔔 All caught up!

You're up to date. We'll notify you when something new happens.
```

---

## 🔔 NOTIFICATION MESSAGES

### System Notifications

**Sale Made:**
```
🎉 You just made a sale!
Marcus bought "Caribbean Wedding Planner" for $9.99

[View Order] button
```

**New Follower:**
```
👥 New follower!
Sarah started following you. Keep creating!

[View Profile] link
```

**Badge Unlocked:**
```
🏆 Badge Unlocked!
You earned "Rising Star" for reaching 50 sales this month!

[View Badges] link
```

**Payout Processed:**
```
💰 Payout Complete!
$247.50 has been sent to your PayPal account.

[View Details] link
```

---

## ⚠️ ERROR MESSAGES

### Network Errors
```
⚠️ Connection Error

Couldn't reach the server. Check your internet and try again.

[Retry] button
```

### Server Errors
```
⚠️ Something went wrong

We're experiencing technical issues. Please try again in a few minutes.

[Go Back] button
```

### Permission Errors
```
🔒 Access Denied

You don't have permission to view this page.

[Go Home] button
```

---

## 💬 MICRO-COPY GLOSSARY

### Buttons
```
Primary CTAs: Create, Publish, Share, Buy, Withdraw, Continue
Secondary CTAs: Cancel, Go Back, Learn More, View Details
Destructive CTAs: Delete, Remove, Disconnect
```

### Helper Text
```
Encouraging: "You're almost there!", "Great choice!", "Looking good!"
Instructive: "Choose one option", "Enter a valid email", "Max 500 characters"
Reassuring: "Your data is secure", "We'll never share this", "100% refund policy"
```

### Progress Indicators
```
"1 of 3 steps", "Step 1: Basic Info", "75% complete", "Almost done!"
```

---

## 📊 ANALYTICS LABELS

### Event Names (for tracking)
```
sign_up_started
sign_up_completed
product_uploaded
product_published
link_copied
link_shared_[platform]
purchase_initiated
purchase_completed
payout_requested
leaderboard_viewed
badge_unlocked
```

---

## 🌐 LOCALIZATION NOTES

### Caribbean English Variants
- Use "you" not "yuh" (formal Caribbean English)
- Celebrate Caribbean culture without stereotypical language
- Include emoji strategically for energy (🔥, 🎉, 💰, 👑, 💙)

### Currency Formatting
- Always show USD: $9.99
- Show local currency option (future): $9.99 USD (≈ $27 TTD)

---

## ✅ COPY REVIEW CHECKLIST

Before publishing any copy:
- [ ] Is it clear and concise?
- [ ] Does it empower the user?
- [ ] Does it celebrate Caribbean culture?
- [ ] Are there any confusing terms?
- [ ] Is the tone friendly and encouraging?
- [ ] Are CTAs action-oriented?
- [ ] Are error messages helpful (not blaming)?
- [ ] Is grammar/spelling correct?

---

**Status:** 🟢 Ready for Implementation  
**Version:** 1.0.0  
**Last Updated:** December 23, 2025  

🔥 **Your Voice. Your Words. Your Sovereignty.** 👑
