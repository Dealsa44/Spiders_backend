# Website Backend API

Backend service for handling contact form submissions and sending emails.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

3. Configure Gmail App Password:
   - Go to your Google Account settings
   - Enable 2-Step Verification
   - Go to App Passwords
   - Generate a new app password for "Mail"
   - Use this password in `GMAIL_APP_PASSWORD`

4. Update `.env` with your credentials:
```
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-char-app-password
ADMIN_EMAIL=your-email@gmail.com
```

## Running Locally

```bash
npm run dev
```

Server will run on `http://localhost:3000`

## API Endpoints

### POST /api/contact
Submit contact form and send emails.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "message": "Hello, I'm interested in your services.",
  "selectedDate": "2025-11-26T00:00:00.000Z",
  "selectedTimeSlot": "09:00"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Your message has been received! We'll get back to you soon."
}
```

## Deployment on Render

**Quick Setup:**
1. Push your code to GitHub
2. Go to https://render.com → New Web Service
3. Connect your repository
4. Set Root Directory: `website_backend`
5. Build Command: `npm install`
6. Start Command: `npm start`
7. Add environment variables:
   - `GMAIL_USER` = `intrinsicspider@gmail.com`
   - `GMAIL_APP_PASSWORD` = `lqjttsuqmsdzhnxy`
   - `ADMIN_EMAIL` = `intrinsicspider@gmail.com`
   - `NODE_ENV` = `production`

**See DEPLOYMENT.md for detailed step-by-step instructions.**

## Environment Variables

- `GMAIL_USER`: Your Gmail address
- `GMAIL_APP_PASSWORD`: Gmail App Password (16 characters)
- `ADMIN_EMAIL`: Email to receive notifications (defaults to GMAIL_USER)
- `PORT`: Server port (defaults to 3000)

