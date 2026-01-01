import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_EMAIL = os.getenv("FROM_EMAIL", "empire@codexdominion.app")


def send_approval_email(to_email: str, context: Dict[str, any]):
    """
    Sends Empire Store Ignition approval email to client.
    
    Args:
        to_email: Client email address
        context: Dict with keys:
            - contact_name
            - brand_name
            - platform_choice
            - target_countries
            - default_currency
            - initial_products
            - estimated_days
    """
    contact_name = context.get("contact_name", "there")
    brand_name = context.get("brand_name", "your brand")
    platform_choice = context.get("platform_choice", "Shopify")
    target_countries = ", ".join(context.get("target_countries", ["US"]))
    default_currency = context.get("default_currency", "USD")
    initial_products = context.get("initial_products", 5)
    estimated_days = context.get("estimated_days", 7)
    
    subject = f"Your Empire Store Ignition is approved – we're building {brand_name}"
    
    body = f"""Hi {contact_name},

Good news — your Empire Store Ignition application for {brand_name} has been approved.

Here's what happens next:

1) We're creating your store foundation
- Platform: {platform_choice} (based on your intake and goals)
- Markets: {target_countries}
- Currency: {default_currency}

2) We're generating your initial product catalog
Using the details you shared about your products and audience, CodexDominion will generate:
- Product names and descriptions
- Pricing suggestions and tags
- A starting set of {initial_products} products

3) We're building your launch-ready site
Your brand story and offers will be turned into:
- A marketing site
- A launch page for your store
- Basic SEO so people can actually find you

4) We're preparing your launch campaign
Once the store and site are ready, we'll generate:
- Social launch posts
- An email sequence outline
- A hero video script

You'll be able to review everything before it goes live.

Timeline
- We expect your initial store foundation to be ready in: {estimated_days} days.
- You'll receive another email as soon as the core setup is complete.

If you have any questions or need to share additional details, just reply to this email.

We're honored to help you bring {brand_name} into the world with real structure.

— Empire Store Ignition
Powered by CodexDominion
"""
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    
    text_part = MIMEText(body, "plain")
    msg.attach(text_part)
    
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        
        print(f"✅ Approval email sent to {to_email}")
        return {"status": "success", "to": to_email}
        
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return {"status": "error", "message": str(e)}


def send_completion_email(to_email: str, context: Dict[str, any]):
    """
    Sends store creation completion email to client.
    
    Args:
        to_email: Client email address
        context: Dict with keys:
            - contact_name
            - brand_name
            - storefront_url
            - admin_url
            - marketing_site_url
            - products_created
    """
    contact_name = context.get("contact_name", "there")
    brand_name = context.get("brand_name", "your brand")
    storefront_url = context.get("storefront_url", "#")
    admin_url = context.get("admin_url", "#")
    marketing_site_url = context.get("marketing_site_url", "#")
    products_created = context.get("products_created", 0)
    
    subject = f"{brand_name} is ready – your store is live"
    
    body = f"""Hi {contact_name},

Your {brand_name} store foundation is complete and ready for your review.

Here's what we built:

🏪 Your Store
- Storefront: {storefront_url}
- Admin panel: {admin_url}
- Products created: {products_created}

🌐 Your Marketing Site
- Launch site: {marketing_site_url}

📢 Next: Launch Campaign
We're now generating your cross-channel launch campaign (social posts, email sequence, video script). You'll receive another email when it's ready for review.

Action needed:
1. Log into your store admin and review the products
2. Check your marketing site and brand story
3. Let us know if you need any adjustments before launch

We're excited to see {brand_name} step into the world.

— Empire Store Ignition
Powered by CodexDominion
"""
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    
    text_part = MIMEText(body, "plain")
    msg.attach(text_part)
    
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        
        print(f"✅ Completion email sent to {to_email}")
        return {"status": "success", "to": to_email}
        
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return {"status": "error", "message": str(e)}
