# Instrukce pro Claude session nad tímto repem

Přečti si tento soubor celý dřív, než cokoli změníš. Uživatel nemusí nic vysvětlovat, kontext je tady.

## O co jde

Petr a Anežka plánují dovolenou v jižním Thajsku, 26. 11.–19. 12. 2026 (přílet do Bangkoku 27. 11., odlet z Phuketu 19. 12.). Lety Etihad přes Abu Dhabi. Repo drží itinerář v Markdownu a generuje z něj web na GitHub Pages.

Zadání dovolené: slow tempo, mladý pár, žádná masová turistická místa, minimum času stráveného přejezdy. Itinerář je osnova, ne pevný rozvrh. Původní podklad je manuál od Anežky (PDF), Markdown je jeho zpracovaná a doplněná podoba.

## Zdroj pravdy

Ruční editace patří výhradně do Markdownu poslední verze: `verze/vN/<md>`, kde `vN` je poslední záznam v `src/verze.json` a `<md>` je jeho pole `md`. K dnešku `verze/v5/thajsko-bangkok-phuket.md`.

Nikdy needituj: `index.html`, `verze/*/index.html`, `thajsko-obsah.js`, `verze.js`, `ZMENY.md` ani kořenový `thajsko-bangkok-phuket.md`. Všechno to generuje `build.py` a ruční změny se ztratí. Kořenový Markdown je kopie poslední verze, ne zdroj.

Starší verze `verze/v1` až `verze/v4` jsou archiv, neměň je.

## Postup při každé změně obsahu

Každá změna, i jednořádková oprava, znamená novou verzi:

1. `cp -r verze/vN verze/vN+1`, ve zkopírované složce nech jen Markdown (`index.html` a `thajsko-obsah.js` dogeneruje build).
2. Uprav Markdown ve `verze/vN+1/`.
3. Přidej záznam do `src/verze.json` na konec pole: `id`, `datum` (formát `30. 10. 2026`), `nazev`, `md`, `smer`, `lede`, `zmeny` (seznam vět, co se změnilo proti předchozí verzi), `hlavicka` (`eyebrow`, `facts`, `route`, `mista`, `faze6`). Pole `route` a `mista` musí mít 9 položek, po jedné na fázi.
4. Commitni text verze a hash tohoto commitu zapiš do pole `commit` nové verze.
5. `python build.py`, zkontroluj výstup, commitni a pushni.

Bez kroku 5 web ukazuje starý obsah. Build vypíše, která verze je aktuální.

Markdown nesmí obsahovat zpětný apostrof, `${` ani zpětné lomítko, build na tom spadne.

## Jak psát obsah

- Česky, věcně, bez marketingového tónu.
- Bez emoji. Bez pomlčky `—` a `–` mimo číselné rozsahy (2020–2024), místo nich čárka, dvojtečka, závorka nebo dvě věty.
- Struktura sekcí je zavedená (číslované `##` sekce 0 až 18 plus příloha), drž ji. Novou sekci zakládej jen když se obsah opravdu nevejde jinam.
- U míst v sekci 3 patří odkaz do Google Maps. Body se souřadnicemi míří přímo na místo, ostatní spouštějí vyhledávání podle názvu.
- U každého přesunu uveď orientační čas, u každé zastávky počet nocí a orientační datum.
- Co není ověřené (jízdní řády, ceny, otevírací doby), označ jako neověřené. Netvrď jistotu, kterou podklad nedává.

## Co je rozpracované

Fáze 1 až 4 odpovídají Anežčině aktualizaci z října 2026. Fáze 5 až 9 mají data k přepočtu: součet fází je 23 nocí, k dispozici jich je 22, jedna se musí ubrat (kandidáti podle sekce 0: Khao Lak, Koh Phayam, Krabi Town) nebo musí Ranong proběhnout bez noci navíc. Pevné body jsou dva: rezervace plovoucího bungalovu na jezeře Cheow Lan a odlet z Phuketu 19. 12.

## Práce v session

S repem pracuje i Anežka, která nepoužívá git ani jeho názvosloví. Slova jako „aktualizuj“, „ulož to“, „dej to na web“, „zveřejni“, „hotovo“ nebo „aktualizace“ znamenají celý řetězec až do konce, bez doptávání na jednotlivé kroky:

1. založit novou verzi a upravit její Markdown,
2. doplnit záznam do `src/verze.json`,
3. commitnout text verze a zapsat jeho hash do pole `commit`,
4. spustit `python build.py`,
5. commitnout a pushnout na `main`.

Hotovo je až tehdy, když je změna na webu https://polachp.github.io/dovolena-thajsko-2026/. Po pushi počkej, až se GitHub Pages obnoví (desítky sekund), a ověř, že se nová verze na webu opravdu ukazuje. Nehlas hotovo dřív.

Nepoužívej v odpovědích slova commit, push, branch ani merge, pokud se na ně uživatel sám nezeptá. Stačí „uloženo a nahráno na web“.

Doptávej se jen na obsah: co přesně se má v itineráři změnit, když to z popisu nevyplývá. Na technický postup se neptej, ten je popsaný tady.

Nevytvářej novou verzi pro změnu, kterou uživatel teprve rozmýšlí. Dokud se bavíte o tom, co a jak, nic neukládej; verzi zakládej, až je obsah dohodnutý.

Jedna výjimka z automatického nahrávání: pokud by změna něco smazala nebo přepsala tak, že to nejde vrátit (zásah do starších verzí v `verze/v1` až `verze/v4`, přepsání cizí změny, smazání sekce bez náhrady), nejdřív se zeptej.

## Autorství commitů

Commity vzniklé v session s Anežkou (mobilní aplikace Claude) musí mít na konci zprávy, jako poslední řádek a oddělené prázdným řádkem, tento trailer:

Co-authored-by: anezka-vibe <291587174+anezka-vibe@users.noreply.github.com>

Bez něj se změny v historii i v přehledu přispěvatelů objevují jen pod identitou Claude. Trailer přidávej ke každému commitu, který vznikl na základě jejího zadání, včetně commitů s vygenerovanými soubory z `build.py`.

U commitů ze session s Petrem trailer nepřidávej.
