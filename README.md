# DPIA-MED — Półautomatyczne narzędzie DPIA dla systemów AI w medycynie

> Mini-projekt indywidualny | Kurs: Aspekty prawne, społeczne i etyczne w sztucznej inteligencji  
> Politechnika Wrocławska, semestr letni 2025/2026  
> Autor: Bartosz Lewandowski (254364)

---

## Cel projektu

Narzędzie przeprowadza **Data Protection Impact Assessment (DPIA)** zgodnie z wymogami RODO art. 35 dla systemów AI przetwarzających dane medyczne. Na podstawie odpowiedzi na pytania kwestionariusza generuje strukturalny raport DPIA w formacie Markdown, zawierający:

- opis systemu i przepływu danych,
- ocenę konieczności i proporcjonalności przetwarzania,
- matrycę ryzyk (prawdopodobieństwo × wpływ),
- mapowanie ryzyk na konkretne artykuły AI Act,
- plan mitygacji z priorytetami.

Narzędzie zostało przetestowane na realnym przypadku — pipeline'u Metal Artifact Reduction (MAR) z projektu SMARTudl (usuwanie artefaktów metalicznych z obrazów CT przy użyciu głębokich sieci neuronowych).

---

## Jak uruchomić

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/JustRacc00n/DPIA_MED.git
cd DPIA_MED

# 2. Utwórz wirtualne środowisko i zainstaluj zależności
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
# .venv\Scripts\activate       # Windows

pip install -r requirements.txt

# 3. Uruchom narzędzie
python dpia_tool.py

# 4. (opcjonalnie) Wczytaj zapisane odpowiedzi i regeneruj raport
python dpia_tool.py --load responses/smartudl_mar.json
```

---

## Co robi

- Prowadzi interaktywny kwestionariusz przez 6 sekcji DPIA (CLI)
- Zapisuje odpowiedzi do pliku JSON (możliwość wznowienia sesji)
- Generuje raport `.md` z uzupełnionymi sekcjami, tabelą ryzyk i planem mitygacji
- Mapuje zidentyfikowane ryzyka na artykuły RODO i AI Act
- Nadaje priorytety środkom zaradczym (Pilne / Ważne / Zalecane)

## Czego nie robi

- Nie zastępuje prawnika ani inspektora ochrony danych (IOD)
- Nie obejmuje DPIA dla systemów w fazie produkcyjnej wdrożonej klinicznie
- Nie obsługuje automatycznie eksportu do PDF (wymaga zewnętrznego `pandoc`)
- Nie przeprowadza konsultacji z organem nadzorczym (art. 36 RODO)

---

## Struktura repozytorium

```
dpia-med/
├── README.md               # Ten plik
├── PROCESS.md              # Dokumentacja procesu: prompty, decyzje, iteracje
├── dpia_tool.py            # Główny skrypt narzędzia
├── templates/
│   └── report.md.j2        # Szablon Jinja2 raportu DPIA
├── responses/
│   └── smartudl_mar.json   # Odpowiedzi dla testowego przypadku MAR
├── wyniki/
│   └── dpia_smartudl.md    # Wygenerowany raport DPIA dla SMARTudl
└── requirements.txt
```

---

## Wnioski z testowania na SMARTudl

System MAR z projektu SMARTudl **nie przetwarza danych osobowych** w normalnym trybie pracy (dane CT są anonimizowane po stronie szpitala przed przekazaniem). Jednak DPIA jest uzasadnione ze względu na:

1. Charakter danych (obrazy medyczne jako dane wrażliwe z art. 9 RODO, nawet po anonimizacji istnieje ryzyko re-identyfikacji przez defacing lub rekonstrukcję 3D twarzy)
2. Potencjalną klasyfikację jako system wysokiego ryzyka wg AI Act (Annex III, pkt 5a) w przypadku wdrożenia klinicznego
3. Współpracę z podmiotem medycznym i wynikające z tego obowiązki umowne

Szczegółowe wnioski: [`wyniki/dpia_smartudl.md`](wyniki/dpia_smartudl.md)
