import fs from 'node:fs/promises';
import path from 'node:path';

const ROOT = process.cwd();
const RESULTS_DIR = path.join(ROOT, 'hosted-json', 'results');
const MAP_DIR = path.join(ROOT, 'root');
const OUT_DIR = path.join(ROOT, 'hosted-json');
const OUT_FILE = path.join(OUT_DIR, 'i18n.kn.json');

const RESERVED_TRANSLATIONS = {
  GEN: 'ಸಾಮಾನ್ಯ',
  SC: 'ಎಸ್‌ಸಿ',
  ST: 'ಎಸ್‌ಟಿ'
};

const STATE_FILES = [
  { state: 'KERALA', type: 'geojson', file: 'KERALA_ASSEMBLY_optimized.geojson' },
  { state: 'TAMIL_NADU', type: 'geojson', file: 'TAMIL_NADU_ASSEMBLY_optimized.geojson' },
  { state: 'WEST_BENGAL', type: 'geojson', file: 'WEST_BENGAL_ASSEMBLY_optimized.geojson' },
  { state: 'PUDUCHERRY', type: 'geojson', file: 'PUDUCHERRY_ASSEMBLY_optimized_compact.geojson' },
  { state: 'ASSAM', type: 'svg', file: 'ASSAM_2023_keyed.svg' }
];

function cleanText(value) {
  return String(value || '').replace(/\s+/g, ' ').trim();
}

function needsTranslation(value) {
  const text = cleanText(value);
  if (!text) return false;
  if (text === 'NA') return false;
  return /[A-Za-z]/.test(text);
}

function postProcessTranslation(source, translated) {
  const original = cleanText(source);
  let text = cleanText(translated)
    .replace(/\u200c/g, '')
    .replace(/\u200d/g, '');

  if (/\(SC\)$/i.test(original)) {
    text = text.replace(/\(SC\)$/i, '(ಎಸ್‌ಸಿ)');
  }
  if (/\(ST\)$/i.test(original)) {
    text = text.replace(/\(ST\)$/i, '(ಎಸ್‌ಟಿ)');
  }
  if (/\(GEN\)$/i.test(original)) {
    text = text.replace(/\(GEN\)$/i, '(ಸಾಮಾನ್ಯ)');
  }

  return text || original;
}

async function translateText(source) {
  const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=kn&dt=t&q=${encodeURIComponent(source)}`;
  const res = await fetch(url, {
    headers: {
      'user-agent': 'Mozilla/5.0'
    }
  });
  if (!res.ok) {
    throw new Error(`Translate HTTP ${res.status} for "${source}"`);
  }
  const data = await res.json();
  const translated = Array.isArray(data?.[0]) ? data[0].map(part => part?.[0] || '').join('') : '';
  return postProcessTranslation(source, translated);
}

async function collectGeoJsonStrings(filePath, strings) {
  const geo = JSON.parse(await fs.readFile(filePath, 'utf8'));
  for (const feature of geo.features || []) {
    const props = feature.properties || {};
    strings.add(cleanText(props.AC_NAME));
    strings.add(cleanText(props.DIST_NAME));
  }
}

async function collectSvgStrings(filePath, strings) {
  const svg = await fs.readFile(filePath, 'utf8');
  const attrPattern = /data-ac-name="([^"]+)"[^>]*data-district="([^"]*)"/g;
  for (const match of svg.matchAll(attrPattern)) {
    strings.add(cleanText(match[1]));
    strings.add(cleanText(match[2]));
  }
}

async function collectResultStrings(strings) {
  const files = (await fs.readdir(RESULTS_DIR)).filter(file => file.endsWith('.json'));
  for (const file of files) {
    const data = JSON.parse(await fs.readFile(path.join(RESULTS_DIR, file), 'utf8'));
    for (const row of data) {
      strings.add(cleanText(row.constituency_name));
      strings.add(cleanText(row.current_mla_name));
      strings.add(cleanText(row.current_mla_party));
      strings.add(cleanText(row.current_mla_alliance));
      strings.add(cleanText(row.y2016_winner_name));
      strings.add(cleanText(row.y2016_winner_party));
      strings.add(cleanText(row.y2016_winner_alliance));
      strings.add(cleanText(row.y2026_winner_name));
      strings.add(cleanText(row.y2026_winner_party));
      strings.add(cleanText(row.y2026_winner_alliance));
    }
  }
}

async function collectPartyStrings(strings) {
  const parties = JSON.parse(await fs.readFile(path.join(ROOT, 'hosted-json', 'parties.json'), 'utf8'));
  for (const party of parties) {
    strings.add(cleanText(party.code));
    strings.add(cleanText(party.name));
    strings.add(cleanText(party.alliance_2020));
    for (const alliance of Object.values(party.alliances || {})) {
      strings.add(cleanText(alliance));
    }
  }
}

async function buildSourceSet() {
  const strings = new Set();

  for (const stateFile of STATE_FILES) {
    const filePath = path.join(MAP_DIR, stateFile.file);
    if (stateFile.type === 'geojson') {
      await collectGeoJsonStrings(filePath, strings);
    } else {
      await collectSvgStrings(filePath, strings);
    }
  }

  await collectResultStrings(strings);
  await collectPartyStrings(strings);

  return [...strings]
    .map(cleanText)
    .filter(needsTranslation)
    .sort((a, b) => a.localeCompare(b, 'en'));
}

async function mapWithConcurrency(items, concurrency, worker) {
  const results = new Array(items.length);
  let index = 0;

  async function runWorker() {
    while (true) {
      const current = index++;
      if (current >= items.length) return;
      results[current] = await worker(items[current], current);
    }
  }

  await Promise.all(Array.from({ length: concurrency }, () => runWorker()));
  return results;
}

async function main() {
  const sources = await buildSourceSet();
  const strings = {};

  console.log(`Translating ${sources.length} unique strings to Kannada...`);

  await mapWithConcurrency(sources, 8, async (source, idx) => {
    const translated = await translateText(source);
    strings[source] = translated;
    if ((idx + 1) % 100 === 0 || idx === sources.length - 1) {
      console.log(`Translated ${idx + 1}/${sources.length}`);
    }
  });

  await fs.mkdir(OUT_DIR, { recursive: true });
  const out = {
    generatedAt: new Date().toISOString(),
    sourceCount: sources.length,
    reserved: RESERVED_TRANSLATIONS,
    strings
  };
  await fs.writeFile(OUT_FILE, `${JSON.stringify(out, null, 2)}\n`, 'utf8');
  console.log(`Wrote ${OUT_FILE}`);
}

main().catch(err => {
  console.error(err);
  process.exitCode = 1;
});
