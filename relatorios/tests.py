from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .forms import RelatorioForm


class RelatorioFormTests(TestCase):
    def test_relatorio_sem_ficheiro_e_invalido(self):
        form = RelatorioForm(data={}, files={})

        self.assertFalse(form.is_valid())
        self.assertIn("ficheiro", form.errors)

    def test_relatorio_com_ficheiro_nao_pdf_e_invalido(self):
        form = RelatorioForm(
            data={},
            files={
                "ficheiro": SimpleUploadedFile(
                    "relatorio.txt",
                    b"conteudo qualquer",
                    content_type="text/plain",
                )
            },
        )

        self.assertFalse(form.is_valid())
        self.assertIn("ficheiro", form.errors)

    def test_relatorio_com_pdf_e_valido(self):
        form = RelatorioForm(
            data={},
            files={
                "ficheiro": SimpleUploadedFile(
                    "relatorio.pdf",
                    b"%PDF-1.4 relatorio",
                    content_type="application/pdf",
                )
            },
        )

        self.assertTrue(form.is_valid())