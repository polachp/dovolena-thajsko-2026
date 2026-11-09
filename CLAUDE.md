# Instrukce pro Claude session nad tímto repem

Přečti si tento soubor celý dřív, než cokoli změníš. Uživatel nemusí nic vysvětlovat, kontext je tady.

## O co jde

Petr a Anežka plánují dovolenou v jižním Thajsku, 26. 11.–19. 12. 2026 (přílet do Bangkoku 27. 11., odlet z Phuketu 19. 12.). Lety Etihad přes Abu Dhabi. Repo drží itinerář v Markdownu a generuje z něj web na GitHub Pages.

Zadání dovolené: slow tempo, mladý pár, žádná masová turistická místa, minimum času stráveného přejezdy. Itinerář je osnova, ne pevný rozvrh. Původní podklad je manuál od Anežky (PDF), Markdown je jeho zpracovaná a doplněná podoba.

## Aktuální stav (aktualizuj při každé nové verzi)

- Poslední verze: **v44** (9. 11. 2026), zdroj `verze/v44/thajsko-bangkok-phuket.md`.
- Archiv: `verze/v1` až `verze/v43`, neměnit.
- Sekce 0 až 16, itinerář je sekce 5. Rozřazení sekcí do záložek webu je v `hlavicka.kam` poslední verze.
- Trasa: 8 fází, 22 nocí. Bangkok 3, Sam Roi Yot 3, Prachuap 1, Ranong 1 + Koh Phayam 3, Khao Sok 4 (8.–12. 12.), Krabi 2 (12.–14. 12.), Koh Yao Noi 4 (14.–18. 12.), Phuket, Nai Yang 1 (18.–19. 12.).
- Pole `route` a `mista` v `src/verze.json` mají 8 položek, po jedné na fázi.
- Vyřazené varianty: Ban Krut (zůstává ve v3), Khao Lak (soubor `varianty/khao-lak.md`, původně fáze 6 ve v3 až v12), další místa v Krabi (soubor `varianty/krabi-dalsi-mista.md`, vyřazená ve v21 kvůli 2 nocím: kajaky v Ao Thalane, Railay, Tha Pom Klong Song Nam, Tiger Cave, sloní útočiště), Phuket Town jako poslední noc (soubor `varianty/phuket-town.md`, původní fáze 8 ve v29, nahrazená vesnicí Nai Yang ve v30), Fun Friday na Boat Avenue a suvenýry na Phuketu (soubor `varianty/phuket-fun-friday-suvenyry.md`, vyřazené ve v31), vodopád Ngao u Ranongu (soubor `varianty/vodopad-ngao.md`, volitelná zastávka fáze 4, vyřazená ve v33), raft housy Praiwan a Keereewarin na jezeře Cheow Lan (soubor `varianty/raft-housy-cheow-lan.md`, odrážka bloku Noc na jezeře ve fázi 5, vyřazená ve v37).

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
- Termíny zrušení ubytování zdarma jsou ve fázích (zdroj) a od v44 také seřazené podle pořadí na cestě v tabulce Do kdy zrušit ubytování zdarma v sekci 11, v thajském i českém čase. Když se rezervace nebo termín změní, uprav fázi i tabulku. V sekci 3 se termíny neuvádějí, v sekci 0 jsou jen u dvojích rezervací a u Wattany, kde se podle nich rozhoduje.
- Fáze jsou nadpisy `### Fáze N: Název (X nocí, datum)` v sekci 5 a web z nich dělá samostatné stránky. Každá fáze má stejnou stavbu:
  1. jeden až dva řádky popisu (web ho ukazuje i na kartě v přehledu),
  2. seznam „co uvidíte“: `- **Místo:** jedna věta`, volitelné věci označené „(volitelně)“,
  3. podrobnosti jako nadpisy `#### ...` (například Program po dnech, jednotlivá místa, Ubytování, Přesun dál, Mapy). Web každý `####` blok zobrazí sbalený a rozbalí ho až po klepnutí. Mapy jsou vždy poslední blok.
- Když se fáze přidá nebo vyřadí, přečísluj i všechny odkazy „fáze N“ v textu a tabulkách.
- U míst v sekci 3 a v bloku Mapy u fáze patří odkaz do Google Maps. Sekce 3 je souhrnný seznam na uložení do offline map, blok u fáze je pro použití na místě. Body se souřadnicemi míří přímo na místo, ostatní spouštějí vyhledávání podle názvu.
- U každého přesunu uveď orientační čas, u každé zastávky počet nocí a orientační datum.
- Co není ověřené (jízdní řády, ceny, otevírací doby), označ jako neověřené. Netvrď jistotu, kterou podklad nedává.

## Co je rozpracované

Stav k v44. Noci jsou přepočtené a sedí na 22, itinerář má novou strukturu (popis, co uvidíte, rozbalovací podrobnosti). Fáze 5 má volitelné sloní útočiště v Khao Sok, fáze 7 má program, rezervované ubytování a rozepsanou loď na Phuket, fáze 8 je nabídka možností v Nai Yang s rezervovaným ubytováním. Nedořešené zůstává:

- Fáze 5: noc na jezeře Cheow Lan (balíček, konkrétní raft house, nebo jen jednodenní výlet). Rezervace bungalovu je jeden ze dvou pevných bodů.
- Fáze 5: čtyřkolky v Khao Sok (Khao sok ATV Adventure): cena (1 500 THB řidič, 2 200 THB dva na jedné čtyřkolce) a odvoz z ubytování zdarma potvrdil provozovatel 3. 11., den se vybere na místě. Chybí odpověď, jestli je potřeba řidičský průkaz.
- Fáze 5: sloní útočiště Khao Sok Elephant Sanctuary (volitelně, nerezervováno). Zdroje si odporují v tom, jestli program zahrnuje koupání a dotyky, cena není známá. Před rezervací se zeptat přímo. Phuket Elephant Sanctuary u Paklok je ve fázi 8 jen jako druhá možnost po sloní lávce Observe v Sakhu.
- Fáze 6: Vacation House (12.–14. 12.) je potvrzený přes Booking.com, zrušit zdarma do 4. 12. 23:59 thajského času. Dragon Crest 13. 12.: skútr z Ao Nang nebo taxi, domluvit s hostitelem.
- Fáze 7: program na Koh Yao Noi (kajak na Koh Nok, loď na Koh Hong, skútr, rybářské vesnice na západě) je dohodnutý, ale neověřený: ceny a půjčovny kajaků a lodi, náročnost vyhlídky na Nok (podle recenzí strmě po laně), restaurace v prosinci.
- Fáze 7: noci 14.–18. 12. jsou zarezervované dvakrát, v Pyramid Bungalow (Booking.com, s klimatizací, zrušit zdarma do 6. 12. 23:59 thajského času, v Česku v 17:59) a v Tabeak View Point (Booking.com, bez klimatizace, zrušit zdarma do 14. 12. 18:00 thajského času, v Česku ve 12:00). Jedno je potřeba zrušit, rozhodnout do 6. 12.
- Fáze 7: loď z Koh Yao Noi na Phuket (18. 12.) je zapsaná, ale časy a ceny jsou neověřené. Dvě mola (Manoh, Laem Sai), obě na Bang Rong, lístek koupit 2 až 3 dny předem (kolem 15. až 16. 12.). Chybí ověřit, které molo je blíž k ubytování. Taxi z mola Bang Rong do Nai Yang (asi 19 minut, 13 až 16 USD) je neověřené.
- Fáze 8: Wattana Bungalow v Nai Yang (18.–19. 12., Booking.com, zrušit zdarma do 16. 12. 23:59 thajského času, v Česku v 17:59, tedy ve stejné době, kdy se kupuje lístek na loď). Program je nabídka možností (trh Nai Yang Fresh Market, letadla a procházky po plážích, sloní lávka Observe v Sakhu, Nai Thon; Fun Friday na Boat Avenue a suvenýry jsou od v31 ve variantách), nic z toho není rezervované. Neověřené zůstává: Observe (cena, délka, časy, storno, rezervace přes web provozovatele), hodiny trhu (Google Maps denně 16:00–19:00, jiné zdroje jen vybrané dny), vzdálenost Wattany od pláže a od trhu, úschova zavazadel po odhlášení do 12:00. Let EY 413 z Phuketu je v sobotu 19. 12. ve 21:00, zapsaný ve fázi 8.
- Rozpočet (sekce 14) nepřepočítává změnu ve v21, položky vyřazené z Krabi v něm zůstávají jako horní odhad. Od v30 je noc v Nai Yang vyčleněná zvlášť (1 700 THB podle rezervace), součty vychází asi 65 150 THB úsporně a 113 500 THB pohodlněji.
- Ubytování ve fázích 5 až 8 je rezervované, kromě nocí 10.–12. 12. v Khao Sok. Na Koh Yao Noi jsou dvě rezervace (viz výše), na Phuketu Wattana Bungalow (viz fáze 8) a v Khao Sok Bingo Hostel Khao Sok (8.–10. 12., Booking.com, zrušit zdarma do 6. 12. 23:59 thajského času) a Flora Hostel KhaoSok (8.–9. 12., Booking.com, zrušit zdarma do 8. 12. 18:00). Noc 8.–9. 12. je zarezervovaná dvakrát, jedno z ubytování je potřeba zrušit. V Krabi je potvrzený Vacation House (12.–14. 12., Booking.com, zrušit zdarma do 4. 12. 23:59 thajského času, to je nejbližší termín ze všech). Noci v Khao Sok 10.–12. 12. se řeší na místě. Fáze 1 až 4 jsou rezervované přes Agodu, termíny zrušení zdarma jsou u fází (22. 11. až 2. 12.) a všechny jsou seřazené v tabulce v sekci 11.

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
