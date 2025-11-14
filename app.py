from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from datetime import datetime
import threading
import resend

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes, allowing your frontend to connect

# Email configuration from environment variables
# Using Resend API instead of SMTP (works on Render's free tier)
RESEND_API_KEY = os.getenv('RESEND_API_KEY')
# Use Resend's default sender for now (works without verification)
# Later you can change this to your verified email
SENDER_EMAIL = os.getenv('GMAIL_USER', 'onboarding@resend.dev')  # Fallback to Resend default

# Resend free tier restriction: can only send to account owner's email
# Get the account owner email from environment or use intrinsicspider@gmail.com
ACCOUNT_OWNER_EMAIL = os.getenv('ACCOUNT_OWNER_EMAIL', 'intrinsicspider@gmail.com')
# Admin email - will use account owner email due to Resend free tier restriction
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', ACCOUNT_OWNER_EMAIL)

# Initialize Resend client
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY
    print(f"[EMAIL] Resend client initialized")
else:
    print(f"[EMAIL] WARNING: RESEND_API_KEY not set!")

def format_user_email(data):
    """Format the confirmation email sent to the user"""
    booking_html = ''
    if data.get('bookingInfo'):
        booking_html = f'''
            <div class="message-box">
              <strong>📅 Your Consultation Booking:</strong><br>
              {data['bookingInfo'].replace(chr(10), '<br>')}
            </div>
        '''
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{
          font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          line-height: 1.6;
          color: #333;
          max-width: 600px;
          margin: 0 auto;
          padding: 20px;
          background-color: #f5f5f5;
        }}
        .container {{
          background: #ffffff;
          border-radius: 12px;
          padding: 40px;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .header {{
          text-align: center;
          margin-bottom: 30px;
        }}
        .logo {{
          font-size: 24px;
          font-weight: 900;
          color: #8B5CF6;
          margin-bottom: 10px;
        }}
        h1 {{
          color: #0A0A0A;
          font-size: 28px;
          margin: 0 0 10px 0;
        }}
        .subtitle {{
          color: #666;
          font-size: 16px;
        }}
        .content {{
          margin: 30px 0;
        }}
        .message-box {{
          background: #f8f9fa;
          border-left: 4px solid #8B5CF6;
          padding: 20px;
          margin: 20px 0;
          border-radius: 4px;
        }}
        .footer {{
          margin-top: 40px;
          padding-top: 20px;
          border-top: 1px solid #e5e7eb;
          text-align: center;
          color: #666;
          font-size: 14px;
        }}
        .highlight {{
          color: #8B5CF6;
          font-weight: 600;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <div class="logo">INTRINSIC SPIDERS</div>
          <h1>Thank You, {data['userName']}!</h1>
          <p class="subtitle">We've received your message and will get back to you within 24 hours.</p>
        </div>
        
        <div class="content">
          <p>Hello {data['userName']},</p>
          
          <p>Thank you for reaching out to Intrinsic Spiders. We're excited about the possibility of working together to bring your vision to life!</p>
          
          {booking_html}
          
          <p>Our team is already reviewing your message and will respond to you at <span class="highlight">{data['userEmail']}</span> within 24 hours.</p>
          
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
    '''
    return html

def format_admin_email(data):
    """Format the notification email sent to admin"""
    message_html = ''
    if data.get('userMessage') and data['userMessage'] != 'No message provided':
        message_html = f'''
        <div class="message-box">
          <strong>💬 Message:</strong><br><br>
          {data['userMessage'].replace(chr(10), '<br>')}
        </div>
        '''
    
    booking_html = ''
    if data.get('bookingInfo'):
        booking_html = f'''
        <div class="booking-box">
          <strong style="font-size: 18px; color: #8B5CF6;">📅 BOOKING REQUEST</strong>
          <div style="margin-top: 15px; font-size: 16px;">
            {data['bookingInfo'].replace(chr(10), '<br>')}
          </div>
        </div>
        '''
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{
          font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          line-height: 1.6;
          color: #333;
          max-width: 700px;
          margin: 0 auto;
          padding: 20px;
          background-color: #f5f5f5;
        }}
        .container {{
          background: #ffffff;
          border-radius: 12px;
          padding: 40px;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .header {{
          background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
          color: white;
          padding: 30px;
          border-radius: 8px;
          margin-bottom: 30px;
          text-align: center;
        }}
        h1 {{
          margin: 0;
          font-size: 24px;
        }}
        .info-section {{
          margin: 25px 0;
          padding: 20px;
          background: #f8f9fa;
          border-radius: 8px;
          border-left: 4px solid #8B5CF6;
        }}
        .info-row {{
          margin: 15px 0;
          padding: 10px 0;
          border-bottom: 1px solid #e5e7eb;
        }}
        .info-row:last-child {{
          border-bottom: none;
        }}
        .label {{
          font-weight: 600;
          color: #8B5CF6;
          display: inline-block;
          min-width: 120px;
        }}
        .value {{
          color: #333;
        }}
        .message-box {{
          background: #fff;
          border: 2px solid #8B5CF6;
          border-radius: 8px;
          padding: 20px;
          margin: 20px 0;
          white-space: pre-wrap;
        }}
        .booking-box {{
          background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%);
          border: 2px solid #8B5CF6;
          border-radius: 8px;
          padding: 20px;
          margin: 20px 0;
        }}
        .footer {{
          margin-top: 30px;
          padding-top: 20px;
          border-top: 1px solid #e5e7eb;
          text-align: center;
          color: #666;
          font-size: 14px;
        }}
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
            <span class="value">{data['userName']}</span>
          </div>
          <div class="info-row">
            <span class="label">📧 Email:</span>
            <span class="value"><a href="mailto:{data['userEmail']}">{data['userEmail']}</a></span>
          </div>
          <div class="info-row">
            <span class="label">📱 Phone:</span>
            <span class="value">{data['userPhone']}</span>
          </div>
        </div>
        
        {message_html}
        
        {booking_html}
        
        <div class="footer">
          <p><strong>Action Required:</strong> Please respond to {data['userName']} at <a href="mailto:{data['userEmail']}">{data['userEmail']}</a></p>
          <p style="margin-top: 10px; font-size: 12px; color: #999;">
            This is an automated notification from your website contact form.
          </p>
        </div>
      </div>
    </body>
    </html>
    '''
    return html

def send_email(to_email, subject, html_body):
    """Send an email using Resend API"""
    if not RESEND_API_KEY:
        raise Exception("Resend client not initialized. Please set RESEND_API_KEY environment variable.")
    
    try:
        print(f"[EMAIL] Sending email via Resend API")
        print(f"[EMAIL] To: {to_email}")
        print(f"[EMAIL] From: {SENDER_EMAIL}")
        print(f"[EMAIL] Subject: {subject}")
        
        # Use Resend's default sender (works without domain/email verification)
        # Format: "Display Name <email@domain.com>"
        from_email = SENDER_EMAIL if SENDER_EMAIL and SENDER_EMAIL != 'onboarding@resend.dev' else 'onboarding@resend.dev'
        
        params = {
            "from": f"Intrinsic Spiders <{from_email}>",
            "to": [to_email],
            "subject": subject,
            "html": html_body
        }
        
        print(f"[EMAIL] Calling Resend API...")
        email_response = resend.Emails.send(params)
        
        print(f"✅ Email sent successfully to {to_email}")
        print(f"✅ Resend response: {email_response}")
        return True
    except Exception as e:
        print(f"❌ Error sending email to {to_email}: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        import traceback
        print(traceback.format_exc())
        raise

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Server is running"}), 200

@app.route('/api/contact', methods=['POST'])
def send_contact_email():
    print('=== CONTACT FORM REQUEST RECEIVED ===')
    print('Request body:', request.get_json())
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone', 'Not provided')
        message = data.get('message', 'No message provided')
        selectedDate = data.get('selectedDate')
        selectedTimeSlot = data.get('selectedTimeSlot')
        
        print('Parsed data:', {
            'name': name,
            'email': email,
            'phone': phone,
            'hasMessage': bool(message),
            'hasBooking': bool(selectedDate and selectedTimeSlot)
        })
        
        # Validate required fields
        if not name or not email:
            return jsonify({
                "success": False,
                "message": "Name and email are required"
            }), 400
        
        # Check if environment variables are set
        if not RESEND_API_KEY:
            print('Missing environment variables:', {
                'RESEND_API_KEY': bool(RESEND_API_KEY)
            })
            return jsonify({
                "success": False,
                "message": "Server configuration error. Please contact support."
            }), 500
        
        # Format booking information if available
        booking_info = ''
        if selectedDate and selectedTimeSlot:
            try:
                # Parse ISO date string - extract just the date part to avoid timezone issues
                # Format: "2025-11-14T20:00:00.000Z" -> extract "2025-11-14"
                date_part = selectedDate.split('T')[0]  # Get just the date part (YYYY-MM-DD)
                # Parse as date only (no time/timezone)
                from datetime import date as date_class
                year, month, day = map(int, date_part.split('-'))
                booking_date = date_class(year, month, day)
                formatted_date = booking_date.strftime('%A, %B %d, %Y')
                booking_info = f'\n\n📅 BOOKING REQUEST:\nDate: {formatted_date}\nTime: {selectedTimeSlot}'
            except Exception as e:
                print(f'Error formatting booking date: {e}')
                # Fallback: try to extract date part manually
                try:
                    date_part = selectedDate.split('T')[0]
                    year, month, day = map(int, date_part.split('-'))
                    from datetime import date as date_class
                    booking_date = date_class(year, month, day)
                    formatted_date = booking_date.strftime('%A, %B %d, %Y')
                    booking_info = f'\n\n📅 BOOKING REQUEST:\nDate: {formatted_date}\nTime: {selectedTimeSlot}'
                except:
                    booking_info = f'\n\n📅 BOOKING REQUEST:\nDate: {selectedDate}\nTime: {selectedTimeSlot}'
        
        # Prepare email data
        email_data = {
            'userName': name,
            'userEmail': email,
            'userPhone': phone,
            'userMessage': message,
            'bookingInfo': booking_info if booking_info else None
        }
        
        print('=== Starting email sending process ===')
        print('Email data:', email_data)
        
        # Send emails in background thread (non-blocking)
        def send_emails_background():
            print('[BACKGROUND THREAD] Starting email sending process...')
            print(f'[BACKGROUND THREAD] SENDER_EMAIL: {SENDER_EMAIL}')
            print(f'[BACKGROUND THREAD] RESEND_API_KEY exists: {bool(RESEND_API_KEY)}')
            print(f'[BACKGROUND THREAD] ACCOUNT_OWNER_EMAIL: {ACCOUNT_OWNER_EMAIL}')
            print(f'[BACKGROUND THREAD] ADMIN_EMAIL (requested): {ADMIN_EMAIL}')
            
            try:
                print(f'=== SENDING USER CONFIRMATION EMAIL ===')
                print(f'To: {email}')
                print(f'From: {SENDER_EMAIL}')
                
                # Resend free tier restriction: can only send to account owner's email
                # If user email is different, send to account owner email instead
                user_recipient = email if email.lower() == ACCOUNT_OWNER_EMAIL.lower() else ACCOUNT_OWNER_EMAIL
                if user_recipient != email:
                    print(f'⚠️ Resend free tier: User email ({email}) is not account owner.')
                    print(f'⚠️ Sending confirmation to account owner ({ACCOUNT_OWNER_EMAIL}) instead.')
                    print(f'⚠️ Note: User will not receive confirmation email due to Resend free tier limitation.')
                
                user_html = format_user_email(email_data)
                send_email(user_recipient, 'Thank You for Contacting Intrinsic Spiders', user_html)
                print('✅ User confirmation email sent successfully!')
            except Exception as user_error:
                print(f'❌ Failed to send user confirmation email: {user_error}')
                print(f'❌ Error type: {type(user_error).__name__}')
                import traceback
                print('❌ Full traceback:')
                print(traceback.format_exc())
            
            try:
                print(f'=== SENDING ADMIN NOTIFICATION EMAIL ===')
                # Resend free tier restriction: can only send to account owner's email
                # Send to account owner email (they can forward or check this inbox)
                admin_recipient = ACCOUNT_OWNER_EMAIL
                print(f'To: {admin_recipient} (Resend free tier: sending to account owner)')
                print(f'From: {SENDER_EMAIL}')
                print(f'Note: Original admin email ({ADMIN_EMAIL}) cannot be used on free tier')
                admin_html = format_admin_email(email_data)
                send_email(admin_recipient, f'New Contact Form Submission from {name}', admin_html)
                print('✅ Admin notification email sent successfully!')
            except Exception as admin_error:
                print(f'❌ Failed to send admin notification email: {admin_error}')
                print(f'❌ Error type: {type(admin_error).__name__}')
                import traceback
                print('❌ Full traceback:')
                print(traceback.format_exc())
            
            print('[BACKGROUND THREAD] Email sending process completed.')
        
        # Start email sending in background thread
        email_thread = threading.Thread(target=send_emails_background)
        email_thread.daemon = True  # Thread will die when main thread exits
        email_thread.start()
        
        # Return success immediately (emails sent in background)
        return jsonify({
            "success": True,
            "message": "Your message has been received! We'll get back to you soon."
        }), 200
        
    except Exception as e:
        print(f'Error processing contact form: {e}')
        import traceback
        print(traceback.format_exc())
        return jsonify({
            "success": False,
            "message": "Something went wrong. Please try again later.",
            "error": str(e) if os.getenv('FLASK_ENV') == 'development' else None
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(debug=True, host='0.0.0.0', port=port)

