#!/bin/bash
# This script deploys the Chalice app to AWS Lambda, injecting sensitive environment variables at runtime
# It reads the TELEGRAM_API_TOKEN and TELEGRAM_CHAT_ID from a local .env.json file
# and updates the .chalice/config.json file before deployment. After deployment, it restores
# the original config file to avoid committing sensitive information to version control.

TELEGRAM_API_TOKEN=$(cat .env.json | jq -r .TELEGRAM_API_TOKEN)
TELEGRAM_CHAT_ID=$(cat .env.json | jq -r .TELEGRAM_CHAT_ID)
if [  "$TELEGRAM_API_TOKEN" == null ] || [ "$TELEGRAM_CHAT_ID" == null ]; then
  echo "Error: TELEGRAM_API_TOKEN or TELEGRAM_CHAT_ID is not set in .env.json"
  exit 1
fi
NEW_CONFIG_FILE=$(cat .chalice/config.json | jq --arg TELEGRAM_API_TOKEN "$TELEGRAM_API_TOKEN" --arg TELEGRAM_CHAT_ID "$TELEGRAM_CHAT_ID" '.stages.dev.environment_variables.TELEGRAM_API_TOKEN = $TELEGRAM_API_TOKEN | .stages.dev.environment_variables.TELEGRAM_CHAT_ID = $TELEGRAM_CHAT_ID')
OLD_CONFIG_FILE=$(cat .chalice/config.json)
echo $NEW_CONFIG_FILE > .chalice/config.json
source .venv/bin/activate
chalice deploy
# Restore the redacted TELEGRAM_API_TOKEN
echo $OLD_CONFIG_FILE > .chalice/config.json