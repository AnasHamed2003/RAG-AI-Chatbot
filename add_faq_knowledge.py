#!/usr/bin/env python3
import requests
import re
import time

def parse_faq_content(content):
    """Parse FAQ markdown content and extract question-answer pairs."""
    qa_pairs = []

    # Split content into sections
    sections = re.split(r'^##\s+', content, flags=re.MULTILINE)[1:]

    for section in sections:
        lines = section.strip().split('\n')
        if not lines:
            continue

        # First line is section title
        section_title = lines[0].strip()

        # Process remaining lines for Q&A pairs
        i = 1
        while i < len(lines):
            line = lines[i].strip()

            # Look for questions (start with ###)
            if line.startswith('###'):
                question = line.replace('###', '').strip()

                # Collect answer until next question or end
                answer_lines = []
                i += 1

                while i < len(lines):
                    next_line = lines[i].strip()
                    if next_line.startswith('###') or (next_line.startswith('##') and not next_line.startswith('###')):
                        break

                    if next_line:  # Skip empty lines in answer collection
                        answer_lines.append(next_line)
                    i += 1

                answer = '\n'.join(answer_lines).strip()

                if question and answer:
                    qa_pairs.append({
                        'question': question,
                        'answer': answer,
                        'category': section_title.lower().replace(' ', '_').replace('&', 'and')
                    })

            else:
                i += 1

    return qa_pairs

def add_qa_to_knowledge_base(question, answer, category, base_url="http://localhost:8000"):
    """Add a single Q&A pair to the knowledge base."""
    try:
        # Combine question and answer for better context
        knowledge_text = f"Question: {question}\n\nAnswer: {answer}"

        response = requests.post(f"{base_url}/add-knowledge", json={
            "text": knowledge_text,
            "source": "swiftfixpro_faq",
            "category": f"faq_{category}"
        })

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Added: {question[:50]}...")
            print(f"   Chunks created: {result.get('chunks_added', 0)}")
            return True
        else:
            print(f"❌ Failed to add: {question[:50]}...")
            print(f"   Status: {response.status_code}, Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error adding Q&A: {str(e)}")
        return False

def main():
    # FAQ content from the attachment
    faq_content = """# SwiftFixPro FAQ Knowledge Base

## General Services

### What is SwiftFixPro?

SwiftFixPro is Singapore's premier property maintenance and repair service platform. We connect property owners with verified, trusted service providers for all types of home and commercial property maintenance needs, from plumbing and electrical work to aircon servicing and renovation projects.

### Which areas in Singapore do you serve?

We provide services across all areas of Singapore including Central Singapore, Ang Mo Kio, Bedok, Bishan, Bukit Batok, Bukit Merah, Bukit Panjang, Bukit Timah, Choa Chu Kang, Clementi, Geylang, Hougang, Jurong East, Jurong West, Kallang, Marine Parade, Novena, Pasir Ris, Punggol, Queenstown, Sembawang, Sengkang, Serangoon, Tampines, Toa Payoh, Woodlands, and Yishun.

### How do I book a service?

Booking is simple! Create an account, browse our services, select what you need, choose a time slot that works for you, and confirm your booking. You'll receive instant confirmation and can track your service provider in real-time.

### Do you provide service guarantees?

Yes! We offer a comprehensive service guarantee. All our service providers are vetted and insured. If you're not satisfied with the work, we'll make it right with free re-service or full refund within 30 days.

### Do you provide emergency services?

Absolutely! We offer 24/7 emergency services for urgent issues like water leaks, electrical problems, aircon breakdowns, and security concerns. Emergency services are available with premium rates and faster response times.

### How transparent is your pricing?

We believe in complete pricing transparency. You'll see upfront costs before booking, with no hidden fees. Our service providers provide detailed quotes, and you only pay after satisfactory completion of work.

## Account & Registration

### How do I create an account?

Creating an account is easy! Click "Register" and choose between Customer or Agent registration. Fill in your personal details, contact information, and create a secure password. For customers, you can also enter a referral code if you have one.

### What are the different account types?

We offer two main account types: Customer accounts for property owners who need services, and Agent accounts for property agents who want to refer clients and earn commissions. Each account type has specific features tailored to your needs.

### What if I forget my password?

No worries! Click "Forgot Password" on the login page, enter your email address, and we'll send you a secure reset link. Follow the instructions in the email to create a new password.

### Can I update my profile information?

Yes, you can update your profile anytime through your dashboard. Go to Account Settings to modify your personal information, contact details, and preferences. Some changes may require verification for security purposes.

### How secure is my account?

Your account security is our priority. We use industry-standard encryption, secure authentication, and optional two-factor authentication. Your payment information is never stored and all transactions are processed through secure, PCI-compliant payment gateways.

### How to delete my account?

You can delete your account from the profile page

## Agent Referral Program

### What is the Agent Referral Program?

Our Agent Referral Program allows property agents to earn 15% commission on every successful client referral. It's designed specifically for licensed property agents who want to provide additional value to their clients while earning extra income.

### Who can become a referral agent?

Only licensed property agents registered with the Council for Estate Agencies (CEA) in Singapore are eligible. You must provide a valid CEA registration number during registration, which we verify through the CEA Public Register.

### Why do I need a CEA registration?

CEA registration ensures that only legitimate, licensed property professionals participate in our program. This maintains the integrity of our referral network and complies with Singapore's property industry regulations.

### How does the commission structure work?

Agents earn 15% commission on the total service value of successful referrals. Commissions are calculated after service completion and customer payment. We also offer a tier progression system from Bronze to Platinum based on performance.

### When and how do I get paid?

Commissions are paid monthly via bank transfer. You can track your earnings in real-time through your agent dashboard, which shows pending commissions, completed payments, and detailed referral history.

### How are referrals tracked?

Each agent receives a unique referral code. When clients use your code during registration or booking, the referral is automatically tracked in our system. You can monitor all your referrals and their status in your dashboard.

## CEA Verification Process

### How does CEA verification work?

After you register with your CEA number, our admin team manually verifies your registration through the CEA Public Register. This process typically takes 1-3 business days. You'll receive an email notification once verification is complete.

### What format should my CEA registration number be in?

CEA registration numbers typically follow formats like R123456A or RB123456. Enter your number exactly as it appears on your CEA license. Our system will automatically format it to uppercase for consistency.

### What can I do while verification is pending?

While your CEA verification is pending, you can complete your profile setup and familiarize yourself with the agent dashboard. However, you won't be able to generate referral codes or earn commissions until verification is approved.

### What if my CEA verification is rejected?

If verification fails, you'll receive an email with the specific reason. Common issues include expired licenses, incorrect registration numbers, or name mismatches. You can update your information and request re-verification.

### What happens when my CEA license expires?

We monitor CEA license expiry dates. Before your license expires, you'll receive renewal reminders. Once expired, your agent status will be temporarily suspended until you provide updated license information.

### Why is verification done manually?

CEA doesn't provide a public API for automated verification. Our admin team manually checks each registration against the official CEA Public Register to ensure accuracy and prevent fraud.

## Privacy & Cookies

### How do you use cookies?

We use cookies to enhance your experience with features like remembering your login, saving form progress, and providing personalized content. We categorize cookies into Essential, Preferences, Analytics, and Marketing, giving you full control over your choices.

### Can I control cookie settings?

Absolutely! You have full control over cookie preferences. You can accept all, reject non-essential cookies, or customize which categories you want to allow. You can change these settings anytime through the cookie banner or privacy settings.

### What personal data do you collect?

We collect only necessary information: contact details for service delivery, payment information for transactions, and usage data to improve our services. For agents, we also collect CEA registration details for verification purposes.

### How is my data protected?

We use industry-standard security measures including encryption, secure servers, and regular security audits. Your payment information is processed through PCI-compliant gateways and never stored on our servers.

### Do you share my data with third parties?

We only share data when necessary for service delivery (e.g., with service providers for job completion) or as required by law. We never sell your personal information to third parties for marketing purposes.

### What are my privacy rights?

You have the right to access, correct, delete, or export your personal data. You can also object to processing or request data portability. Contact our privacy team to exercise these rights or if you have privacy concerns.

## Payments & Billing

### What payment methods do you accept?

All payments are processed securely through HitPay. HitPay supports credit/debit cards (Visa, MasterCard, American Express), PayNow, online banking, and digital wallets. All transactions are encrypted and PCI-compliant for your security.

### When do I pay for services?

Payment is due after service completion and your satisfaction confirmation. You'll receive a detailed invoice via email and can pay through your dashboard or the payment link provided.

### What is your refund policy?

We offer full refunds for cancelled bookings (with appropriate notice) and unsatisfactory services. If you're not satisfied with the work, we'll first attempt to resolve the issue with free re-service. If that's not possible, we provide full refunds within 30 days.

### Can I get invoices and receipts?

Yes! You'll automatically receive detailed invoices and receipts via email for all transactions. You can also download them from your dashboard anytime. All invoices include GST where applicable.

### How secure are my payments?

Payment security is our top priority. We use 256-bit SSL encryption, PCI DSS compliant processors, and never store your payment information. All transactions are monitored for fraud protection.

## Technical Support

### What are the system requirements?

Our platform works on all modern browsers (Chrome, Firefox, Safari, Edge) on desktop, tablet, and mobile devices. For the best experience, ensure your browser is updated to the latest version and JavaScript is enabled.

### Do you have a mobile app?

Currently, we offer a responsive web platform that works perfectly on mobile browsers. A dedicated mobile app is in development and will be available soon for both iOS and Android devices.

### I'm experiencing technical issues. What should I do?

First, try refreshing the page or clearing your browser cache. If issues persist, try using a different browser or incognito mode. For ongoing problems, contact our technical support team with details about your device and browser.

### I can't access my account. What should I do?

Check if you're using the correct email and password. Try the "Forgot Password" option if needed. Clear your browser cache and cookies, or try accessing from a different device. If problems continue, contact our support team.

### Can I suggest new features?

Absolutely! We value user feedback and continuously improve our platform. You can submit feature requests through the feedback form in your dashboard or contact our support team with your suggestions.

## Contact & Support

### How can I contact customer support?

You can reach us through multiple channels: 24/7 live chat on our website, email at support@swiftfixpro.sg, phone at +65 6XXX XXXX, or through the contact form in your dashboard. We typically respond within 2 hours during business hours.

### What are your support hours?

Our customer support team is available 24/7 for emergencies. For general inquiries, our main support hours are Monday to Friday, 8 AM to 8 PM, and weekends 9 AM to 6 PM Singapore time.

### How do I reach you in an emergency?

For urgent property emergencies (water leaks, electrical issues, security concerns), call our 24/7 emergency hotline at +65 6XXX XXXX or use the "Emergency Service" button in your dashboard for immediate assistance.

### How do I provide feedback or file a complaint?

We welcome all feedback! You can provide feedback through your dashboard after each service, email us at feedback@swiftfixpro.sg, or use the feedback form on our website. For complaints, we have a dedicated resolution process to address your concerns quickly.

### I have a business inquiry. Who should I contact?

For business partnerships, bulk service contracts, or corporate accounts, contact our business development team at business@swiftfixpro.sg or call +65 6XXX XXXX extension 2. We offer special rates for property management companies and large-scale projects."""

    print("🚀 Adding SwiftFixPro FAQ to Knowledge Base")
    print("=" * 50)

    # Parse the FAQ content
    qa_pairs = parse_faq_content(faq_content)

    print(f"📋 Found {len(qa_pairs)} question-answer pairs to add")
    print()

    # Add each Q&A pair to the knowledge base
    successful_additions = 0
    failed_additions = 0

    for i, qa_pair in enumerate(qa_pairs, 1):
        print(f"[{i}/{len(qa_pairs)}] Processing: {qa_pair['category']}")

        success = add_qa_to_knowledge_base(
            qa_pair['question'],
            qa_pair['answer'],
            qa_pair['category']
        )

        if success:
            successful_additions += 1
        else:
            failed_additions += 1

        # Small delay to avoid overwhelming the API
        time.sleep(0.5)

    print()
    print("📊 Summary:")
    print(f"✅ Successfully added: {successful_additions} Q&A pairs")
    print(f"❌ Failed to add: {failed_additions} Q&A pairs")
    print(f"📚 Total knowledge base entries: {len(qa_pairs)}")

    if successful_additions > 0:
        print()
        print("🎉 FAQ knowledge base has been successfully added!")
        print("Your chatbot can now answer questions about SwiftFixPro services.")
        print()
        print("Test it with questions like:")
        print("- What is SwiftFixPro?")
        print("- Do you provide emergency services?")
        print("- How do I book a service?")
        print("- What payment methods do you accept?")

if __name__ == "__main__":
    main()