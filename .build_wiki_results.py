import json
import re
from pathlib import Path

ROOT = Path(r"C:\Users\suhas.bhandari\Downloads\Claude\Experiments\Elections")
OUT_BASE = ROOT / "hosted-json"
OUT_RESULTS = OUT_BASE / "results"
RAW_DIR = ROOT / "misc" / "raw-wiki"


def raw_file(name: str) -> Path:
    root_path = ROOT / name
    return root_path if root_path.exists() else (RAW_DIR / name)

STATE_FILES = {
    "ASSAM": raw_file(".assam_2021_wiki.raw.txt"),
    "KERALA": raw_file(".kerala_2021_wiki.raw.txt"),
    "PUDUCHERRY": raw_file(".puducherry_2021_wiki.raw.txt"),
    "TAMIL_NADU": raw_file(".tamil_nadu_2021_wiki.raw.txt"),
    "WEST_BENGAL": raw_file(".west_bengal_2021_wiki.raw.txt"),
}

# Canonical seat list from your active map sources
GEO_CANON = {
    "KERALA": ROOT / "data" / "geojson" / "KERALA_ASSEMBLY_optimized.geojson",
    "PUDUCHERRY": ROOT / "data" / "geojson" / "PUDUCHERRY_ASSEMBLY_optimized.geojson",
    "TAMIL_NADU": ROOT / "data" / "geojson" / "TAMIL_NADU_ASSEMBLY_optimized.geojson",
    "WEST_BENGAL": ROOT / "data" / "geojson" / "WEST_BENGAL_ASSEMBLY_optimized.geojson",
}
ASSAM_SVG = ROOT / "data" / "svg" / "ASSAM_2023_keyed.svg"

ALLIANCE_COLORS = {
    "NDA": "#FF9933",
    "MAHAJOT": "#00BFFF",
    "LDF": "#E31E24",
    "UDF": "#0078FF",
    "UPA": "#00BFFF",
    "SPA": "#DD1100",
    "TMC": "#23A455",
    "SM": "#D32F2F",
    "OTH": "#9CA3AF",
    "IND": "#6B7280",
}

PARTY_COLOR_HINTS = {
    "BJP": "#FF9933",
    "INC": "#00BFFF",
    "AIUDF": "#29A745",
    "AGP": "#FFA726",
    "UPPL": "#8BC34A",
    "BPF": "#4CAF50",
    "TMC": "#23A455",
    "AITC": "#23A455",
    "CPI(M)": "#D32F2F",
    "CPI": "#E53935",
    "RSP": "#C62828",
    "AIFB": "#B71C1C",
    "IUML": "#2E7D32",
    "DMK": "#DD1100",
    "AIADMK": "#1E88E5",
    "PMK": "#FF7043",
    "AINRC": "#FBC02D",
    "JD(S)": "#388E3C",
    "NCP": "#1976D2",
    "VCK": "#7B1FA2",
    "IND": "#6B7280",
    "RD": "#8D6E63",
    "GJM": "#8E24AA",
    "ISF": "#43A047",
}

PARTY_NORMALIZE = {
    "BHARATIYA JANATA PARTY": "BJP",
    "INDIAN NATIONAL CONGRESS": "INC",
    "TRINAMOOL CONGRESS": "TMC",
    "ALL INDIA TRINAMOOL CONGRESS": "TMC",
    "COMMUNIST PARTY OF INDIA (MARXIST)": "CPI(M)",
    "COMMUNIST PARTY OF INDIA": "CPI",
    "INDIAN UNION MUSLIM LEAGUE": "IUML",
    "DRAVIDA MUNNETRA KAZHAGAM": "DMK",
    "ALL INDIA ANNA DRAVIDA MUNNETRA KAZHAGAM": "AIADMK",
    "PATTALI MAKKAL KATCHI": "PMK",
    "ALL INDIA N.R. CONGRESS": "AINRC",
    "ASOM GANA PARISHAD": "AGP",
    "ALL INDIA UNITED DEMOCRATIC FRONT": "AIUDF",
    "BODOLAND PEOPLE'S FRONT": "BPF",
    "BODOLAND PEOPLES FRONT": "BPF",
    "UNITED PEOPLE'S PARTY LIBERAL": "UPPL",
    "REVOLUTIONARY SOCIALIST PARTY": "RSP",
    "ALL INDIA FORWARD BLOC": "AIFB",
    "FORWARD BLOC": "AIFB",
    "INDEPENDENT": "IND",
    "INDEPENDENT POLITICIAN": "IND",
    "RAIJOR DAL": "RD",
    "JANATA DAL (SECULAR)": "JD(S)",
    "NATIONALIST CONGRESS PARTY": "NCP",
    "INDIAN SECULAR FRONT": "ISF",
    "GORKHA JANMUKTI MORCHA": "GJM",
    "ADMK": "AIADMK",
    "IND.": "IND",
}

ASSAM_ALLIANCE = {
    "BJP": "NDA", "AGP": "NDA", "UPPL": "NDA",
    "INC": "MAHAJOT", "AIUDF": "MAHAJOT", "BPF": "MAHAJOT", "CPI": "MAHAJOT", "CPI(M)": "MAHAJOT", "RJD": "MAHAJOT",
}
KERALA_ALLIANCE = {
    "CPI(M)": "LDF", "CPI": "LDF", "JD(S)": "LDF", "NCP": "LDF",
    "INC": "UDF", "IUML": "UDF", "RSP": "UDF",
    "BJP": "NDA",
}
PUDUCHERRY_ALLIANCE = {
    "AINRC": "NDA", "BJP": "NDA", "AIADMK": "NDA",
    "INC": "UPA", "DMK": "UPA", "CPI": "UPA", "CPI(M)": "UPA", "VCK": "UPA",
}
TN_ALLIANCE = {
    "DMK": "SPA", "INC": "SPA", "CPI": "SPA", "CPI(M)": "SPA", "VCK": "SPA", "MDMK": "SPA", "IUML": "SPA",
    "KMDK": "SPA",
    "AIADMK": "NDA", "BJP": "NDA", "PMK": "NDA",
}
WB_ALLIANCE = {
    "TMC": "TMC", "AITC": "TMC",
    "BJP": "NDA", "GJM": "NDA",
    "INC": "SM", "CPI(M)": "SM", "CPI": "SM", "RSP": "SM", "AIFB": "SM", "ISF": "SM",
}


def clean_refs(s: str) -> str:
    s = re.sub(r"<ref[^>/]*/>", "", s)
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    return s


def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    return s


def unbold(s: str) -> str:
    return s.replace("'''", "").replace("''", "")


def decode_wikilinks(s: str) -> str:
    def repl(m):
        a = m.group(1)
        b = m.group(2)
        return (b or a).strip()
    s = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", repl, s)
    return s


def decode_templates_simple(s: str) -> str:
    # legend2 with explicit wikilink party
    m = re.search(r"\{\{\s*legend2\s*\|[^|]*\|\s*\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", s, flags=re.I)
    if m:
        return (m.group(2) or m.group(1)).strip()
    # party name with color template
    m = re.search(r"\{\{\s*(?:[Pp]arty name with color|[Pp]arty name with colour)\s*\|\s*([^}|]+)", s)
    if m:
        return m.group(1).strip()
    # fallback legend2 second arg if no wikilink
    m = re.search(r"\{\{\s*legend2\s*\|[^|]*\|\s*([^|}]+)", s, flags=re.I)
    if m:
        return m.group(1).strip()
    return s


def clean_cell(raw: str) -> str:
    s = clean_refs(raw)
    s = s.strip()
    # Pure formatting cells: style/bgcolor/align with no trailing value.
    if re.match(r"^(?:style|bgcolor|align|data-sort-type|rowspan|colspan)\s*=.*\|\s*$", s, flags=re.I):
        return ""
    # Trim style/bgcolor prefixes if present: style=...|value
    s = re.sub(r"^(?:style|bgcolor|align|data-sort-type|rowspan|colspan)[^|]*\|", "", s, flags=re.I)
    s = decode_templates_simple(s)
    s = decode_wikilinks(s)
    s = strip_tags(s)
    s = unbold(s)
    s = s.replace("&nbsp;", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def normalize_party(p: str) -> str:
    if not p:
        return "NA"
    p = decode_templates_simple(p)
    p = decode_wikilinks(p)
    p = strip_tags(p)
    p = unbold(p)
    p = p.strip()
    p = re.sub(r"[{}|\"`]+", " ", p)
    p = re.sub(r"\s+", " ", p).strip()
    p = p.strip(". ,;:-")
    if not p:
        return "NA"
    k = p.upper().strip()
    if k in PARTY_NORMALIZE:
        return PARTY_NORMALIZE[k]
    if k in {"IND", "INDEPENDENT"}:
        return "IND"
    if k.startswith("GJM"):
        return "GJM"
    # Already short code
    if re.fullmatch(r"[A-Z][A-Z0-9()\-.]{1,9}", p):
        return p
    # Normalize common uppercase long forms
    if "TRINAMOOL CONGRESS" in k:
        return "TMC"
    if "BHARATIYA JANATA PARTY" in k:
        return "BJP"
    if "INDIAN NATIONAL CONGRESS" in k:
        return "INC"
    # Last chance: keep uppercase acronym words
    if len(p) <= 12 and p.upper() == p:
        return p
    return p


def reserve_from_name(name: str) -> str:
    n = (name or "").upper()
    if "(SC)" in n:
        return "SC"
    if "(ST)" in n:
        return "ST"
    return "GEN"


def norm_name(s: str) -> str:
    s = (s or "").upper()
    s = re.sub(r"\(SC\)|\(ST\)", "", s)
    s = re.sub(r"[^A-Z0-9]+", "", s)
    return s


def load_geo_canonical(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    by_no = {}
    for f in data.get("features", []):
        p = f.get("properties", {})
        no = p.get("AC_NO")
        if no is None:
            continue
        no = int(no)
        if no not in by_no:
            by_no[no] = str(p.get("AC_NAME", "")).strip()
    return by_no


def load_assam_svg_canonical(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    out = {}
    for tag in re.findall(r"<polygon\b[^>]*>", text, flags=re.I):
        m_no = re.search(r"\bdata-ac-no\s*=\s*\"(\d+)\"", tag, flags=re.I)
        m_nm = re.search(r"\bdata-ac-name\s*=\s*\"([^\"]+)\"", tag, flags=re.I)
        if not m_no or not m_nm:
            continue
        no = int(m_no.group(1))
        if no not in out:
            out[no] = m_nm.group(1).strip()
    return out


def section_lines(text: str, state: str):
    lines = text.splitlines()
    start = None
    want = "BY CONSTITUENCY" if state in {"KERALA", "TAMIL_NADU"} else "RESULTS BY CONSTITUENCY"
    for i, ln in enumerate(lines):
        m = re.match(r"^={2,5}\s*([^=]+?)\s*={2,5}\s*$", ln)
        if not m:
            continue
        head = m.group(1).strip().upper()
        if head == want or (want in head):
            start = i + 1
            break
    if start is None:
        return []
    out = []
    for ln in lines[start:]:
        if re.match(r"^={2,5}\s*[^=]+?\s*={2,5}\s*$", ln):
            break
        out.append(ln)
    return out


def parse_rows(lines):
    rows = []
    cells = []
    for ln in lines:
        if ln.startswith("|-"):
            if cells:
                rows.append(cells)
                cells = []
            continue
        if not (ln.startswith("|") or ln.startswith("!")):
            continue
        if ln.startswith("|+"):
            continue
        body = ln[1:].strip()
        parts = body.split("||")
        for p in parts:
            cells.append(clean_cell(p))
    if cells:
        rows.append(cells)
    return rows


def extract_row_data(state: str, row):
    if not row:
        return None
    first = row[0].strip()
    m = re.match(r"^(\d{1,3})$", first)
    if not m:
        return None
    no = int(m.group(1))
    if len(row) < 4:
        return None

    name = row[1].strip()

    # Detect turnout column presence after name
    offset = 0
    if len(row) > 2 and re.match(r"^\d{1,3}(?:\.\d+)?$", row[2].replace(",", "")):
        offset = 1

    winner_candidate_idx = 2 + offset
    winner_candidate = row[winner_candidate_idx].strip() if winner_candidate_idx < len(row) else ""

    # Find first party-like cell after candidate
    winner_party = "NA"
    for i in range(winner_candidate_idx + 1, min(len(row), winner_candidate_idx + 7)):
        c = row[i].strip()
        if not c:
            continue
        if re.match(r"^\d[\d,]*(?:\.\d+)?$", c):
            continue
        p = normalize_party(c)
        # skip obvious non-party tokens
        if p.upper().startswith("BACKGROUND"):
            continue
        if "DISTRICT" in p.upper():
            continue
        if p == winner_candidate:
            continue
        if len(p) > 2 and len(p) < 40:
            winner_party = p
            break

    reserved = reserve_from_name(name)

    alliance = "OTH"
    if state == "ASSAM":
        alliance = ASSAM_ALLIANCE.get(winner_party, "OTH")
    elif state == "KERALA":
        # Kerala has explicit alliance in table at index 5 with turnout present
        ai = 5
        if ai < len(row):
            a = row[ai].strip().upper()
            if a in {"LDF", "UDF", "NDA"}:
                alliance = a
            else:
                alliance = KERALA_ALLIANCE.get(winner_party, "OTH")
        else:
            alliance = KERALA_ALLIANCE.get(winner_party, "OTH")
    elif state == "PUDUCHERRY":
        alliance = PUDUCHERRY_ALLIANCE.get(winner_party, "OTH")
    elif state == "TAMIL_NADU":
        alliance = TN_ALLIANCE.get(winner_party, "OTH")
    elif state == "WEST_BENGAL":
        alliance = WB_ALLIANCE.get(winner_party, "OTH")

    return {
        "no": no,
        "name": name,
        "winner": winner_candidate,
        "party": winner_party,
        "alliance": alliance,
        "reserved": reserved,
    }


def build_state_results(state: str, canonical_map: dict):
    text = STATE_FILES[state].read_text(encoding="utf-8", errors="ignore")
    lines = section_lines(text, state)
    rows = parse_rows(lines)
    parsed = {}
    for r in rows:
        d = extract_row_data(state, r)
        if not d:
            continue
        no = d["no"]
        # First valid row wins for that seat number
        if no not in parsed:
            parsed[no] = d

    out = []
    for no in sorted(canonical_map.keys()):
        cname = canonical_map[no]
        d = parsed.get(no)
        if d:
            reserved = d["reserved"]
            # prefer canonical name to keep map and sheet consistent
            row = {
                "no": str(no),
                "constituency_name": cname,
                "current_mla_name": d["winner"] or "NA",
                "current_mla_party": d["party"] or "NA",
                "current_mla_alliance": d["alliance"] or "OTH",
                "reserved": reserved if reserved in {"SC", "ST"} else reserve_from_name(cname),
            }
        else:
            row = {
                "no": str(no),
                "constituency_name": cname,
                "current_mla_name": "NA",
                "current_mla_party": "NA",
                "current_mla_alliance": "OTH",
                "reserved": reserve_from_name(cname),
            }
        out.append(row)
    return out, parsed


def deterministic_color(code: str) -> str:
    h = 0
    for ch in code:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    # simple HSV-ish mapping
    r = 80 + (h & 0x7F)
    g = 80 + ((h >> 8) & 0x7F)
    b = 80 + ((h >> 16) & 0x7F)
    return f"#{r:02x}{g:02x}{b:02x}"


def main():
    OUT_RESULTS.mkdir(parents=True, exist_ok=True)

    canonical = {}
    canonical["ASSAM"] = load_assam_svg_canonical(ASSAM_SVG)
    for st, p in GEO_CANON.items():
        canonical[st] = load_geo_canonical(p)

    all_results = {}
    parsed_by_state = {}
    for st in ["ASSAM", "KERALA", "PUDUCHERRY", "TAMIL_NADU", "WEST_BENGAL"]:
        rows, parsed = build_state_results(st, canonical[st])
        if st == "ASSAM":
            # Assam 2021 constituency numbering/names do not align with current 2023 map.
            # Avoid writing misleading mapped winners into the active map dataset.
            exact = sum(
                1 for no, cname in canonical[st].items()
                if no in parsed and norm_name(parsed[no]["name"]) == norm_name(cname)
            )
            if exact <= 10:
                legacy_rows = []
                for no in sorted(parsed.keys()):
                    d = parsed[no]
                    legacy_rows.append({
                        "no": str(no),
                        "constituency_name": d["name"],
                        "current_mla_name": d["winner"] or "NA",
                        "current_mla_party": d["party"] or "NA",
                        "current_mla_alliance": d["alliance"] or "OTH",
                        "reserved": d["reserved"] if d["reserved"] in {"SC", "ST"} else reserve_from_name(d["name"]),
                    })
                (OUT_RESULTS / "ASSAM_2021_legacy_results.json").write_text(
                    json.dumps(legacy_rows, ensure_ascii=False, indent=2), encoding="utf-8"
                )
                rows = [
                    {
                        "no": str(no),
                        "constituency_name": cname,
                        "current_mla_name": "NA",
                        "current_mla_party": "NA",
                        "current_mla_alliance": "OTH",
                        "reserved": reserve_from_name(cname),
                    }
                    for no, cname in sorted(canonical[st].items())
                ]
        all_results[st] = rows
        parsed_by_state[st] = parsed
        out_path = OUT_RESULTS / f"{st}_results.json"
        out_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    # parties.json + alliances.json for color modes
    parties = {}
    alliances_seen = set()
    for st, rows in all_results.items():
        for r in rows:
            party = (r.get("current_mla_party") or "NA").strip()
            alliance = (r.get("current_mla_alliance") or "OTH").strip().upper()
            if alliance:
                alliances_seen.add(alliance)
            if not party or party == "NA":
                continue
            if party not in parties:
                color = PARTY_COLOR_HINTS.get(party, deterministic_color(party))
                parties[party] = {
                    "code": party,
                    "name": party,
                    "color": color,
                    "alliances": {"2020": alliance if alliance else "OTH"},
                    "alliance_2020": alliance if alliance else "OTH",
                }

    alliances_out = {}
    for a in sorted(alliances_seen):
        alliances_out[a] = ALLIANCE_COLORS.get(a, deterministic_color(a))
    if "NA" not in alliances_out:
        alliances_out["NA"] = "#999999"

    (OUT_BASE / "parties.json").write_text(json.dumps(sorted(parties.values(), key=lambda x: x["code"]), ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_BASE / "alliances.json").write_text(json.dumps(alliances_out, ensure_ascii=False, indent=2), encoding="utf-8")

    # validation report
    print("Wrote results files:")
    for st in ["ASSAM", "KERALA", "PUDUCHERRY", "TAMIL_NADU", "WEST_BENGAL"]:
        total = len(all_results[st])
        parsed_n = len(parsed_by_state[st])
        missing = total - sum(1 for r in all_results[st] if r["current_mla_party"] != "NA")
        print(f"{st}: total={total}, parsed_rows={parsed_n}, filled={total-missing}, missing={missing}")


if __name__ == "__main__":
    main()
