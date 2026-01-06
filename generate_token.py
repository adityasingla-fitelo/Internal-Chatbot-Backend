from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

flow = InstalledAppFlow.from_client_config(
    {
        "installed": {
            "client_id": "1030782714364-tedgc23hmqu8p5o241tja2mo7j0fgv6c.apps.googleusercontent.com",
            "client_secret": "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",
            "redirect_uris": ["http://localhost:8080/"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    },
    SCOPES,
)

creds = flow.run_local_server(port=8080)

print("REFRESH TOKEN:", creds.refresh_token)
