# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a price tracking application built with AWS Chalice that monitors an Effeuno pizza oven product page and sends Telegram notifications when the price drops below 899 or the promotion text changes. The application runs on a scheduled basis (every 12 hours) via AWS Lambda.

## Architecture

- **app.py**: Main Chalice application with scheduled Lambda function and Telegram messaging
- **chalicelib/scrape_effeuno.py**: Web scraping module that extracts price and promotion data from the target website
- **Telegram Integration**: Uses direct HTTP requests to Telegram Bot API instead of the full SDK

## Common Commands

### Development
- Test scraping locally: `python chalicelib/scrape_effeuno.py`
- Invoke function locally: `./invoke_local.sh` (simulates scheduled event)
- View logs: `./read_logs.sh`

### Deployment
- Deploy to AWS: `./deploy.sh` (runs `chalice deploy`)

## Environment Variables

- `TELEGRAM_API_TOKEN`: Required for sending Telegram messages

## Key Configuration

- **Schedule**: Function runs every 12 hours (`Rate(12, unit=Rate.HOURS)`)
- **Price threshold**: Triggers notification when price < 899
- **Telegram Chat ID**: Hard-coded to "172709986"
- **Target URL**: Monitors specific Effeuno pizza oven product page

## Dependencies

The project uses minimal dependencies:
- `requests`: For HTTP requests to Telegram API
- `chalice`: AWS serverless framework
- Built-in Python libraries for web scraping (`urllib.request`, `re`)