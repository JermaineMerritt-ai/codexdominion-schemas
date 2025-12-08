import nodemailer from 'nodemailer';

export const email = {
  async send({ to, subject, html }: { to: string[]; subject: string; html: string }) {
    if (to.length === 0) return;
    const transporter = nodemailer.createTransport({
      host: 'smtp.sendgrid.net', port: 587, secure: false,
      auth: { user: 'apikey', pass: process.env.SENDGRID_API_KEY! }
    });
    await transporter.sendMail({ from: process.env.EMAIL_FROM!, to, subject, html });
  }
};
