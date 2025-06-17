# 💸 Automated Bill Payment with Python & Selenium

A Python automation script that securely logs in to an online billing portal and submits monthly payments — built to replace the need for manual bill payments at companies that do not offer auto-pay features.

---

## 🚀 Project Overview

This script automates the end-to-end bill payment process using **Selenium WebDriver**. It handles login, navigation, payment form submission, and optional CSV logging or email confirmations — saving time and ensuring no missed payments.

---

## 🛠️ Technologies Used

- **Python 3.x**
- **Selenium WebDriver**
- **ChromeDriver / GeckoDriver**
- **dotenv** (for managing credentials securely)
- *(Optional)* `smtplib` for email confirmation
- *(Optional)* `pandas` or `csv` for logging queries

---

## 🔐 Key Features

- ✅ Automated login to billing portal  
- ✅ Secure credential handling with `.env`  
- ✅ Form-filling and payment submission  
- ✅ Optional query tool to filter past payments by:
  - File extension (CSV)
  - Event type (e.g., success/failure)
  - Date range  
- ✅ Email export feature — send the full database or filtered results as a `.csv` file  
- ✅ Designed for Windows (Task Scheduler compatible)

---

## 🧪 How It Works

1. Script starts manually or via schedule.
2. Loads secure credentials from `.env` file.
3. Launches browser using Selenium and logs into the payment website.
4. Navigates to the payment page, selects amount/method, and submits.
5. (Optional) Sends confirmation email or logs event to a database.
6. Query tool allows you to view and export transaction history.

---

## 📦 Setup Instructions

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/automated-bill-payment.git
cd automated-bill-payment

