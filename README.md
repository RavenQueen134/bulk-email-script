# bulk-email-script README
This simple script was created to get around an issue in Gmail where bcc would fail to send an email to some recipients if too many email addresses were included. It works by sending the same email individually to each recipient.

## Setup
Clone this repo and install dependencies using `pip install -r requirements.txt` (it just uses `python-dotenv`).

Once you've done that, follow the below instructions.

## Google App Password
In order to use this script, you will need to create an App Password for your Google account, which requires that you have 2FA enabled. To do this, go to myaccount.google.com, and, after verifying that you have 2FA set up, search for the "App Passwords" setting to create one. Note that Google will only show you the password one time upon creation, so make sure to copy it immediately. As for what to use for the app name, feel free to call it whatever you want, or just name it `bulk-email-script`

## .env Setup
This repo includes a `.env.example` file. In order for the script to be used, you must rename it to simply `.env` and replace the placeholder values with your actual Gmail address and Google App Password.

## .csv Setup
This script requires a `recipients.csv` file with column `email`. Each line will contain an individual recipient's email address. A template `recipients.csv.example` has been included, which you can edit the contents of and rename to `recipients.csv`

## Writing your email
A template file `email_body.txt.example` has been included. Rename this to `email_body.txt` and edit the contents to whatever it is you want your email to say!

## Usage
`python bulk_email_script.py`

## Note
Gmail will rate-limit how many emails you can send to around 500/day for regular accounts. This script is not intended for a larger number of recipients than that.