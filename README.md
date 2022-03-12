# Stock_alerts
This app sends email/text alerts with stock information periodically.

# Getting Started

1. In an anaconda prompt, run "conda env create -f environment.yml" then run "conda activate stockEnv"

2. Add your portfolio to the "portfolio_qty" dataframe in check_stocks.py

3. Create a free email account to send alerts from using ClarityCoder's Tutorial found [here](https://www.youtube.com/watch?v=B1IsCbXp0uE)

4. Update the alert email credentials and desired recipient information in alert_server.py
    - self.user: Username for alert email
    - self.password: App password for alert email
    - send_email create_message function: recipient email
    - send_text create_message function: recipeint phone number (as an email service - See ClarityCoder's video)

5. Run check_stocks.py to send an alert. This can be automated using windows' Task Scheduler. See [here](https://datatofish.com/python-script-windows-scheduler/) for instructions on how.
