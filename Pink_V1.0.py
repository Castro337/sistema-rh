import flet as ft
import os

# 1. PALETA DE ALTO CONTRASTE (Visual Confortável e Letras Visíveis)
PALETA = {
    "primaria": ft.Colors.PINK_600,
    "fundo_tela": ft.Colors.WHITE,
    "fundo_card": "#FFF0F5",
    "texto_preto": ft.Colors.BLACK,
    "texto_destaque": ft.Colors.PINK_900
}

def main(page: ft.Page):
    page.title = "PINK Calculo Salarial V3.4 | By Jean Castro "
    page.bgcolor = PALETA["fundo_tela"]
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 30
    page.spacing = 20

    # Estilo de texto para Labels
    estilo_label = ft.TextStyle(color=PALETA["texto_preto"], weight="bold")

    # --- CAMPOS PRINCIPAIS ---
    salario_in = ft.TextField(
        label="Salário Base",
        prefix=ft.Text("R$ ", color=PALETA["texto_preto"]),
        border_color=PALETA["primaria"],
        border_radius=12,
        color=PALETA["texto_preto"],
        label_style=estilo_label
    )

    # --- ESTRUTURA DE VENDAS (QTD + MATERIAL + VALOR + %) ---
    vendas_widgets = []
    
    def criar_item_venda(i):
        qtd = ft.TextField(label="Qtd", value="1", width=65, color=PALETA["texto_preto"], border_color="pink")
        material = ft.TextField(label=f"Material {i}", hint_text="Ex: Pendrive", expand=True, color=PALETA["texto_preto"], border_color="pink")
        valor = ft.TextField(label="Valor Un.", prefix=ft.Text("R$ "), width=110, color=PALETA["texto_preto"], border_color="pink")
        perc = ft.Slider(min=0, max=100, divisions=100, label="Comissão: {value}%", value=3, thumb_color=PALETA["primaria"])
        
        container = ft.Container(
            content=ft.Column([
                ft.Row([qtd, material, valor], spacing=10),
                ft.Text(f"Definir % de Comissão do Produto {i}:", size=12, color=PALETA["texto_preto"]),
                perc,
                ft.Divider(color=ft.Colors.PINK_100)
            ]),
            padding=15,
            bgcolor=PALETA["fundo_card"],
            border_radius=15
        )
        return {"ui": container, "qtd": qtd, "mat": material, "val": valor, "perc": perc}

    for i in range(1, 6):
        vendas_widgets.append(criar_item_venda(i))

    # --- BENEFÍCIOS ---
    ben_in = ft.TextField(label="Outros Benefícios/Extras", prefix=ft.Text("R$ "), color=PALETA["texto_preto"], border_color=PALETA["primaria"])

    # --- OPÇÕES DE CÁLCULO E RESCISÃO ---
    tipo_calc = ft.Dropdown(
        label="Tipo de Operação",
        options=[ft.dropdown.Option("Mensal"), ft.dropdown.Option("Férias"), ft.dropdown.Option("Rescisão")],
        value="Mensal", color=PALETA["texto_preto"], border_color=PALETA["primaria"]
    )
    
    meses_rescisao = ft.TextField(label="Meses Trabalhados", visible=False, color=PALETA["texto_preto"])
    
    def on_tipo_change(e):
        meses_rescisao.visible = (tipo_calc.value == "Rescisão")
        page.update()
    tipo_calc.on_change = on_tipo_change

    # --- RESULTADO ---
    res_txt = ft.Text("", color=PALETA["texto_preto"], size=16, weight="bold")
    res_container = ft.Container(content=res_txt, visible=False, padding=25, bgcolor=ft.Colors.AMBER_100, border_radius=15, border=ft.border.all(2, "pink"))

    def calcular(e):
        try:
            total_comissao = 0
            resumo_vendas = "📦 DETALHES DAS VENDAS:\n"
            
            for item in vendas_widgets:
                q = float(item["qtd"].value or 0)
                v = float(item["val"].value or 0)
                p = item["perc"].value / 100
                
                if q > 0 and v > 0:
                    subtotal = (q * v) * p
                    total_comissao += subtotal
                    resumo_vendas += f"• {item['mat'].value}: {q:.0f} un x R$ {v:.2f} (%{item['perc'].value}) = R$ {subtotal:.2f}\n"

            sal = float(salario_in.value or 0)
            bruto = sal + total_comissao + float(ben_in.value or 0)
            
            # Resultado Final
            relatorio = f"{resumo_vendas}\n💰 SALÁRIO BRUTO: R$ {bruto:.2f}\n📈 TOTAL COMISSÕES: R$ {total_comissao:.2f}"
            
            if tipo_calc.value == "Rescisão":
                m = int(meses_rescisao.value or 0)
                valor_rescisao = bruto + (sal/12 * m)
                relatorio += f"\n\n🔥 ESTIMATIVA RESCISÃO: R$ {valor_rescisao:.2f}"

            res_txt.value = relatorio
            res_container.visible = True
            page.update()
        except:
            res_txt.value = "⚠️ Erro: Use apenas números e preencha o salário."
            res_container.visible = True
            page.update()

    # --- MONTAGEM DA TELA ---
    page.add(
        ft.Text("SISTEMA PINK V3.4", size=28, weight="bold", color=PALETA["texto_destaque"]),
        
        ft.Text("Configurações de Salário", weight="bold", color=PALETA["texto_preto"]),
        salario_in,
        ben_in,

        ft.ExpansionTile(
            title=ft.Text("🛒 LANÇAR VENDAS (QTD / MATERIAL / VALOR)", color=PALETA["texto_destaque"], weight="bold"),
            controls=[item["ui"] for item in vendas_widgets]
        ),

        ft.Container(
            content=ft.Column([
                tipo_calc,
                meses_rescisao,
                ft.Text("Possui férias vencidas?", color=PALETA["texto_preto"], weight="bold"),
                ft.RadioGroup(content=ft.Row([ft.Radio(value="s", label="Sim"), ft.Radio(value="n", label="Não")]), value="n")
            ]),
            padding=20, bgcolor=PALETA["fundo_card"], border_radius=15
        ),

        ft.ElevatedButton(
            "CALCULAR TUDO",
            on_click=calcular,
            bgcolor=PALETA["primaria"],
            color=ft.Colors.WHITE,
            height=55,
            width=500
        ),
        
        res_container
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
