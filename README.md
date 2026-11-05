# Dovolená Thajsko 2026

Itinerář jižního Thajska podle manuálu od Anežky. Aktuální verze: směr Bangkok → Phuket, 26. 11.–19. 12. 2026.

- Web (aktuální verze): https://polachp.github.io/dovolena-thajsko-2026/
- Starší verze: `verze/<id>/` (web i Markdown), přehled v [ZMENY.md](ZMENY.md)

## Pravidlo číslo jedna: Markdown je zdroj, web se generuje

Jediný soubor, který se edituje ručně, je Markdown poslední verze:

```
verze/v35/thajsko-bangkok-phuket.md
```

Poslední verze je poslední záznam v `src/verze.json`, název jejího Markdownu je v poli `md`.

Z tohoto Markdownu se generuje všechno ostatní. Po každé změně textu se musí znovu spustit `python build.py`, jinak web ukazuje starý obsah.

Generované soubory, do kterých se nikdy nepíše ručně (build je přepíše):

- `index.html` a `verze/*/index.html`
- `thajsko-obsah.js` a `verze/*/thajsko-obsah.js`
- `verze.js`
- `ZMENY.md`
- `thajsko-bangkok-phuket.md` v kořeni repa (kopie Markdownu poslední verze, dělá ji `build.py` kvůli odkazu z webu)

Editace kořenového `thajsko-bangkok-phuket.md` je typická chyba: soubor vypadá jako hlavní zdroj, ale je to kopie a příští build ji přepíše. Totéž platí pro editaci přes webové rozhraní GitHubu.

Starší verze (`verze/v1` až `verze/v34`) se neupravují, slouží jako archiv. Číslo poslední verze se v tomto souboru i v `CLAUDE.md` přepisuje s každou novou verzí.

## Struktura

- `verze/vN/<md>`: zdrojový text verze N, jediné místo, kde se text edituje
- `src/verze.json`: seznam verzí, změnový list a údaje do hlavičky webu
- `src/sablona.html`: šablona stránky
- `build.py`: vygeneruje `index.html`, `verze/*/index.html`, `thajsko-obsah.js`, `verze.js`, `ZMENY.md` a kopii Markdownu v kořeni
- `varianty/`: vyřazené části itineráře uložené jako záložní varianty (build je nezpracovává), například [Khao Lak](varianty/khao-lak.md), [další místa v Krabi](varianty/krabi-dalsi-mista.md), [Phuket Town jako poslední noc](varianty/phuket-town.md), [Fun Friday a suvenýry na Phuketu](varianty/phuket-fun-friday-suvenyry.md) a [vodopád Ngao u Ranongu](varianty/vodopad-ngao.md)
- `CLAUDE.md`: postup pro práci s repem v Claude session

## Jak udělat změnu v itineráři

Drobná oprava i velký zásah se řeší stejně: vznikne nová verze. Stará zůstane dostupná na webu i v repu.

1. Zkopírovat `verze/vN/` do `verze/vN+1/` (stačí Markdown, zbytek dogeneruje build).
2. Upravit Markdown ve `verze/vN+1/`.
3. Přidat záznam `vN+1` do `src/verze.json`: `id`, `datum`, `nazev`, `md`, `smer`, `lede`, `zmeny`, `hlavicka`. Přepsat číslo poslední verze a stav rozpracovaného v `README.md` a `CLAUDE.md`.
4. Commit textu verze. Hash tohoto commitu zapsat do pole `commit` u nové verze v `src/verze.json` (slouží pro odkaz na rozdíl proti předchozí verzi).
5. `python build.py`, commit, push.

Build vypíše seznam verzí a která je aktuální. Po pushi se web na GitHub Pages obnoví do pár desítek sekund.

### Omezení build skriptu

Markdown nesmí obsahovat zpětný apostrof, `${` ani zpětné lomítko. Vkládá se do JS template literálu a build v takovém případě skončí chybou.

## Co je v itineráři rozpracované

Stav k v35: 8 fází, 22 nocí, přepočet nocí je hotový (Khao Lak vyřazený). Itinerář má jednotnou stavbu fází: krátký popis, co uvidíte, podrobnosti jako nadpisy 4. úrovně, které web zobrazí sbalené (pravidla v `CLAUDE.md`). Khao Sok má 4 noci (8.–12. 12.), Krabi 2 (12.–14. 12.) a Koh Yao Noi 4 (14.–18. 12.). Nedořešená je noc na jezeře Cheow Lan, ověření programu na Koh Yao Noi (kajak na Koh Nok, loď na Koh Hong, skútr a rybářské vesnice na západě jsou dohodnuté, ale neověřené) a rezervace ubytování ve fázích 5 až 8, která je až na noci 10.–12. 12. v Khao Sok hotová (na Phuketu je rezervovaný Wattana Bungalow v Nai Yang, 18.–19. 12., přes Booking.com, zrušit zdarma do 16. 12.; v Khao Sok jsou rezervované Bingo Hostel Khao Sok, 8.–10. 12., a Flora Hostel KhaoSok, 8.–9. 12., oba přes Booking.com; noc 8.–9. 12. je zarezervovaná dvakrát a jedno z ubytování je potřeba zrušit; v Krabi je potvrzený Vacation House, 12.–14. 12., přes Booking.com; na Koh Yao Noi jsou na noci 14.–18. 12. zarezervované Pyramid Bungalow, s klimatizací, zrušit zdarma do 6. 12., a Tabeak View Point, bez klimatizace, zrušit zdarma do 14. 12., obě přes Booking.com, jedno je potřeba zrušit; fáze 1 až 4 jsou rezervované přes Agodu, termíny zrušení zdarma jsou u fází). Loď z Koh Yao Noi na Phuket (18. 12., mola Manoh a Laem Sai, obě na Bang Rong, lístek 2 až 3 dny předem) je zapsaná ve fázi 7, časy a ceny jsou neověřené. Ve fázi 5 je volitelné sloní útočiště Khao Sok Elephant Sanctuary (program a cena se ověřují). Fáze 8 je nabídka možností v Nai Yang (trh, letadla a procházky po plážích, sloní lávka Observe, Nai Thon), cena a hodiny jsou neověřené, odlet je v sobotu 19. 12. ve 21:00. Podrobnosti v sekci 0 Markdownu.
