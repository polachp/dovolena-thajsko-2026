# Instrukce pro Claude session nad tímto repem

Přečti si tento soubor celý dřív, než cokoli změníš. Uživatel nemusí nic vysvětlovat, kontext je tady.

## O co jde

Petr a Anežka plánují dovolenou v jižním Thajsku, 26. 11.–19. 12. 2026 (přílet do Bangkoku 27. 11., odlet z Phuketu 19. 12.). Lety Etihad přes Abu Dhabi. Repo drží itinerář v Markdownu a generuje z něj web na GitHub Pages.

Zadání dovolené: slow tempo, mladý pár, žádná masová turistická místa, minimum času stráveného přejezdy. Itinerář je osnova, ne pevný rozvrh. Původní podklad je manuál od Anežky (PDF), Markdown je jeho zpracovaná a doplněná podoba.

## Aktuální stav (aktualizuj při každé nové verzi)

- Poslední verze: **v18** (2. 11. 2026), zdroj `verze/v18/thajsko-bangkok-phuket.md`.
- Archiv: `verze/v1` až `verze/v17`, neměnit.
- Sekce 0 až 16, itinerář je sekce 5. Rozřazení sekcí do záložek webu je v `hlavicka.kam` poslední verze.
- Trasa: 8 fází, 22 nocí. Bangkok 3, Sam Roi Yot 3, Prachuap 1, Ranong 1 + Koh Phayam 3, Khao Sok 3 (8.–11. 12.), Krabi 4 (11.–15. 12.), Koh Yao Noi 3 (15.–18. 12.), Phuket Town 1 (18.–19. 12.).
- Pole `route` a `mista` v `src/verze.json` mají 8 položek, po jedné na fázi.
- Vyřazené varianty: Ban Krut (zůstává ve v3), Khao Lak (soubor `varianty/khao-lak.md`, původně fáze 6 ve v3 až v12).

Tenhle oddíl a oddíl „Co je rozpracované“ jsou součástí každé nové verze. Když se změní číslo verze, počet fází, noci nebo to, co je nedořešené, uprav je ve stejném kroku jako `src/verze.json` (krok 3 postupu níže). Stejné údaje drž i v `README.md` (cesta k Markdownu poslední verze, archiv, rozpracované).

## Zdroj pravdy

Ruční editace patří výhradně do Markdownu poslední verze: `verze/vN/<md>`, kde `vN` je poslední záznam v `src/verze.json` a `<md>` je jeho pole `md`. Číslo aktuální verze je v oddílu „Aktuální stav“ výše. Když se s `src/verze.json` neshoduje, platí `src/verze.json` a tento soubor oprav.

Nikdy needituj: `index.html`, `verze/*/index.html`, `thajsko-obsah.js`, `verze.js`, `ZMENY.md` ani kořenový `thajsko-bangkok-phuket.md`. Všechno to generuje `build.py` a ruční změny se ztratí. Kořenový Markdown je kopie poslední verze, ne zdroj.

Starší verze jsou archiv, neměň je.

Složka `varianty/` drží vyřazené části itineráře, aby se informace neztratily. Build ji nezpracovává, na webu se neukazuje a odkazuje se na ni přes GitHub. Když se z itineráře něco vyřazuje, přesuň obsah sem do vlastního souboru a v sekci 0 na něj odkaž. Pokud se varianta vrací zpátky do itineráře, vezmi text odsud.

## Postup při každé změně obsahu

Každá změna, i jednořádková oprava, znamená novou verzi:

1. `cp -r verze/vN verze/vN+1`, ve zkopírované složce nech jen Markdown (`index.html` a `thajsko-obsah.js` dogeneruje build).
2. Uprav Markdown ve `verze/vN+1/`.
3. Přidej záznam do `src/verze.json` na konec pole: `id`, `datum` (formát `30. 10. 2026`), `nazev`, `md`, `smer`, `lede`, `zmeny` (seznam vět, co se změnilo proti předchozí verzi), `hlavicka` (`eyebrow`, `facts`, `route`, `mista`, `kam`). Počet položek v `route` a `mista` se rovná počtu fází. `kam` přiřazuje číslo sekce záložce webu (`pred` = Před cestou, `misto` = Na místě); itinerář se pozná podle nadpisů fází a do `kam` nepatří. Když se sekce přečíslují, uprav `kam`, jinak ho zkopíruj z předchozí verze. Ve stejném kroku uprav oddíly „Aktuální stav“ a „Co je rozpracované“ v tomto souboru a odpovídající místa v `README.md`.
4. Commitni text verze (včetně CLAUDE.md a README.md) a hash tohoto commitu zapiš do pole `commit` nové verze.
5. `python build.py`, zkontroluj výstup, commitni a pushni.

Bez kroku 5 web ukazuje starý obsah. Build vypíše, která verze je aktuální.

Markdown verze nesmí obsahovat zpětný apostrof, `${` ani zpětné lomítko, build na tom spadne.

## Jak psát obsah

- Česky, věcně, bez marketingového tónu.
- Bez emoji. Bez pomlčky `—` a `–` mimo číselné rozsahy (2020–2024), místo nich čárka, dvojtečka, závorka nebo dvě věty.
- Struktura sekcí je zavedená (číslované `##` sekce 0 až 16), drž ji. Novou sekci zakládej jen když se obsah opravdu nevejde jinam. Při přečíslování uprav všechny odkazy „sekce N“ a `hlavicka.kam`.
- Každá informace patří na jedno místo. Co se týká konkrétní fáze (program, ceny, přesun, ubytování), patří do fáze, obecné sekce jen odkazují. Sekce 0 drží jen to, co je nedořešené, historie změn patří do `zmeny` v `src/verze.json`.
- Fáze jsou nadpisy `### Fáze N: Název (X nocí, datum)` v sekci 5 a web z nich dělá samostatné stránky. Každá fáze má stejnou stavbu:
  1. jeden až dva řádky popisu (web ho ukazuje i na kartě v přehledu),
  2. seznam „co uvidíte“: `- **Místo:** jedna věta`, volitelné věci označené „(volitelně)“,
  3. podrobnosti jako nadpisy `#### ...` (například Program po dnech, jednotlivá místa, Ubytování, Přesun dál, Mapy). Web každý `####` blok zobrazí sbalený a rozbalí ho až po klepnutí. Mapy jsou vždy poslední blok.
- Když se fáze přidá nebo vyřadí, přečísluj i všechny odkazy „fáze N“ v textu a tabulkách.
- U míst v sekci 3 a v bloku Mapy u fáze patří odkaz do Google Maps. Sekce 3 je souhrnný seznam na uložení do offline map, blok u fáze je pro použití na místě. Body se souřadnicemi míří přímo na místo, ostatní spouštějí vyhledávání podle názvu.
- U každého přesunu uveď orientační čas, u každé zastávky počet nocí a orientační datum.
- Co není ověřené (jízdní řády, ceny, otevírací doby), označ jako neověřené. Netvrď jistotu, kterou podklad nedává.

## Co je rozpracované

Stav k v18. Noci jsou přepočtené a sedí na 22, itinerář má novou strukturu (popis, co uvidíte, rozbalovací podrobnosti). Nedořešené zůstává:

- Fáze 5: noc na jezeře Cheow Lan (balíček, konkrétní raft house, nebo jen jednodenní výlet). Rezervace bungalovu je jeden ze dvou pevných bodů.
- Fáze 6: základna v Krabi (Krabi Town, nebo pláže Tub Kaek či Klong Muang u Dragon Crest) a případný přesun jedné noci z Krabi na Koh Yao Noi.
- Ubytování ve fázích 5 až 8 není rezervované, kromě první noci v Khao Sok (Flora Hostel KhaoSok, 8.–9. 12., Booking.com, zrušit zdarma do 8. 12.). Zbylé noci v Khao Sok (9.–11. 12.) se řeší na místě. Fáze 1 až 4 jsou rezervované přes Agodu, termíny zrušení zdarma jsou u fází (22. 11. až 2. 12.).

Pevné body jsou dva: rezervace plovoucího bungalovu na jezeře Cheow Lan a odlet z Phuketu 19. 12.

## Práce v session

S repem pracuje i Anežka, která nepoužívá git ani jeho názvosloví. Slova jako „aktualizuj“, „ulož to“, „dej to na web“, „zveřejni“, „hotovo“ nebo „aktualizace“ znamenají celý řetězec až do konce, bez doptávání na jednotlivé kroky:

1. založit novou verzi a upravit její Markdown,
2. doplnit záznam do `src/verze.json` a oddíly „Aktuální stav“ a „Co je rozpracované“ v tomto souboru,
3. commitnout text verze a zapsat jeho hash do pole `commit`,
4. spustit `python build.py`,
5. commitnout a pushnout na `main`.

Hotovo je až tehdy, když je změna na webu https://polachp.github.io/dovolena-thajsko-2026/. Po pushi počkej, až se GitHub Pages obnoví (desítky sekund), a ověř, že se nová verze na webu opravdu ukazuje. Nehlas hotovo dřív.

Nepoužívej v odpovědích slova commit, push, branch ani merge, pokud se na ně uživatel sám nezeptá. Stačí „uloženo a nahráno na web“.

Doptávej se jen na obsah: co přesně se má v itineráři změnit, když to z popisu nevyplývá. Na technický postup se neptej, ten je popsaný tady.

Nevytvářej novou verzi pro změnu, kterou uživatel teprve rozmýšlí. Dokud se bavíte o tom, co a jak, nic neukládej; verzi zakládej, až je obsah dohodnutý.

Jedna výjimka z automatického nahrávání: pokud by změna něco smazala nebo přepsala tak, že to nejde vrátit (zásah do starších verzí, přepsání cizí změny, smazání sekce bez náhrady), nejdřív se zeptej.

## Autorství commitů

Commity vzniklé v session s Anežkou (mobilní aplikace Claude) musí mít na konci zprávy, jako poslední řádek a oddělené prázdným řádkem, tento trailer:

Co-authored-by: anezka-vibe <291587174+anezka-vibe@users.noreply.github.com>

Bez něj se změny v historii i v přehledu přispěvatelů objevují jen pod identitou Claude. Trailer přidávej ke každému commitu, který vznikl na základě jejího zadání, včetně commitů s vygenerovanými soubory z `build.py`.

U commitů ze session s Petrem trailer nepřidávej.
