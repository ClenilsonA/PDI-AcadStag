from .models import ProcessoEstagio


def criar_ou_obter_processo(candidatura):
    processo, _ = ProcessoEstagio.objects.get_or_create(candidatura=candidatura)
    return processo


def atualizar_estado_processo(processo):
    """
    Atualiza o estado global do processo com base nos dados já preenchidos.

    Regra simples:
    - CONCLUIDO: nota final lançada e publicada
    - EM_AVALIACAO: relatório submetido
    - EM_CURSO: processo formalizado e validado
    - PREPARACAO: caso contrário
    """

    if processo.nota_final is not None and processo.nota_publicada:
        novo_estado = ProcessoEstagio.Estado.CONCLUIDO

    elif hasattr(processo.candidatura, "relatorio"):
        novo_estado = ProcessoEstagio.Estado.EM_AVALIACAO

    elif processo_pronto_para_iniciar(processo):
        novo_estado = ProcessoEstagio.Estado.EM_CURSO

    else:
        novo_estado = ProcessoEstagio.Estado.PREPARACAO

    if processo.estado != novo_estado:
        processo.estado = novo_estado
        processo.save(update_fields=["estado"])

    return processo


def processo_pronto_para_iniciar(processo):
    return all(
        [
            processo.candidatura.status == "ACEITE",
            processo.orientador,
            processo.supervisor_nome,
            processo.local_estagio,
            processo.data_inicio,
            processo.data_fim,
            processo.empresa_confirmada,
            processo.validado_servicos_academicos,
        ]
    )