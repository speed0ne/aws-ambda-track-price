TELEGRAM_API_TOKEN=cat .env.json | jq -r TELEGRAM_API_TOKEN
TELEGRAM_CHAT_ID=cat .env.json | jq -r TELEGRAM_CHAT_ID
OLD_CONFIG_FILE=cat .chalice/config.json
NEW_CONFIG_FILE=cat .chalice/config.json | jq --arg TELEGRAM_API_TOKEN "$TELEGRAM_API_TOKEN" --arg TELEGRAM_CHAT_ID "$TELEGRAM_CHAT_ID" '.stages.dev.environment_variables.TELEGRAM_API_TOKEN = $TELEGRAM_API_TOKEN | .stages.dev.environment_variables.TELEGRAM_CHAT_ID = $TELEGRAM_CHAT_ID'
echo $NEW_CONFIG_FILE > .chalice/config.json
source .venv/bin/activate
chalice deploy
# Restore the redacted TELEGRAM_API_TOKEN
echo $OLD_CONFIG_FILE > .chalice/config.json