import { Injectable, Logger } from '@nestjs/common';

/**
 * Message Generator Service
 * 
 * Generates personalized follow-up messages for different task types.
 * Uses templates and AI-powered content generation.
 * 
 * V0 Implementation:
 * - Template-based generation (no AI yet)
 * - Two message types: INVOICE_FOLLOW_UP, LEAD_FOLLOW_UP
 * - English only
 * - Email channel only
 * 
 * Future enhancements:
 * - AI-powered content generation (OpenAI, Anthropic)
 * - Multi-language support
 * - SMS/WhatsApp templates
 * - A/B testing variants
 */
@Injectable()
export class MessageGeneratorService {
  private readonly logger = new Logger(MessageGeneratorService.name);

  /**
   * Generate follow-up message based on task type and payload
   * 
   * @param taskType - Type of task (INVOICE_FOLLOW_UP, LEAD_FOLLOW_UP)
   * @param payload - Task payload containing entity details
   * @returns { subject, body_text, body_html, metadata }
   */
  async generateMessage(taskType: string, payload: any): Promise<{
    subject: string;
    body_text: string;
    body_html: string;
    metadata: any;
  }> {
    this.logger.log(`Generating ${taskType} message`);

    switch (taskType) {
      case 'INVOICE_FOLLOW_UP':
        return this.generateInvoiceFollowUp(payload);
      case 'LEAD_FOLLOW_UP':
        return this.generateLeadFollowUp(payload);
      default:
        throw new Error(`Unsupported task type: ${taskType}`);
    }
  }

  /**
   * Generate invoice follow-up email
   */
  private generateInvoiceFollowUp(payload: any): {
    subject: string;
    body_text: string;
    body_html: string;
    metadata: any;
  } {
    const {
      customer_name,
      invoice_number,
      invoice_amount,
      currency,
      days_overdue,
      invoice_url,
    } = payload;

    const subject = `Friendly Reminder: Invoice ${invoice_number} Past Due`;

    const body_text = `Dear ${customer_name},

I hope this message finds you well.

I'm reaching out regarding Invoice ${invoice_number} for ${currency} ${invoice_amount.toFixed(2)}, which is now ${days_overdue} day${days_overdue > 1 ? 's' : ''} past due.

We understand that oversights happen, and we want to make the payment process as easy as possible for you.

Invoice Details:
- Invoice Number: ${invoice_number}
- Amount Due: ${currency} ${invoice_amount.toFixed(2)}
- Days Overdue: ${days_overdue}
- View Invoice: ${invoice_url || '[Invoice URL]'}

If you've already sent payment, please disregard this message. If you have any questions about this invoice or need assistance, please don't hesitate to reach out.

We appreciate your business and look forward to continuing our partnership.

Best regards,
The Accounts Team`;

    const body_html = `
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
    .invoice-details { background-color: #e9ecef; padding: 15px; border-radius: 5px; margin: 20px 0; }
    .invoice-details ul { list-style: none; padding: 0; }
    .invoice-details li { padding: 5px 0; }
    .amount { font-weight: bold; color: #dc3545; font-size: 18px; }
    .cta-button { display: inline-block; background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
    .footer { margin-top: 30px; font-size: 12px; color: #6c757d; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h2>Payment Reminder</h2>
    </div>
    
    <p>Dear ${customer_name},</p>
    
    <p>I hope this message finds you well.</p>
    
    <p>I'm reaching out regarding <strong>Invoice ${invoice_number}</strong> for <span class="amount">${currency} ${invoice_amount.toFixed(2)}</span>, which is now <strong>${days_overdue} day${days_overdue > 1 ? 's' : ''} past due</strong>.</p>
    
    <p>We understand that oversights happen, and we want to make the payment process as easy as possible for you.</p>
    
    <div class="invoice-details">
      <h3>Invoice Details</h3>
      <ul>
        <li><strong>Invoice Number:</strong> ${invoice_number}</li>
        <li><strong>Amount Due:</strong> <span class="amount">${currency} ${invoice_amount.toFixed(2)}</span></li>
        <li><strong>Days Overdue:</strong> ${days_overdue}</li>
      </ul>
      ${invoice_url ? `<a href="${invoice_url}" class="cta-button">View Invoice</a>` : ''}
    </div>
    
    <p>If you've already sent payment, please disregard this message. If you have any questions about this invoice or need assistance, please don't hesitate to reach out.</p>
    
    <p>We appreciate your business and look forward to continuing our partnership.</p>
    
    <p>Best regards,<br>The Accounts Team</p>
    
    <div class="footer">
      <p>This is an automated message from our accounts receivable system.</p>
    </div>
  </div>
</body>
</html>`;

    return {
      subject,
      body_text,
      body_html,
      metadata: {
        template: 'invoice_follow_up_v1',
        tone: days_overdue > 30 ? 'firm' : 'friendly',
        days_overdue,
        amount: invoice_amount,
      },
    };
  }

  /**
   * Generate lead follow-up email
   */
  private generateLeadFollowUp(payload: any): {
    subject: string;
    body_text: string;
    body_html: string;
    metadata: any;
  } {
    const {
      lead_name,
      company,
      lead_stage,
      days_since_contact,
      notes,
    } = payload;

    // Customize subject and body based on stage
    let subject: string;
    let body_text: string;

    switch (lead_stage) {
      case 'CONTACTED':
        subject = `Following Up: ${company} Partnership Opportunity`;
        body_text = `Hi ${lead_name},

I wanted to follow up on our recent conversation about how we can support ${company}.

It's been ${days_since_contact} days since we last connected, and I'd love to continue our discussion about your needs and how we can help.

${notes ? `Previously discussed: ${notes}` : ''}

Would you have time this week for a quick call to explore next steps?

I'm excited about the potential to work together and help ${company} achieve its goals.

Looking forward to hearing from you!

Best regards`;
        break;

      case 'QUALIFIED':
        subject = `Checking In: Next Steps for ${company}`;
        body_text = `Hi ${lead_name},

I hope you're doing well!

I wanted to check in regarding our previous discussion about ${company}'s needs. It's been ${days_since_contact} days since we last spoke.

${notes ? `Context: ${notes}` : ''}

I understand timing and priorities can shift. If you're still interested in exploring how we can help, I'd love to schedule a brief call to discuss next steps.

Are you available this week for a 15-minute conversation?

Best regards`;
        break;

      case 'PROPOSAL_SENT':
        subject = `Following Up: Proposal for ${company}`;
        body_text = `Hi ${lead_name},

I wanted to follow up on the proposal we sent ${days_since_contact} days ago for ${company}.

${notes ? `Context: ${notes}` : ''}

I understand reviewing proposals takes time, and you may have questions or need clarification on any aspects.

Would you be open to a quick call this week to discuss:
- Any questions about the proposal
- Timeline and next steps
- How we can best support your decision-making process

I'm here to help make this process as smooth as possible for you.

Looking forward to your thoughts!

Best regards`;
        break;

      default:
        subject = `Reconnecting: ${company} Partnership`;
        body_text = `Hi ${lead_name},

I wanted to reach out as it's been ${days_since_contact} days since we last connected about ${company}.

${notes ? `Previously: ${notes}` : ''}

I'd love to reconnect and see if there's anything we can help with at this time.

Would you be open to a brief conversation this week?

Best regards`;
    }

    // Generate HTML version
    const body_html = `
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .greeting { font-size: 16px; margin-bottom: 15px; }
    .content { margin: 20px 0; }
    .cta { background-color: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
    .footer { margin-top: 30px; font-size: 12px; color: #6c757d; }
    .highlight { background-color: #fff3cd; padding: 2px 6px; border-radius: 3px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="greeting">
      ${body_text.split('\n\n')[0]}
    </div>
    <div class="content">
      ${body_text.split('\n\n').slice(1).map(p => `<p>${p.replace(/\n/g, '<br>')}</p>`).join('')}
    </div>
    <div class="footer">
      <p>This is an automated follow-up from our lead management system.</p>
    </div>
  </div>
</body>
</html>`;

    return {
      subject,
      body_text,
      body_html,
      metadata: {
        template: 'lead_follow_up_v1',
        stage: lead_stage,
        days_since_contact,
        tone: 'professional_friendly',
      },
    };
  }

  /**
   * Generate AI-powered message (placeholder for future enhancement)
   * 
   * Future: Call OpenAI/Anthropic API with:
   * - Task context
   * - Customer history
   * - Brand voice guidelines
   * - Generate personalized, contextual message
   */
  private async generateAIPoweredMessage(
    taskType: string,
    payload: any,
  ): Promise<{ subject: string; body_text: string; body_html: string; metadata: any }> {
    // TODO: Implement AI generation
    // const completion = await this.openai.chat.completions.create({
    //   model: 'gpt-4',
    //   messages: [{
    //     role: 'system',
    //     content: 'You are a professional business communication assistant...'
    //   }, {
    //     role: 'user',
    //     content: JSON.stringify(payload)
    //   }]
    // });

    this.logger.warn('AI generation not yet implemented, falling back to templates');
    return this.generateMessage(taskType, payload);
  }
}
