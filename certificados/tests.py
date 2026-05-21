from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .forms import CertificadoForm


class CertificadoFormTests(TestCase):
    def test_certificado_com_ficheiro_nao_pdf_e_invalido(self):
        form = CertificadoForm(
            data={
                "observacoes": "Certificado de teste",
                "ativo": True,
            },
            files={
                "ficheiro": SimpleUploadedFile(
                    "certificado.txt",
                    b"conteudo qualquer",
                    content_type="text/plain",
                )
            },
        )

        self.assertFalse(form.is_valid())
        self.assertIn("ficheiro", form.errors)

    def test_certificado_com_pdf_e_valido(self):
        form = CertificadoForm(
            data={
                "observacoes": "Certificado de teste",
                "ativo": True,
            },
            files={
                "ficheiro": SimpleUploadedFile(
                    "certificado.pdf",
                    b"%PDF-1.4 certificado",
                    content_type="application/pdf",
                )
            },
        )

        self.assertTrue(form.is_valid())

    def test_certificado_sem_ficheiro_e_valido(self):
        form = CertificadoForm(
            data={
                "observacoes": "Certificado sem ficheiro",
                "ativo": True,
            },
            files={},
        )

        self.assertTrue(form.is_valid())