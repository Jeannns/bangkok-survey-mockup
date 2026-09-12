"""
Patch script (audit trail, not an active build pipeline): documents the "Level 2" graphic
upgrade to the SP scenario cards -- adding a small flat-style inline SVG "scene" per card
(escort by car/motorcycle, child travels alone by PT, third-party escort, School A/B),
replacing the plain emoji-in-a-box from the Level 1 upgrade (build_survey_mockup_5).

The scene bakes the option's actual danger/crime/trust values into the drawing itself
(hazard triangle count, a dark overlay for high crime risk, a colored trust badge) instead
of being purely decorative, so what the respondent sees stays tied to the real attribute
levels being tested. No external image files are used -- everything is generated inline as
SVG strings by JS functions -- so the mockup stays a single self-contained HTML file.

Run this against a checkout of the commit *before* this change to reproduce it, e.g.:
    git show <prev_commit>:survey_mockup.html > /tmp/survey_mockup_prev.html
    python3 build_survey_mockup_6_scene_illustrations.py /tmp/survey_mockup_prev.html /tmp/out.html
    diff /tmp/out.html survey_mockup.html   # should be empty
"""
import sys


def rep(text, old, new, expect=1):
    count = text.count(old)
    if count != expect:
        raise SystemExit(f"Expected {expect} occurrence(s) of {old!r}, found {count}")
    return text.replace(old, new)


ILLUSTRATION_JS = '''
/* Level-2 graphic upgrade: a small flat-style SVG "scene" per scenario card, replacing the plain
   emoji-in-a-box. Danger/crime/trust levels are drawn into the scene itself (hazard marks, a
   dark overlay for high crime risk, a trust badge) so the illustration reflects the actual
   attribute values for that option rather than being purely decorative. No external image
   files are used, so the mockup stays a single self-contained HTML file. */
function hazardMarks(level, color, yOffset){
  let out = '';
  const n = Math.max(0, Math.min(5, level|0));
  for(let i=0;i<n;i++){
    const x = 10 + i*15;
    const y = yOffset||8;
    out += `<polygon points="${x},${y} ${x+6},${y+11} ${x-6},${y+11}" fill="${color}" opacity="0.9"/><text x="${x}" y="${y+9}" font-size="7" fill="#fff" text-anchor="middle" font-weight="700">!</text>`;
  }
  return out;
}
function sceneWrap(inner, bg){
  return `<svg class="scene-illust" viewBox="0 0 220 110" xmlns="http://www.w3.org/2000/svg">
    <rect width="220" height="110" rx="14" fill="${bg}"/>
    ${inner}
  </svg>`;
}
function illustDrive(danger, isMoto){
  const road = `<rect x="0" y="82" width="220" height="28" fill="#94a3b8"/><rect x="0" y="82" width="220" height="4" fill="#e2e8f0"/>`;
  const trees = `<circle cx="20" cy="60" r="12" fill="#86efac"/><rect x="17" y="68" width="6" height="14" fill="#a16207"/><circle cx="200" cy="55" r="10" fill="#86efac"/><rect x="197" y="62" width="6" height="12" fill="#a16207"/>`;
  const vehicle = isMoto
    ? `<g transform="translate(85,50)"><circle cx="10" cy="34" r="9" fill="#1f2937"/><circle cx="52" cy="34" r="9" fill="#1f2937"/><path d="M8 34 L30 18 L46 18 L52 34" stroke="#7c3aed" stroke-width="6" fill="none" stroke-linecap="round"/><circle cx="30" cy="10" r="7" fill="#fbbf24"/></g>`
    : `<g transform="translate(60,44)"><rect x="0" y="18" width="100" height="26" rx="9" fill="#7c3aed"/><rect x="14" y="2" width="60" height="22" rx="6" fill="#a78bfa"/><rect x="20" y="6" width="20" height="13" rx="2" fill="#e0e7ff"/><rect x="48" y="6" width="20" height="13" rx="2" fill="#e0e7ff"/><circle cx="20" cy="48" r="9" fill="#1f2937"/><circle cx="80" cy="48" r="9" fill="#1f2937"/></g>`;
  return sceneWrap(`${trees}${road}${vehicle}${hazardMarks(danger,'#ef4444')}`, '#dbeafe');
}
function illustPT(danger, crime){
  const road = `<rect x="0" y="82" width="220" height="28" fill="#94a3b8"/>`;
  const stop = `<rect x="150" y="30" width="6" height="52" fill="#94a3b8"/><rect x="128" y="18" width="50" height="16" rx="3" fill="#3b82f6"/><text x="153" y="30" font-size="8" fill="#fff" text-anchor="middle" font-weight="700">BUS</text>`;
  const child = `<g transform="translate(38,46)"><circle cx="10" cy="0" r="9" fill="#fbbf24"/><rect x="2" y="9" width="16" height="26" rx="6" fill="#f97316"/></g>`;
  const crimeOverlay = crime>=4 ? `<rect width="220" height="110" rx="14" fill="#1e293b" opacity="0.32"/>` : '';
  const crimeMark = crime>=3 ? `<circle cx="196" cy="20" r="12" fill="#a855f7"/><text x="196" y="24" font-size="9" fill="#fff" text-anchor="middle" font-weight="700">!</text>` : '';
  return sceneWrap(`${road}${stop}${child}${crimeOverlay}${hazardMarks(danger,'#ef4444')}${crimeMark}`, '#e0f2fe');
}
function illustThirdParty(trust){
  const van = `<g transform="translate(50,38)"><rect x="0" y="16" width="104" height="36" rx="10" fill="#0ea5e9"/><rect x="10" y="2" width="42" height="22" rx="6" fill="#38bdf8"/><rect x="16" y="6" width="14" height="12" rx="2" fill="#e0f2fe"/><circle cx="22" cy="56" r="9" fill="#1f2937"/><circle cx="84" cy="56" r="9" fill="#1f2937"/></g>`;
  const trustColor = trust==='High' ? '#22c55e' : trust==='Low' ? '#ef4444' : '#f59e0b';
  const trustGlyph = trust==='High' ? '✓' : trust==='Low' ? '!' : '~';
  const badge = `<circle cx="190" cy="22" r="14" fill="${trustColor}"/><text x="190" y="27" font-size="10" fill="#fff" text-anchor="middle" font-weight="700">${trustGlyph}</text>`;
  return sceneWrap(`${van}${badge}`, '#f0fdf4');
}
function illustSchool(letter, accent){
  const building = `<rect x="58" y="42" width="104" height="54" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/><polygon points="58,42 110,16 162,42" fill="${accent}"/><rect x="96" y="66" width="28" height="30" fill="${accent}"/><rect x="68" y="54" width="16" height="16" fill="#bae6fd"/><rect x="136" y="54" width="16" height="16" fill="#bae6fd"/>`;
  const badge = `<circle cx="190" cy="22" r="16" fill="${accent}"/><text x="190" y="28" font-size="15" fill="#fff" text-anchor="middle" font-weight="800">${letter}</text>`;
  return sceneWrap(`${building}${badge}`, '#fefce8');
}
function sceneFor(cardIcon, opt){
  if(!opt) return '';
  if(cardIcon==='CAR') return illustDrive(opt.danger||0, false);
  if(cardIcon==='MOTO') return illustDrive(opt.danger||0, true);
  if(cardIcon==='BUS') return illustPT(opt.danger||0, opt.crime||0);
  if(cardIcon==='VAN') return illustThirdParty(opt.trust||'Medium');
  if(cardIcon==='A') return illustSchool('A', '#3b82f6');
  if(cardIcon==='B') return illustSchool('B', '#f97316');
  return '';
}'''


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "survey_mockup.html"
    dst = sys.argv[2] if len(sys.argv) > 2 else src
    html = open(src, encoding="utf-8").read()

    # --- SECTION A: CSS for the new .scene-illust element ---
    html = rep(
        html,
        ".opt-card .icon{font-size:26px;line-height:1;margin-bottom:8px}",
        ".opt-card .icon{font-size:26px;line-height:1;margin-bottom:8px}\n"
        ".opt-card .scene-illust{width:100%;height:auto;border-radius:12px;margin-bottom:10px;display:block}",
    )

    # --- SECTION B: append the illustration generator functions right after iconGlyph() ---
    html = rep(
        html,
        "function iconGlyph(code){ return ICON_MAP[code] || code; }",
        "function iconGlyph(code){ return ICON_MAP[code] || code; }\n" + ILLUSTRATION_JS,
    )

    # --- SECTION C: scenarioCard() takes an extra `opt` (raw option object) param and renders
    # the scene above the title, falling back to the plain emoji icon if no scene matches ---
    html = rep(
        html,
        "function scenarioCard(title,cardIcon,rows,selKey,idx,note){\n"
        "  const selected = A[selKey]===idx;\n"
        '  return `<div class="opt-card ${selected?\'selected\':\'\'}" onclick="A[\'${selKey}\']=${idx};renderSP()">\n'
        '    <span class="pick-badge">${t(\'Your choice\')}</span>\n'
        '    <div class="icon">${iconGlyph(cardIcon)}</div>\n'
        '    <div class="opt-title">${t(title)}</div>\n'
        "    ${note?`<div class=\"q-help\" style=\"margin-bottom:8px\">${note}</div>`:''}\n"
        "    ${rows.map(r=>`<div class=\"attr-row\"><span class=\"ic\">${iconGlyph(r.icon)}</span> ${t(r.label)}${r.ctrl?` <span style=\"color:var(--purple);font-weight:700;font-size:10px\">(${t('Ctrl')})</span>`:''} ${r.bar?r.bar:`<b>${r.value}</b>`}</div>`).join('')}\n"
        "  </div>`;\n"
        "}",
        "function scenarioCard(title,cardIcon,rows,selKey,idx,note,opt){\n"
        "  const selected = A[selKey]===idx;\n"
        "  const scene = sceneFor(cardIcon, opt);\n"
        '  return `<div class="opt-card ${selected?\'selected\':\'\'}" onclick="A[\'${selKey}\']=${idx};renderSP()">\n'
        '    <span class="pick-badge">${t(\'Your choice\')}</span>\n'
        "    ${scene || `<div class=\"icon\">${iconGlyph(cardIcon)}</div>`}\n"
        '    <div class="opt-title">${t(title)}</div>\n'
        "    ${note?`<div class=\"q-help\" style=\"margin-bottom:8px\">${note}</div>`:''}\n"
        "    ${rows.map(r=>`<div class=\"attr-row\"><span class=\"ic\">${iconGlyph(r.icon)}</span> ${t(r.label)}${r.ctrl?` <span style=\"color:var(--purple);font-weight:700;font-size:10px\">(${t('Ctrl')})</span>`:''} ${r.bar?r.bar:`<b>${r.value}</b>`}</div>`).join('')}\n"
        "  </div>`;\n"
        "}",
    )

    # --- SECTION D: pass the raw option object `o` through to scenarioCard so it can build
    # the illustration from the option's actual danger/crime/trust values ---
    html = rep(
        html,
        "<div class=\"option-row\">${sc.options.map((o,oi)=>scenarioCard(o.title,o.icon,rowsFn(o),selKey,oi,o.fixed?t('(reference only - based on your earlier answers)'):null)).join('')}</div>",
        "<div class=\"option-row\">${sc.options.map((o,oi)=>scenarioCard(o.title,o.icon,rowsFn(o),selKey,oi,o.fixed?t('(reference only - based on your earlier answers)'):null,o)).join('')}</div>",
    )

    open(dst, "w", encoding="utf-8").write(html)
    print(f"Wrote {dst} ({len(html)} chars)")


if __name__ == "__main__":
    main()
