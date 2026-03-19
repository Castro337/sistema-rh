import flet as ft
import os

# 1. PALETA DE CORES DE ALTO CONTRASTE
PALETA = {
    "primaria": ft.Colors.PINK_600,       # Rosa forte para botões
    "fundo_tela": ft.Colors.WHITE,       # Fundo branco puro
    "fundo_card": "#FFF0F5",             # Rosa ultra claro para destacar blocos
    "texto_preto": ft.Colors.BLACK,      # Texto principal sempre preto
    "texto_destaque": ft.Colors.PINK_900 # Títulos em rosa bem escuro
}

def main(page: ft.Page):
    page.title = "Pink V3.2 | By Jean Castro"
    page.bgcolor = PALETA["fundo_tela"]
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 30
    page.spacing = 25

    # Estilo padrão para os textos das etiquetas (Labels)
    estilo_label = ft.TextStyle(color=PALETA["texto_preto"], weight="bold")

    def criar_input_monetario(label):
        return ft.TextField(
            label=label,
            prefix=ft.Text("R$ ", color=PALETA["texto_preto"]),
            label_style=ft.TextStyle(color=ft.Colors.PINK_800, weight="bold"),
            color=PALETA["texto_preto"],
            border_color=PALETA["primaria"],
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            focused_border_color=ft.Colors.PINK_900
        )

    # --- CAMPOS ---
    salario_in = criar_input_monetario("Salário Base")
    
    # 5 Produtos (Valor + %)
    vendas_data = []
    for i in range(5):
        v = criar_input_monetario(f"Valor Venda Produto {i+1}")
        p = ft.Slider(min=0, max=100, divisions=100, label="Comissão: {value}%", thumb_color=PALETA["primaria"])
        vendas_data.append({"v": v, "p": p})

    # 5 Benefícios (Valor + %)
    ben_data = []
    for i in range(5):
        v = criar_input_monetario(f"Valor Base Benefício {i+1}")
        p = ft.Slider(min=0, max=100, divisions=100, label="Pagar: {value}%", thumb_color=ft.Colors.BLUE_700)
        ben_data.append({"v": v, "p": p})

    tipo_calc = ft.Dropdown(
        label="Escolha o Tipo de Cálculo",
        label_style=estilo_label,
        options=[ft.dropdown.Option("Mensal"), ft.dropdown.Option("Férias"), ft.dropdown.Option("Rescisão")],
        value="Mensal",
        color=PALETA["texto_preto"],
        border_color=PALETA["primaria"]
    )
    
    radio_ferias = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="sim", label="Sim", label_style=estilo_label),
            ft.Radio(value="nao", label="Não", label_style=estilo_label)
        ], alignment=ft.MainAxisAlignment.CENTER),
        value="nao"
    )

    meses_txt = ft.TextField(label="Meses Trabalhados", visible=False, color=PALETA["texto_preto"])

    # --- LOGICA ---
    def atualizar_campos(e):
        meses_txt.visible = (tipo_calc.value == "Rescisão")
        page.update()
    
    tipo_calc.on_change = atualizar_campos

    res_container = ft.Container(
        content=ft.Text("", color=PALETA["texto_preto"], size=16, weight="bold"),
        visible=False,
        padding=20,
        bgcolor=ft.Colors.AMBER_100,
        border_radius=15,
        border=ft.border.all(2, PALETA["primaria"])
    )

    def calcular(e):
        try:
            sal = float(salario_in.value or 0)
            c_total = sum([float(item["v"].value or 0) * (item["p"].value / 100) for item in vendas_data])
            b_total = sum([float(item["v"].value or 0) * (item["p"].value / 100) for item in ben_data])
            
            bruto = sal + c_total + b_total
            liq = bruto * 0.85 # Simulação simples de impostos
            
            texto_res = f"📊 RESUMO DO CÁLCULO\n\n💰 Bruto: R$ {bruto:.2f}\n📈 Comissões: R$ {c_total:.2f}\n🌟 Benefícios: R$ {b_total:.2f}\n💵 Líquido Est.: R$ {liq:.2f}"
            
            if tipo_calc.value == "Rescisão":
                m = int(meses_txt.value or 0)
                rescisao = liq + (sal/12 * m)
                texto_res += f"\n\n🔥 TOTAL RESCISÃO: R$ {rescisao:.2f}"

            res_container.content.value = texto_res
            res_container.visible = True
            page.update()
        except:
            res_container.content.value = "⚠️ Erro: Use apenas números nos valores."
            res_container.visible = True
            page.update()

    # --- LAYOUT ESTRUTURADO ---
    page.add(
        ft.Text("SISTEMA PINK V3.2", size=28, weight="bold", color=PALETA["texto_destaque"]),
        
        ft.Container(content=salario_in, padding=10, bgcolor=PALETA["fundo_card"], border_radius=15),
        
        ft.ExpansionTile(
            title=ft.Text("📦 VENDAS (VALOR + % INDIVIDUAL)", color=PALETA["texto_destaque"], weight="bold"),
            controls=[ft.Column([ft.Container(content=ft.Column([item["v"], item["p"]]), padding=15) for item in vendas_data])]
        ),
        
        ft.ExpansionTile(
            title=ft.Text("🎁 BENEFÍCIOS (VALOR + % INDIVIDUAL)", color=PALETA["texto_destaque"], weight="bold"),
            controls=[ft.Column([ft.Container(content=ft.Column([item["v"], item["p"]]), padding=15) for item in ben_data])]
        ),
        
        ft.Container(
            content=ft.Column([
                tipo_calc,
                ft.Text("Possui férias vencidas?", color=PALETA["texto_preto"], weight="bold"),
                radio_ferias,
                meses_txt
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20, bgcolor=PALETA["fundo_card"], border_radius=15
        ),
        
        ft.ElevatedButton(
            "CALCULAR RESULTADOS",
            on_click=calcular,
            bgcolor=PALETA["primaria"],
            color=ft.Colors.WHITE,
            height=60,
            width=400
        ),
        
        res_container
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
