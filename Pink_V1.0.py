import flet as ft # type: ignore

# 1. CONSTANTES DE DESIGN (Padronizado com Letra Maiúscula conforme novas versões)
PALETA_CORES = {
    "primaria": ft.Colors.PINK_400,      
    "secundaria": ft.Colors.PINK_100,    
    "texto": ft.Colors.PINK_900,         
    "acento": ft.Colors.DEEP_PURPLE_200, 
    "erro": ft.Colors.RED_700
}

# 2. FUNÇÃO DE LÓGICA (Backend Separado)
def calcular_proventos_logica(s_base_str, v_total_str, d_trab_str, n_faltas_str):
    try:
        s_base = float(s_base_str.replace(",", ".")) if s_base_str else 0.0
        v_total = float(v_total_str.replace(",", ".")) if v_total_str else 0.0
        d_trab = int(d_trab_str) if d_trab_str else 30
        n_faltas = int(n_faltas_str) if n_faltas_str else 0

        dias_liquidos = d_trab - n_faltas
        valor_dia = s_base / 30
        valor_receber_dias = dias_liquidos * valor_dia
        comissao = v_total * 0.03
        total_final = valor_receber_dias + comissao

        return True, {
            "dias_liquidos": dias_liquidos,
            "valor_dias": valor_receber_dias,
            "faltas": n_faltas,
            "comissao": comissao,
            "total": total_final
        }
    except ValueError:
        return False, "Erro: Insira apenas números válidos."

# 3. INTERFACE DE USUÁRIO (Frontend)
def main(page: ft.Page):
    page.title = "Pink| Calculadora de Proventos| By Jean Castro"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.bgcolor = ft.Colors.WHITE 
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 500  # Ajuste para visualização desktop
    page.window_height = 800

    # Cabeçalho
    cabecalho = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.WALLET, color="white", size=35),
            ft.Text("PINK - RH PROVENTOS - By Jean Castro", size=24, weight="bold", color="white")
        ], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=PALETA_CORES["primaria"],
        padding=15,
        border_radius=ft.border_radius.only(top_left=15, top_right=15),
    )

    # Estilização Padrão corrigida (sem prefix_text para evitar erros de versão)
    style_textfield = {
        "border_color": PALETA_CORES["primaria"],
        "cursor_color": PALETA_CORES["primaria"],
        "label_style": ft.TextStyle(color=PALETA_CORES["texto"]),
        "keyboard_type": ft.KeyboardType.NUMBER,
        "border_radius": 10,
        "width": 300,
        "dense": True
    }

    # Campos de Entrada com correção do prefix
    salario_base = ft.TextField(label="Salário Base Mensal", prefix=ft.Text("R$ "), **style_textfield)
    vendas = ft.TextField(label="Total de Vendas (R$)", prefix=ft.Text("R$ "), **style_textfield)
    dias_trabalhados = ft.TextField(label="Dias Trabalhados", value="30", **style_textfield)
    faltas = ft.TextField(label="Quantidade de Faltas", value="0", **style_textfield)
    
    # Seção de Inputs
    secao_inputs = ft.Container(
        content=ft.Column([
            ft.Text("Dados Operacionais", size=18, weight="bold", color=PALETA_CORES["texto"]),
            salario_base, 
            vendas, 
            ft.Row([
                ft.Container(content=dias_trabalhados, width=145),
                ft.Container(content=faltas, width=145)
            ], spacing=10)
        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=PALETA_CORES["secundaria"],
        padding=20,
        border_radius=15,
    )

    # Área de Resultado
    res_txt = ft.Text(size=16, color=PALETA_CORES["texto"])
    container_resultado = ft.Container(
        content=ft.Column([
            ft.Text("Detalhamento", size=18, weight="bold", color=PALETA_CORES["texto"]),
            ft.Divider(color=ft.Colors.PINK_200),
            res_txt
        ]),
        bgcolor=ft.Colors.GREY_50,
        padding=20,
        border_radius=15,
        visible=False,
    )

    def acao_calcular(e):
        sucesso, dados = calcular_proventos_logica(
            salario_base.value, vendas.value, 
            dias_trabalhados.value, faltas.value
        )

        if sucesso:
            res_txt.value = (
                f"👤 Dias Líquidos: {dados['dias_liquidos']}\n"
                f"💰 Valor Dias: R$ {dados['valor_dias']:.2f}\n"
                f"❌ Faltas: {dados['faltas']}\n"
                f"📈 Comissão (3%): R$ {dados['comissao']:.2f}\n"
                f"{'-'*25}\n"
                f"👉 TOTAL: R$ {dados['total']:.2f}"
            )
            container_resultado.bgcolor = ft.Colors.GREEN_50
        else:
            res_txt.value = dados
            container_resultado.bgcolor = ft.Colors.RED_50

        container_resultado.visible = True
        page.update()

    btn_calcular = ft.ElevatedButton(
        "Calcular Proventos", 
        icon=ft.Icons.CALCULATE, 
        bgcolor=PALETA_CORES["primaria"],
        color="white",
        height=50,
        on_click=acao_calcular
    )

    # Layout Final
    page.add(
        ft.Column([
            ft.Container(
                content=ft.Column([
                    cabecalho,
                    ft.Container(
                        content=ft.Column([
                            secao_inputs, 
                            ft.Container(content=btn_calcular, alignment=ft.Alignment.CENTER, padding=10),
                            container_resultado
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20
                    )
                ]),
                border_radius=15,
                bgcolor="white",
                shadow=ft.BoxShadow(blur_radius=10, color="grey300"),
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    # Roda como WEB_BROWSER para abrir no seu navegador padrão
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)