# PROCESS.md — Dokumentacja procesu pracy

> Ten plik dokumentuje jak pracowałem nad mini-projektem DPIA (#26): jakie narzędzia AI
> wykorzystałem, jakie prompty pisałem, jakie decyzje podjąłem i co nie zadziałało.
> Bartosz Lewandowski (254364) | PWr 2025/2026

---

## Narzędzia AI użyte w projekcie

| Narzędzie | Do czego użyte |
|-----------|----------------|
| Claude (Cowork — Sonnet 4.6) | Planowanie struktury projektu, generowanie kodu Python, konsultacje prawne dot. RODO/AI Act, pobieranie i analiza źródeł prawnych, generowanie całego raportu i porównania DPIA |
| GitHub Copilot | Uzupełnianie kodu w edytorze (drobne), generowanie docstringów |

Główną rolę odegrał Claude w trybie Cowork — narzędzie mogło pisać pliki bezpośrednio do folderu projektu i wykonywać komendy powłoki w izolowanym środowisku Linux.

---

## Prompty użyte podczas pracy

### Krok 1 — Planowanie

**Prompt wejściowy:**
```
Na podstawie pliku z opisem projektu, pliku z wymaganiami i zasadami oceniania do zadania
oraz opisu projektu napisz dla mnie najpierw plan krok po kroku na ten projekt.
[treść opisu projektu #26 DPIA]
```

**Dlaczego taki prompt:** Zaczęłem od planu zamiast od kodu, bo chciałem zweryfikować, że rozumiem zakres wymagań na każdy poziom oceny (zwłaszcza różnicę między "Dobry" a "Celujący").

---

### Krok 2 — Struktura narzędzia

**Prompt wejściowy:**
```
Na podstawie wymagań RODO art. 35 i szablonów DPIA (CNIL, ICO) zaprojektuj strukturę
interaktywnego kwestionariusza Python do przeprowadzania DPIA dla systemów AI
przetwarzających dane medyczne. Określ sekcje, typy pytań (zamknięte/otwarte) i logikę
oceny ryzyka (matryca prawdopodobieństwo × wpływ). Wyjście powinno być raportem Markdown
generowanym przez Jinja2.
```

**Co Claude zaproponował:**
- 6 sekcji kwestionariusza: opis systemu, konieczność i proporcjonalność, ryzyka, środki zaradcze, AI Act, wnioski
- Skala 1–3 × 1–3 dla prawdopodobieństwa i wpływu (razem max 9 punktów)
- Próg WYSOKIEGO ryzyka: ≥ 6/9
- 6 predefiniowanych kategorii ryzyk z mapowaniem na artykuły RODO i AI Act
- CLI z argparse + opcja `--load` do wczytania poprzedniej sesji

---

### Krok 3 — Implementacja kodu

**Prompt wejściowy:**
```
Zaimplementuj narzędzie dpia_tool.py zgodnie z powyższą strukturą. Użyj:
- argparse z opcją --load (wczytanie JSON z poprzedniej sesji) i --output-dir
- Jinja2 do generowania raportu
- JSON do zapisu odpowiedzi (automatyczny zapis po każdej sesji)
- Kolorowe wyróżnienia w terminalu dla nagłówków sekcji (opcjonalnie)
Wygeneruj też plik responses/smartudl_mar.json z wypełnionymi odpowiedziami dla
projektu SMARTudl Metal Artifact Reduction.
```

**Efekt:** Pełny plik `dpia_tool.py` (~350 linii) + `responses/smartudl_mar.json`.

---

### Krok 4 — Mapowanie ryzyk na AI Act

**Prompt wejściowy:**
```
Dla systemu AI do usuwania artefaktów metalicznych z obrazów CT (narzędzie wspierające
lekarza, nie decyzyjne, faza badawcza, dane ze szpitala anonimizowane przed przekazaniem)
zidentyfikuj ryzyka DPIA i zmapuj je na konkretne artykuły AI Act (rozporządzenie UE
2024/1689). Podaj numer artykułu i krótkie uzasadnienie. Uwzględnij też Annex III pkt 5a.
```

**Co Claude zidentyfikował i dlaczego:**

| Ryzyko | Artykuł AI Act | Uzasadnienie |
|--------|----------------|--------------|
| Wyciek danych | art. 15 | Dokładność i cyberbezpieczeństwo systemów high-risk |
| Błąd diagnostyczny | art. 9, 14, 15 | Zarządzanie ryzykiem, nadzór człowieka, dokładność |
| Bias danych | art. 10, 13 | Dane reprezentatywne, informacje dla użytkowników |
| Re-identyfikacja | art. 10 | Jakość i integralność danych |
| Bezpieczeństwo HPC | art. 15 | Cyberbezpieczeństwo |
| Wagi modelu | art. 11 | Dokumentacja techniczna |

Szczególnie istotna była dyskusja o **Annex III pkt 5a** (systemy AI jako wyroby medyczne). Claude wyjaśnił, że w fazie badawczej klasyfikacja jest "ograniczone", ale wdrożenie kliniczne automatycznie podniosłoby ją do "wysokiego ryzyka".

---

### Krok 5 — Szablon Jinja2

**Prompt wejściowy:**
```
Napisz szablon Jinja2 dla raportu DPIA w Markdown z 7 sekcjami. Sekcja 6 powinna
zawierać plan mitygacji podzielony na Pilne/Ważne/Zalecane. Użyj pętli Jinja2
do iteracji po tabeli ryzyk. Plik: templates/report.md.j2
```

**Trudność:** Pierwsze podejście używało `selectattr` do filtrowania ryzyk po priorytecie.
Szczegóły błędu opisano w sekcji "Co nie zadziałało".

---

### Krok 6 — Porównanie z innymi DPIA (poziom Celujący)

**Prompt wejściowy:**
```
Napisz szczegółowe porównanie DPIA SMARTudl z DPIA innych znanych systemów AI.
Porównaj z: (1) Spelthorne Borough Council AI Corporate Policy DPIA 2024
(https://democracy.spelthorne.gov.uk/documents/s66605/Appendix+C_DPIA.pdf),
(2) Royal College of Radiologists AI deployment fundamentals 2024
(https://www.rcr.ac.uk/media/sbdhwnfl/ai-deployment-fundamentals-for-medical-imaging-2024.pdf),
(3) Gilbert et al. 2025 Frontiers in Health Services o DPIA w NHS.
Zidentyfikuj luki w naszej DPIA i co robimy lepiej. Zapisz jako wyniki/porownanie_dpia.md
```

**Co Claude zrobił:** Pobrał rzeczywiste dokumenty PDF z podanych URL (WebFetch), przeanalizował je i wygenerował porównanie z tabelami, analizą luk i rekomendacjami. Identyfikacja luki z *exit strategy* i niejednoznaczności statusu anonimizacji CT po defacingu (pseudonimizacja vs. pełna anonimizacja według Gilbert et al. 2025) była kluczowa — to nie był wynik z wiedzy treningowej, ale z analizy konkretnych dokumentów.

---

## Decyzje projektowe i uzasadnienia

### Dlaczego CLI zamiast GUI/web?

Kurs ocenia głębokość analizy prawnej, nie wygląd aplikacji. CLI jest szybsze w implementacji, nie wymaga zależności od frameworków webowych (Flask, FastAPI) i ułatwia automatyzację — użytkownik może użyć `--load` do regeneracji raportu bez ponownego kwestionariusza. Flagą `--output-dir` można kierować wyniki do różnych folderów.

### Dlaczego Jinja2 zamiast f-stringów?

Szablon Jinja2 jest oddzielony od logiki aplikacji. Można:
- Zmienić format raportu bez modyfikacji kodu Python
- Potencjalnie eksportować do HTML → PDF przez `weasyprint`
- Testować szablon niezależnie od kodu

Alternatywą był prosty Python z f-stringami, ale utrzymanie 150-liniowego szablonu wbudowanego w kod byłoby nieczytelne.

### Dlaczego JSON dla odpowiedzi?

JSON jest czytelny dla człowieka i edytowalny ręcznie — ważne przy testowaniu narzędzia na różnych przypadkach. Format pozwala też na wersjonowanie odpowiedzi w git. Alternatywą było SQLite, ale byłoby overkill dla projektu jednoosobowego.

### Struktura matrycy ryzyk (skala 1–3, nie 1–5)

Skala 1–3 × 1–3 (max 9 punktów) zamiast popularnej 1–5 × 1–5:
- Prostsze do wypełnienia przez osobę niebędącą ekspertem ds. bezpieczeństwa
- Wystarczająco granularna dla etapu badawczego (nie certyfikowanego wyrobu medycznego)
- Próg wysokiego ryzyka: ≥ 6/9 (odpowiada 2/3 maksimum)
- Trzy stopnie priorytetu: Pilne (≥6), Ważne (≥3), Zalecane (<3)

### Predefiniowane vs. dynamiczne ryzyka

Zdecydowałem się na 6 predefiniowanych kategorii ryzyk zamiast pozwalania użytkownikowi na definiowanie własnych. Uzasadnienie: DPIA dla systemu medycznego zawsze powinna obejmować te same klasy ryzyk (wyciek danych art. 9, re-identyfikacja, błąd diagnostyczny, bias). Predefiniowane kategorie gwarantują, że żadna kluczowa klasa nie zostanie pominięta przez użytkownika nieznającego RODO.

---

## Co nie zadziałało i jak to rozwiązałem

### Problem 1: Nieprawidłowe nazwy plików z polskimi znakami i myślnikami

**Objaw:** System generował plik `dpia_smartudl_—_metal_artifact_reduction_(mar)_pipeline.md` zamiast `dpia_smartudl_mar.md`. Myślnik em-dash (—) i nawiasy były przekazywane bezpośrednio do nazwy pliku.

**Co próbowałem:** Proste `.replace(" ", "_")` — nie obsługiwało em-dasha i nawiasów.

**Rozwiązanie:** Dodanie funkcji `_slugify()` z regexem:
```python
def _slugify(text: str) -> str:
    import re
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)   # usuń znaki niebędące literami/cyframi
    text = re.sub(r"\s+", "_", text)       # spacje → podkreślenia
    text = re.sub(r"_+", "_", text)        # wielokrotne _ → pojedyncze
    return text.strip("_")[:50]            # obetnij do 50 znaków
```

Istniejący plik z błędną nazwą był już zapisany w systemie, więc ręcznie go przemianowałem przez `mv`.

---

### Problem 2: Formuła priorytetu dawała błędne wyniki

**Objaw:** Ryzyka o poziomie 6/9 (WYSOKIE) otrzymywały priorytet "Ważne" zamiast "Pilne".

**Pierwotna formuła:**
```python
priority_num = min(3, round((level / 9 * 2 + mapping["priority_base"] / 3)))
```

**Diagnoza:** Formuła mieszała dwa czynniki (poziom ryzyka i bazowy priorytet z mappingu) w sposób, który dla level=6 i priority_base=3 dawał zaokrąglenie do 2 → "Ważne". Było to zbyt skomplikowane i nieintuicyjne.

**Rozwiązanie:** Proste progi if/elif:
```python
if level >= 6:
    priority = "Pilne"
elif level >= 3:
    priority = "Ważne"
else:
    priority = "Zalecane"
```

Lepsza czytelność i bezpośrednie odzwierciedlenie semantyki (ryzyka WYSOKIE = zawsze Pilne, ŚREDNIE = Ważne, NISKIE = Zalecane).

---

### Problem 3: `selectattr` w Jinja2 nie filtrował po polskich stringach

**Objaw:** Sekcja "Pilne" w raporcie była pusta, mimo że tabela ryzyk zawierała pozycje z `priority = "Pilne"`.

**Pierwotny kod szablonu:**
```jinja2
{% for r in risk_table | selectattr("priority", "equalto", "Pilne") %}
- **{{ r.risk }}** — {{ r.mitigation }}
{% endfor %}
```

**Diagnoza:** Filtr `selectattr` z `equalto` nie dopasowywał polskich znaków (ę, ż, ź) w wyniku niezgodności kodowania między stringami Python a Jinja2 w konkretnej wersji środowiska. Technicznie wartości były identyczne, ale filtr zwracał pustą listę.

**Rozwiązanie:** Zastąpienie `selectattr` jawną pętlą z instrukcją `{% if %}` i obiektem `namespace` dla mutowalnej flagi:
```jinja2
{% set ns = namespace(found=false) %}
{% for r in risk_table %}{% if r.priority == "Pilne" %}{% set ns.found = true %}
- **{{ r.risk }}** — {{ r.mitigation }}
  *(poziom ryzyka: {{ r.level }}/9 | RODO: {{ r.rodo }} | AI Act: {{ r.ai_act }})*
{% endif %}{% endfor %}
{% if not ns.found %}*Brak ryzyk wymagających pilnego działania.*{% endif %}
```

Użycie `namespace` jest wymagane w Jinja2 — zmienne ustawione wewnątrz `{% for %}` nie są widoczne po pętli bez tego mechanizmu.

---

### Problem 4: Błąd narzędzia Write na istniejącym pliku

**Objaw:** Próba nadpisania `.gitignore` zwróciła błąd "File has not been read yet".

**Przyczyna:** Narzędzie Write wymaga wcześniejszego odczytania pliku przez Read, jeśli plik już istnieje (zabezpieczenie przed przypadkowym nadpisaniem).

**Rozwiązanie:** Zawsze Read → Edit lub Read → Write dla istniejących plików. Dla plików tworzonych od zera — Write bezpośrednio.

---

## Iteracje i zmiany w trakcie pracy

### Iteracja 1 — Planowanie i struktura (2026-05-09, rano)

- Omówienie planu krok po kroku z Claude
- Ustalenie 6 sekcji kwestionariusza i 6 kategorii ryzyk
- Decyzja o Jinja2 + JSON + CLI z argparse
- Stworzenie struktury katalogów repozytorium

### Iteracja 2 — Implementacja narzędzia (2026-05-09)

- Wygenerowanie `dpia_tool.py` (~350 linii)
- Wygenerowanie `templates/report.md.j2`
- Wygenerowanie `responses/smartudl_mar.json` z wypełnionymi odpowiedziami dla SMARTudl MAR
- **Wykryto i naprawiono:** błędna formuła priorytetu (Problem 2)

### Iteracja 3 — Generowanie raportu (2026-05-09)

- Uruchomienie `python dpia_tool.py --load responses/smartudl_mar.json`
- **Wykryto i naprawiono:** `selectattr` nie filtruje polskich stringów (Problem 3)
- **Wykryto i naprawiono:** błędne nazwy plików (Problem 1)
- Wygenerowanie `wyniki/dpia_smartudl.md` — pełny raport DPIA

### Iteracja 4 — Elementy Celujące (2026-05-09, po południu)

- Pobranie i analiza 3 zewnętrznych dokumentów DPIA/frameworków
- Wygenerowanie `wyniki/porownanie_dpia.md` z porównaniem
- Kluczowe odkrycie: Gilbert et al. (2025) wskazuje na niejednoznaczność statusu danych CT po defacingu — czy to pseudonimizacja czy pełna anonimizacja? Ta luka trafiła do sekcji rekomendacji.
- Aktualizacja `PROCESS.md` (ten plik)

---

## Wnioski z procesu

### Co AI zrobiło dobrze

**Generowanie kodu według specyfikacji:** Po opisaniu wymagań (6 sekcji, Jinja2, JSON, argparse) Claude wygenerował działający kod za pierwszym razem. Nie wymagał iteracji dla logiki głównej — tylko dla edge case'ów (polskie znaki, formuła priorytetu).

**Analiza dokumentów prawnych:** Claude pobrał rzeczywiste PDFy (Spelthorne Council, RCR) i wyciągnął konkretne informacje, a nie generyczne odpowiedzi "oparte na wiedzy treningowej". To znacząco podniosło jakość porównania.

**Mapowanie na artykuły:** Mapowanie ryzyk na konkretne artykuły RODO i AI Act było dokładne — weryfikowałem manualnie artykuły 9, 10, 13, 14, 15 AI Act i numery się zgadzały z treścią rozporządzenia.

### Co wymagało ręcznej interwencji

**Debugowanie zachowania Jinja2:** Problem z `selectattr` był trudny do zdiagnozowania — wymagał znajomości, że Jinja2 ma specyficzne zachowanie przy `namespace` wewnątrz pętli. Claude zaproponował oba: najpierw `selectattr` (nie zadziałał), potem jawną pętlę (zadziałała).

**Weryfikacja poprawności prawnej:** Nie polegałem ślepo na odpowiedziach Claude w kwestiach prawnych — sprawdzałem treść przywołanych artykułów RODO i AI Act. AI Act art. 50 (obowiązki transparentności dla systemów generujących treść) — Claude zastosował go dyskusyjnie do systemu generującego przetworzone obrazy CT, co wymagało ostrożnej oceny.

### Wnioski ogólne

1. **Specyfikuj format wyjściowy explicite.** Prompt "napisz narzędzie DPIA" daje gorszy rezultat niż "napisz narzędzie z argparse, Jinja2, JSON, 6 sekcjami, wyjście .md".

2. **Testuj edge case'y natychmiast.** Problem z polskimi znakami w Jinja2 pojawił się dopiero przy pierwszym uruchomieniu z rzeczywistymi danymi. Wcześniejszy test z prostymi angielskimi stringami go nie ujawnił.

3. **AI jest dobrym "pierwszym szkicem" kodu, nie końcowym.** Wygenerowany kod wymagał poprawek (formuła priorytetu, `selectattr`), ale był dobrym punktem startowym — szybciej niż pisanie od zera.

4. **Dokumentuj błędy na bieżąco.** Ten plik uzupełniałem równolegle z pracą. Retrospektywne rekonstruowanie "co nie zadziałało" jest znacznie trudniejsze.

---

*Dokumentacja procesu — Bartosz Lewandowski (254364), mini-projekt DPIA #26, PWr 2025/2026*
