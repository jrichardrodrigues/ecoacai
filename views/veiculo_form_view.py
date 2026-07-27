from __future__ import annotations

from collections.abc import Callable

import flet as ft

from config.constants import (
    STATUS_VEICULOS,
    STATUS_VEICULO_DISPONIVEL,
    MARCAS_VEICULOS,
    TIPOS_VEICULOS,
    CAPACIDADES_VEICULOS,
    ANOS_VEICULOS
)
from controllers.motorista_controller import MotoristaController
from controllers.veiculo_controller import VeiculoController
from models import Veiculo
from datetime import datetime
from utils.messages import (
    mostrar_erro,
    mostrar_sucesso,
)

class VeiculoFormView:
    """Formulário de cadastro e edição de veículos."""

    def __init__(
        self,
        page: ft.Page,
        veiculo: Veiculo | None = None,
        controller: VeiculoController | None = None,
        motorista_controller: MotoristaController | None = None,
        ao_salvar: Callable[[Veiculo], None] | None = None,
        ao_cancelar: Callable[[], None] | None = None,
    ) -> None:
        self.page = page
        self.controller = controller or VeiculoController()
        self.motorista_controller = (
            motorista_controller or MotoristaController()
        )

        self.veiculo = veiculo
        self.ao_salvar = ao_salvar
        self.ao_cancelar = ao_cancelar

        self._salvando = False

        self.titulo = ft.Text(
            "Editar veículo" if self._esta_editando else "Cadastrar veículo",
            size=24,
            weight=ft.FontWeight.BOLD,
        )

        self.placa_field = ft.TextField(
            label="Placa *",
            hint_text="Ex.: QWE1A23",
            prefix_icon=ft.Icons.PIN,
            capitalization=ft.TextCapitalization.CHARACTERS,
            max_length=8,
            autofocus=True,
            expand=True,
        )

        self.marca_dropdown = ft.Dropdown(
            label="Marca *",
            options=[
                ft.DropdownOption(key=marca, text=marca)
                for marca in MARCAS_VEICULOS
            ],
            expand=True,
        )

        self.modelo_field = ft.TextField(
            label="Modelo *",
            hint_text="Ex.: Atego 1719",
            prefix_icon=ft.Icons.LOCAL_SHIPPING,
            capitalization=ft.TextCapitalization.WORDS,
            expand=True,
        )

        self.ano_dropdown = ft.Dropdown(
            label="Ano *",
            options=[
                ft.DropdownOption(
                    key=ano,
                    text=ano,
                )
                for ano in ANOS_VEICULOS
            ],
            expand=True,
        )

        self.tipo_dropdown = ft.Dropdown(
            label="Tipo *",
            options=[
                ft.DropdownOption(
                    key=tipo,
                    text=tipo,
                )
                for tipo in TIPOS_VEICULOS
            ],
            expand=True,
        )

        self.capacidade_dropdown = ft.Dropdown(
            label="Capacidade (t) *",
            options=[
                ft.DropdownOption(
                    key=str(capacidade),
                    text=str(capacidade),
                )
                for capacidade in CAPACIDADES_VEICULOS
            ],
            expand=True,
        )

        self.motorista_dropdown = ft.Dropdown(
            label="Motorista responsável",
            hint_text="Nenhum motorista selecionado",
            options=[],
            expand=True,
        )

        self.status_dropdown = ft.Dropdown(
            label="Status *",
            value=STATUS_VEICULO_DISPONIVEL,
            options=[
                ft.DropdownOption(
                    key=valor,
                    text=descricao,
                )
                for valor, descricao in STATUS_VEICULOS
            ],
            expand=True,
        )

        self.salvar_button = ft.Button(
            content="Salvar",
            icon=ft.Icons.SAVE,
            on_click=self._salvar,
        )

        self.cancelar_button = ft.TextButton(
            content="Cancelar",
            icon=ft.Icons.CLOSE,
            on_click=self._cancelar,
        )

        self.container = ft.Container(
            padding=24,
            expand=True,
            content=ft.Column(
                controls=[
                    self.titulo,
                    ft.Text(
                        "Preencha os dados do veículo. "
                        "Os campos marcados com * são obrigatórios.",
                    ),
                    ft.Divider(),
                    self._construir_formulario(),
                    ft.Divider(),
                    ft.Row(
                        controls=[
                            self.cancelar_button,
                            self.salvar_button,
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                spacing=20,
                scroll=ft.ScrollMode.AUTO,
            ),
        )

        self._carregar_motoristas()
        self._carregar_dados()

    # ==========================================================
    # PROPRIEDADES
    # ==========================================================

    @property
    def _esta_editando(self) -> bool:
        return self.veiculo is not None and self.veiculo.id is not None

    # ==========================================================
    # CONSTRUÇÃO DA INTERFACE
    # ==========================================================

    def build(self) -> ft.Control:
        return self.container

    def _construir_formulario(self) -> ft.Control:
        return ft.Column(
            controls=[
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            content=self.marca_dropdown,
                            col={"sm": 12, "md": 4},
                        ),
                        ft.Container(
                            content=self.modelo_field,
                            col={"sm": 12, "md": 4},
                        ),
                        ft.Container(
                            content=self.placa_field,
                            col={"sm": 12, "md": 4},
                        ),
                    ],
                    spacing=16,
                    run_spacing=16,
                ),
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            content=self.ano_dropdown,
                            col={"sm": 12, "md": 3},
                        ),
                        ft.Container(
                            content=self.tipo_dropdown,
                            col={"sm": 12, "md": 3},
                        ),
                        ft.Container(
                            content=self.capacidade_dropdown,
                            col={"sm": 12, "md": 3},
                        ),
                        ft.Container(
                            content=self.status_dropdown,
                            col={"sm": 12, "md": 3},
                        ),
                    ],
                    spacing=16,
                    run_spacing=16,
                ),
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            content=self.motorista_dropdown,
                            col={"sm": 12, "md": 6},
                        ),
                    ],
                    spacing=16,
                    run_spacing=16,
                ),
            ],
            spacing=16,
        )

    # ==========================================================
    # CARREGAMENTO
    # ==========================================================

    def _carregar_motoristas(self) -> None:
        try:
            motoristas = self.motorista_controller.listar_ativos()

            opcoes = [
                ft.DropdownOption(
                    key="",
                    text="Nenhum motorista",
                )
            ]

            for motorista in motoristas:
                motorista_id = getattr(
                    motorista,
                    "id",
                    None,
                )

                if motorista_id is None:
                    continue

                nome = str(
                    getattr(
                        motorista,
                        "nome",
                        "Motorista",
                    )
                    or "Motorista"
                ).strip()

                cnh = str(
                    getattr(
                        motorista,
                        "cnh",
                        "",
                    )
                    or ""
                ).strip()

                descricao = nome

                if cnh:
                    descricao = f"{nome} — CNH {cnh}"

                opcoes.append(
                    ft.DropdownOption(
                        key=str(motorista_id),
                        text=descricao,
                    )
                )

            self.motorista_dropdown.options = opcoes

        except Exception as erro:
            self.motorista_dropdown.options = [
                ft.DropdownOption(
                    key="",
                    text="Nenhum motorista",
                )
            ]

            mostrar_erro(
                self.page,
                f"Não foi possível carregar os motoristas: {erro}",
            )

    def _carregar_dados(self) -> None:
        if self.veiculo is None:
            self.tipo_dropdown.value = TIPOS_VEICULOS[0]
            self.status_dropdown.value = STATUS_VEICULO_DISPONIVEL
            self.motorista_dropdown.value = ""
            return

        self.placa_field.value = self.veiculo.placa or ""
        self.marca_dropdown.value = self.veiculo.marca
        self.modelo_field.value = self.veiculo.modelo or ""

        self.ano_dropdown.value = (
            str(self.veiculo.ano)
            if self.veiculo.ano is not None
            else None
        )

        self.tipo_dropdown.value = self.veiculo.tipo or None

        self.capacidade_dropdown.value = (
            str(self.veiculo.capacidade)
            if self.veiculo.capacidade is not None
            else None
        )

        self.motorista_dropdown.value = (
            str(self.veiculo.motorista_id)
            if self.veiculo.motorista_id is not None
            else ""
        )

        self.status_dropdown.value = (
            self.veiculo.status or STATUS_VEICULO_DISPONIVEL
        )

    # ==========================================================
    # SALVAMENTO
    # ==========================================================

    def _salvar(
        self,
        event: ft.Event[ft.Control] | None = None,
    ) -> None:
        if self._salvando:
            return

        self._salvando = True
        self._alterar_estado_salvamento(True)

        try:
            veiculo = self._montar_veiculo()

            if self._esta_editando:
                veiculo_salvo = self.controller.atualizar(
                    veiculo,
                )
                mensagem = "Veículo atualizado com sucesso."
            else:
                veiculo_salvo = self.controller.cadastrar(
                    veiculo,
                )
                mensagem = "Veículo cadastrado com sucesso."

            self.veiculo = veiculo_salvo

            mostrar_sucesso(
                self.page,
                mensagem,
            )

            if self.ao_salvar is not None:
                self.ao_salvar(veiculo_salvo)

        except ValueError as erro:
            mostrar_erro(
                self.page,
                str(erro),
            )

        except Exception as erro:
            mostrar_erro(
                self.page,
                f"Não foi possível salvar o veículo: {erro}",
            )

        finally:
            self._salvando = False
            self._alterar_estado_salvamento(False)

    def _montar_veiculo(self) -> Veiculo:
        placa = self._normalizar_placa(
            self.placa_field.value
        )

        marca = str(
            self.marca_dropdown.value or ""
        ).strip()

        modelo = str(
            self.modelo_field.value or ""
        ).strip()

        tipo = str(
            self.tipo_dropdown.value or ""
        ).strip()

        ano = self._converter_ano(
            self.ano_dropdown.value
        )

        capacidade = self._converter_capacidade(
            self.capacidade_dropdown.value
        )

        motorista_id = self._converter_motorista_id(
            self.motorista_dropdown.value
        )

        status = str(
            self.status_dropdown.value
            or STATUS_VEICULO_DISPONIVEL
        ).strip().upper()

        return Veiculo(
            id=self.veiculo.id if self.veiculo else None,
            placa=placa,
            marca=marca,
            modelo=modelo,
            ano=ano,
            tipo=tipo,
            capacidade=capacidade,
            motorista_id=motorista_id,
            status=status,
            ativo=self.veiculo.ativo if self.veiculo else True,
        )

    # ==========================================================
    # CANCELAMENTO
    # ==========================================================

    def _cancelar(
        self,
        event: ft.Event[ft.Control] | None = None,
    ) -> None:
        if self.ao_cancelar is not None:
            self.ao_cancelar()
            return

        if len(self.page.views) > 1:
            self.page.views.pop()
            self.page.update()

    # ==========================================================
    # CONVERSÕES
    # ==========================================================

    @staticmethod
    def _normalizar_placa(
        valor: str | None,
    ) -> str:
        return "".join(
            caractere
            for caractere in str(valor or "").upper()
            if caractere.isalnum()
        )

    @staticmethod
    def _converter_ano(
        valor: str | None,
    ) -> int | None:
        texto = str(valor or "").strip()

        if not texto:
            return None

        if not texto.isdigit():
            raise ValueError(
                "O ano deve conter somente números."
            )

        return int(texto)

    @staticmethod
    def _converter_capacidade(
            valor: str | None,
    ) -> int | None:
        texto = str(valor or "").strip()

        if not texto:
            return None

        try:
            capacidade = int(texto)
        except ValueError as erro:
            raise ValueError(
                "Selecione uma capacidade válida."
            ) from erro

        if capacidade <= 0:
            raise ValueError(
                "A capacidade deve ser maior que zero."
            )

        return capacidade

    @staticmethod
    def _converter_motorista_id(
        valor: str | None,
    ) -> int | None:
        texto = str(valor or "").strip()

        if not texto:
            return None

        try:
            return int(texto)
        except ValueError as erro:
            raise ValueError(
                "Motorista selecionado inválido."
            ) from erro

    @staticmethod
    def _formatar_numero(
        valor: float,
    ) -> str:
        numero = float(valor)

        if numero.is_integer():
            return str(int(numero))

        return str(numero).replace(".", ",")

    @staticmethod
    def _formatar_status(
        status: str,
    ) -> str:
        return status.replace("_", " ").title()

    # ==========================================================
    # INTERFACE
    # ==========================================================

    def _alterar_estado_salvamento(
        self,
        salvando: bool,
    ) -> None:
        self.salvar_button.disabled = salvando
        self.cancelar_button.disabled = salvando

        self.salvar_button.content = (
            "Salvando..."
            if salvando
            else "Salvar"
        )

        try:
            self.salvar_button.update()
            self.cancelar_button.update()
        except RuntimeError:
            # O controle ainda pode não ter sido adicionado à página.
            pass

    def _mostrar_mensagem(
            self,
            mensagem: str,
            erro: bool,
    ) -> None:
        snackbar = ft.SnackBar(
            content=ft.Text(mensagem),
            bgcolor=(
                ft.Colors.ERROR_CONTAINER
                if erro
                else ft.Colors.PRIMARY_CONTAINER
            ),
        )

        self.page.show_dialog(snackbar)