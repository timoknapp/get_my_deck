# Steam Deck Refurbished Stock Checker

A simple scraper which checks the Steam Deck Refurb page for stock. This script sends notifications when the Steam Deck is in stock.

## Requirements

- Python (Latest version)
- Selenium WebDriver for Firefox via PIP
  ```sh
  pip install selenium webdriver-manager
  ```
- Email account or [Signal account](https://github.com/bbernhard/signal-cli-rest-api) for sending notifications

## Getting Started

### Command Line

```sh
python get_my_deck.py --email <your_email> --password <your_password> --send_to_email <recipient_email> --smtp_host <smtp_host> [--test_notification] [--refresh_time <seconds>]
```
or
```sh
python get_my_deck.py --signal_api_url <signal_api_url> --signal_number <signal_number> --send_to_number <recipient_number> [--test_notification] [--refresh_time <seconds>]
```

### Docker

1. Build the Docker image:
   ```sh
   docker build -t get_my_deck .
   ```
2. Run the Docker container:
   ```sh
   docker run \
       -d \
       --name get_my_deck \
       -e EMAIL=<your_email> \
       -e PASSWORD=<your_password> \
       -e SEND_TO_EMAIL=<recipient_email> \
       -e SMTP_HOST=<smtp_host> \
       -e TEST_NOTIFICATION=<true|false> \
       -e REFRESH_TIME=<seconds> \
       -e DEVICES_TO_MONITOR=<devices> \
       get_my_deck
   ```
or
   ```sh
   docker run \
       -d \
       --name get_my_deck \
       -e SIGNAL_API_URL=<signal_api_url> \
       -e SIGNAL_NUMBER=<signal_number> \
       -e SEND_TO_NUMBER=<recipient_number> \
       -e TEST_NOTIFICATION=<true|false> \
       -e REFRESH_TIME=<seconds> \
       -e DEVICES_TO_MONITOR=<devices> \
       get_my_deck
   ```

## Parameters

You can pass the following parameters to the script via the command line or environment variables.

### Arguments

| Parameter             | Description                                      | Required | Default |
|-----------------------|--------------------------------------------------|----------|---------|
| `--email`             | Email address to send notifications from         | Yes (if using email) | N/A     |
| `--password`          | Password for the email account                   | Yes (if using email) | N/A     |
| `--send_to_email`     | Email address to send notifications to           | Yes (if using email) | N/A     |
| `--smtp_host`         | SMTP host for sending email                      | Yes (if using email) | N/A     |
| `--signal_api_url`    | Signal API URL for sending notifications         | Yes (if using Signal) | N/A     |
| `--signal_number`     | Signal number to send notifications from         | Yes (if using Signal) | N/A     |
| `--send_to_number`    | Signal number to send notifications to           | Yes (if using Signal) | N/A     |
| `--test_notification` | Send a test notification and exit                | No       | False   |
| `--refresh_time`      | Time in seconds between page refreshes           | No       | 3600    |
| `--devices_to_monitor`| List of devices to monitor, separated by space. e.g. "Steam Deck 512 GB OLED" "Steam Deck 1TB OLED". Use the names from this [page](https://store.steampowered.com/sale/steamdeckrefurbished/) | No       | All devices |

### Environment Variables

You can also set the parameters via environment variables:

- `EMAIL`
- `PASSWORD`
- `SEND_TO_EMAIL`
- `SMTP_HOST`
- `SIGNAL_API_URL`
- `SIGNAL_NUMBER`
- `SEND_TO_NUMBER`
- `TEST_NOTIFICATION` (set to `true` to send a test notification and exit)
- `REFRESH_TIME` (time in seconds between page refreshes, default is 3600)
- `DEVICES_TO_MONITOR` (comma-separated list of devices to monitor, e.g. "Steam Deck 512 GB OLED,Steam Deck 1TB OLED". Use the names from this [page](https://store.steampowered.com/sale/steamdeckrefurbished/), default is all devices)

## Note

Only one type of notification method (email or Signal) is supported at a time. If both types of parameters are provided, the script will show an error message and quit.

## Credits

This is a fork of [maroofc/get_my_deck](https://github.com/maroofc/get_my_deck).