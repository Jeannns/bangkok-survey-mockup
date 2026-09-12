"""
Flattens an exported copy of the "Responses" sheet (columns: code, status,
created_at, updated_at, data_json) into one column per survey question, for
analysis once fieldwork data starts coming in.

Usage:
    1. In the Google Sheet, File > Download > Comma Separated Values (.csv),
       save it as e.g. responses_raw.csv
    2. python3 flatten_responses.py responses_raw.csv responses_flat.xlsx

Notes:
    - Only rows with status == 'submitted' are included by default (pass
      --include-drafts to keep in-progress rows too).
    - The nested "A" object (all opts()/likert()/input answers, keyed by
      question id) is flattened with an "A." prefix per column, e.g.
      A.n_cars, A.p1_name, A.escort_reason_p2_3.
    - "characters" (the household roster) and "tripsByPerson" (the travel
      diary) are list/dict-shaped and are kept as raw JSON in their own
      columns rather than flattened, since their shape varies by household
      size - reshape those separately depending on the analysis (e.g. one
      row per person, or one row per trip segment).
"""
import argparse
import json
import sys

try:
    import pandas as pd
except ImportError:
    sys.exit("This script needs pandas: pip install pandas openpyxl --break-system-packages")


def flatten_answers(data):
    out = {}
    a = data.get('A', {})
    for k, v in a.items():
        out['A.' + k] = v
    out['characters_json'] = json.dumps(data.get('characters', []), ensure_ascii=False)
    out['tripsByPerson_json'] = json.dumps(data.get('tripsByPerson', {}), ensure_ascii=False)
    out['diaryDate'] = data.get('diaryDate', '')
    out['lang'] = data.get('lang', '')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input_csv')
    ap.add_argument('output_xlsx')
    ap.add_argument('--include-drafts', action='store_true', help='keep in_progress rows too, not just submitted')
    args = ap.parse_args()

    df = pd.read_csv(args.input_csv, dtype=str)
    required = {'code', 'status', 'created_at', 'updated_at', 'data_json'}
    missing = required - set(df.columns)
    if missing:
        sys.exit(f"Input is missing expected columns: {missing}")

    if not args.include_drafts:
        df = df[df['status'] == 'submitted']

    rows = []
    for _, r in df.iterrows():
        try:
            data = json.loads(r['data_json'] or '{}')
        except json.JSONDecodeError:
            data = {}
        flat = {'code': r['code'], 'status': r['status'], 'created_at': r['created_at'], 'updated_at': r['updated_at']}
        flat.update(flatten_answers(data))
        rows.append(flat)

    out = pd.DataFrame(rows)
    out.to_excel(args.output_xlsx, index=False)
    print(f"Wrote {args.output_xlsx}: {len(out)} respondents, {len(out.columns)} columns")


if __name__ == '__main__':
    main()
