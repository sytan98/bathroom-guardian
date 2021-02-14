### telegram-notifier-bot
Send notifications to users who have started the bot from a command line interface. 

## How to use
1. Obtain a key from the telegram Botfather by following these [instructions](https://core.telegram.org/bots#6-botfather)
2. Create a `secret.py` file to hold the following variables:
    - BOT_TOKEN       : str
    - MESSAGE_PORT    : int 
    - PICKLE_FILEPATH : str
    - AUTH_KEY        : bytes
    - PASSWORD        : str 
3. Run `python3 main.py` to start the telegram bot instance and the message listener.
4. Open telegram, go to your bot and type `/start`. You should receive a message "Welcome! This bot does nothing."
5. Type in the PASSWORD as defined in your `secret.py` file. This will authenticate you.
6. On a separate terminal, run `python3 messageClient.py` to get a CLI interface to type messages in. Any messages sent here will be routed to your telegram bot.