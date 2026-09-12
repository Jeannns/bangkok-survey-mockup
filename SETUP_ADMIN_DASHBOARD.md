# Setting up the restricted admin dashboard

This is a **separate tool** from the survey itself, for you to privately check incoming responses (counts, a filterable/groupable chart, a recent-responses table) while fieldwork is running. It reads the same Google Sheet the survey writes to, but lives at its own URL, deployed with access locked to your Google account only. Nobody who has the survey link can find or reach this - there is no link between them.

## Why a separate Apps Script project

The survey's own backend (`google_apps_script/Code.gs`) has to be deployed with **Who has access: Anyone**, since real respondents (who aren't logged into anything) need to reach it. This dashboard needs the opposite - **Who has access: Only myself**. Apps Script's access setting applies to an entire deployment, not to individual actions inside one script, so the only safe way to have one "Anyone" endpoint and one "Only myself" endpoint is to keep them as two completely separate Apps Script projects. That's why `Dashboard.gs` is its own file/project, not an addition to `Code.gs`.

## Setup steps

1. Open the same Google Sheet the survey backend writes to (the one you deployed `Code.gs` on). Copy its **Sheet ID** from the browser address bar:
   ```
   https://docs.google.com/spreadsheets/d/  THIS_LONG_ID_HERE  /edit
   ```
2. Go to **script.google.com** (not through Extensions this time - open a brand new, standalone project) and click **New project**.
3. Delete the placeholder code and paste in the contents of `google_apps_script_dashboard/Dashboard.gs` from this repo.
4. Find this line near the top and paste in the Sheet ID from step 1:
   ```js
   const SHEET_ID = ''; // <- paste the Google Sheet ID here (the long id in its URL)
   ```
5. Click **Deploy > New deployment**.
   - Select type: **Web app**.
   - Execute as: **Me**.
   - Who has access: **Only myself**. (This is the important difference from the survey's own deployment - do not set this to "Anyone".)
6. Click **Deploy**, authorize when prompted, and copy the **Web app URL**.
7. Open that URL in your browser. Since it's restricted to your account, Google may ask you to confirm/sign in first - that's expected. You should then see the dashboard: total/submitted/in-progress counts, a chart you can group and filter by any answered field, and a table of the most recent responses.
8. Bookmark this URL. It's yours alone - it doesn't appear anywhere in the public survey.

## Using the dashboard

- **Group by**: pick any question to see a bar chart of how many respondents answered each value.
- **Filter by**: optionally narrow to one value of a second question first (e.g. filter to `income = 15,000-30,000`, then group by `escort_mode`).
- **Include**: submitted-only (default) or submitted + in-progress drafts.
- **Auto-refresh**: on by default, polls every 30 seconds. Turn off with the checkbox, or click "Refresh now" any time.
- The field lists are discovered dynamically from whatever's actually in the data, so if you add/remove survey questions later, the dropdowns update on their own with no changes needed here.

## Giving teammates access later

When you're ready to add people: **Deploy > Manage deployments > Edit (pencil) > Who has access**, change to a specific list and add their email addresses (they'll need a Google account), or switch to "Anyone within [your Google Workspace domain]" if you're all on the same organization's Workspace. Re-deploy (new version) for the change to apply.

## Notes

- This dashboard only reads data - it never writes to the Sheet, so it can't corrupt or overwrite survey responses.
- If you edit `Dashboard.gs` later, remember the same rule as the survey backend: saving the script alone doesn't update the live URL - use **Manage deployments > Edit > New version**.
