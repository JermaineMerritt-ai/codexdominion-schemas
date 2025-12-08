"""
Customer Setup Assistant Avatar
AI-powered guide for Codex Dominion customers setting up their accounts
"""

class CustomerSetupAvatar:
    """Friendly AI assistant for customer onboarding"""

    def __init__(self, customer_name: str):
        self.customer_name = customer_name
        self.onboarding_progress = {
            "account_created": False,
            "profile_completed": False,
            "first_purchase": False,
            "subscription_active": False,
            "downloads_accessed": False
        }

    def greet(self):
        """Personalized welcome message"""
        return f"""
🌟 Welcome to Codex Dominion, {self.customer_name}!

I'm your personal setup assistant. I'm here to help you:
✓ Set up your account
✓ Find the perfect products for your needs
✓ Access your digital downloads
✓ Get the most from your subscription

What would you like help with first?
1. Browse our Christian printables
2. Set up a subscription (save 30%!)
3. Download your free lead magnet
4. Learn about our product categories
        """

    def guide_subscription_setup(self, interests: list):
        """Guide customer through subscription selection"""
        recommendations = []

        if "homeschool" in interests:
            recommendations.append({
                "plan": "Homeschool Monthly ($19.99)",
                "benefits": [
                    "Access to 50+ curriculum printables",
                    "Monthly new lesson plans",
                    "Bible-based learning activities",
                    "Save $15/month vs buying individually"
                ],
                "best_for": "Families homeschooling 2+ children"
            })

        if "kids" in interests or "children" in interests:
            recommendations.append({
                "plan": "Kids Bible Monthly ($9.99)",
                "benefits": [
                    "Weekly coloring pages with scripture",
                    "Bible story activities",
                    "Memory verse cards",
                    "Early access to new designs"
                ],
                "best_for": "Parents with children ages 3-12"
            })

        if "wedding" in interests:
            recommendations.append({
                "plan": "Wedding Planning Monthly ($14.99)",
                "benefits": [
                    "Complete wedding planning checklist",
                    "Invitation templates",
                    "Program & place card designs",
                    "Scripture selection guide"
                ],
                "best_for": "Engaged couples planning a Christian wedding"
            })

        message = f"Based on your interests ({', '.join(interests)}), here are my recommendations:\n\n"

        for i, rec in enumerate(recommendations, 1):
            message += f"{i}. {rec['plan']}\n"
            message += f"   Best for: {rec['best_for']}\n"
            message += "   Benefits:\n"
            for benefit in rec['benefits']:
                message += f"   • {benefit}\n"
            message += "\n"

        message += "💡 Tip: All subscriptions include access to our entire archive!\n"
        message += "🎁 First month free with code WELCOME2025"

        return message

    def explain_downloads(self):
        """Explain how to access digital products"""
        return """
📥 How to Access Your Downloads:

1. Complete Purchase
   → You'll receive an order confirmation email immediately

2. Check Your Email
   → Download links are in the "Your Order" email
   → Links are valid for 30 days

3. Access from Account
   → Log in at codexdominion.app
   → Go to "My Account" → "Downloads"
   → All purchases are stored here forever

4. Download Tips
   • Files are in PDF format (print-ready)
   • Save to your device for offline access
   • Print unlimited copies for personal use
   • Need help? Email support@codexdominion.app

🎨 After downloading:
   • Open in Adobe Reader or Preview
   • Print on cardstock for best results
   • Use standard letter (8.5" x 11") or A4 paper
        """

    def suggest_products(self, category: str, budget: float):
        """Suggest products based on category and budget"""
        suggestions = {
            "kids": [
                {"name": "30 Days of Bible Stories Coloring Pack", "price": 12.99},
                {"name": "Memory Verse Challenge Cards", "price": 8.99},
                {"name": "Bible Heroes Activity Bundle", "price": 15.99}
            ],
            "homeschool": [
                {"name": "Genesis Study Workbook", "price": 19.99},
                {"name": "Christian Character Building Activities", "price": 14.99},
                {"name": "Bible Timeline Poster Set", "price": 9.99}
            ],
            "wedding": [
                {"name": "Christian Wedding Planning Checklist", "price": 14.99},
                {"name": "Rustic Wedding Invitation Suite", "price": 12.99},
                {"name": "Wedding Program Templates Pack", "price": 8.99}
            ]
        }

        products = suggestions.get(category.lower(), [])
        affordable = [p for p in products if p["price"] <= budget]

        if not affordable:
            return f"I don't have many options under ${budget:.2f} in {category}. Consider our subscription for better value!"

        message = f"Here are {category} products within your ${budget:.2f} budget:\n\n"
        for p in affordable:
            message += f"• {p['name']} - ${p['price']}\n"

        total = sum(p["price"] for p in affordable)
        if total > budget * 1.2:  # If buying all is expensive
            message += f"\n💡 Save money! Our subscription includes all of these for just $9.99-19.99/month"

        return message

    def troubleshoot_download(self, issue: str):
        """Help customer with download issues"""
        solutions = {
            "link_expired": """
Your download link has expired. Here's how to get a new one:

1. Log in to your account at codexdominion.app
2. Go to "My Account" → "Downloads"
3. Click the "Download" button next to your order
4. If you still have issues, email support@codexdominion.app with your order number

🔒 Links expire after 30 days for security, but you can always re-download from your account!
            """,
            "wont_open": """
If your PDF won't open, try these steps:

1. Make sure you have a PDF reader installed:
   • Mac: Preview (built-in)
   • Windows: Adobe Acrobat Reader (free)
   • Chrome/Edge: Opens PDFs natively

2. Re-download the file
   • Sometimes downloads get corrupted
   • Try a different browser

3. Check file size
   • Should be 1-5 MB typically
   • If it's only a few KB, it didn't download fully

Still stuck? Email us the error message: support@codexdominion.app
            """,
            "print_issues": """
Having trouble printing? Here's what to check:

✓ Paper Size: Set to Letter (8.5" x 11") or A4
✓ Scale: Choose "Actual Size" not "Fit to Page"
✓ Quality: Select "High Quality" or "Best"
✓ Color: Use color printer for best results (or print B&W on cardstock)

🎨 Pro tip: Print on 110lb cardstock from any office supply store for professional results!
            """
        }

        return solutions.get(issue, "I'm not sure about that issue. Email support@codexdominion.app for personalized help!")

    def get_started_checklist(self):
        """Provide getting started checklist"""
        return """
✅ Your Codex Dominion Getting Started Checklist:

☐ 1. Complete Your Profile (2 min)
     → Add name, interests, favorite categories
     → Get personalized recommendations

☐ 2. Download Your Free Lead Magnet (5 min)
     → Choose from 4 free printables
     → No credit card required
     → Instant access

☐ 3. Browse Our 6 Categories
     • Kids Bible Stories
     • Homeschool Resources
     • Wedding Planning
     • Memory Verse Cards
     • Seasonal Printables
     • Digital Downloads

☐ 4. Consider a Subscription (Save 30%!)
     → Kids: $9.99/month
     → Homeschool: $19.99/month
     → Wedding: $14.99/month
     → Access to EVERYTHING in your category

☐ 5. Join Our Community
     → Follow on Instagram @codexdominion
     → Get exclusive freebies & early access
     → Share your creations with #CodexDominion

💌 Questions? I'm here to help! Or email support@codexdominion.app
        """

    def explain_subscription_benefits(self, plan: str):
        """Detailed explanation of subscription benefits"""
        plans = {
            "kids": {
                "name": "Kids Bible Monthly",
                "price": "$9.99/month",
                "savings": "Save $40/month vs buying individually",
                "includes": [
                    "🎨 Unlimited coloring pages (50+ designs)",
                    "📖 Weekly Bible story activities",
                    "💭 Memory verse challenge cards",
                    "🌟 New designs every week",
                    "⚡ Early access to seasonal content",
                    "👨‍👩‍👧‍👦 Family license (print for all your kids)"
                ],
                "best_for": "Families with children ages 3-12"
            },
            "homeschool": {
                "name": "Homeschool Master Pack",
                "price": "$19.99/month",
                "savings": "Save $60/month vs buying individually",
                "includes": [
                    "📚 Complete curriculum printables (200+ pages)",
                    "✏️ Monthly lesson plans",
                    "🔬 Science & history activities",
                    "📖 Bible integration guides",
                    "🎓 Progress trackers & certificates",
                    "👪 Unlimited student license"
                ],
                "best_for": "Homeschooling families (K-8th grade)"
            },
            "wedding": {
                "name": "Wedding Planning Monthly",
                "price": "$14.99/month",
                "savings": "Save $100+ on your wedding",
                "includes": [
                    "📋 Complete planning checklist",
                    "💌 Invitation templates (10+ styles)",
                    "📜 Program & place card designs",
                    "📸 Photo booth props",
                    "🙏 Scripture selection guide",
                    "✨ DIY decoration templates"
                ],
                "best_for": "Engaged couples (6-18 months before wedding)"
            }
        }

        plan_info = plans.get(plan.lower(), None)
        if not plan_info:
            return "I don't have info on that plan. Try 'kids', 'homeschool', or 'wedding'."

        message = f"""
📦 {plan_info['name']} - {plan_info['price']}

💰 {plan_info['savings']}

What's Included:
"""
        for item in plan_info['includes']:
            message += f"   {item}\n"

        message += f"\n👥 Best for: {plan_info['best_for']}\n"
        message += "\n🎁 Special Offer: First month FREE with code WELCOME2025"
        message += "\n❌ Cancel anytime, no questions asked"
        message += "\n💳 Secure payment via Stripe"

        return message


# Example usage
if __name__ == "__main__":
    # Simulate customer interaction
    avatar = CustomerSetupAvatar("Sarah")

    print(avatar.greet())
    print("\n" + "="*60 + "\n")

    print(avatar.guide_subscription_setup(["homeschool", "kids"]))
    print("\n" + "="*60 + "\n")

    print(avatar.explain_subscription_benefits("homeschool"))
    print("\n" + "="*60 + "\n")

    print(avatar.get_started_checklist())
