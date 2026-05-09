# Raport DPIA — SMARTudl — Metal Artifact Reduction (MAR) pipeline

> **Data Protection Impact Assessment** zgodnie z RODO art. 35
> Wygenerowano: 2026-05-09T10:00:00
> Narzędzie: DPIA-MED v1.0.0 | Bartosz Lewandowski (254364), PWr 2025/2026

---

## 1. Opis systemu

| Pole | Wartość |
|------|---------|
| **Nazwa systemu** | SMARTudl — Metal Artifact Reduction (MAR) pipeline |
| **Cel przetwarzania** | Usuwanie artefaktów metalicznych z obrazów tomografii komputerowej (CT) przy użyciu głębokich sieci neuronowych, w celu poprawy jakości diagnostycznej obrazów pacjentów z implantami metalowymi (protezy, śruby ortopedyczne, implanty dentystyczne). System ma charakter wspierający — nie podejmuje decyzji diagnostycznych. |
| **Przetwarzane dane** | Obrazy tomografii komputerowej w formacie DICOM (28 realnych skanów ze szpitala + publiczne datasety: AAPM CT MAR, DeepLesion). Dane mogą zawierać przekroje głowy, klatki piersiowej i brzucha. Przed przekazaniem do zespołu dane są anonimizowane po stronie szpitala. |
| **Podmioty danych** | Pacjenci szpitala partnerskiego posiadający metalowe implanty (protezy stawowe, śruby ortopedyczne, implanty dentystyczne). Dane szpitalne: 28 osób. Dane publiczne: anonimowe zbiory bez możliwości identyfikacji. |
| **Zautomatyzowane decyzje** | nie |
| **Duża skala** | nie |
| **Dane wrażliwe (art. 9 RODO)** | tak |

### Przepływ danych

Szpital (eksport DICOM z usunięciem identyfikatorów) → zaszyfrowany nośnik fizyczny → Bartosz Lewandowski (weryfikacja anonimizacji + defacing) → usunięcie niezanonimizowanych plików → klaster HPC Helios/PLGrid (SSH/SFTP, odizolowana przestrzeń robocza) → trening modelu MAR → wagi modelu + wyniki → publikacja (bez danych szpitalnych).

---

## 2. Konieczność i proporcjonalność

| Aspekt | Opis |
|--------|------|
| **Podstawa prawna** | art. 9 ust. 2 lit. j RODO (przetwarzanie do celów badań naukowych) w związku z art. 89 RODO (zabezpieczenia przy przetwarzaniu do celów naukowych). Podstawa uzupełniająca: Data Use Agreement podpisana ze szpitalem regulująca zakres i cel przetwarzania. |
| **Minimalizacja danych** | Zasada minimalizacji (art. 5 ust. 1 lit. c RODO) jest realizowana przez: (1) anonimizację danych przed przekazaniem, (2) ograniczenie dostępu do danych niezanonimizowanych wyłącznie do jednej osoby, (3) natychmiastowe usunięcie surowych danych po anonimizacji, (4) brak przesyłania danych szpitalnych poza Polskę. |
| **Okres retencji** | Dane szpitalne (zanonimizowane): przechowywane na czas realizacji projektu. Niezanonimizowane dane: usuwane niezwłocznie po anonimizacji (brak kopii zapasowych). Po zakończeniu projektu: zanonimizowane dane usuwane zgodnie z warunkami DUA. Wagi modelu: mogą być przechowywane dłużej, ale bez możliwości publikacji bez zgody szpitala. |
| **Anonimizacja / pseudonimizacja** | Wieloetapowa anonimizacja danych DICOM: (1) usunięcie bezpośrednich identyfikatorów z nagłówków pliku (imię, nazwisko, PESEL, data urodzenia, adres, ID pacjenta w systemie szpitalnym); (2) uogólnienie dat — zastąpienie dokładnej daty urodzenia i badania samym rokiem; (3) weryfikacja warstwy wizualnej skanów i zamazanie ewentualnych danych nałożonych na piksele przez sprzęt medyczny; (4) defacing — algorytmiczne usunięcie rysów twarzy z skanów 3D obejmujących twarzoczaszkę. |
| **Nadzór człowieka (human-in-the-loop)** | Lekarz/radiolog pozostaje w pętli decyzyjnej na każdym etapie diagnostycznym. Model przetwarza obrazy jako narzędzie wspomagające (human-in-the-loop): przygotowanie danych (ocena jakości przez badacza), ocena wyników modelu (weryfikacja przez specjalistę), interpretacja kliniczna (wyłączna kompetencja lekarza). Obrazy przetworzone przez AI są oznaczane jako 'AI-processed'. |

---

## 3. Matryca ryzyk

> Skala: Prawdopodobieństwo × Wpływ (1–3 × 1–3).
> Poziom ryzyka wysokiego: ≥ 6/9. **Ogólny poziom ryzyka: WYSOKIE**

| # | Ryzyko | P | W | Poziom | Ocena | Art. RODO | Art. AI Act | Środek zaradczy | Priorytet |
|---|--------|---|---|--------|-------|-----------|-------------|-----------------|-----------|
| 1 | Wyciek lub nieautoryzowany dostęp do danych medycznych | 2 | 3 | 6/9 | WYSOKIE | art. 5 ust. 1 lit. f, art. 32 | art. 15 (dokładność i cyberbezpieczeństwo) | Szyfrowanie nośników i kanałów transmisji, kontrola dostępu, monitoring | **Pilne** |
| 2 | Błąd diagnostyczny spowodowany przez model (usunięcie istotnej informacji klinicznej razem z artefaktem) | 2 | 3 | 6/9 | WYSOKIE | art. 5 ust. 1 lit. d (rzetelność danych) | art. 9 (zarządzanie ryzykiem), art. 14 (nadzór człowieka), art. 15 | Walidacja kliniczna, human-in-the-loop, oznaczanie obrazów jako przetworzonych przez AI | **Pilne** |
| 3 | Nierówna jakość działania modelu dla różnych grup pacjentów lub typów implantów (bias danych) | 2 | 2 | 4/9 | ŚREDNIE | art. 5 ust. 1 lit. d (rzetelność) | art. 10 (dane reprezentatywne), art. 13 (informacje dla użytkowników) | Zróżnicowany zbiór danych treningowych, testy na różnych grupach, dokumentacja ograniczeń | **Ważne** |
| 4 | Re-identyfikacja pacjenta pomimo anonimizacji (np. defacing, rekonstrukcja 3D twarzy) | 1 | 3 | 3/9 | ŚREDNIE | art. 9 (dane wrażliwe), art. 89 (zabezpieczenia naukowe) | art. 10 (jakość danych) | Defacing, usunięcie metadanych DICOM, pseudonimizacja identyfikatorów | **Ważne** |
| 5 | Naruszenie bezpieczeństwa danych na infrastrukturze obliczeniowej (np. klaster HPC) | 1 | 2 | 2/9 | NISKIE | art. 32 (bezpieczeństwo przetwarzania) | art. 15 (cyberbezpieczeństwo) | Szyfrowane kanały (SSH/SFTP), odizolowana przestrzeń robocza na klastrze HPC | **Zalecane** |
| 6 | Nieautoryzowane udostępnienie wag modelu wytrenowanego na danych szpitalnych | 1 | 2 | 2/9 | NISKIE | art. 9 (dane wrażliwe — wagi mogą enkodować info o pacjentach) | art. 11 (dokumentacja techniczna) | Zakaz publicznego udostępniania wag bez zgody partnera medycznego, umowa z szpitalem | **Zalecane** |


*P = Prawdopodobieństwo, W = Wpływ*

---

## 4. Środki zaradcze

### Techniczne

Szyfrowanie nośników fizycznych (full-disk encryption, silne hasło); przesyłanie danych wyłącznie przez SSH/SFTP; odizolowana przestrzeń robocza na klastrze Helios; brak dostępu do danych niezanonimizowanych dla pozostałych członków zespołu; brak kopii zapasowych danych surowych.

### Organizacyjne

Data Use Agreement podpisana ze szpitalem (zakres, cel, warunki usunięcia danych); ograniczenie dostępu do danych niezanonimizowanych wyłącznie do Bartosza Lewandowskiego; procedura natychmiastowego usunięcia niezanonimizowanych plików po anonimizacji; świadome korzystanie z infrastruktury PLGrid zgodnie z regulaminem (cytowanie Heliosa w publikacjach); brak możliwości udostępniania danych szpitalnych ani wag modelu bez wyraźnej zgody szpitala.

### Anonimizacja danych DICOM

Anonimizacja plików DICOM w 4 etapach: (1) Usunięcie tagów identyfikacyjnych z nagłówka DICOM: PatientName, PatientID, PatientBirthDate, PatientSex (pełna data → rok), StudyDate, StudyTime, InstitutionName, ReferringPhysicianName, PatientAddress; (2) Przypisanie losowego pseudonimu jako nowego PatientID; (3) Weryfikacja warstwy pikselowej — sprawdzenie czy sprzęt medyczny nie nałożył danych na obraz (pixel burn-in) i zamazanie ewentualnych napisów; (4) Defacing algorytmem usuwającym zewnętrzne rysy twarzy z skanów 3D (dotyczy skanów obejmujących głowę i twarzoczaszkę).

### Walidacja jakości modelu

Walidacja ilościowa na zbiorze testowym: metryki PSNR (Peak Signal-to-Noise Ratio) i SSIM (Structural Similarity Index) porównywane z obrazami referencyjnymi. Walidacja jakościowa: ocena przez specjalistę radiologii — czy kliniczne struktury anatomiczne są zachowane. Oznaczanie wszystkich obrazów przetworzonych przez model adnotacją 'AI-processed — not for direct clinical use'. Testy na zróżnicowanych przypadkach (różne typy implantów, różne protokoły skanowania).

---

## 5. Klasyfikacja wg AI Act

| Pole | Wartość |
|------|---------|
| **Klasyfikacja ryzyka** | ograniczone |
| **Uzasadnienie** | W obecnej formie system jest narzędziem badawczym wspomagającym poprawę jakości obrazów CT — nie podejmuje autonomicznych decyzji medycznych i nie jest wdrożony klinicznie. Annex III pkt 5a AI Act obejmuje systemy AI przeznaczone do stosowania jako wyroby medyczne lub w wyrobach medycznych w rozumieniu dyrektywy 93/42/EWG lub rozporządzenia (UE) 2017/745 — co nie dotyczy etapu badawczego projektu. Gdyby system został włączony do produktu klinicznego lub używany bezpośrednio w diagnostyce, wymagałaby klasyfikacji jako wysokiego ryzyka. Ograniczone obowiązki transparentności (art. 50 AI Act) mogą dotyczyć systemu jeśli generuje treści mogące być mylone z autentycznymi obrazami medycznymi. |
| **Obowiązki** | Transparentność: oznaczanie przetworzonych obrazów jako 'AI-processed' (art. 13 AI Act — informacje dla użytkowników); nadzór człowieka na każdym etapie diagnostycznym (art. 14 AI Act); zarządzanie ryzykiem przez cały cykl życia systemu (art. 9 AI Act); odpowiednia jakość i reprezentatywność danych treningowych — unikanie bias wobec grup pacjentów (art. 10 AI Act); dokumentacja techniczna opisująca ograniczenia modelu (art. 11 AI Act w przypadku klasyfikacji jako high-risk). |

---

## 6. Plan mitygacji z priorytetami

Poniżej zestawienie środków zaradczych posortowanych według priorytetu:

### 🔴 Pilne



- **Wyciek lub nieautoryzowany dostęp do danych medycznych** — Szyfrowanie nośników i kanałów transmisji, kontrola dostępu, monitoring
  *(poziom ryzyka: 6/9 | RODO: art. 5 ust. 1 lit. f, art. 32 | AI Act: art. 15 (dokładność i cyberbezpieczeństwo))*

- **Błąd diagnostyczny spowodowany przez model (usunięcie istotnej informacji klinicznej razem z artefaktem)** — Walidacja kliniczna, human-in-the-loop, oznaczanie obrazów jako przetworzonych przez AI
  *(poziom ryzyka: 6/9 | RODO: art. 5 ust. 1 lit. d (rzetelność danych) | AI Act: art. 9 (zarządzanie ryzykiem), art. 14 (nadzór człowieka), art. 15)*



### 🟡 Ważne



- **Nierówna jakość działania modelu dla różnych grup pacjentów lub typów implantów (bias danych)** — Zróżnicowany zbiór danych treningowych, testy na różnych grupach, dokumentacja ograniczeń
  *(poziom ryzyka: 4/9 | RODO: art. 5 ust. 1 lit. d (rzetelność) | AI Act: art. 10 (dane reprezentatywne), art. 13 (informacje dla użytkowników))*

- **Re-identyfikacja pacjenta pomimo anonimizacji (np. defacing, rekonstrukcja 3D twarzy)** — Defacing, usunięcie metadanych DICOM, pseudonimizacja identyfikatorów
  *(poziom ryzyka: 3/9 | RODO: art. 9 (dane wrażliwe), art. 89 (zabezpieczenia naukowe) | AI Act: art. 10 (jakość danych))*



### 🟢 Zalecane



- **Naruszenie bezpieczeństwa danych na infrastrukturze obliczeniowej (np. klaster HPC)** — Szyfrowane kanały (SSH/SFTP), odizolowana przestrzeń robocza na klastrze HPC
  *(poziom ryzyka: 2/9 | RODO: art. 32 (bezpieczeństwo przetwarzania) | AI Act: art. 15 (cyberbezpieczeństwo))*

- **Nieautoryzowane udostępnienie wag modelu wytrenowanego na danych szpitalnych** — Zakaz publicznego udostępniania wag bez zgody partnera medycznego, umowa z szpitalem
  *(poziom ryzyka: 2/9 | RODO: art. 9 (dane wrażliwe — wagi mogą enkodować info o pacjentach) | AI Act: art. 11 (dokumentacja techniczna))*



---

## 7. Wnioski i decyzja

| Pole | Wartość |
|------|---------|
| **Decyzja** | **wdrożyć po wdrożeniu środków zaradczych** |
| **Uzasadnienie** | System MAR w fazie badawczej może być używany po potwierdzeniu wdrożenia opisanych środków technicznych i organizacyjnych. Dwa ryzyka wysokiego poziomu (wyciek danych medycznych oraz błąd diagnostyczny spowodowany przez model) wymagają priorytetowego zaadresowania: szyfrowania nośników i kanałów transmisji oraz utrzymania nadzoru lekarza z obligatoryjnym oznaczaniem obrazów przetworzonych przez AI. System nie powinien być używany w praktyce klinicznej bez uprzedniej pełnej walidacji klinicznej i zmiany klasyfikacji wg AI Act na 'wysokie ryzyko' z odpowiadającymi obowiązkami compliance. |
| **Konsultacja z IOD** | nie |


> ⚠️ **Uwaga:** Zidentyfikowano ryzyka wysokiego poziomu. Przed przetwarzaniem danych należy wdrożyć środki zaradcze oznaczone jako **Pilne**. Rozważyć uprzednią konsultację z organem nadzorczym (art. 36 RODO).


---

*Raport wygenerowany przez DPIA-MED — narzędzie półautomatyczne. Nie zastępuje opinii prawnej ani decyzji Inspektora Ochrony Danych.*