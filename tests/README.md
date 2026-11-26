# Navigation UI tests

Run from the worktree root:

    python3 -m unittest discover -s tests -v

Stdlib `unittest` only — the project has no pytest, no package.json and no
frontend framework; the UI is server-rendered Python strings plus vanilla
CSS/JS, so no new dependency is needed (or wanted).

What each test guards:

- `test_six_sections_in_agreed_order` — six sections and their first-child paths stay in the agreed order.
- `test_every_nav_path_appears_once` — no nav path is duplicated across sections.
- `test_labels_unique_within_sections` — subpage labels are unique and never repeat the section label.
- `test_heute_marks_exactly_one_subpage` — `/heute` gets one `aria-current` on the right link and the right section is active.
- `test_kalibrierung_marks_exactly_one_subpage` — same for the expert-only calibration page.
- `test_readme_has_no_active_section_or_subnav` — leaf pages without a section show no active state and no second row.
- `test_landmarks_present` — accessible top nav, subnav, skip link and `<main id="inhalt">` are rendered.
- `test_no_loose_header_buttons` — no old `rmk` class or `/systemstat` link leaked into the header buttons.
- `test_easy_mode_page_flags` — `/gpu` stays Easy, `/kalibrierung` stays expert-only.
- `test_locale_keys_present_in_all_languages` — all 32 nav label keys exist and are non-empty in de/en/es/fi/fr/it.
- `test_landmark_placeholder_in_all_languages` — `nav.landmark.seiten` keeps its literal `{bereich}` placeholder.
- `test_locale_labels_are_escaped` — a malicious locale label is HTML-escaped, not emitted as raw markup.
