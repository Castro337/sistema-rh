import flet as ft
import os

# 1. ESTILOS E CONFIGURAÇÃO VISUAL
PALETA = {
    "primaria": ft.Colors.PINK_400,
    "ia": ft.Colors.DEEP_PURPLE_400,
    "fundo": ft.Colors.PINK_50,
    "card": ft.Colors.WHITE
}

def main(page: ft.Page):
    page.title = "Pink V2.9 | RH & Vendas"
    page.bgcolor = PALETA["fundo"]
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 30  # Espaçamento nas bordas da tela
    page.spacing = 20  # Espaçamento vertical entre os elementos principais

    # --- ENTRADAS COM ESPAÇAMENTO ---
    def criar_campo(label, prefixo=None):
        return ft.TextField(
            label=label,
            prefix=ft.Text(prefixo) if prefixo else None,
            border_color=PALETA["primaria"],
            border_radius=12,
            bgcolor=PALETA["card"],
            content_padding=15
        )

    salario_in = criar_campo("Salário Base", "R$ ")
    comissao_perc = ft.Slider(min=0, max=20, divisions=20, label="Comissão Geral: {value}%", value=3)
    
    # 5 Produtos com espaçamento interno
    vendas_inputs = [criar_campo(f"Valor Venda Produto {i+1}", "R$ ") for i in range(5)]
    
    # 5 Benefícios com Sliders organizados em Containers
    ben_widgets = []
    for i in range(5):
        ben_widgets.append(
            ft.Container(
                content=ft.Column([
                    criar_campo(f"Valor Benefício {i+1}", "R$ "),
                    ft.Text(f"Porcentagem a pagar do Benefício {i+1}:", size=12),
                    ft.Slider(min=0, max=100, divisions=10, label="{value}%", value=100)
                ], spacing=10),
                padding=15,
                border=ft.border.all(1, ft.Colors.PINK_100),
                border_radius=12,
                margin=ft.margin.only(bottom=10)
            )
        )

    tipo_op = ft.Dropdown(
        label="Tipo de Cálculo",
        options=[ft.dropdown.Option("Mensal"), ft.dropdown.Option("Férias")],
        value="Mensal",
        border_radius=12
    )
    
    # Opção Sim/Não para Férias
    ferias_venc_radio = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="sim", label="Sim"),
            ft.Radio(value="nao", label="Não")
        ], spacing=20),
        value="nao"
    )

    # --- ÁREA DE RESULTADO ---
    res_txt = ft.Text("", color="black", weight="bold", size=16)
    container_res = ft.Container(
        content=res_txt,
        visible=False,
        padding=20,
        bgcolor=ft.Colors.GREEN_50,
        border_radius=15,
        border=ft.border.all(2, ft.Colors.GREEN_200)
    )

    def calcular(e):
        try:
            # Lógica de soma e cálculo
            v_total = sum([float(v.value or 0) for v in vendas_inputs])
            comissao = v_total * (comissao_perc.value / 100)
            
            # Aqui você pode expandir a lógica conforme as versões anteriores
            bruto = float(salario_in.value or 0) + comissao
            
            res_txt.value = f"✅ Cálculo Concluído!\n💰 Bruto Total: R$ {bruto:.2f}\n📈 Comissão: R$ {comissao:.2f}"
            container_res.visible = True
            page.update()
        except:
            res_txt.value = "⚠️ Erro: Verifique se preencheu os números corretamente."
            container_res.visible = True
            page.update()

    # --- MONTAGEM DA PÁGINA COM GRUPOS (CARDS) ---
    page.add(
        ft.Text("SISTEMA PINK V2.9", size=28, weight="bold", color=PALETA["primaria"]),
        
        ft.Text("Informações Salariais", size=18, weight="w600"),
        salario_in,
        
        ft.ExpansionTile(
            title=ft.Text("Vendas e Produtos (5 Itens)", weight="bold"),
            controls=[ft.Container(content=ft.Column([comissao_perc] + vendas_inputs, spacing=15), padding=10)]
        ),
        
        ft.ExpansionTile(
            title=ft.Text("Benefícios e Porcentagens", weight="bold"),
            controls=[ft.Column(ben_widgets, spacing=5)]
        ),
        
        ft.Container(
            content=ft.Column([
                ft.Text("Configurações Adicionais", size=18, weight="w600"),
                tipo_op,
                ft.Text("Possui férias vencidas?"),
                ferias_venc_radio,
            ], spacing=15),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=15
        ),
        
        ft.ElevatedButton(
            "CALCULAR RESULTADOS",
            on_click=calcular,
            bgcolor=PALETA["primaria"],
            color="white",
            height=50,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
        ),
        
        container_res
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
