#!/usr/bin/env python

from __future__ import print_function
import os
import httplib2
import time

from apiclient import discovery
from apiclient import errors
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
        flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
# Full access scope
# see more here https://developers.google.com/gmail/api/auth/scopes
SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client-secret.json'
APPLICATION_NAME = 'Gmail API batchDelete by Query'

# IMPORTANT #
# This query determines which emails will be returned for deletion.
# It is HIGHLY recommended to check this query in the UI before deletion.
# After deletion, THERE IS NO GOING BACK.
QUERY = 'from:root@'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
            Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def list_filtered_messages(service):
    user_id = "me"

    try:
        response = service.users().messages().list(userId=user_id,
                                                   q=QUERY).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(
                userId=user_id,
                q=QUERY,
                pageToken=page_token
            ).execute()
            messages.extend(response['messages'])
            if len(messages) > 999:
                break

        return messages
    except errors.HttpError, error:
        print('An error occurred: {0}'.format(error))


def prep_messages_for_delete(raw_messages):
    message = {
        'ids': []
    }

    message['ids'].extend([str(d['id']) for d in raw_messages])

    print("got {0} ids".format(len(message['ids'])))
    return message


def batch_delete_messages(service, messages):
    print("ready to delete {} messages".format(len(messages['ids'])))
    user_id = "me"

    try:
        service.users().messages().batchDelete(
            userId=user_id,
            body=messages
        ).execute()

        print("I deleted stuff!")
    except errors.HttpError, error:
        print('An error occurred while batchDeleting: {0}'.format(error))


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    i = 0

    while i < 600:
        raw_messages = list_filtered_messages(service)
        if raw_messages:
            print("got messages!")
            messages_list = prep_messages_for_delete(raw_messages)
            batch_delete_messages(service, messages_list)
        else:
            print("i got nothin")

        i = i + 1
        # Sleep allows some time for Gmail to perform the batchDelete in async.
        # The endpoint does not guarantee that the emails are gone by the next
        # call, and won't be sent again on the next call, so this tries to
        # prevent running a delete on the same emails twice.
        time.sleep(8)

if __name__ == '__main__':
    main()
