#!/usr/bin/env python3
"""gdocs.py — Google Docs API utility

Usage:
  python3 gdocs.py read --doc-id DOC_ID                # Print doc as markdown (tables preserved)
  python3 gdocs.py write --doc-id DOC_ID --file FILE   # Replace doc contents (markdown → native Docs formatting)
  python3 gdocs.py create --title TITLE --file FILE    # Create new doc, prints URL

DOC_ID can be a bare ID or a full Google Docs URL (the ID is extracted automatically).
Input/output format is markdown. Tables, headers, bold, links are preserved on read and write.

Configuration (environment variables):
  GOOGLE_OAUTH_CLIENT_FILE  Path to the OAuth client secrets JSON downloaded from
                            Google Cloud Console. Default: ~/.config/ai-cos/gcp-oauth.keys.json
  GOOGLE_TOKEN_FILE         Path where the cached user token is stored after the
                            first authorization. Default: ~/.config/ai-cos/google-token.json
"""

import argparse
import os
import re
import socket
import sys
import warnings

# Large docs export to multi-MB HTML and can take 60s+ to come back from the Drive
# export endpoint. The default socket timeout cuts these off mid-stream
# (socket.timeout). Raise it so slow large-doc reads/writes finish.
socket.setdefaulttimeout(300)

warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', message='.*NotOpenSSLWarning.*')
warnings.filterwarnings('ignore', message='.*urllib3.*')

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
from markdownify import markdownify as html_to_md
import markdown

SCOPES = [
    'https://www.googleapis.com/auth/documents',
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


def extract_doc_id(doc_id_or_url):
    """Extract bare doc ID from a URL or return the ID as-is."""
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', doc_id_or_url)
    return match.group(1) if match else doc_id_or_url


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


def _export_with_retry(drive_service, doc_id, mime_type, attempts=4):
    """Export a Doc via Drive, robust to large/slow exports.

    Large docs (multi-MB HTML) take 60s+ and Google frequently drops the
    connection mid-stream on a single buffered .execute() (RemoteDisconnected).
    Retry with increasing backoff so the throttle clears before retrying."""
    import time
    import http.client

    last_err = None
    for i in range(attempts):
        try:
            return drive_service.files().export(
                fileId=doc_id, mimeType=mime_type
            ).execute()
        except (http.client.RemoteDisconnected, http.client.IncompleteRead,
                ConnectionError, socket.timeout, OSError) as e:
            last_err = e
            # Google drops the connection (RemoteDisconnected) on rapid repeated
            # exports of a large doc -- abuse protection / throttling. Back off
            # with increasing sleeps so the throttle clears before retrying.
            if i < attempts - 1:
                wait = 10 * (2 ** i)  # 10s, 20s, 40s, ...
                sys.stderr.write(
                    f"export attempt {i + 1}/{attempts} failed "
                    f"({type(e).__name__}); backing off {wait}s...\n"
                )
                time.sleep(wait)
    raise last_err


_HEADING_PREFIX = {
    'TITLE': '# ', 'SUBTITLE': '## ',
    'HEADING_1': '# ', 'HEADING_2': '## ', 'HEADING_3': '### ',
    'HEADING_4': '#### ', 'HEADING_5': '##### ', 'HEADING_6': '###### ',
}


def _runs_to_md(elements):
    """Convert a paragraph's textRun elements to inline markdown."""
    out = []
    for el in elements:
        tr = el.get('textRun')
        if not tr:
            continue
        text = tr.get('content', '').replace('\xa0', ' ').replace('\x0b', '\n')
        text = text.rstrip('\n')
        if not text:
            continue
        style = tr.get('textStyle', {})
        if style.get('bold'):
            text = f'**{text}**'
        if style.get('italic'):
            text = f'*{text}*'
        link = style.get('link', {}).get('url')
        if link:
            text = f'[{text}]({link})'
        out.append(text)
    return ''.join(out)


def _docs_json_to_md(doc):
    """Convert a Docs API document() resource to markdown.

    Uses the Docs API (documents.get) instead of Drive HTML export -- the export
    endpoint throttles/drops the connection on large docs (multi-MB HTML); the
    Docs API returns compact structured JSON quickly on a separate quota."""
    lists = doc.get('lists', {})

    def is_ordered(list_id, level):
        try:
            glyph = lists[list_id]['listProperties']['nestingLevels'][level].get('glyphType', '')
        except (KeyError, IndexError):
            return False
        return any(k in glyph for k in ('DECIMAL', 'ALPHA', 'ROMAN', 'ZERO'))

    out = []

    def render(content):
        for block in content:
            para = block.get('paragraph')
            if para:
                text = _runs_to_md(para.get('elements', []))
                if not text.strip():
                    out.append('')
                    continue
                bullet = para.get('bullet')
                if bullet:
                    level = bullet.get('nestingLevel', 0)
                    indent = '    ' * level
                    marker = '1.' if is_ordered(bullet.get('listId', ''), level) else '-'
                    out.append(f'{indent}{marker} {text}')
                else:
                    named = para.get('paragraphStyle', {}).get('namedStyleType', 'NORMAL_TEXT')
                    out.append(_HEADING_PREFIX.get(named, '') + text)
                continue
            table = block.get('table')
            if table:
                rows = table.get('tableRows', [])
                for r_idx, row in enumerate(rows):
                    cells = []
                    for cell in row.get('cells', []):
                        parts = []
                        for c in cell.get('content', []):
                            cp = c.get('paragraph')
                            if cp:
                                parts.append(_runs_to_md(cp.get('elements', [])))
                        cells.append(' '.join(p for p in parts if p).strip())
                    out.append('| ' + ' | '.join(cells) + ' |')
                    if r_idx == 0:
                        out.append('| ' + ' | '.join('---' for _ in cells) + ' |')
                out.append('')
                continue
            toc = block.get('tableOfContents')
            if toc:
                render(toc.get('content', []))

    render(doc.get('body', {}).get('content', []))
    md = '\n'.join(out)
    md = re.sub(r'\n{3,}', '\n\n', md)
    return md.strip()


def _get_doc_with_retry(docs_service, doc_id, attempts=3):
    """documents.get with a small backoff for transient connection drops."""
    import time
    import http.client
    last_err = None
    for i in range(attempts):
        try:
            return docs_service.documents().get(documentId=doc_id).execute()
        except (http.client.RemoteDisconnected, http.client.IncompleteRead,
                ConnectionError, socket.timeout, OSError) as e:
            last_err = e
            if i < attempts - 1:
                time.sleep(5 * (2 ** i))
    raise last_err


def read_doc(doc_id):
    """Read a Google Doc as markdown via the Docs API (robust for large docs).

    Falls back to the Drive HTML export path if the Docs API call fails."""
    creds = get_credentials()
    try:
        docs_service = build('docs', 'v1', credentials=creds)
        doc = _get_doc_with_retry(docs_service, doc_id)
        print(_docs_json_to_md(doc))
        return
    except Exception as e:
        sys.stderr.write(
            f"Docs API read failed ({type(e).__name__}: {e}); "
            f"falling back to Drive HTML export...\n"
        )

    drive_service = build('drive', 'v3', credentials=creds)
    html_bytes = _export_with_retry(drive_service, doc_id, 'text/html')
    html_content = html_bytes.decode('utf-8')
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL)
    md_content = html_to_md(html_content, heading_style='ATX', bullets='-', strip=['img'])
    md_content = re.sub(r'\n{3,}', '\n\n', md_content)
    md_content = re.sub(r'\|(\s*\|)+\n\|\s*---', '| ---', md_content)
    print(md_content.strip())


def md_to_html(md_content):
    """Convert markdown to HTML suitable for Google Docs import."""
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'nl2br', 'sane_lists'],
    )
    # Wrap in basic HTML document for Drive API import
    return f"""<html>
<head><meta charset="utf-8"></head>
<body>{html_content}</body>
</html>"""


def write_doc(doc_id, content):
    """Replace Google Doc contents. Converts markdown → HTML → native Docs formatting."""
    creds = get_credentials()
    drive_service = build('drive', 'v3', credentials=creds)

    html_content = md_to_html(content)

    media = MediaInMemoryUpload(
        html_content.encode('utf-8'),
        mimetype='text/html',
        resumable=False
    )

    drive_service.files().update(
        fileId=doc_id,
        media_body=media,
        supportsAllDrives=True,
    ).execute()

    print(f"https://docs.google.com/document/d/{doc_id}/edit")


def create_doc(title, content):
    """Create a new Google Doc from markdown content."""
    creds = get_credentials()
    drive_service = build('drive', 'v3', credentials=creds)

    html_content = md_to_html(content)

    file_metadata = {
        'name': title,
        'mimeType': 'application/vnd.google-apps.document',
    }

    media = MediaInMemoryUpload(
        html_content.encode('utf-8'),
        mimetype='text/html',
        resumable=False
    )

    doc = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        supportsAllDrives=True,
    ).execute()

    doc_id = doc['id']
    print(f"https://docs.google.com/document/d/{doc_id}/edit")


def main():
    parser = argparse.ArgumentParser(description='Google Docs API utility')
    subparsers = parser.add_subparsers(dest='command')

    write_parser = subparsers.add_parser('write', help='Replace doc contents')
    write_parser.add_argument('--doc-id', required=True, help='Google Doc ID')
    write_parser.add_argument('--file', required=True, help='File with content to write')

    create_parser = subparsers.add_parser('create', help='Create new doc')
    create_parser.add_argument('--title', required=True, help='Document title')
    create_parser.add_argument('--file', required=True, help='File with content to write')

    read_parser = subparsers.add_parser('read', help='Print doc as markdown')
    read_parser.add_argument('--doc-id', required=True, help='Google Doc ID or URL')

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'read':
        read_doc(extract_doc_id(args.doc_id))
    else:
        with open(args.file, 'r') as f:
            content = f.read()
        doc_id = extract_doc_id(args.doc_id) if hasattr(args, 'doc_id') else None
        if args.command == 'write':
            write_doc(doc_id, content)
        elif args.command == 'create':
            create_doc(args.title, content)


if __name__ == '__main__':
    main()
