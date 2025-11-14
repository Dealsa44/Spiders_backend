# Render Deployment Guide

## Step 1: Push to GitHub

1. Make sure your code is committed and pushed to GitHub
2. The `website_backend` folder should be in your repository

## Step 2: Create Web Service on Render

1. Go to https://render.com and sign in
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select the repository containing `website_backend`

## Step 3: Configure the Service

**Name:** `website-backend` (or any name you prefer)

**Region:** Choose closest to you

**Branch:** `main` (or your default branch)

**Root Directory:** `website_backend`

**Runtime:** `Node`

**Build Command:** `npm install`

**Start Command:** `npm start`

## Step 4: Set Environment Variables

Click on "Environment" tab and add these variables:

```
GMAIL_USER=intrinsicspider@gmail.com
GMAIL_APP_PASSWORD=lqjttsuqmsdzhnxy
ADMIN_EMAIL=intrinsicspider@gmail.com
NODE_ENV=production
```

**Important:** 
- Use the exact values above (your email and app password)
- No quotes around values
- No spaces

## Step 5: Deploy

1. Click "Create Web Service"
2. Wait for deployment to complete (usually 2-3 minutes)
3. Your backend URL: `https://spiders-backend.onrender.com`

## Step 6: Update Frontend

After deployment, update the frontend environment file:

1. Open `website/src/environments/environment.prod.ts`
2. Backend URL is already configured: `apiUrl: 'https://spiders-backend.onrender.com/api'`

## Step 7: Test

1. Deploy your frontend (or test locally with production build)
2. Submit the contact form
3. Check your email (intrinsicspider@gmail.com) for both:
   - User confirmation email
   - Admin notification email

## Troubleshooting

- **Build fails:** Check that `package.json` is in `website_backend` folder
- **Emails not sending:** Verify environment variables are set correctly
- **CORS errors:** The backend allows all origins by default, should work
- **500 errors:** Check Render logs for detailed error messages

## Render Free Tier Notes

- Service may spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- This is normal for free tier

