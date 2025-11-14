import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { sendEmails } from './services/emailService.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors({
  origin: process.env.FRONTEND_URL || '*', // Allow all origins in production, or set specific URL
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
    res.status(500).json({ 
      success: false, 
      message: 'Something went wrong. Please try again later.' 
    });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

