# PROCESS.md — Dokumentacja procesu pracy

> Ten plik dokumentuje jak pracowałem nad mini-projektem: jakie narzędzia AI wykorzystałem,
> jakie prompty pisałem, jakie decyzje podjąłem i co nie zadziałało.

---

## Narzędzia AI użyte w projekcie

| Narzędzie | Do czego użyte |
|-----------|----------------|
| Claude (Cowork) | Planowanie struktury projektu, generowanie szkieletu kodu, konsultacje prawne dot. RODO/AI Act |
| GitHub Copilot | Uzupełnianie kodu w edytorze, generowanie docstringów |

---

## Prompty użyte podczas pracy

### Planowanie struktury narzędzia
```
Na podstawie wymagań RODO art. 35 i szablonów DPIA (CNIL, ICO) zaprojektuj
strukturę interaktywnego kwestionariusza Python do przeprowadzania DPIA dla
systemów AI przetwarzających dane medyczne. Określ sekcje, typy pytań
(zamknięte/otwarte) i logikę oceny ryzyka (matryca prawdopodobieństwo × wpływ).
```

### Mapowanie ryzyk na AI Act
```
Dla systemu AI do usuwania artefaktów metalicznych z obrazów CT (narzędzie
wspierające lekarza, nie decyzyjne) zidentyfikuj ryzyka DPIA i zmapuj je na
konkretne artykuły AI Act. System używa danych medycznych ze szpitala,
anonimizowanych przed przekazaniem. Podaj artykuł i krótkie uzasadnienie.
```

### Generowanie szablonu raportu Jinja2
```
Napisz szablon Jinja2 dla raportu DPIA w formacie Markdown. Szablon powinien
zawierać: opis systemu, tabelę ryzyk z kolumnami (ryzyko, prawdopodobieństwo,
wpływ, poziom, artykuł RODO, artykuł AI Act, środek zaradczy, priorytet),
sekcję wniosków i decyzji. Używaj zmiennych Jinja2 dla wszystkich pól
wypełnianych przez użytkownika.
```

---

## Decyzje projektowe i uzasadnienia

### Dlaczego CLI zamiast GUI/web?
Kurs ocenia głębokość analizy prawnej, nie wygląd aplikacji. CLI jest szybsze
w implementacji i łatwiejsze do uruchomienia bez zależności od frameworków webowych.
Użytkownik może przekierować output do pliku lub użyć `--load` do regeneracji raportu.

### Dlaczego Jinja2 zamiast f-stringów?
Szablon Jinja2 jest oddzielony od logiki — można zmienić format raportu bez
modyfikacji kodu Python. Ułatwia też potencjalny eksport do innych formatów
(HTML, a następnie PDF przez weasyprint).

### Dlaczego JSON dla odpowiedzi?
JSON jest czytelny dla człowieka i pozwala na ręczną edycję odpowiedzi bez
ponownego przechodzenia przez cały kwestionariusz. Ważne przy testowaniu
narzędzia na różnych przypadkach.

### Struktura matrycy ryzyk
Zdecydowałem się na skalę 1–3 (nie 1–5) dla prawdopodobieństwa i wpływu, bo:
- Prostsze do wypełnienia przez osobę niebędącą ekspertem
- Wystarczająco granularna dla projektu badawczego (nie produkcyjnego)
- Próg ryzyka wysokiego: >= 6 (z max 9)

---

## Co nie zadziałało i jak to rozwiązałem

*(sekcja uzupełniana na bieżąco podczas pracy)*

| Problem | Co próbowałem | Rozwiązanie |
|---------|---------------|-------------|
| | | |

---

## Iteracje i zmiany w trakcie pracy

*(sekcja uzupełniana na bieżąco)*

### Iteracja 1 — szkielet (data: 2026-05-09)
- Stworzono strukturę repozytorium
- Zdefiniowano sekcje DPIA i logikę pytań
- Zaimplementowano szkielet `dpia_tool.py`

---

## Wnioski z procesu

*(sekcja uzupełniana po zakończeniu projektu)*
