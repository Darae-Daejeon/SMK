import unittest
from pathlib import Path


class ExtractEtriSourcesTests(unittest.TestCase):
    def test_source_map_contains_four_ordered_technologies(self):
        from scripts.extract_etri_smk_sources import SOURCE_MAP

        self.assertEqual([item["slug"] for item in SOURCE_MAP], [
            "tech-01",
            "tech-02",
            "tech-03",
            "tech-04",
        ])
        self.assertEqual([item["tech_id"] for item in SOURCE_MAP], [
            "3610-2021-02099",
            "3610-2023-00011",
            "5310-2023-00421",
            "5310-2025-00388",
        ])

    def test_validate_sources_reports_exact_missing_path(self):
        from scripts.extract_etri_smk_sources import ROOT, validate_sources

        missing = ROOT / "tmp" / "etri-smk" / "test-missing" / "missing.pptx"
        with self.assertRaisesRegex(FileNotFoundError, str(missing).replace("\\", "\\\\")):
            validate_sources([{"path": Path(missing)}])

    def test_pdf_renderer_wraps_windows_cmd_launcher(self):
        from scripts.extract_etri_smk_sources import build_pdftoppm_command

        command = build_pdftoppm_command(
            Path(r"C:\tools\pdftoppm.cmd"),
            Path(r"C:\input\source.pdf"),
            Path(r"C:\output\page"),
        )
        self.assertEqual(command[:3], ["cmd.exe", "/d", "/c"])
        self.assertEqual(command[-4:], ["-r", "150", r"C:\input\source.pdf", r"C:\output\page"])

    def test_override_wrapper_maps_to_native_poppler_executable(self):
        from scripts.extract_etri_smk_sources import native_pdftoppm_candidate

        wrapper = Path(r"C:\runtime\dependencies\bin\override\pdftoppm.cmd")
        self.assertEqual(
            native_pdftoppm_candidate(wrapper),
            Path(r"C:\runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe"),
        )


if __name__ == "__main__":
    unittest.main()
