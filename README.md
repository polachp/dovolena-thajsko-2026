# Dovolená Thajsko 2026

Itinerář jižního Thajska ve směru Phuket → Bangkok (podle manuálu od Anežky).

- Web (aktuální verze): https://polachp.github.io/dovolena-thajsko-2026/
- Starší verze: `verze/<id>/` (web i Markdown), přehled v [ZMENY.md](ZMENY.md)

## Struktura

- `verze/vN/thajsko-phuket-bangkok.md`: zdrojový text verze N (jediné místo, kde se text edituje)
- `src/verze.json`: seznam verzí, změnový list a údaje do hlavičky webu
- `src/sablona.html`: šablona stránky
- `build.py`: vygeneruje `index.html`, `verze/*/index.html`, `thajsko-obsah.js`, `verze.js` a `ZMENY.md`

## Nová verze

1. Zkopírovat poslední `verze/vN/` do `verze/vN+1/` a upravit tam `thajsko-phuket-bangkok.md`.
2. Přidat záznam do `src/verze.json` (datum, název, seznam změn, hlavička).
3. `python build.py`, commit, `git tag vN+1`, push včetně tagů.

Starší verze se neupravují.
