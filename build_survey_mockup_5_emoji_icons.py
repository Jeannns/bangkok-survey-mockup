"""
Patch script (audit trail, not an active build pipeline): documents the "Level 1" graphic
upgrade to the SP scenario cards -- replacing plain text-code icons (e.g. "CAR", "BUS", "A")
with real emoji glyphs, via an ICON_MAP lookup so the underlying data codes (used elsewhere
for logic) don't need to change.

Rationale for this being a lookup-table approach rather than editing each of the ~24 places
that set icon:'CAR' / icon:'BUS' / etc.: keeps the data layer (semantic codes) separate from
the presentation layer (what glyph is shown), so a future icon change is a one-line edit to
ICON_MAP instead of a find-and-replace across every scenario definition.

Run this against a checkout of the commit *before* this change to reproduce it, e.g.:
    git show <prev_commit>:survey_mockup.html > /tmp/survey_mockup_prev.html
    python3 build_survey_mockup_5_emoji_icons.py /tmp/survey_mockup_prev.html /tmp/out.html
    diff /tmp/out.html survey_mockup.html   # should be empty
"""
import sys


def rep(text, old, new, expect=1):
    count = text.count(old)
    if count != expect:
        raise SystemExit(f"Expected {expect} occurrence(s) of {old!r}, found {count}")
    return text.replace(old, new)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "survey_mockup.html"
    dst = sys.argv[2] if len(sys.argv) > 2 else src
    html = open(src, encoding="utf-8").read()

    # --- SECTION A: bump icon font sizes so emoji read clearly, drop the old bold-purple
    # text-label styling (font-weight/letter-spacing/color only made sense for text codes) ---
    html = rep(
        html,
        '.opt-card .icon{font-size:13px;font-weight:800;letter-spacing:.03em;color:var(--purple);margin-bottom:8px}\n'
        '.opt-card .opt-title{font-weight:700;font-size:15.5px;margin-bottom:12px}\n'
        '.attr-row{display:flex;align-items:center;gap:8px;font-size:13px;margin-bottom:8px;color:var(--ink)}\n'
        '.attr-row .ic{width:20px;text-align:center;flex-shrink:0;color:var(--sub);font-size:11px}',
        '.opt-card .icon{font-size:26px;line-height:1;margin-bottom:8px}\n'
        '.opt-card .opt-title{font-weight:700;font-size:15.5px;margin-bottom:12px}\n'
        '.attr-row{display:flex;align-items:center;gap:8px;font-size:13px;margin-bottom:8px;color:var(--ink)}\n'
        '.attr-row .ic{width:20px;text-align:center;flex-shrink:0;font-size:14px}',
    )

    # --- SECTION B: add the ICON_MAP lookup + iconGlyph() helper right after dangerBar() ---
    html = rep(
        html,
        "function dangerBar(level){\n"
        "  let s='';\n"
        "  for(let i=1;i<=5;i++) s+=`<span class=\"${i<=level?'on':''}\"></span>`;\n"
        "  return `<div class=\"danger-bar\">${s}</div>`;\n"
        "}",
        "function dangerBar(level){\n"
        "  let s='';\n"
        "  for(let i=1;i<=5;i++) s+=`<span class=\"${i<=level?'on':''}\"></span>`;\n"
        "  return `<div class=\"danger-bar\">${s}</div>`;\n"
        "}\n"
        "\n"
        "/* Level-1 graphic upgrade: map each internal icon code (kept as-is for data/logic) to a real\n"
        "   emoji glyph shown to the respondent, instead of the old plain text label (e.g. \"CAR\", \"BUS\"). */\n"
        "const ICON_MAP = {\n"
        "  CAR:'\\u{1F697}', MOTO:'\\u{1F3CD}\\u{FE0F}', BUS:'\\u{1F68C}', VAN:'\\u{1F690}',\n"
        "  A:'\\u{24B6}', B:'\\u{24B7}',\n"
        "  TIME:'\\u{23F1}\\u{FE0F}', WAIT:'\\u{23F3}', WALK:'\\u{1F6B6}', FARE:'\\u{1F4B5}',\n"
        "  TRAF:'\\u{1F6A6}', CRIME:'\\u{1F6A8}', COMP:'\\u{1F465}', TRUST:'\\u{1F91D}',\n"
        "  FEE:'\\u{1F4B0}', REP:'\\u{2B50}', TYPE:'\\u{1F3EB}', SIZE:'\\u{1F9D1}\\u{200D}\\u{1F91D}\\u{200D}\\u{1F9D1}',\n"
        "  MODE:'\\u{1F6E3}\\u{FE0F}', SAFE:'\\u{1F6E1}\\u{FE0F}'\n"
        "};\n"
        "function iconGlyph(code){ return ICON_MAP[code] || code; }",
    )

    # --- SECTION C: scenarioCard() renders the mapped glyph instead of the raw code ---
    html = rep(
        html,
        '    <div class="icon">${cardIcon}</div>\n'
        "    <div class=\"opt-title\">${t(title)}</div>\n"
        "    ${note?`<div class=\"q-help\" style=\"margin-bottom:8px\">${note}</div>`:''}\n"
        "    ${rows.map(r=>`<div class=\"attr-row\"><span class=\"ic\">${r.icon}</span> ${t(r.label)}${r.ctrl?` <span style=\"color:var(--purple);font-weight:700;font-size:10px\">(${t('Ctrl')})</span>`:''} ${r.bar?r.bar:`<b>${r.value}</b>`}</div>`).join('')}",
        '    <div class="icon">${iconGlyph(cardIcon)}</div>\n'
        "    <div class=\"opt-title\">${t(title)}</div>\n"
        "    ${note?`<div class=\"q-help\" style=\"margin-bottom:8px\">${note}</div>`:''}\n"
        "    ${rows.map(r=>`<div class=\"attr-row\"><span class=\"ic\">${iconGlyph(r.icon)}</span> ${t(r.label)}${r.ctrl?` <span style=\"color:var(--purple);font-weight:700;font-size:10px\">(${t('Ctrl')})</span>`:''} ${r.bar?r.bar:`<b>${r.value}</b>`}</div>`).join('')}",
    )

    open(dst, "w", encoding="utf-8").write(html)
    print(f"Wrote {dst} ({len(html)} chars)")


if __name__ == "__main__":
    main()
