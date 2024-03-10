# Alpha Vantage API bot

AVBot provides financial market information using the Alpha Vantage API. It offers various commands to retrieve real-time and historical data about stocks, cryptocurrencies, and more.

## Features

- /quote: Get information about a specific ticker.
- /all: Get a .csv file containing information about all - available tickers.
- /popular: Get the top 10 popular tickers of the day.
- /history: Get a history of the commands used by the user.
- /graph: Get a graph of price changes for a desired time range (e.g., 8 hours, 32 hours, 3 days, 10 days).
- /low: Get the top losers of the day.
- /high: Get the top gainers of the day.

## Configuration

1. Navigate to the bot folder and run this command

```pip install -r requirements.txt```

to install required Python packages.

2. Create a .env file in the root folder of the bot.

3. Add the following variables to the .env file:

        KEY: API key if you're using RapidAPI for accessing the API.
        AV_KEY: Alpha Vantage API key.
        HOST: The host URL for the Alpha Vantage API (alpha-vantage.p.rapidapi.com/query).
        TOKEN: Your Telegram bot token.

## Usage

Start the bot by running the script.

Interact with the bot on Telegram using the provided commands.

## Contributors

- Murad Mikogaziev - author
- Aleksandr Mordvinov - mentor

## License

This project is licensed under the MIT License.