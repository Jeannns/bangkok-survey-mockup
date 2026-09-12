"""
Patch script (audit trail, not an active build pipeline): removes the small purple "(Ctrl)"
label that used to appear next to each control-attribute row in the SP scenario cards
(scenarioCard's rows.map(...) in Module 1 / Module 2). The `ctrl:true` flag stays on the row
data itself (still useful internally / for future reference), only the visible label is gone.

Run this against a checkout of the commit *before* this change to reproduce it, e.g.:
    git show <prev_commit>:survey_mockup.html > /tmp/survey_mockup_prev.html
    python3 build_survey_mockup_7_remove_ctrl_label.py /tmp/survey_mockup_prev.html /tmp/out.html
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

    html = rep(
        html,
        "    ${rows.map(r=>`<div class=\"attr-row\"><span class=\"ic\">${iconGlyph(r.icon)}</span> ${t(r.label)}${r.ctrl?` <span style=\"color:var(--purple);font-weight:700;font-size:10px\">(${t('Ctrl')})</span>`:''} ${r.bar?r.bar:`<b>${r.value}</b>`}</div>`).join('')}",
        "    ${rows.map(r=>`<div class=\"attr-row\"><span class=\"ic\">${iconGlyph(r.icon)}</span> ${t(r.label)} ${r.bar?r.bar:`<b>${r.value}</b>`}</div>`).join('')}",
    )

    open(dst, "w", encoding="utf-8").write(html)
    print(f"Wrote {dst} ({len(html)} chars)")


if __name__ == "__main__":
    main()
