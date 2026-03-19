import flet as ft
import os

# 1. PADRÕES DE DESIGN (Contraste Máximo e Cores Profissionais)
PALETA = {
    "primaria": ft.Colors.PINK_600,
    "fundo": ft.Colors.WHITE,
    "card_fundo": "#F5F5F5",
    "ia_cor": ft.Colors.PINK_700,
    "texto": ft.Colors.BLACK,
    "positivo": ft.Colors.GREEN_800,
    "negativo": ft.Colors.RED_800
}

def main(page: ft.Page):
    page.title = "PINK Calculo Salarial | By Jean Castro"
    page.bgcolor = PALETA["fundo"]
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 30

    # --- MOTOR DE CÁLCULO CLT ---
    def calcular_impostos(valor):
        if valor <= 1518: inss = valor * 0.075
        elif valor <= 2793: inss = (valor * 0.09) - 22.77
        elif valor <= 4190: inss = (valor * 0.12) - 106.56
        else: inss = (valor * 0.14) - 190.36
        
        base_ir = valor - inss
        irrf = (base_ir * 0.075) - 169.44 if base_ir > 2259 else 0
        return round(inss, 2), round(max(0, irrf), 2)

    # --- CAMPOS DE ENTRADA ---
    modo_calc = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="mensal", label="Cálculo Mensal", label_style=ft.TextStyle(color=PALETA["texto"])),
            ft.Radio(value="rescisao", label="Cálculo Rescisão", label_style=ft.TextStyle(color=PALETA["texto"]))
        ]), 
        value="mensal"
    )

    salario_in = ft.TextField(
        label="Salário Base", 
        prefix=ft.Text("R$ ", color=PALETA["texto"]), 
        border_color=PALETA["primaria"],
        color=PALETA["texto"],
        text_style=ft.TextStyle(weight="bold")
    )

    extra_in = ft.TextField(
        label="Benefícios / Prêmios Extras", 
        prefix=ft.Text("R$ ", color=PALETA["texto"]), 
        border_color=PALETA["primaria"],
        color=PALETA["texto"],
        value="0"
    )

    # LISTA DE PRODUTOS COM QUANTIDADE
    vendas_lista = []
    for i in range(1, 4):
        qtd = ft.TextField(label="Qtd", value="1", width=80, color=PALETA["texto"])
        prod = ft.TextField(label=f"Produto {i}", expand=True, color=PALETA["texto"])
        val_un = ft.TextField(label="Valor Un.", prefix=ft.Text("R$ "), width=120, color=PALETA["texto"])
        perc = ft.Slider(min=0, max=20, divisions=20, label="Comissão: {value}%", value=3)
        
        vendas_lista.append({"qtd": qtd, "prod": prod, "val": val_un, "perc": perc})

    # --- ÁREA DE RESULTADO ---
    res_container = ft.Container(visible=False, padding=25, border_radius=20, bgcolor=PALETA["card_fundo"], border=ft.border.all(1, ft.Colors.GREY_400))
    res_txt = ft.Text("", color=PALETA["texto"], size=15)
    ia_txt = ft.Text("", color=PALETA["ia_cor"], italic=True, weight="bold")

    def processar(e):
        try:
            base = float(salario_in.value or 0)
            extras = float(extra_in.value or 0)
            
            comissao_total = 0
            detalhe_itens = ""
            
            for item in vendas_lista:
                q = float(item["qtd"].value or 0)
                v = float(item["val"].value or 0)
                p = item["perc"].value / 100
                if q > 0 and v > 0:
                    subtotal = (q * v) * p
                    comissao_total += subtotal
                    nome = item["prod"].value or f"Produto"
                    detalhe_itens += f"   • {int(q)}x {nome}: R$ {subtotal:.2f}\n"

            bruto = base + extras + comissao_total
            aviso_previo = 0
            if modo_calc.value == "rescisao":
                aviso_previo = base
                bruto += aviso_previo

            inss, irrf = calcular_impostos(bruto)
            liquido = bruto - inss - irrf

            res_txt.value = (
                f"📊 RELATÓRIO: {modo_calc.value.upper()}\n"
                f"-------------------------------------------\n"
                f"✅ PROVENTOS (ENTRADAS):\n"
                f"   • Salário Base: R$ {base:.2f}\n"
                f"   • Extras: R$ {extras:.2f}\n"
                f"   • Comissões: R$ {comissao_total:.2f}\n"
                f"{detalhe_itens}"
                + (f"   • Aviso Prévio: R$ {aviso_previo:.2f}\n" if aviso_previo > 0 else "") +
                f"\n❌ DEDUÇÕES (SAÍDAS):\n"
                f"   • INSS: R$ {inss:.2f}\n"
                f"   • IRRF: R$ {irrf:.2f}\n"
                f"-------------------------------------------\n"
                f"💰 LÍQUIDO FINAL: R$ {liquido:.2f}"
            )

            ia_txt.value = "🤖 IA PINK: Vendas processadas por quantidade. Tudo pronto!"
            res_container.visible = True
            page.update()
        except:
            page.snack_bar = ft.SnackBar(ft.Text("Erro: Use números e ponto nos valores."))
            page.snack_bar.open = True
            page.update()

    # --- LAYOUT FINAL ---
    page.add(
        ft.Text("PINKCalculo Salarial | By Jean Castro", size=28, weight="bold", color=PALETA["primaria"]),
        modo_calc,
        salario_in,
        extra_in,
        ft.ExpansionTile(
            title=ft.Text("🛒 Lançar Vendas (Qtd x Valor)", color=PALETA["texto"], weight="bold"),
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Row([i["qtd"], i["prod"], i["val"]], spacing=10),
                        i["perc"],
                        ft.Divider()
                    ]), padding=15
                ) for i in vendas_lista
            ]
        ),
        ft.ElevatedButton("GERAR EXTRATO COMPLETO", on_click=processar, bgcolor=PALETA["primaria"], color="white", height=55, width=float("inf")),
        res_container
    )
    res_container.content = ft.Column([res_txt, ft.Divider(), ia_txt])

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
