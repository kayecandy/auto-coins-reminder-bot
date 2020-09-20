# auto-coins-reminder-bot [![Say Hi!](https://img.shields.io/static/v1?label=&message=Say%20Hi%20to%20the%20bot!&color=2CA5E0&style=for-the-badge&logo=telegram)](https://t.me/AutoCoinsReminderBot)

_(It's still very shy though so be patient...)_

~~A telegram chat bot for checking crypto/PSE rates~~

A binance auto trading bot which supports telegram notifications... possibly telegram chat interface as well. We'll see.

[![Made with python](https://img.shields.io/static/v1?label=Made%20with&message=Python&color=3776AB&style=for-the-badge&logo=python)](http://coinsbot.cndce.me/) ![Supports Binance](https://img.shields.io/static/v1?label=Supports&message=Binance&color=F7931A&style=for-the-badge&logo=bitcoin)

> _**Note:**_ I started this project as a notification tool for `CoinsPH` and `COL Financial`/`PSE`; discovered `Binance` while doing initial research and completely shifted the focus to auto-trading bots

> _**Note (September 2020):**_ Will update this as I go, but I still need to find an actual job so I might just park it here for the mean time

### In a nutshell...

- Auto buy/sell for `Binance`
- Sends a `Telegram` message every buy sell
- Uses `MA(7)` and `MA(25)` for determining buy/sell
  - Simple algorithm based on the trend movement

#### Current auto-trade logic

_This has to be improved; but for now, this works....._

> _**TODO:** I'm aware that current implementation is processing heavy. But it saves me a few lines of code and less things to implement_

> _**Note:**_ Refer to `get_slope()` in `binance.py` for code

For every iteration (specified in `.env` as seconds), do:

- **Step 1** Retrieve k-lines data from Binance
- **Step 2** Retrieve current price
- **Step 3** Calculate moving averages (both `MA(7)` and `MA(25)`) from **`Step 1`**
- **Step 3** Also calculate previous candle moving averages (`pMA(7)` and `pMA(25)`) from **`Step 1`**
- **Step 4** Determine Buy/Sell and send Telegram message

  ```python
      if MA(7) > pMA(7):
          if MA(25) > pMA(25):
              # BUY ACTION
      elif:
          # SELL ACTION

      # SEND TELEGRAM MESSAGE
  ```

### `Todos`

- **IMPORTANT BEFORE I PARK THIS!!** AUTO MARGINS TRADING FOR DOWN TREND
- Telegram start/stop commands
- Telegram switch/add current stock code (`UNIBTC` is hardcoded for now since I just want this to work)
- Multiple users support (currently only have support for myself. Hardcoded binance account in _binance module_ >\_\_<"")
- _ERROR HANDLING_. Entire thread will crash if an exception is encountered (ie. Request/timeout errors)
- Research on better algorithms for determining buy/sell
