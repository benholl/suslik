"""Dependency-free checks for the restructured navigation UI (stdlib unittest only).

Run from the worktree root: python3 -m unittest discover -s tests -v
"""
import importlib
import os
import re
import sys
import unittest

# Make the worktree root importable no matter how discovery is invoked.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import webui

LOCALES = ("de", "en", "es", "fi", "fr", "it")

# Navigation label keys of the restructure: the 30 keys touched in the locale
# diff plus the two adjacent section-label keys of the same nav label block.
NAV_LOCALE_KEYS = (
    "anwesenheit.knopf", "gpu.knopf", "kalib.knopf",
    "nav.anker", "nav.areas", "nav.benachrichtigungen",
    "nav.bereich.faces", "nav.bereich.person", "nav.bereich.vision",
    "nav.durchgaenge", "nav.ereignisse", "nav.erkennung",
    "nav.erkennungstest", "nav.faces", "nav.frigate", "nav.gesichter",
    "nav.kette", "nav.koerpernamen", "nav.konfiguration",
    "nav.landmark.seiten", "nav.landmark.sektionen", "nav.lernen",
    "nav.lernlauf", "nav.live", "nav.live_alerts", "nav.qualitaet",
    "nav.sync_auswahl", "nav.system", "nav.systemstat", "nav.unbekannte",
    "nav.vision", "ui.skip",
)

EXPECTED_FIRST_PATHS = ["/heute", "/faces", "/lernlauf", "/live", "/erkennung", "/system"]


class NavTests(unittest.TestCase):
    def test_six_sections_in_agreed_order(self):
        sections = webui._nav()
        self.assertEqual(len(sections), 6)
        self.assertEqual([kids[0][0] for _, kids in sections], EXPECTED_FIRST_PATHS)

    def test_every_nav_path_appears_once(self):
        paths = [p for _, kids in webui._nav() for p, _ in kids]
        for path in paths:
            self.assertEqual(paths.count(path), 1, path)

    def test_labels_unique_within_sections(self):
        for label, kids in webui._nav():
            labels = [name for _, name in kids]
            self.assertEqual(len(labels), len(set(labels)), label)
            self.assertNotIn(label, labels, label)

    def test_heute_marks_exactly_one_subpage(self):
        out = webui.layout("T", "/heute", "")
        self.assertEqual(out.count('aria-current="page"'), 1)
        self.assertIn('<a href="/heute" class="aktiv" aria-current="page">', out)
        self.assertIn('<a href="/heute" class=aktiv>', out)

    def test_kalibrierung_marks_exactly_one_subpage(self):
        out = webui.layout("T", "/kalibrierung", "")
        self.assertEqual(out.count('aria-current="page"'), 1)
        self.assertIn('<a href="/kalibrierung" class="aktiv nur-expert" aria-current="page">', out)
        self.assertIn('<a href="/erkennung" class=aktiv>', out)

    def test_readme_has_no_active_section_or_subnav(self):
        out = webui.layout("T", "/readme", "")
        self.assertNotIn("class=aktiv", out)
        self.assertNotIn('aria-current="page"', out)
        self.assertNotIn('<nav class="subnav"', out)

    def test_landmarks_present(self):
        out = webui.layout("T", "/heute", "")
        self.assertIn('<nav aria-label="', out)
        self.assertIn('<nav class="subnav" aria-label="', out)
        self.assertIn('class="skip" href="#inhalt"', out)
        main_tag = re.search(r"<main\b[^>]*>", out).group(0)
        self.assertIn('id="inhalt"', main_tag)
        self.assertIn('tabindex="-1"', main_tag)

    def test_no_loose_header_buttons(self):
        out = webui.layout("T", "/heute", "")
        self.assertNotIn('class="rmk"', out)
        rechts = out.split('<span class="rechts">', 1)[1].split("</nav>", 1)[0]
        self.assertNotIn('href="/systemstat"', rechts)

    def test_easy_mode_page_flags(self):
        self.assertNotIn("/gpu", webui.NUR_EXPERT_BLAETTER)
        self.assertIn("/kalibrierung", webui.NUR_EXPERT_BLAETTER)

    def test_locale_keys_present_in_all_languages(self):
        self.assertEqual(len(NAV_LOCALE_KEYS), 32)
        for loc in LOCALES:
            table = importlib.import_module("core.texte." + loc).T
            for key in NAV_LOCALE_KEYS:
                self.assertIn(key, table, "%s: %s" % (loc, key))
                self.assertTrue(str(table[key]).strip(), "%s: %s" % (loc, key))

    def test_landmark_placeholder_in_all_languages(self):
        for loc in LOCALES:
            table = importlib.import_module("core.texte." + loc).T
            self.assertIn("{bereich}", table["nav.landmark.seiten"], loc)

    def test_locale_labels_are_escaped(self):
        payload = "<script>alert(1)</script>"
        original = webui.t
        try:
            webui.t = lambda key, **kwargs: payload
            out = webui.layout("T", "/heute", "")
        finally:
            webui.t = original
        self.assertIn("&lt;script&gt;", out)
        self.assertNotIn(payload, out)


if __name__ == "__main__":
    unittest.main()
