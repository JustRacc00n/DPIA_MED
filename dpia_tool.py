#!/usr/bin/env python3
"""
dpia_tool.py — Półautomatyczne narzędzie DPIA dla systemów AI w medycynie
Autor: Bartosz Lewandowski (254364)
Kurs: Aspekty prawne, społeczne i etyczne w sztucznej inteligencji, PWr 2025/2026

Przeprowadza interaktywny kwestionariusz DPIA zgodnie z RODO art. 35,
generuje strukturalny raport Markdown z matrycą ryzyk i planem mitygacji.
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


# ---------------------------------------------------------------------------
# Definicja kwestionariusza DPIA
# ---------------------------------------------------------------------------

SECTIONS = [
    {
        "id": "system",
        "title": "Sekcja 1 — Opis systemu",
        "questions": [
            {
                "id": "system_name",
                "text": "Nazwa systemu AI",
                "type": "open",
            },
            {
                "id": "system_purpose",
                "text": "Cel przetwarzania danych (co system robi i po co)",
                "type": "open",
            },
            {
                "id": "data_types",
                "text": "Jakie dane są przetwarzane? (opisz krótko)",
                "type": "open",
            },
            {
                "id": "data_subjects",
                "text": "Czyje dane są przetwarzane? (np. pacjenci, lekarze)",
                "type": "open",
            },
            {
                "id": "data_flow",
                "text": "Opisz przepływ danych od źródła do modelu AI",
                "type": "open",
            },
            {
                "id": "is_automated_decision",
                "text": "Czy system podejmuje autonomiczne decyzje wywołujące skutki prawne lub podobnie istotne skutki?",
                "type": "yesno",
            },
            {
                "id": "is_large_scale",
                "text": "Czy przetwarzanie odbywa się na dużą skalę (duże wolumeny danych lub wielu podmiotów)?",
                "type": "yesno",
            },
            {
                "id": "is_sensitive_data",
                "text": "Czy przetwarzane dane należą do szczególnych kategorii z art. 9 RODO (dane zdrowotne, genetyczne, biometryczne itp.)?",
                "type": "yesno",
            },
        ],
    },
    {
        "id": "necessity",
        "title": "Sekcja 2 — Konieczność i proporcjonalność",
        "questions": [
            {
                "id": "legal_basis",
                "text": "Jaka jest podstawa prawna przetwarzania? (np. art. 9 ust. 2 lit. j RODO — cele naukowe)",
                "type": "open",
            },
            {
                "id": "data_minimization",
                "text": "Czy przetwarzasz tylko dane niezbędne do celu? Opisz jak zapewniasz minimalizację danych (art. 5 ust. 1 lit. c RODO).",
                "type": "open",
            },
            {
                "id": "retention_period",
                "text": "Jak długo dane są przechowywane i co się z nimi dzieje po zakończeniu projektu?",
                "type": "open",
            },
            {
                "id": "anonymization",
                "text": "Czy dane są anonimizowane lub pseudonimizowane? Opisz zastosowane metody.",
                "type": "open",
            },
            {
                "id": "human_oversight",
                "text": "Czy człowiek pozostaje w pętli decyzyjnej (human-in-the-loop)? Opisz na jakim etapie.",
                "type": "open",
            },
        ],
    },
    {
        "id": "risks",
        "title": "Sekcja 3 — Identyfikacja i ocena ryzyk",
        "description": (
            "Dla każdego ryzyka podaj: prawdopodobieństwo (1=niskie, 2=średnie, 3=wysokie) "
            "oraz wpływ (1=niski, 2=średni, 3=wysoki). "
            "Poziom ryzyka = prawdopodobieństwo × wpływ. Próg ryzyka wysokiego: >= 6."
        ),
        "questions": [
            {
                "id": "risk_data_breach",
                "text": "Ryzyko: Wyciek lub nieautoryzowany dostęp do danych medycznych",
                "type": "risk",
            },
            {
                "id": "risk_reidentification",
                "text": "Ryzyko: Re-identyfikacja pacjenta pomimo anonimizacji (np. defacing, rekonstrukcja 3D twarzy)",
                "type": "risk",
            },
            {
                "id": "risk_diagnostic_error",
                "text": "Ryzyko: Błąd diagnostyczny spowodowany przez model (usunięcie istotnej informacji klinicznej razem z artefaktem)",
                "type": "risk",
            },
            {
                "id": "risk_bias",
                "text": "Ryzyko: Nierówna jakość działania modelu dla różnych grup pacjentów lub typów implantów (bias danych)",
                "type": "risk",
            },
            {
                "id": "risk_infrastructure",
                "text": "Ryzyko: Naruszenie bezpieczeństwa danych na infrastrukturze obliczeniowej (np. klaster HPC)",
                "type": "risk",
            },
            {
                "id": "risk_model_weights",
                "text": "Ryzyko: Nieautoryzowane udostępnienie wag modelu wytrenowanego na danych szpitalnych",
                "type": "risk",
            },
        ],
    },
    {
        "id": "measures",
        "title": "Sekcja 4 — Środki zaradcze",
        "questions": [
            {
                "id": "measure_technical",
                "text": "Jakie techniczne środki bezpieczeństwa są stosowane? (szyfrowanie, kontrola dostępu, itp.)",
                "type": "open",
            },
            {
                "id": "measure_organizational",
                "text": "Jakie organizacyjne środki są stosowane? (umowy, szkolenia, procedury, itp.)",
                "type": "open",
            },
            {
                "id": "measure_anonymization_method",
                "text": "Opisz dokładnie zastosowaną metodę anonimizacji danych DICOM",
                "type": "open",
            },
            {
                "id": "measure_validation",
                "text": "Jak walidowana jest jakość i bezpieczeństwo wyników modelu?",
                "type": "open",
            },
        ],
    },
    {
        "id": "ai_act",
        "title": "Sekcja 5 — Klasyfikacja wg AI Act",
        "questions": [
            {
                "id": "ai_act_classification",
                "text": "Jaka jest klasyfikacja ryzyka systemu wg AI Act? (niedopuszczalne / wysokie / ograniczone / minimalne)",
                "type": "choice",
                "options": ["niedopuszczalne", "wysokie", "ograniczone", "minimalne"],
            },
            {
                "id": "ai_act_justification",
                "text": "Uzasadnij klasyfikację (odwołaj się do Annex III lub konkretnych artykułów AI Act)",
                "type": "open",
            },
            {
                "id": "ai_act_obligations",
                "text": "Jakie obowiązki z AI Act dotyczą tego systemu?",
                "type": "open",
            },
        ],
    },
    {
        "id": "conclusion",
        "title": "Sekcja 6 — Wnioski i decyzja",
        "questions": [
            {
                "id": "conclusion_decision",
                "text": "Decyzja końcowa",
                "type": "choice",
                "options": [
                    "wdrożyć bez zastrzeżeń",
                    "wdrożyć po wdrożeniu środków zaradczych",
                    "nie wdrażać — ryzyko zbyt wysokie",
                    "wymagana konsultacja z organem nadzorczym (art. 36 RODO)",
                ],
            },
            {
                "id": "conclusion_summary",
                "text": "Krótkie uzasadnienie decyzji",
                "type": "open",
            },
            {
                "id": "dpo_consulted",
                "text": "Czy skonsultowano się z Inspektorem Ochrony Danych (IOD)?",
                "type": "yesno",
            },
        ],
    },
]

# Mapowanie ryzyk na artykuły RODO i AI Act
RISK_MAPPING = {
    "risk_data_breach": {
        "rodo": "art. 5 ust. 1 lit. f, art. 32",
        "ai_act": "art. 15 (dokładność i cyberbezpieczeństwo)",
        "mitigation": "Szyfrowanie nośników i kanałów transmisji, kontrola dostępu, monitoring",
        "priority_base": 3,
    },
    "risk_reidentification": {
        "rodo": "art. 9 (dane wrażliwe), art. 89 (zabezpieczenia naukowe)",
        "ai_act": "art. 10 (jakość danych)",
        "mitigation": "Defacing, usunięcie metadanych DICOM, pseudonimizacja identyfikatorów",
        "priority_base": 3,
    },
    "risk_diagnostic_error": {
        "rodo": "art. 5 ust. 1 lit. d (rzetelność danych)",
        "ai_act": "art. 9 (zarządzanie ryzykiem), art. 14 (nadzór człowieka), art. 15",
        "mitigation": "Walidacja kliniczna, human-in-the-loop, oznaczanie obrazów jako przetworzonych przez AI",
        "priority_base": 2,
    },
    "risk_bias": {
        "rodo": "art. 5 ust. 1 lit. d (rzetelność)",
        "ai_act": "art. 10 (dane reprezentatywne), art. 13 (informacje dla użytkowników)",
        "mitigation": "Zróżnicowany zbiór danych treningowych, testy na różnych grupach, dokumentacja ograniczeń",
        "priority_base": 2,
    },
    "risk_infrastructure": {
        "rodo": "art. 32 (bezpieczeństwo przetwarzania)",
        "ai_act": "art. 15 (cyberbezpieczeństwo)",
        "mitigation": "Szyfrowane kanały (SSH/SFTP), odizolowana przestrzeń robocza na klastrze HPC",
        "priority_base": 2,
    },
    "risk_model_weights": {
        "rodo": "art. 9 (dane wrażliwe — wagi mogą enkodować info o pacjentach)",
        "ai_act": "art. 11 (dokumentacja techniczna)",
        "mitigation": "Zakaz publicznego udostępniania wag bez zgody partnera medycznego, umowa z szpitalem",
        "priority_base": 2,
    },
}

PRIORITY_LABELS = {1: "Zalecane", 2: "Ważne", 3: "Pilne"}


# ---------------------------------------------------------------------------
# Funkcje pomocnicze
# ---------------------------------------------------------------------------

def ask_open(question_text: str) -> str:
    print(f"\n  {question_text}")
    print("  > ", end="")
    return input().strip()


def ask_yesno(question_text: str) -> str:
    while True:
        print(f"\n  {question_text} [tak/nie]")
        print("  > ", end="")
        answer = input().strip().lower()
        if answer in ("tak", "nie", "t", "n"):
            return "tak" if answer in ("tak", "t") else "nie"
        print("  Proszę wpisać 'tak' lub 'nie'.")


def ask_choice(question_text: str, options: list) -> str:
    print(f"\n  {question_text}")
    for i, opt in enumerate(options, 1):
        print(f"    {i}. {opt}")
    while True:
        print("  Wybierz numer > ", end="")
        try:
            idx = int(input().strip()) - 1
            if 0 <= idx < len(options):
                return options[idx]
        except ValueError:
            pass
        print(f"  Proszę wpisać liczbę od 1 do {len(options)}.")


def ask_risk(question_text: str) -> dict:
    print(f"\n  {question_text}")
    while True:
        print("  Prawdopodobieństwo (1=niskie, 2=średnie, 3=wysokie) > ", end="")
        try:
            prob = int(input().strip())
            if 1 <= prob <= 3:
                break
        except ValueError:
            pass
        print("  Proszę wpisać 1, 2 lub 3.")
    while True:
        print("  Wpływ (1=niski, 2=średni, 3=wysoki) > ", end="")
        try:
            impact = int(input().strip())
            if 1 <= impact <= 3:
                break
        except ValueError:
            pass
        print("  Proszę wpisać 1, 2 lub 3.")
    level = prob * impact
    level_label = "WYSOKIE" if level >= 6 else ("ŚREDNIE" if level >= 3 else "NISKIE")
    print(f"  → Poziom ryzyka: {level}/9 ({level_label})")
    return {"probability": prob, "impact": impact, "level": level, "level_label": level_label}


def run_questionnaire() -> dict:
    """Przeprowadza interaktywny kwestionariusz DPIA."""
    responses = {
        "meta": {
            "generated_at": datetime.now().isoformat(),
            "tool_version": "1.0.0",
        }
    }

    print("\n" + "=" * 70)
    print("  DPIA-MED — Kwestionariusz Data Protection Impact Assessment")
    print("  Zgodnie z RODO art. 35 | Bartosz Lewandowski, PWr 2025/2026")
    print("=" * 70)
    print("\nNarzędzie przeprowadzi Cię przez 6 sekcji DPIA.")
    print("Odpowiedzi zostaną zapisane do pliku JSON i użyte do wygenerowania raportu.\n")

    for section in SECTIONS:
        print(f"\n{'─' * 70}")
        print(f"  {section['title']}")
        if "description" in section:
            print(f"  {section['description']}")
        print(f"{'─' * 70}")

        section_responses = {}
        for q in section["questions"]:
            if q["type"] == "open":
                section_responses[q["id"]] = ask_open(q["text"])
            elif q["type"] == "yesno":
                section_responses[q["id"]] = ask_yesno(q["text"])
            elif q["type"] == "choice":
                section_responses[q["id"]] = ask_choice(q["text"], q["options"])
            elif q["type"] == "risk":
                section_responses[q["id"]] = ask_risk(q["text"])

        responses[section["id"]] = section_responses

    return responses


def calculate_overall_risk(responses: dict) -> str:
    """Oblicza ogólny poziom ryzyka na podstawie najwyższego zidentyfikowanego ryzyka."""
    max_level = 0
    for risk_id in RISK_MAPPING:
        risk_data = responses.get("risks", {}).get(risk_id, {})
        if isinstance(risk_data, dict) and "level" in risk_data:
            max_level = max(max_level, risk_data["level"])
    if max_level >= 6:
        return "WYSOKIE"
    elif max_level >= 3:
        return "ŚREDNIE"
    return "NISKIE"


def build_risk_table(responses: dict) -> list:
    """Buduje tabelę ryzyk z mapowaniem na RODO i AI Act."""
    table = []
    risk_responses = responses.get("risks", {})

    for risk_id, mapping in RISK_MAPPING.items():
        risk_data = risk_responses.get(risk_id, {})
        if not isinstance(risk_data, dict):
            continue

        level = risk_data.get("level", 0)
        # Priorytet środka zaradczego: kombinacja poziomu ryzyka i priority_base
        priority_score = min(3, round((level / 9 * 2 + mapping["priority_base"] / 3) ))
        priority = PRIORITY_LABELS.get(priority_score, "Zalecane")

        # Znajdź opis ryzyka z kwestionariusza
        risk_label = next(
            (q["text"] for s in SECTIONS for q in s["questions"] if q["id"] == risk_id),
            risk_id,
        )

        table.append({
            "risk": risk_label.replace("Ryzyko: ", ""),
            "probability": risk_data.get("probability", "-"),
            "impact": risk_data.get("impact", "-"),
            "level": level,
            "level_label": risk_data.get("level_label", "-"),
            "rodo": mapping["rodo"],
            "ai_act": mapping["ai_act"],
            "mitigation": mapping["mitigation"],
            "priority": priority,
        })

    return sorted(table, key=lambda x: x["level"], reverse=True)


def generate_report(responses: dict, output_path: Path) -> None:
    """Generuje raport DPIA w formacie Markdown na podstawie odpowiedzi."""
    templates_dir = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    template = env.get_template("report.md.j2")

    risk_table = build_risk_table(responses)
    overall_risk = calculate_overall_risk(responses)

    context = {
        "responses": responses,
        "risk_table": risk_table,
        "overall_risk": overall_risk,
        "generated_at": responses["meta"]["generated_at"],
    }

    report_content = template.render(**context)
    output_path.write_text(report_content, encoding="utf-8")
    print(f"\n✓ Raport DPIA zapisany: {output_path}")


def save_responses(responses: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(responses, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ Odpowiedzi zapisane: {output_path}")


def load_responses(input_path: Path) -> dict:
    return json.loads(input_path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Główna funkcja
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="DPIA-MED — Półautomatyczne narzędzie DPIA dla systemów AI w medycynie"
    )
    parser.add_argument(
        "--load",
        type=Path,
        help="Wczytaj zapisane odpowiedzi z pliku JSON i regeneruj raport (pomija kwestionariusz)",
        metavar="PLIK.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("wyniki"),
        help="Katalog wyjściowy dla raportu (domyślnie: wyniki/)",
    )
    parser.add_argument(
        "--responses-dir",
        type=Path,
        default=Path("responses"),
        help="Katalog dla plików JSON z odpowiedziami (domyślnie: responses/)",
    )
    args = parser.parse_args()

    if args.load:
        print(f"Wczytywanie odpowiedzi z: {args.load}")
        responses = load_responses(args.load)
    else:
        responses = run_questionnaire()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        system_name = responses.get("system", {}).get("system_name", "dpia").replace(" ", "_").lower()
        responses_path = args.responses_dir / f"{system_name}_{timestamp}.json"
        save_responses(responses, responses_path)

    # Generuj raport
    args.output_dir.mkdir(parents=True, exist_ok=True)
    system_name = responses.get("system", {}).get("system_name", "dpia").replace(" ", "_").lower()
    report_path = args.output_dir / f"dpia_{system_name}.md"
    generate_report(responses, report_path)

    print(f"\nGotowe! Otwórz raport: {report_path}")


if __name__ == "__main__":
    main()
