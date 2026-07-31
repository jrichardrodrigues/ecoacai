from repositories import SolicitacaoColetaRepository


class ColetasAgendadasService:
    """Serviço responsável pelas operações das coletas agendadas."""

    def __init__(self):
        self.repository = SolicitacaoColetaRepository()