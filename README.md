# Gmail Delete by Filter
*TL;DR: This script will indiscriminantly delete emails matching the query via the Gmail API, 1000 at a time. Use extreme caution!*

## Why the script?
Did you have some kind of automated system emailing you hundreds or thousands of times a day to alert you? Do you now have tens of gigabytes of email in your Gmail account?

I did—1.7 million emails, in fact. I had something like 22GB of emails. Which is fine, if you are using the Gmail or Inbox web interfaces. However, if you actually want to use an email client, you are either fine-tuning folders and IMAP sync settings, or you are waiting 17 years for it to download all of your emails locally, and wasting multiple gigs on your system for emails you never cared about.

Enter **gmail_delete_by_filter**.

This is a quick (and very dirty) script I wrote based on the Gmail API docs to delete emails matching a query 1000 at a time (the max for Gmail's batchDelete endpoint). The query is very simply a string that exactly matches what you would [input in the Gmail UI's search bar](https://support.google.com/mail/answer/7190?hl=en)—same exact results, in my testing.

As of this moment, I have deleted about 6GB of emails in hours, without bumping into quotas or errors.

So, without further ado...

## Setup

### Script setup
The first thing you need to do after you've pulled down this repo is get some Oauth2 credentials. You can do that [here](https://console.developers.google.com/apis/credentials), and select "Oauth Client ID" under "Create credentials". Once you create the credentials, save them to the root of this repo. **Make sure you update the `CLIENT_SECRET_FILE` global in the script to match your credential file's name.**

Now, you simply need to generate the [proper query](https://support.google.com/mail/answer/7190?hl=en) to get the emails you want to delete, and set it using the `QUERY` global at the top of the script.

```
  It is HIGHLY recommended to check this query in the UI before deletion. This is a full delete, not a move to the trash, so after deletion, THERE IS NO GOING BACK.
```

### Dependencies
The last thing you need to do is install the dependencies for the script via pip:

```
  pip install oauth2client apiclient google-api-python-client
```

## Running
Now, just run the script without arguments.

```
  ./deleter.py
```

Because this is a dirty script, it just runs the batchDelete 600 times and stops. I'm sure there is a better
method, but this works fine so I didn't do the work to change it :).

It is probably worth mentioning one more time that this is a **permanent,
indiscriminant delete of 1000 emails at a time**. These emails will *not* go to the trash, they will be deleted **forever**.

## Final thoughts

Use at your own risk, and be very careful!
