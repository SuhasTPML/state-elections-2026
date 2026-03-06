import json
import re
from pathlib import Path

ROOT = Path(r"C:\Users\suhas.bhandari\Downloads\Claude\Experiments\Elections")
RESULTS_DIR = ROOT / "hosted-json" / "results"

STATE_2016_FILES = {
    "ASSAM": ROOT / ".assam_2016_wiki.raw.txt",
    "KERALA": ROOT / ".kerala_2016_wiki.raw.txt",
    "PUDUCHERRY": ROOT / ".puducherry_2016_wiki.raw.txt",
    "TAMIL_NADU": ROOT / ".tamil_nadu_2016_wiki.raw.txt",
    "WEST_BENGAL": ROOT / ".west_bengal_2016_wiki.raw.txt",
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
    "BJP": "NDA",
    "AGP": "NDA",
    "UPPL": "NDA",
    "INC": "MAHAJOT",
    "AIUDF": "MAHAJOT",
    "BPF": "MAHAJOT",
    "CPI": "MAHAJOT",
    "CPI(M)": "MAHAJOT",
    "RJD": "MAHAJOT",
}
KERALA_ALLIANCE = {
    "CPI(M)": "LDF",
    "CPI": "LDF",
    "JD(S)": "LDF",
    "NCP": "LDF",
    "INC": "UDF",
    "IUML": "UDF",
    "RSP": "UDF",
    "BJP": "NDA",
}
PUDUCHERRY_ALLIANCE = {
    "AINRC": "NDA",
    "BJP": "NDA",
    "AIADMK": "NDA",
    "INC": "UPA",
    "DMK": "UPA",
    "CPI": "UPA",
    "CPI(M)": "UPA",
    "VCK": "UPA",
}
TN_ALLIANCE = {
    "DMK": "SPA",
    "INC": "SPA",
    "CPI": "SPA",
    "CPI(M)": "SPA",
    "VCK": "SPA",
    "MDMK": "SPA",
    "IUML": "SPA",
    "KMDK": "SPA",
    "AIADMK": "NDA",
    "BJP": "NDA",
    "PMK": "NDA",
}
WB_ALLIANCE = {
    "TMC": "TMC",
    "AITC": "TMC",
    "BJP": "NDA",
    "GJM": "NDA",
    "INC": "SM",
    "CPI(M)": "SM",
    "CPI": "SM",
    "RSP": "SM",
    "AIFB": "SM",
    "ISF": "SM",
}


def clean_refs(s: str) -> str:
    s = re.sub(r"<ref[^>/]*/>", "", s)
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    return s


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s)


def unbold(s: str) -> str:
    return s.replace("'''", "").replace("''", "")


def decode_wikilinks(s: str) -> str:
    def repl(m):
        return (m.group(2) or m.group(1)).strip()

    return re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", repl, s)


def decode_templates_simple(s: str) -> str:
    m = re.search(r"\{\{\s*legend2\s*\|[^|]*\|\s*\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", s, flags=re.I)
    if m:
        return (m.group(2) or m.group(1)).strip()
    m = re.search(r"\{\{\s*(?:[Pp]arty name with color|[Pp]arty name with colour)\s*\|\s*([^}|]+)", s)
    if m:
        return m.group(1).strip()
    m = re.search(r"\{\{\s*legend2\s*\|[^|]*\|\s*([^|}]+)", s, flags=re.I)
    if m:
        return m.group(1).strip()
    return s


def clean_cell(raw: str) -> str:
    s = clean_refs(raw).strip()
    if re.match(r"^(?:style|bgcolor|align|data-sort-type|rowspan|colspan)\s*=.*\|\s*$", s, flags=re.I):
        return ""
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
    if re.fullmatch(r"[A-Z][A-Z0-9()\-.]{1,9}", p):
        return p
    if "TRINAMOOL CONGRESS" in k:
        return "TMC"
    if "BHARATIYA JANATA PARTY" in k:
        return "BJP"
    if "INDIAN NATIONAL CONGRESS" in k:
        return "INC"
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
        for p in body.split("||"):
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
    offset = 0
    if len(row) > 2 and re.match(r"^\d{1,3}(?:\.\d+)?$", row[2].replace(",", "")):
        offset = 1
    winner_candidate_idx = 2 + offset
    winner_candidate = row[winner_candidate_idx].strip() if winner_candidate_idx < len(row) else ""
    winner_party = "NA"
    for i in range(winner_candidate_idx + 1, min(len(row), winner_candidate_idx + 7)):
        c = row[i].strip()
        if not c:
            continue
        if re.match(r"^\d[\d,]*(?:\.\d+)?$", c):
            continue
        p = normalize_party(c)
        if p.upper().startswith("BACKGROUND"):
            continue
        if "DISTRICT" in p.upper():
            continue
        if p == winner_candidate:
            continue
        if 2 < len(p) < 40:
            winner_party = p
            break

    reserved = reserve_from_name(name)
    alliance = "OTH"
    if state == "ASSAM":
        alliance = ASSAM_ALLIANCE.get(winner_party, "OTH")
    elif state == "KERALA":
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
        "winner": winner_candidate or "NA",
        "party": winner_party or "NA",
        "alliance": alliance or "OTH",
        "reserved": reserved,
    }


def parse_2016(state: str):
    text = STATE_2016_FILES[state].read_text(encoding="utf-8", errors="ignore")
    lines = section_lines(text, state)
    rows = parse_rows(lines)
    parsed = {}
    for r in rows:
        d = extract_row_data(state, r)
        if not d:
            continue
        if d["no"] not in parsed:
            parsed[d["no"]] = d
    return parsed


def extract_no(raw) -> int | None:
    m = re.search(r"\d+", str(raw or ""))
    return int(m.group(0)) if m else None


def apply_2016_rows(state: str, rows: list[dict], parsed: dict[int, dict]):
    for row in rows:
        row["y2016_winner_name"] = "NA"
        row["y2016_winner_party"] = "NA"
        row["y2016_winner_alliance"] = "OTH"

    matched = 0
    if state == "ASSAM":
        by_name = {}
        for d in parsed.values():
            key = norm_name(d["name"])
            if key and key not in by_name:
                by_name[key] = d
        for row in rows:
            d = by_name.get(norm_name(row.get("constituency_name", "")))
            if not d:
                continue
            row["y2016_winner_name"] = d["winner"] or "NA"
            row["y2016_winner_party"] = d["party"] or "NA"
            row["y2016_winner_alliance"] = d["alliance"] or "OTH"
            matched += 1
    else:
        for row in rows:
            no = extract_no(row.get("no"))
            d = parsed.get(no) if no is not None else None
            if not d:
                continue
            row["y2016_winner_name"] = d["winner"] or "NA"
            row["y2016_winner_party"] = d["party"] or "NA"
            row["y2016_winner_alliance"] = d["alliance"] or "OTH"
            matched += 1
    return matched


def main():
    for state in ["ASSAM", "KERALA", "PUDUCHERRY", "TAMIL_NADU", "WEST_BENGAL"]:
        result_path = RESULTS_DIR / f"{state}_results.json"
        rows = json.loads(result_path.read_text(encoding="utf-8"))
        parsed_2016 = parse_2016(state)
        matched = apply_2016_rows(state, rows, parsed_2016)
        result_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(
            f"{state}: total={len(rows)} parsed2016={len(parsed_2016)} matched={matched} "
            f"missing={len(rows)-matched}"
        )


if __name__ == "__main__":
    main()
