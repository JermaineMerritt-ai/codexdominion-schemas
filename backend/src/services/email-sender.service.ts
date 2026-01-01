import { Injectable, Logger } from '@nestjs/common';
import * as nodemailer from 'nodemailer';
import type { Transporter } from 'nodemailer';

/**
 * Email Sender Service
 * 
 * Handles actual email sending via SMTP.
 * Uses nodemailer for reliable email delivery.
 * 
 * V0 Implementation:
 * - SMTP transport (Gmail, SendGrid, AWS SES, etc.)
 * - Basic error handling and retry logic
 * - Email delivery tracking
 * 
 * Configuration via environment variables:
 * - SMTP_HOST
 * - SMTP_PORT
 * - SMTP_USER
 * - SMTP_PASS
 * - SMTP_FROM_EMAIL
 * - SMTP_FROM_NAME
 */
@Injectable()
export class EmailSenderService {
  private readonly logger = new Logger(EmailSenderService.name);
  private transporter: Transporter | null;

  constructor() {
    this.initializeTransporter();
  }

  /**
   * Initialize SMTP transporter with configuration
   */
  private initializeTransporter() {
    const smtpConfig = {
      host: process.env.SMTP_HOST || 'smtp.gmail.com',
      port: parseInt(process.env.SMTP_PORT || '587', 10),
      secure: false, // true for 465, false for other ports
      auth: {
        user: process.env.SMTP_USER || '',
        pass: process.env.SMTP_PASS || '',
      },
    };

    // V0: If SMTP not configured, use test mode (log emails instead of sending)
    if (!process.env.SMTP_USER || !process.env.SMTP_PASS) {
      this.logger.warn(
        'SMTP not configured. Emails will be logged but not sent. ' +
        'Set SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS to enable real sending.',
      );
      this.transporter = null;
    } else {
      try {
        this.transporter = nodemailer.createTransport(smtpConfig);
        this.logger.log(`SMTP transporter initialized: ${smtpConfig.host}:${smtpConfig.port}`);
      } catch (error) {
        this.logger.error('Failed to initialize SMTP transporter:', error.message);
        this.transporter = null;
      }
    }
  }

  /**
   * Send email
   * 
   * @param to - Recipient email address
   * @param subject - Email subject
   * @param bodyText - Email body (plain text)
   * @param bodyHtml - Email body (HTML)
   * @param options - Additional options (cc, bcc, replyTo, etc.)
   * @returns { success: boolean, messageId?: string, error?: string }
   */
  async sendEmail(
    to: string,
    subject: string,
    bodyText: string,
    bodyHtml?: string,
    options?: {
      cc?: string[];
      bcc?: string[];
      replyTo?: string;
    },
  ): Promise<{ success: boolean; messageId?: string; error?: string }> {
    this.logger.log(`Sending email to ${to}: ${subject}`);

    // V0: If no transporter (SMTP not configured), simulate sending
    if (!this.transporter) {
      this.logger.log('TEST MODE - Email content:');
      this.logger.log(`To: ${to}`);
      this.logger.log(`Subject: ${subject}`);
      this.logger.log(`Body (text):\n${bodyText}`);
      if (bodyHtml) {
        this.logger.log(`Body (HTML): ${bodyHtml.substring(0, 100)}...`);
      }
      
      return {
        success: true,
        messageId: `test-${Date.now()}`,
      };
    }

    try {
      const mailOptions = {
        from: `${process.env.SMTP_FROM_NAME || 'Action AI'} <${process.env.SMTP_FROM_EMAIL || process.env.SMTP_USER}>`,
        to,
        subject,
        text: bodyText,
        html: bodyHtml || this.convertToHTML(bodyText),
        cc: options?.cc,
        bcc: options?.bcc,
        replyTo: options?.replyTo,
      };

      const info = await this.transporter.sendMail(mailOptions);

      this.logger.log(`Email sent successfully: ${info.messageId}`);

      return {
        success: true,
        messageId: info.messageId,
      };
    } catch (error) {
      this.logger.error(`Failed to send email to ${to}:`, error.message);

      return {
        success: false,
        error: error.message,
      };
    }
  }

  /**
   * Send email with retry logic
   * 
   * @param to - Recipient email
   * @param subject - Email subject
   * @param bodyText - Email body (plain text)
   * @param bodyHtml - Email body (HTML)
   * @param maxRetries - Maximum retry attempts (default: 3)
   * @returns { success: boolean, messageId?: string, error?: string }
   */
  async sendEmailWithRetry(
    to: string,
    subject: string,
    bodyText: string,
    bodyHtml?: string,
    maxRetries = 3,
  ): Promise<{ success: boolean; messageId?: string; error?: string }> {
    let lastError: string = 'Unknown error';

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      this.logger.log(`Email send attempt ${attempt}/${maxRetries} to ${to}`);

      const result = await this.sendEmail(to, subject, bodyText, bodyHtml);

      if (result.success) {
        return result;
      }

      lastError = result.error || 'Unknown error';

      // Wait before retry (exponential backoff)
      if (attempt < maxRetries) {
        const delay = Math.pow(2, attempt) * 1000; // 2s, 4s, 8s
        this.logger.log(`Retrying in ${delay}ms...`);
        await this.sleep(delay);
      }
    }

    return {
      success: false,
      error: `Failed after ${maxRetries} attempts: ${lastError}`,
    };
  }

  /**
   * Convert plain text to HTML (basic formatting)
   */
  private convertToHTML(text: string): string {
    return text
      .split('\n\n')
      .map((paragraph) => `<p>${paragraph.replace(/\n/g, '<br>')}</p>`)
      .join('');
  }

  /**
   * Verify SMTP connection
   */
  async verifyConnection(): Promise<boolean> {
    if (!this.transporter) {
      this.logger.warn('SMTP not configured, skipping verification');
      return false;
    }

    try {
      await this.transporter.verify();
      this.logger.log('SMTP connection verified successfully');
      return true;
    } catch (error) {
      this.logger.error('SMTP connection verification failed:', error.message);
      return false;
    }
  }

  /**
   * Sleep utility for retry delays
   */
  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}
