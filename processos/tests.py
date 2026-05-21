from decimal import Decimal

from django.test import TestCase

from candidaturas.models import Candidatura
from empresas.models import Empresa
from estagios.models import Estagio
from processos.models import ProcessoEstagio
from processos.services import atualizar_estado_processo
from relatorios.models import Relatorio
from users.models import User


class ProcessoEstadoTests(TestCase):
    def setUp(self):
        self.aluno = User.objects.create_user(
            username="aluno_teste",
            email="aluno_teste@example.com",
            password="teste123",
            role="ALUNO",
        )

        self.empresa_user = User.objects.create_user(
            username="empresa_teste",
            email="empresa_teste@example.com",
            password="teste123",
            role="EMPRESA",
        )

        self.orientador = User.objects.create_user(
            username="orientador_teste",
            email="orientador_teste@example.com",
            password="teste123",
            role="ORIENTADOR",
        )

        self.empresa = Empresa.objects.create(
            user=self.empresa_user,
            nome="Empresa Teste",
            nif="123456789",
        )

        self.estagio = Estagio.objects.create(
            empresa=self.empresa,
            titulo="Estágio de Teste",
            area="Informática",
            descricao="Descrição do estágio de teste",
            duracao_meses=3,
            ativo=True,
        )

        self.candidatura = Candidatura.objects.create(
            aluno=self.aluno,
            estagio=self.estagio,
            status=Candidatura.Status.ACEITE,
        )

        self.processo = ProcessoEstagio.objects.create(
            candidatura=self.candidatura,
        )

    def test_processo_comeca_em_preparacao(self):
        self.assertEqual(
            self.processo.estado,
            ProcessoEstagio.Estado.PREPARACAO,
        )

    def test_processo_passa_para_em_curso_quando_tem_dados_completos(self):
        self.processo.orientador = self.orientador
        self.processo.supervisor_nome = "Supervisor Teste"
        self.processo.local_estagio = "Lisboa"
        self.processo.data_inicio = "2026-01-01"
        self.processo.data_fim = "2026-04-01"
        self.processo.empresa_confirmada = True
        self.processo.validado_servicos_academicos = True
        self.processo.save()

        atualizar_estado_processo(self.processo)
        self.processo.refresh_from_db()

        self.assertEqual(
            self.processo.estado,
            ProcessoEstagio.Estado.EM_CURSO,
        )

    def test_processo_passa_para_em_avaliacao_quando_tem_relatorio(self):
        self.processo.orientador = self.orientador
        self.processo.supervisor_nome = "Supervisor Teste"
        self.processo.local_estagio = "Lisboa"
        self.processo.data_inicio = "2026-01-01"
        self.processo.data_fim = "2026-04-01"
        self.processo.empresa_confirmada = True
        self.processo.validado_servicos_academicos = True
        self.processo.save()

        Relatorio.objects.create(
            candidatura=self.candidatura,
            ficheiro="relatorios/teste.pdf",
            estado="PENDENTE",
        )

        atualizar_estado_processo(self.processo)
        self.processo.refresh_from_db()

        self.assertEqual(
            self.processo.estado,
            ProcessoEstagio.Estado.EM_AVALIACAO,
        )

    def test_processo_passa_para_concluido_quando_nota_final_publicada(self):
        self.processo.nota_final = Decimal("17.50")
        self.processo.nota_publicada = True
        self.processo.save()

        atualizar_estado_processo(self.processo)
        self.processo.refresh_from_db()

        self.assertEqual(
            self.processo.estado,
            ProcessoEstagio.Estado.CONCLUIDO,
        )

    def test_processo_nao_passa_para_em_curso_sem_validacao_academica(self):
        self.processo.orientador = self.orientador
        self.processo.supervisor_nome = "Supervisor Teste"
        self.processo.local_estagio = "Lisboa"
        self.processo.data_inicio = "2026-01-01"
        self.processo.data_fim = "2026-04-01"
        self.processo.empresa_confirmada = True
        self.processo.validado_servicos_academicos = False
        self.processo.save()

        atualizar_estado_processo(self.processo)
        self.processo.refresh_from_db()

        self.assertEqual(
            self.processo.estado,
            ProcessoEstagio.Estado.PREPARACAO,
        )