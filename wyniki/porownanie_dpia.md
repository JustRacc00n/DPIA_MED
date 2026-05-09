# Porównanie DPIA — SMARTudl vs. znane systemy AI

> Autor: Bartosz Lewandowski (254364) | PWr 2025/2026
> Źródła: Gilbert et al. (2025) *Frontiers in Health Services*; Spelthorne Borough Council AI DPIA (2024);
> Royal College of Radiologists, *AI deployment fundamentals for medical imaging* (2024);
> CNIL guidance on DPIA for AI systems; EDPB Guidelines 9/2022

---

## 1. Przegląd porównywanych systemów

| Cecha | **SMARTudl MAR** (nasz projekt) | **Spelthorne Council AI Policy** (2024) | **NHS Medical Imaging AI** (RCR 2024) |
|-------|----------------------------------|------------------------------------------|----------------------------------------|
| Typ systemu | Sieć neuronowa do poprawy jakości obrazów CT | Ogólna polityka korporacyjna dla LLM/GenAI | Framework wdrożeń AI w radiologii klinicznej |
| Dane wrażliwe | ✅ Tak — art. 9 RODO (dane zdrowotne) | ❌ Nie — zakazano wprowadzania danych osobowych do narzędzi AI | ✅ Tak — dane medyczne pacjentów |
| Etap | Badawczy (nie kliniczny) | Operacyjny (wdrożony) | Kliniczny (wdrożenie produkcyjne) |
| Autonomiczne decyzje | ❌ Nie — lekarz w pętli | ❌ Nie — wymagany przegląd przez pracownika | ❌ Nie — radiolog podejmuje decyzje |
| Klasyfikacja AI Act | Ograniczone (badania) / potencjalnie Wysokie (klinicznie) | Ograniczone / Minimalne | Wysokie (Annex III pkt 5a) |
| Konsultacja IOD | Nie (faza badawcza) | Tak — DPO uczestniczył aktywnie | Wymagana — NHS ma dedykowane zespoły IG |
| Opublikowane DPIA | ✅ Tak (nasz raport) | ✅ Tak (jawny dokument rady miejskiej) | ⚠️ Częściowo — brak jednolitego standardu wg Gilbert et al. (2025) |

---

## 2. Porównanie identyfikacji ryzyk

### 2.1 Ryzyka w SMARTudl vs. Spelthorne Council

Spelthorne Council (DPIA dla GenAI) identyfikuje znacznie mniej ryzyk niż SMARTudl, co wynika z prostszego przypadku użycia (brak danych wrażliwych). Kluczowe różnice:

| Ryzyko | SMARTudl | Spelthorne |
|--------|----------|------------|
| Wyciek danych medycznych (art. 9 RODO) | ✅ Zidentyfikowane, poziom WYSOKI | ❌ Nie dotyczy — brak danych osobowych |
| Błąd diagnostyczny / nieprawidłowy wynik | ✅ Zidentyfikowane, poziom WYSOKI | ⚠️ Częściowo — ogólne ryzyko błędu AI |
| Re-identyfikacja przez AI | ✅ Zidentyfikowane (defacing, DICOM) | ❌ Nie rozważane |
| Bias danych / nierówna jakość | ✅ Zidentyfikowane | ✅ Zidentyfikowane — "AI może utrwalać bias" |
| Bezpieczeństwo infrastruktury | ✅ Zidentyfikowane | ✅ Zidentyfikowane — M365 security boundary |
| Transparentność wobec użytkownika | ✅ Oznaczanie "AI-processed" | ✅ Autor musi ujawnić użycie GenAI |

**Wniosek**: Spelthorne DPIA jest szablonem do prostych zastosowań korporacyjnych i nie nadaje się do systemów medycznych. Brakuje mu całkowicie kategorii ryzyk związanych z art. 9 RODO, re-identyfikacją i błędami diagnostycznymi — co udowadnia, że DPIA musi być dostosowane do kontekstu.

### 2.2 SMARTudl vs. wymagania NHS/RCR dla AI w radiologii

Royal College of Radiologists (2024) wskazuje następujące elementy DPIA dla AI w obrazowaniu medycznym, których **SMARTudl wymaga lub ma zaimplementowane**:

| Wymaganie RCR | Status w SMARTudl |
|---------------|-------------------|
| DPIA przed wdrożeniem | ✅ Przeprowadzone |
| Hazard log (rejestr zagrożeń) | ✅ Matryca ryzyk w sekcji 3 |
| Shadow mode assessment (walidacja "w cieniu") | ⚠️ Planowana — walidacja kliniczna przed użyciem |
| Szkolenie personelu w zakresie ograniczeń AI | ⚠️ Nie formalizowane — lekarz musi znać ograniczenia modelu |
| Niezależna walidacja | ✅ Planowane — PSNR/SSIM + ocena radiologa |
| Oznaczanie wyników AI | ✅ "AI-processed — not for direct clinical use" |
| Plan wycofania AI z użycia (exit strategy) | ❌ Brak — nie opisano co się dzieje gdy model zawodzi |

**Kluczowa luka zidentyfikowana przez porównanie**: SMARTudl nie opisuje **exit strategy** — procedury wycofania modelu z użycia w przypadku wykrycia błędów systemowych lub dryfu danych. RCR wskazuje to jako element obowiązkowy przy wdrożeniu klinicznym.

---

## 3. Porównanie podejść do konieczności DPIA

### CNIL: DPIA jako warunek dla AI Act high-risk

CNIL (fr. organ nadzorczy) stwierdza, że dla **wszystkich systemów AI wysokiego ryzyka** objętych AI Act, DPIA jest domyślnie wymagana jeśli przetwarzanie obejmuje dane osobowe. Co istotne dla SMARTudl:

- W fazie **badawczej**: podstawa prawna z art. 9 ust. 2 lit. j RODO + art. 89, DPIA jako *good practice*
- W fazie **klinicznej**: DPIA **obowiązkowe** (art. 35 RODO + AI Act Annex III pkt 5a) — system staje się wyrobem medycznym

CNIL wskazuje też, że DPIA dla systemów AI powinna uwzględniać **cykl życia modelu** (od treningu po wycofanie), co nasza DPIA pokrywa jedynie częściowo — brakuje sekcji o monitoringu po wdrożeniu.

### Gilbert et al. (2025): wyzwania systemowe DPIA w NHS

Badanie (University of Cambridge + University Hospitals Birmingham) identyfikuje kluczowe problemy DPIA dla AI w ochronie zdrowia w UK:

1. **Brak standaryzacji**: każda instytucja NHS wymaga własnego DPIA — brak jednolitego szablonu
2. **Ryzyko "governance gridlock"**: bezpieczeństwo kliniczne może być uzależnione od zatwierdzonego DPIA i vice versa
3. **Różne interpretacje "skutecznej anonimizacji"**: niektóre instytucje traktują zanonimizowane DICOM jako nadal podlegające RODO (pseudonimizacja vs. pełna anonimizacja)
4. **Ciągłe uczenie się modeli**: jeśli model uczy się na danych z praktyki klinicznej, DPIA wymaga aktualizacji

**Bezpośrednie implikacje dla SMARTudl**: punkt 3 jest szczególnie istotny — nasze założenie, że szpital dostarcza "zanonimizowane" dane, może być kwestionowane przez organ nadzorczy. Zdjęcia CT nawet po defacingu mogą być uznane za pseudonimizowane (możliwa re-identyfikacja przez specjalistę z dostępem do historii medycznej), nie w pełni anonimowe — co oznaczałoby, że RODO nadal ma zastosowanie.

---

## 4. Co SMARTudl robi lepiej niż porównywane systemy

| Aspekt | SMARTudl | Spelthorne | NHS (RCR) |
|--------|----------|------------|-----------|
| Mapowanie ryzyk na konkretne artykuły RODO | ✅ Tak | ❌ Nie | ⚠️ Ogólne |
| Mapowanie ryzyk na artykuły AI Act | ✅ Tak | ❌ Nie | ⚠️ Ogólne |
| Plan mitygacji z priorytetami (Pilne/Ważne/Zalecane) | ✅ Tak | ❌ Nie | ⚠️ Hazard log bez priorytetów |
| Opis przepływu danych krok po kroku | ✅ Szczegółowy | ⚠️ Ogólny | ✅ Tak |
| Narzędzie automatyzujące DPIA | ✅ dpia_tool.py | ❌ Szablon Word | ❌ Szablon Word |
| Uwzględnienie ryzyka wag modelu jako nośnika info | ✅ Tak | ❌ Nie | ❌ Nie |

---

## 5. Luki w DPIA SMARTudl — rekomendacje

Na podstawie porównania zidentyfikowano następujące braki, które należałoby uzupełnić przed wdrożeniem klinicznym:

**Priorytet: Pilny** (brak przy potencjalnym wdrożeniu klinicznym)
- Brak formalnej konsultacji z IOD
- Brak exit strategy (procedury wycofania modelu)
- Niejasność statusu anonimizacji — weryfikacja czy dane DICOM po anonimizacji to pseudonimizacja czy pełna anonimizacja

**Priorytet: Ważny**
- Brak sekcji o monitoringu i drycie modelu po wdrożeniu
- Brak planu aktualizacji DPIA przy zmianie zakresu przetwarzania

**Priorytet: Zalecany**
- Formalizacja szkolenia lekarzy w zakresie ograniczeń modelu
- Dokumentacja procesu wycofywania danych po zakończeniu projektu

---

## 6. Wnioski

Porównanie pokazuje, że DPIA SMARTudl jest **bardziej zaawansowane** od typowych korporacyjnych DPIA dla GenAI (jak Spelthorne), bo operuje na prawdziwych danych wrażliwych i wymaga głębszej analizy ryzyk medycznych. Jest jednocześnie **niepełne** w stosunku do wymagań klinicznych (RCR 2024, CNIL) — co jest uzasadnione etapem badawczym projektu, ale musi być uzupełnione przed ewentualnym wdrożeniem produkcyjnym.

Kluczowa obserwacja z Gilbert et al. (2025): granica między "zanonimizowanymi" a "pseudonimizowanymi" danymi CT jest niejednoznaczna i może być różnie interpretowana przez różne organy nadzorcze — co jest istotnym ryzykiem prawnym dla projektu SMARTudl, którego nie opisano wystarczająco w istniejącej DPIA.

---

*Źródła:*
- *Gilbert FJ et al. (2025). Data and data privacy impact assessments in the context of AI research and practice in the UK. Front. Health Serv. 5:1525955. https://doi.org/10.3389/frhs.2025.1525955*
- *Spelthorne Borough Council (2024). Artificial Intelligence Corporate Policy DPIA. https://democracy.spelthorne.gov.uk/documents/s66605/Appendix+C_DPIA.pdf*
- *Royal College of Radiologists (2024). AI deployment fundamentals for medical imaging. https://www.rcr.ac.uk/media/sbdhwnfl/ai-deployment-fundamentals-for-medical-imaging-2024.pdf*
- *CNIL (2024). Carrying out a data protection impact assessment. https://www.cnil.fr/en/carrying-out-protection-impact-assessment-if-necessary*
- *EDPB Guidelines 9/2022 on personal data breach notification*
