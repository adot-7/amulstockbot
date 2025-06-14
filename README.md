# 🥛 Amul Stock Bot

A Python automation script that monitors Amul's Protein Lassi products for stock availability and sends WhatsApp notifications when items are in stock (quantity > 100). Can be adapted to track any product available on shop.amul.com.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technical Challenges](#technical-challenges)
- [Deployment Options](#deployment-options)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Learning Journey](#learning-journey)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)

## 🎯 Overview

This is a personal convenience project to track availability of Amul's Protein Lassi products, which often go out of stock quickly. The bot automatically checks stock levels every hour and sends WhatsApp notifications when items are available.

**Note**: This is a personal project and not ready for production use. It's specifically designed for my needs but can be adapted for other Amul products.

## ✨ Features

- **Automated Stock Monitoring**: Checks Amul's internal API for Protein Lassi availability
- **Smart Filtering**: Focuses specifically on products with "lassi" in their alias
- **WhatsApp Notifications**: Sends formatted messages via Twilio WhatsApp API
- **Multi-Region Support**: Includes substore IDs for Delhi, Bangalore, and Mumbai regions
- **Threshold-Based Alerts**: Only alerts when stock quantity exceeds 100 units
- **Multiple Deployment Options**: Supports local execution, Vercel, GitHub Actions, and AWS Lambda

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Scheduler     │───▶│   Stock Bot      │───▶│   Twilio API    │
│ (Cron/Lambda)   │    │                  │    │  (WhatsApp)     │
└─────────────────┘    │  1. API Call     │    └─────────────────┘
                       │  2. Parse Data   │              │
┌─────────────────┐    │  3. Filter Items │              ▼
│   Amul API      │◀───│  4. Send Alerts  │    ┌─────────────────┐
│ (shop.amul.com) │    │                  │    │   Your Phone    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚧 Technical Challenges

### 1. Finding the API Endpoint
**Problem**: Amul's website doesn't publicly document their API and uses JavaScript blockers
- Main website is hard to scrape due to pincode requirements and JS blocking
- Tried cookie copying methods but didn't work
- **Solution**: Used browser dev tools Network tab, filtered by Fetch/XHR to find the actual API endpoint they hit

### 2. IP Blocking by Cloud Providers
**Problem**: Amul's API blocks requests from cloud service IP ranges (AWS Lambda, Vercel, GitHub Actions)
- Works fine locally with simple curl requests
- Fails silently on cloud platforms, returning empty `data` arrays
- API returns valid JSON structure but with no actual product data

**Solutions**:
- Added browser-like headers (User-Agent, Referer, etc.)
- Implemented retry logic with exponential backoff
- Tested different AWS regions - **only ap-south-1 (Mumbai) worked consistently**
- GitHub Actions worked rarely, mostly returned empty data

### 3. Lambda Timeout Issues
**Problem**: Default 3-second Lambda timeout insufficient for API call + Twilio messaging
**Solution**: Increased timeout to 10 seconds and added proper error handling

### 4. Why curl over requests?
- **Local Success**: curl worked perfectly in local environment
- **Library Issues**: Python `requests` library faced same IP blocking issues
- **Subprocess Approach**: Using `subprocess.run()` with curl provided better reliability
- **Header Control**: Easier to replicate exact browser behavior with curl

### 5. Finding Substore IDs for Different Regions
To use this bot for your region, you need to find your substore ID:
1. Go to shop.amul.com
2. Navigate to protein section 
3. Open browser dev tools (F12)
4. Go to Network tab, filter by Fetch/XHR
5. Reload the page
6. Look for the API call to `/api/1/entity/ms.products`
7. The substore ID will be at the end of the URL

**Current substore IDs included**:
- Delhi: `66505ff5145c16635e6cc74d` 
- Bangalore: `66505ff0998183e1b1935c75`
- Mumbai: `66506004a7cddee1b8adb014`

## 🚀 Deployment Options

### 1. AWS Lambda (Works Reliably)
- **Pros**: Serverless, automatic scaling, integrated with EventBridge for scheduling
- **Cons**: Only works in ap-south-1 region
- **Reality**: **Only ap-south-1 (Mumbai) region works consistently** - other regions get blocked

### 2. Vercel
- **Pros**: Easy deployment, webhook-triggered execution
- **Cons**: Not ideal for scheduled tasks, IP blocking issues
- **Reality**: Hit or miss due to IP blocking

### 3. GitHub Actions  
- **Pros**: Free, version controlled, scheduled execution
- **Cons**: IP blocking, limited to public repositories for free tier
- **Reality**: **Rarely works** - mostly returns empty data due to IP blocking

### 4. Local/VPS Cron (Most Reliable)
- **Pros**: No IP restrictions, full control, works every time
- **Cons**: Requires dedicated server, manual maintenance
- **Best For**: Personal use, guaranteed reliability

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- Twilio Account with WhatsApp Business API
- Environment variables configuration

### Local Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/amulstockbot.git
cd amulstockbot

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# Run locally
python main.py
```

### AWS Lambda Deployment
```bash
# Create deployment package
mkdir deployment
pip install twilio -t deployment/
cp main.py deployment/
cd deployment
zip -r ../amul-stock-bot.zip .

# Upload to Lambda and set handler to: main.lambda_handler, make sure to create a lambda_handler function.
```

## 🔧 Environment Variables

Create a `.env` file with the following variables:

```env
# Twilio Configuration
ACCOUNT_SID=your_twilio_account_sid
AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE=your_twilio_whatsapp_number
MY_PHONE=your_phone_number

# Optional: For Vercel webhook protection
WEBHOOK_KEY=your_secret_key
```

## 📱 Usage

### Manual Execution
```bash
python main.py
```

### Scheduled Execution (cron)
```bash
# Add to crontab for hourly execution
0 * * * * /usr/bin/python3 /path/to/amulstockbot/main.py
```

### Vercel Webhook
```bash
curl "https://your-vercel-app.vercel.app/run?key=your_webhook_key"
```

## 📚 Learning Journey

This project was a good way to learn several technologies:

### Cloud Platforms & Serverless
- **AWS Lambda**: Serverless functions, event triggers, and deployment packages
- **EventBridge**: Cron-like scheduling in AWS
- **Vercel**: Serverless deployment for Python Flask applications

### Automation & Scheduling
- **Cron Jobs**: Unix cron syntax and scheduling
- **GitHub Actions**: YAML workflow configuration and scheduled triggers
- **Event-Driven Architecture**: Triggers and automated responses

### API Integration Challenges
- **Rate Limiting**: API rate limiting issues
- **IP Whitelisting**: Cloud provider IP blocking by e-commerce sites
- **Header Manipulation**: Proper HTTP headers for API access
- **Error Handling**: Retry mechanisms and timeout handling

### Communication APIs
- **Twilio WhatsApp API**: Business messaging capabilities
- **Content Templates**: Twilio's message templates for structured notifications
- **Webhook Security**: Basic authentication for webhook endpoints

### Debugging & Monitoring
- **CloudWatch Logs**: Debug serverless functions using AWS logs
- **Environment-Specific Issues**: Differences between local and cloud execution
- **Timeout Management**: Execution time vs. cost optimization

## 🔍 Troubleshooting

### Common Issues

1. **Empty Data Response**
   - Check if running from cloud provider IP
   - Try different AWS regions
   - Consider using proxy services

2. **Lambda Timeout**
   - Increase function timeout (default 3s → 10s)
   - Optimize API call timeouts
   - Add proper error handling

3. **Twilio Authentication Errors**
   - Verify ACCOUNT_SID and AUTH_TOKEN
   - Check WhatsApp number format (+country_code)
   - Ensure Content Template ID is correct

## 🚀 Future Improvements

Since this is a personal project, these are more like "maybe someday" ideas:

### Technical Stuff
- [ ] **Proxy Integration**: Add residential proxy support for IP blocking
- [ ] **Database Storage**: Track stock history and price changes  
- [ ] **Multiple Products**: Expand beyond Protein Lassi to other Amul products
- [ ] **Smart Notifications**: Avoid spam by tracking previous alerts

### Features
- [ ] **Price Alerts**: Notify on price drops or offers
- [ ] **Multiple Recipients**: Support family/friend groups
- [ ] **Custom Thresholds**: User-configurable stock quantity limits
- [ ] **Web Dashboard**: Simple UI to view stock status

### Infrastructure  
- [ ] **Monitoring**: Add health checks and alerting
- [ ] **CI/CD Pipeline**: Automated testing and deployment
- [ ] **Cost Optimization**: Fine-tune Lambda execution time

## 📜 Legal Disclaimer

This project uses Amul's internal API found through browser dev tools. The API is not publicly documented. This is for personal/educational use only. Please respect Amul's terms of service and don't abuse their API.

## 🤝 Contributing

This is a personal convenience project, but feel free to fork it for your own use!

---

*Built while learning cloud technologies and trying to get protein lassi*

