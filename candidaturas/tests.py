from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .forms import CandidaturaForm


class CandidaturaFormTests(TestCase):
    def test_candidatura_sem_cv_e_invalida(self):
        form = CandidaturaForm(
            data={},
            files={
                "comprovativo_frequencia": SimpleUploadedFile(
                    "comprovativo.pdf",
                    b"%PDF-1.4 comprovativo",
                    content_type="application/pdf",
                )
            },
        )

        self.assertFalse(form.is_valid())
        self.assertIn("cv", form.errors)

    def test_candidatura_sem_comprovativo_e_invalida(self):
        form = CandidaturaForm(
            data={},
            files={
                "cv": SimpleUploadedFile(
                    "cv.pdf",
                    b"%PDF-1.4 cv",
                    content_type="application/pdf",
                )
            },
        )

        self.assertFalse(form.is_valid())
        self.assertIn("comprovativo_frequencia", form.errors)

    def test_candidatura_com_ficheiro_nao_pdf_e_invalida(self):
        form = CandidaturaForm(
            data={},
            files={
                "cv": SimpleUploadedFile(
                    "cv.txt",
                    b"texto qualquer",
                    content_type="text/plain",
                ),
                "comprovativo_frequencia": SimpleUploadedFile(
                    "comprovativo.pdf",
                    b"%PDF-1.4 comprovativo",
                    content_type="application/pdf",
                ),
            },
        )

        self.assertFalse(form.is_valid())
        self.assertIn("cv", form.errors)

    def test_candidatura_com_cv_e_comprovativo_pdf_e_valida(self):
        form = CandidaturaForm(
            data={},
            files={
                "cv": SimpleUploadedFile(
                    "cv.pdf",
                    b"%PDF-1.4 cv",
                    content_type="application/pdf",
                ),
                "comprovativo_frequencia": SimpleUploadedFile(
                    "comprovativo.pdf",
                    b"%PDF-1.4 comprovativo",
                    content_type="application/pdf",
                ),
            },
        )

        self.assertTrue(form.is_valid())