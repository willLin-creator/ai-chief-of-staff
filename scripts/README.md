# scripts/

Command-line utilities for reading and writing Google Docs and Google Sheets via the
official Google APIs. They share one OAuth flow and one cached token.

## Scripts

### `gdocs.py` — Google Docs

Reads and writes Google Docs as Markdown. Tables, headers, bold, italic, and links are
preserved in both directions.

```bash
# Read a doc as Markdown (accepts a bare ID or a full Docs URL)
python3 gdocs.py read --doc-id DOC_ID

# Replace a doc's contents from a Markdown file
python3 gdocs.py write --doc-id DOC_ID --file content.md

# Create a new doc from a Markdown file (prints the new doc URL)
python3 gdocs.py create --title "My Doc" --file content.md
```

Reads go through the Docs API (`documents.get`) for speed and reliability on large docs,
with a Drive HTML-export fallback if that call fails.

### `gsheets.py` — Google Sheets

Reads and writes Google Sheets as CSV.

```bash
# Read a sheet as CSV (defaults to the first sheet if no range given)
python3 gsheets.py read --sheet-id SHEET_ID [--range "Sheet1!A1:Z100"]

# Overwrite a sheet from a CSV file
python3 gsheets.py write --sheet-id SHEET_ID --file data.csv [--range "Sheet1!A1"]

# Update specific cells with a JSON array of values
python3 gsheets.py update --sheet-id SHEET_ID --range "Sheet1!B2:B5" --values '["x","y","z","w"]'
```

`SHEET_ID` and `DOC_ID` may be either a bare ID or a full Google URL — the ID is
extracted automatically.

## Dependencies

```bash
pip install google-auth google-auth-oauthlib google-api-python-client markdownify markdown
```

(`google-auth google-auth-oauthlib google-api-python-client` are the core Google API
packages. `markdownify` and `markdown` are used only by `gdocs.py` for Markdown ↔ HTML
conversion.)

## Configuration

Both scripts read two environment variables. See [`../.env.example`](../.env.example)
for the canonical list and defaults.

| Variable | Purpose | Default |
|----------|---------|---------|
| `GOOGLE_OAUTH_CLIENT_FILE` | Path to your OAuth **client** secrets JSON (downloaded from Google Cloud Console) | `~/.config/ai-cos/gcp-oauth.keys.json` |
| `GOOGLE_TOKEN_FILE` | Path where the cached user **token** is written after first authorization | `~/.config/ai-cos/google-token.json` |

Neither file is committed to the repo. Keep both out of version control.

## One-time OAuth authorization

1. **Create a Google Cloud project** and enable the **Google Docs API**, **Google Sheets
   API**, and **Google Drive API**.
2. **Create OAuth client credentials** of type *Desktop app* and download the client
   secrets JSON.
3. **Place the file** at the path in `GOOGLE_OAUTH_CLIENT_FILE` (default
   `~/.config/ai-cos/gcp-oauth.keys.json`), creating the directory if needed:
   ```bash
   mkdir -p ~/.config/ai-cos
   mv ~/Downloads/client_secret_*.json ~/.config/ai-cos/gcp-oauth.keys.json
   ```
4. **Run any command once.** On first run the script opens a browser for you to grant
   access, then writes the resulting token to `GOOGLE_TOKEN_FILE`:
   ```bash
   python3 gdocs.py read --doc-id YOUR_DOC_ID_HERE
   ```
   Subsequent runs reuse and silently refresh the cached token — no browser prompt.

To re-authorize (for example after changing accounts or scopes), delete the token file
and run any command again:

```bash
rm "$GOOGLE_TOKEN_FILE"   # or the default ~/.config/ai-cos/google-token.json
```
