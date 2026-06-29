#!/usr/bin/env python3
"""gsheets.py — Google Sheets API utility

Usage:
  python3 gsheets.py read --sheet-id SHEET_ID [--range "Sheet1!A1:Z100"]   # Print as CSV
  python3 gsheets.py write --sheet-id SHEET_ID --file FILE [--range "Sheet1!A1"]  # Write CSV to sheet
  python3 gsheets.py update --sheet-id SHEET_ID --range "Sheet1!B2:B5" --values '["x","y","z","w"]'  # Update specific cells

SHEET_ID can be a bare ID or a full Google Sheets URL (the ID is extracted automatically).

Configuration (environment variables):
  GOOGLE_OAUTH_CLIENT_FILE  Path to the OAuth client secrets JSON downloaded from
                            Google Cloud Console. Default: ~/.config/ai-cos/gcp-oauth.keys.json
  GOOGLE_TOKEN_FILE         Path where the cached user token is stored after the
                            first authorization. Default: ~/.config/ai-cos/google-token.json
"""

import argparse
import csv
import io
import json
import os
import re
import sys
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', message='.*NotOpenSSLWarning.*')
warnings.filterwarnings('ignore', message='.*urllib3.*')

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]
CREDENTIALS_PATH = os.environ.get(
    "GOOGLE_OAUTH_CLIENT_FILE",
    os.path.expanduser("~/.config/ai-cos/gcp-oauth.keys.json"),
)
TOKEN_PATH = os.environ.get(
    "GOOGLE_TOKEN_FILE",
    os.path.expanduser("~/.config/ai-cos/google-token.json"),
)


def extract_sheet_id(sheet_id_or_url):
    """Extract bare sheet ID from a URL or return the ID as-is."""
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', sheet_id_or_url)
    return match.group(1) if match else sheet_id_or_url


def get_credentials():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
        with open(TOKEN_PATH, 'w') as f:
            f.write(creds.to_json())
    return creds


def get_sheets_service():
    creds = get_credentials()
    return build('sheets', 'v4', credentials=creds)


def read_sheet(sheet_id, range_name=None):
    """Read a Google Sheet and print as CSV."""
    service = get_sheets_service()

    if not range_name:
        # Get sheet metadata to find the first sheet name
        meta = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        first_sheet = meta['sheets'][0]['properties']['title']
        range_name = first_sheet

    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=range_name,
    ).execute()

    rows = result.get('values', [])

    output = io.StringIO()
    writer = csv.writer(output)
    for row in rows:
        writer.writerow(row)

    print(output.getvalue().strip())


def write_sheet(sheet_id, filepath, range_name=None):
    """Write a CSV file to a Google Sheet."""
    service = get_sheets_service()

    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        values = list(reader)

    if not range_name:
        meta = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        first_sheet = meta['sheets'][0]['properties']['title']
        range_name = f"{first_sheet}!A1"

    # Clear existing content first
    sheet_name = range_name.split('!')[0] if '!' in range_name else range_name
    try:
        service.spreadsheets().values().clear(
            spreadsheetId=sheet_id,
            range=sheet_name,
        ).execute()
    except Exception:
        pass

    body = {'values': values}
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=body,
    ).execute()

    print(f"Wrote {len(values)} rows to https://docs.google.com/spreadsheets/d/{sheet_id}/edit")


def update_cells(sheet_id, range_name, values):
    """Update specific cells in a Google Sheet."""
    service = get_sheets_service()

    # values can be a flat list (single column) or list of lists
    if values and not isinstance(values[0], list):
        values = [[v] for v in values]

    body = {'values': values}
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=body,
    ).execute()

    print(f"Updated {range_name} in https://docs.google.com/spreadsheets/d/{sheet_id}/edit")


def main():
    parser = argparse.ArgumentParser(description='Google Sheets API utility')
    subparsers = parser.add_subparsers(dest='command')

    read_parser = subparsers.add_parser('read', help='Read sheet as CSV')
    read_parser.add_argument('--sheet-id', required=True, help='Google Sheet ID or URL')
    read_parser.add_argument('--range', dest='range_name', help='Range (e.g., "Sheet1!A1:Z100")')

    write_parser = subparsers.add_parser('write', help='Write CSV to sheet')
    write_parser.add_argument('--sheet-id', required=True, help='Google Sheet ID or URL')
    write_parser.add_argument('--file', required=True, help='CSV file to write')
    write_parser.add_argument('--range', dest='range_name', help='Start range (e.g., "Sheet1!A1")')

    update_parser = subparsers.add_parser('update', help='Update specific cells')
    update_parser.add_argument('--sheet-id', required=True, help='Google Sheet ID or URL')
    update_parser.add_argument('--range', dest='range_name', required=True, help='Range (e.g., "Sheet1!B2:B5")')
    update_parser.add_argument('--values', required=True, help='JSON array of values')

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    sheet_id = extract_sheet_id(args.sheet_id)

    if args.command == 'read':
        read_sheet(sheet_id, args.range_name)
    elif args.command == 'write':
        write_sheet(sheet_id, args.file, args.range_name)
    elif args.command == 'update':
        values = json.loads(args.values)
        update_cells(sheet_id, args.range_name, values)


if __name__ == '__main__':
    main()
