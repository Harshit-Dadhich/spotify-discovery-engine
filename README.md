# AI-Powered Review Discovery Engine

Automated workflow: point it at any Play Store app → it scrapes live reviews →
Claude analyzes them for music-discovery insights (frustrations, segments, unmet needs).

## Deploy to Streamlit Community Cloud (free, ~2 minutes)

1. **Create a new GitHub repo** (e.g. `discovery-engine`) and upload these 3 files:
   - `app.py`
   - `requirements.txt`
   - `README.md`

   Easiest way: go to github.com/new → create repo → "uploading an existing file" → drag these 3 files in → commit.

2. **Go to** [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.

3. Click **"New app"** → select your `discovery-engine` repo → branch `main` → main file path `app.py` → **Deploy**.

4. Wait ~60-90 seconds. You'll get a public URL like:
   `https://your-app-name.streamlit.app`

5. **That's your public link** for Part 1 of the submission.

## How to use it once live

- Open the link.
- Paste your Claude API key in the sidebar (get one free at console.anthropic.com if you don't have one — a few cents of usage covers this whole project).
- Leave App ID as `com.spotify.music` (or change it to test any other app).
- Click **Scrape & Analyze**.
- It will pull live reviews from the Play Store right then, and Claude will return structured insights.

## Note on API key

The sidebar asks for a Claude API key so *anyone* opening your public link can run it
without you exposing your own key in the code (which would be a security risk on a public repo).
This is standard practice for public AI demos.
