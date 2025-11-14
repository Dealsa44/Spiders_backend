import nodemailer from 'nodemailer';
import dotenv from 'dotenv';

dotenv.config();

// Create transporter for Gmail
const createTransporter = () => {
  return nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: process.env.GMAIL_USER,
      pass: process.env.GMAIL_APP_PASSWORD // Use App Password, not regular password
    }
  });
};

// Format email content for user (confirmation email)
const formatUserEmail = (data) => {
  return {
    subject: 'Thank You for Contacting Intrinsic Spiders',
    html: `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <style>
          body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
          }
          .container {
            background: #ffffff;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
          }
          .header {
            text-align: center;
            margin-bottom: 30px;
          }
          .logo {
            font-size: 24px;
            font-weight: 900;
            color: #8B5CF6;
            margin-bottom: 10px;
          }
          h1 {
            color: #0A0A0A;
            font-size: 28px;
            margin: 0 0 10px 0;
          }
          .subtitle {
            color: #666;
            font-size: 16px;
          }
          .content {
            margin: 30px 0;
          }
          .message-box {
            background: #f8f9fa;
            border-left: 4px solid #8B5CF6;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
          }
          .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            text-align: center;
            color: #666;
            font-size: 14px;
          }
          .highlight {
            color: #8B5CF6;
            font-weight: 600;
          }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <div class="logo">INTRINSIC SPIDERS</div>
            <h1>Thank You, ${data.userName}!</h1>
            <p class="subtitle">We've received your message and will get back to you within 24 hours.</p>
          </div>
          
          <div class="content">
            <p>Hello ${data.userName},</p>
            
            <p>Thank you for reaching out to Intrinsic Spiders. We're excited about the possibility of working together to bring your vision to life!</p>
            
            ${data.bookingInfo ? `
            <div class="message-box">
              <strong>📅 Your Consultation Booking:</strong><br>
              ${data.bookingInfo.replace(/\n/g, '<br>')}
            </div>
            ` : ''}
            
            <p>Our team is already reviewing your message and will respond to you at <span class="highlight">${data.userEmail}</span> within 24 hours.</p>
            
            <p>In the meantime, feel free to reach out to us directly:</p>
            <ul>
              <li><strong>WhatsApp:</strong> +34 632 63 54 44</li>
              <li><strong>Email:</strong> intrinsicspiderlab@gmail.com</li>
            </ul>
          </div>
          
          
          <div class="footer">
            <p>Best regards,<br><strong>The Intrinsic Spiders Team</strong></p>
            <p style="margin-top: 20px; font-size: 12px; color: #999;">
              This is an automated confirmation email. Please do not reply to this message.
            </p>
          </div>
        </div>
      </body>
      </html>
    `
  };
};

// Format email content for admin (notification email)
const formatAdminEmail = (data) => {
  return {
    subject: `New Contact Form Submission from ${data.userName}`,
    html: `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <style>
          body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 700px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
          }
          .container {
            background: #ffffff;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
          }
          .header {
            background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            text-align: center;
          }
          h1 {
            margin: 0;
            font-size: 24px;
          }
          .info-section {
            margin: 25px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #8B5CF6;
          }
          .info-row {
            margin: 15px 0;
            padding: 10px 0;
            border-bottom: 1px solid #e5e7eb;
          }
          .info-row:last-child {
            border-bottom: none;
          }
          .label {
            font-weight: 600;
            color: #8B5CF6;
            display: inline-block;
            min-width: 120px;
          }
          .value {
            color: #333;
          }
          .message-box {
            background: #fff;
            border: 2px solid #8B5CF6;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            white-space: pre-wrap;
          }
          .booking-box {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%);
            border: 2px solid #8B5CF6;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
          }
          .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            text-align: center;
            color: #666;
            font-size: 14px;
          }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>🚀 New Contact Form Submission</h1>
            <p style="margin: 10px 0 0 0; opacity: 0.9;">You have a new inquiry from your website</p>
          </div>
          
          <div class="info-section">
            <div class="info-row">
              <span class="label">👤 Name:</span>
              <span class="value">${data.userName}</span>
            </div>
            <div class="info-row">
              <span class="label">📧 Email:</span>
              <span class="value"><a href="mailto:${data.userEmail}">${data.userEmail}</a></span>
            </div>
            <div class="info-row">
              <span class="label">📱 Phone:</span>
              <span class="value">${data.userPhone}</span>
            </div>
          </div>
          
          ${data.userMessage && data.userMessage !== 'No message provided' ? `
          <div class="message-box">
            <strong>💬 Message:</strong><br><br>
            ${data.userMessage.replace(/\n/g, '<br>')}
          </div>
          ` : ''}
          
          ${data.bookingInfo ? `
          <div class="booking-box">
            <strong style="font-size: 18px; color: #8B5CF6;">📅 BOOKING REQUEST</strong>
            <div style="margin-top: 15px; font-size: 16px;">
              ${data.bookingInfo.replace(/\n/g, '<br>')}
            </div>
          </div>
          ` : ''}
          
          <div class="footer">
            <p><strong>Action Required:</strong> Please respond to ${data.userName} at <a href="mailto:${data.userEmail}">${data.userEmail}</a></p>
            <p style="margin-top: 10px; font-size: 12px; color: #999;">
              This is an automated notification from your website contact form.
            </p>
          </div>
        </div>
      </body>
      </html>
    `
  };
};

// Send emails to both user and admin
export const sendEmails = async (data) => {
  try {
    // Validate environment variables
    if (!process.env.GMAIL_USER || !process.env.GMAIL_APP_PASSWORD) {
      throw new Error('Gmail credentials not configured. Please set GMAIL_USER and GMAIL_APP_PASSWORD environment variables.');
    }

    const transporter = createTransporter();
    const adminEmail = process.env.ADMIN_EMAIL || process.env.GMAIL_USER;

    // Verify transporter connection
    await transporter.verify();
    console.log('Email transporter verified successfully');

    // Prepare email content
    const userEmailContent = formatUserEmail(data);
    const adminEmailContent = formatAdminEmail(data);

    // Send confirmation email to user
    const userResult = await transporter.sendMail({
      from: `"Intrinsic Spiders" <${process.env.GMAIL_USER}>`,
      to: data.userEmail,
      replyTo: adminEmail,
      ...userEmailContent
    });
    console.log('User confirmation email sent:', userResult.messageId);

    // Send notification email to admin
    const adminResult = await transporter.sendMail({
      from: `"Website Contact Form" <${process.env.GMAIL_USER}>`,
      to: adminEmail,
      ...adminEmailContent
    });
    console.log('Admin notification email sent:', adminResult.messageId);

    console.log(`Emails sent successfully to ${data.userEmail} and ${adminEmail}`);
  } catch (error) {
    console.error('Error sending emails:', error);
    console.error('Error details:', {
      message: error.message,
      code: error.code,
      command: error.command,
      response: error.response
    });
    throw error; // Re-throw to be handled by the route handler
  }
};

