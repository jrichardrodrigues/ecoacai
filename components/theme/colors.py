class Colors:
    """
    Paleta oficial do EcoAçaí.

    A identidade institucional utiliza tons inspirados no fruto do açaí.
    As cores estão organizadas por responsabilidade para facilitar a
    manutenção e permitir a criação de outros temas futuramente.

    As constantes no nível principal foram preservadas para manter
    compatibilidade com os componentes já existentes.
    """

    # ==========================================================
    # MARCA
    # ==========================================================

    class Brand:
        PRIMARY = "#781946"
        PRIMARY_LIGHT = "#A42B69"
        PRIMARY_DARK = "#56102F"
        SECONDARY = "#B95D8D"

    # ==========================================================
    # FUNDOS E SUPERFÍCIES
    # ==========================================================

    class Background:
        DEFAULT = "#F8F4F6"
        ALTERNATIVE = "#F2E9EE"
        SURFACE = "#FFFFFF"
        SURFACE_MUTED = "#FCF9FB"

    # ==========================================================
    # TEXTOS
    # ==========================================================

    class Text:
        PRIMARY = "#2D1B25"
        SECONDARY = "#6B5A63"
        MUTED = "#8C7B84"
        ON_PRIMARY = "#FFFFFF"
        DISABLED = "#A99BA2"

    # ==========================================================
    # STATUS
    # ==========================================================

    class Status:
        SUCCESS = "#2E7D32"
        SUCCESS_LIGHT = "#E8F5E9"

        WARNING = "#F9A825"
        WARNING_LIGHT = "#FFF8E1"

        ERROR = "#C62828"
        ERROR_LIGHT = "#FFEBEE"

        INFO = "#1976D2"
        INFO_LIGHT = "#E3F2FD"

    # ==========================================================
    # BORDAS E DIVISORES
    # ==========================================================

    class Border:
        DEFAULT = "#E5D9DF"
        STRONG = "#CFBCC6"
        DIVIDER = "#EEE4E9"

    # ==========================================================
    # INTERAÇÕES
    # ==========================================================

    class Interaction:
        HOVER = "#F1E4EA"
        SELECTED = "#EAD4DF"
        DISABLED = "#B8ABB1"
        DISABLED_BG = "#F1ECEE"

    # ==========================================================
    # DASHBOARD
    # ==========================================================

    class Dashboard:
        REQUESTS = "#1976D2"
        REQUESTS_BG = "#E3F2FD"

        ESTABLISHMENTS = "#00897B"
        ESTABLISHMENTS_BG = "#E0F2F1"

        PENDING = "#F9A825"
        PENDING_BG = "#FFF8E1"

        SCHEDULED = "#8E24AA"
        SCHEDULED_BG = "#F3E5F5"

        TODAY = "#5E35B1"
        TODAY_BG = "#EDE7F6"

        COLLECTING = "#F57C00"
        COLLECTING_BG = "#FFF3E0"

        COMPLETED = "#388E3C"
        COMPLETED_BG = "#E8F5E9"

        SACKS = "#6D4C41"
        SACKS_BG = "#EFEBE9"

        WEIGHT = "#7B1FA2"
        WEIGHT_BG = "#F3E5F5"

        CHART_BACKGROUND = "#F7F9FA"

    # ==========================================================
    # SOMBRAS E SOBREPOSIÇÕES
    # ==========================================================

    class Overlay:
        SHADOW = "#26000000"
        BACKDROP = "#66000000"

    # ==========================================================
    # COMPATIBILIDADE COM O CÓDIGO ATUAL
    # ==========================================================

    PRIMARY = Brand.PRIMARY
    PRIMARY_LIGHT = Brand.PRIMARY_LIGHT
    PRIMARY_DARK = Brand.PRIMARY_DARK
    SECONDARY = Brand.SECONDARY

    BACKGROUND = Background.DEFAULT
    BACKGROUND_ALT = Background.ALTERNATIVE
    SURFACE = Background.SURFACE
    SURFACE_MUTED = Background.SURFACE_MUTED

    TEXT = Text.PRIMARY
    TEXT_SECONDARY = Text.SECONDARY
    TEXT_MUTED = Text.MUTED
    TEXT_ON_PRIMARY = Text.ON_PRIMARY

    SUCCESS = Status.SUCCESS
    SUCCESS_LIGHT = Status.SUCCESS_LIGHT

    WARNING = Status.WARNING
    WARNING_LIGHT = Status.WARNING_LIGHT

    ERROR = Status.ERROR
    ERROR_LIGHT = Status.ERROR_LIGHT

    INFO = Status.INFO
    INFO_LIGHT = Status.INFO_LIGHT

    BORDER = Border.DEFAULT
    BORDER_STRONG = Border.STRONG
    DIVIDER = Border.DIVIDER

    HOVER = Interaction.HOVER
    SELECTED = Interaction.SELECTED
    DISABLED = Interaction.DISABLED
    DISABLED_BG = Interaction.DISABLED_BG

    SHADOW = Overlay.SHADOW
    OVERLAY = Overlay.BACKDROP

    # Compatibilidade temporária com a primeira estrutura do Dashboard.

    DASHBOARD_REQUESTS = Dashboard.REQUESTS
    DASHBOARD_REQUESTS_BG = Dashboard.REQUESTS_BG

    DASHBOARD_ESTABLISHMENTS = Dashboard.ESTABLISHMENTS
    DASHBOARD_ESTABLISHMENTS_BG = Dashboard.ESTABLISHMENTS_BG

    DASHBOARD_PENDING = Dashboard.PENDING
    DASHBOARD_PENDING_BG = Dashboard.PENDING_BG

    DASHBOARD_SCHEDULED = Dashboard.SCHEDULED
    DASHBOARD_SCHEDULED_BG = Dashboard.SCHEDULED_BG

    DASHBOARD_TODAY = Dashboard.TODAY
    DASHBOARD_TODAY_BG = Dashboard.TODAY_BG

    DASHBOARD_COLLECTING = Dashboard.COLLECTING
    DASHBOARD_COLLECTING_BG = Dashboard.COLLECTING_BG

    DASHBOARD_COMPLETED = Dashboard.COMPLETED
    DASHBOARD_COMPLETED_BG = Dashboard.COMPLETED_BG