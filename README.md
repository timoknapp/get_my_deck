# Steam Deck Refurbished Stock Checker

A simple scraper which checks the Steam Deck Refurb page for stock. This script sends email notifications when the Steam Deck is in stock.

## Requirements

- Python (Latest version)
- Selenium WebDriver for Firefox via PIP
  ```sh
  pip install selenium webdriver-manager
  ```
- Email account for sending notifications

## Getting Started

### Command Line

```sh
python get_my_deck.py --email <your_email> --password <your_password> --send_to_email <recipient_email> --smtp_host <smtp_host> [--test_email] [--refresh_time <seconds>]
```

### Docker

1. Build the Docker image:
   ```sh
   docker build -t get_my_deck .
   ```
2. Run the Docker container:
   ```sh
   docker run get_my_deck --email <your_email> --password <your_password> --send_to_email <recipient_email> --smtp_host <smtp_host> [--test_email] [--refresh_time <seconds>]
   ```

## Parameters

You can pass the following parameters to the script via the command line or environment variables.

### Arguments

| Parameter       | Description                                      | Required | Default |
|-----------------|--------------------------------------------------|----------|---------|
| `--email`       | Email address to send notifications from         | Yes      | N/A     |
| `--password`    | Password for the email account                   | Yes      | N/A     |
| `--send_to_email` | Email address to send notifications to         | Yes      | N/A     |
| `--smtp_host`   | SMTP host for sending email                      | Yes      | N/A     |
| `--test_email`  | Send a test email and exit                       | No       | False   |
| `--refresh_time`| Time in seconds between page refreshes           | No       | 3600    |

### Environment Variables

You can also set the parameters via environment variables:

- `EMAIL`
- `PASSWORD`
- `SEND_TO_EMAIL`
- `SMTP_HOST`
- `TEST_EMAIL` (set to `true` to send a test email and exit)
- `REFRESH_TIME` (time in seconds between page refreshes, default is 3600)

## Credits

This is a fork of [maroofc/get_my_deck](https://github.com/maroofc/get_my_deck).