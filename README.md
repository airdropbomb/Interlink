# 🌅 Interlink BOT

> Automated Mining $ITLG with multi-account and proxy support

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/vonssy/Interlink-BOT.svg)](https://github.com/vonssy/Interlink-BOT/stargazers)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Setup & Usage](#setup--usage)
- [Proxy Recommendation](#proxy-recommendation)
- [Support](#support)
- [Contributing](#contributing)

## 🎯 Overview

Interlink BOT is an automated tool designed to mining $ITLG tokens across multiple accounts. It provides seamless offers robust proxy support for enhanced security and reliability.performance.

**🔗 Get Started:** [Register on Interlink Validator](https://interlinklabs.ai/referral?refCode=162325)

> **Referral Code:** Use code `162325` during registration for benefits!

## ✨ Features

- 🔄 **Automated Account Management** - Retrieve account information automatically
- 🌐 **Flexible Proxy Support** - Run with or without proxy configuration
- 🔀 **Smart Proxy Rotation** - Automatic rotation of invalid proxies
- ⛏️ **Mining $ITLG Tokens** - Automated claim $ITLG tokens every 4 hours
- 👥 **Multi-Account Support** - Manage multiple accounts simultaneously

## 📋 Requirements

- **Python:** Version 3.9 or higher
- **pip:** Latest version recommended

## 🛠 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/airdropbomb/Interlink.git && cd Interlink
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
# or for Python 3 specifically
pip3 install -r requirements.txt
```

## ⚙️ Configuration

### Account Configuration

Create or edit `accounts.josn` in the project directory:

```json
[
    {
        "email": "your_email_address_1",
        "passcode": "your_passcode",
        "interlinkId": "your_interlink_id ( without xxxx@, only number )"
    },
    {
        "email": "your_email_address_2",
        "passcode": "your_passcode",
        "interlinkId": "your_interlink_id ( without xxxx@, only number )"
    }
]
```

### Proxy Configuration (Optional)

Create or edit `proxy.txt` in the project directory:

```
# Simple format (HTTP protocol by default)
192.168.1.1:8080

# With protocol specification
http://192.168.1.1:8080
https://192.168.1.1:8080

# With authentication
http://username:password@192.168.1.1:8080
```

## 🚀 Setup & Usage

### Automatic Token Setup

Run the setup script to automatically fetch tokens using your configured account credentials:

```bash
python setup.py
# or for Python 3 specifically
python3 setup.py
```

> **💡 What does setup.py do?**
> - Automatically logs in to your Interlink App accounts
> - Extracts bearer tokens automatically
> - Saves tokens to `tokens.json` for the bot to use

### Start the Bot

After running the setup, launch the Interlink BOT:

```bash
python bot.py
# or for Python 3 specifically
python3 bot.py
```
