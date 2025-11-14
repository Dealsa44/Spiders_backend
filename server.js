import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { sendEmails } from './services/emailService.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
// Allow requests from localhost (development) and Vercel (production)
const allowedOrigins = [
  'http://localhost:4200',
  'https://spiders-umber.vercel.app',
  process.env.FRONTEND_URL
].filter(Boolean); // Remove any undefined values

app.use(cors({
  origin: function (origin, callback) {
    // Allow requests with no origin (like mobile apps or curl requests)
    if (!origin) return callback(null, true);
    
    // Allow all origins if FRONTEND_URL is not set (for development)
    if (allowedOrigins.length === 0 || process.env.FRONTEND_URL === '*') {
      return callback(null, true);
    }
    
    if (allowedOrigins.indexOf(origin) !== -1 || origin?.includes('localhost') || origin?.includes('vercel.app')) {
      callback(null, true);
    } else {
      callback(null, true); // Allow all for now, can be restricted later
    }
  },
  credentials: true
}));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', message: 'Server is running' });
});

// Contact form submission endpoint
app.post('/api/contact', async (req, res) => {
  try {
    const { name, email, phone, message, selectedDate, selectedTimeSlot } = req.body;

    // Validate required fields
    if (!name || !email) {
      return res.status(400).json({ 
        success: false, 
        message: 'Name and email are required' 
      });
    }

    // Check if environment variables are set
    if (!process.env.GMAIL_USER || !process.env.GMAIL_APP_PASSWORD) {
      console.error('Missing environment variables:', {
        GMAIL_USER: !!process.env.GMAIL_USER,
        GMAIL_APP_PASSWORD: !!process.env.GMAIL_APP_PASSWORD
      });
      return res.status(500).json({ 
        success: false, 
        message: 'Server configuration error. Please contact support.' 
      });
    }

    // Format booking information if available
    let bookingInfo = '';
    if (selectedDate && selectedTimeSlot) {
      const bookingDate = new Date(selectedDate);
      const formattedDate = bookingDate.toLocaleDateString('en-US', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      });
      bookingInfo = `\n\n📅 BOOKING REQUEST:\nDate: ${formattedDate}\nTime: ${selectedTimeSlot}`;
    }

    // Send emails
    await sendEmails({
      userName: name,
      userEmail: email,
      userPhone: phone || 'Not provided',
      userMessage: message || 'No message provided',
      bookingInfo: bookingInfo
    });

    res.json({ 
      success: true, 
      message: 'Your message has been received! We\'ll get back to you soon.' 
    });
  } catch (error) {
    console.error('Error processing contact form:', error);
    console.error('Error stack:', error.stack);
    res.status(500).json({ 
      success: false, 
      message: 'Something went wrong. Please try again later.',
      error: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

