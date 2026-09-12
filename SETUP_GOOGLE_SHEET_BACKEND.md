# Connecting the RP mockup to a Google Sheet

`survey_mockup.html` can now save real answers to a Google Sheet instead of just running in-memory. This is off by default (`API_URL` is empty, so Save/Submit show a "demo mode - not saved" message) - follow the steps below to turn it on.

## How it works

- The survey has **one shared link** for everyone (no pre-generated per-household links, since there's no fixed recruitment list to hand them out to).
- The first time someone opens the page, it silently generates a random **progress code** (e.g. `XK7T-2931`) and stores it in that browser's `localStorage`. This code is shown on the Welcome screen.
- Pressing **Save draft** sends the current answers to the Sheet, tagged with that code. Opening the survey again on the same device/browser resumes automatically. On a different device, entering the same code in the "Resume" box on the Welcome screen pulls the saved answers back down.
- Pressing **Submit Survey** sends a final copy and marks that row `submitted`.
- Because there's no pre-registered household list, duplicate prevention is soft: a submitted flag is kept in that browser's `localStorage` so the same device won't be shown an easy way to resubmit, but nothing stops someone from using a second device. Plan to de-duplicate at the data-cleaning stage instead (e.g. flag rows with matching household composition + home location).

## Setup steps

1. **Create a new Google Sheet.** Any name is fine (e.g. "Bangkok School Escorting Survey - Responses"). Leave it empty - the script creates its own "Responses" tab automatically the first time it runs.
2. In the Sheet, go to **Extensions > Apps Script**.
3. Delete the placeholder `Code.gs` content and paste in the contents of `google_apps_script/Code.gs` from this repo.
4. Click **Deploy > New deployment**.
   - Select type: **Web app**.
   - Execute as: **Me**.
   - Who has access: **Anyone**.
5. Click **Deploy**, authorize the script when prompted (it only needs access to this one Sheet), and copy the **Web app URL** it gives you (ends in `/exec`).
6. Open `survey_mockup.html`, find this line near the top of the `<script>` block:
   ```js
   const API_URL = ''; // <- paste your Apps Script Web App URL here after deploying
   ```
   and paste the URL between the quotes.
7. Reload the page. Try filling in a few answers, press **Save draft**, then check the Sheet - a new row should appear in the "Responses" tab with your progress code and a `data_json` column holding your answers.

## If you change the questionnaire later

Every answer is stored as a single JSON blob per respondent row, not one spreadsheet column per question - so adding, renaming, or removing questions in the mockup never requires touching `Code.gs` or the Sheet's columns. When you're ready to analyze the data, use `google_apps_script/flatten_responses.py` to expand that JSON into one column per question:

```
# In the Sheet: File > Download > Comma Separated Values (.csv)
python3 flatten_responses.py responses_raw.csv responses_flat.xlsx
```

## Re-deploying after editing Code.gs

If you edit `Code.gs` later, you need **Deploy > Manage deployments > Edit (pencil icon) > New version** for the change to take effect - saving the script alone does not update the live Web App.

## Known limitations to revisit before real fieldwork

- **Redeployment note above** - easy to forget and debug the wrong version.
- **Household location privacy** - `data_json` will include whatever precision the home-location picker captures. Decide before fieldwork whether to store it as-is or generalize it (the questionnaire's own notes suggest anonymizing to below street level, or falling back to district/postcode).
- **Apps Script quotas** - fine at this survey's scale (500-1,000 respondents), but each Google account has a daily quota on Apps Script executions; if the account has other heavy scripts running, keep an eye on quota usage during fieldwork.
- **No enforcement of "one link per person"** - since there's no household list, anyone with the link can start a response. This was an intentional trade-off (see the design discussion in the chat that led to this file) given there's no fixed distribution list to assign links against.
