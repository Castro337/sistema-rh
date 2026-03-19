import flet as ft
import os

# 1. PADRÕES DE DESIGN (Foco em Legibilidade e Alto Contraste)
PALETA = {
    "primaria": ft.Colors.DEEP_PURPLE_700,
    "fundo": ft.Colors.WHITE,
    "card_fundo": "#F5F5F5",
    "ia_cor": ft.Colors.PINK_700,
    "texto_preto": ft.Colors.BLACK,
    "positivo": ft.Colors.GREEN_800,
    "negativo": ft.Colors.RED_800
}

def main(page: ft.Page):
    page.title = "PINK Calculo Salarial | By Jean Castro"
    page.bgcolor = PALETA["fundo"]
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 30

    # --- MOTOR DE CÁLCULO (CLT + RESCISÃO) ---
    def calcular_impostos(valor):
        # Simulação de INSS Progressivo 2026
        if valor <= 1518: inss = valor * 0.075
        elif valor <= 2793: inss = (valor * 0.09) - 22.77
        elif valor <= 4190: inss = (valor * 0.12) - 106.56
        else: inss = (valor * 0.14) - 190.36
        
        # Base de Cálculo IRRF
        base_ir = valor - inss
        irrf = (base_ir * 0.075) - 169.44 if base_ir > 2259 else 0
        return round(inss, 2), round(max(0, irrf), 2)

    # --- CAMPOS DE ENTRADA ---
    modo_calc = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="mensal", label="Cálculo Mensal", fill_color=PALETA["primaria"]),
            ft.Radio(value="rescisao", label="Cálculo Rescisão", fill_color=PALETA["primaria"])
        ]),
        value="mensal"
    )

    salario_in = ft.TextField(
        label="Salário Base", 
        prefix=ft.Text("R$ ", color=PALETA["texto_preto"]), 
        border_color=PALETA["primaria"],
        color=PALETA["texto_preto"],
        text_style=ft.TextStyle(weight="bold")
    )

    extra_in = ft.TextField(
        label="Benefícios e Prêmios Extras", 
        prefix=ft.Text("R$ ", color=PALETA["texto_preto"]), 
        border_color=PALETA["primaria"],
        color=PALETA["texto_preto"],
        value="0"
    )

    # Gerador de campos de vendas
    vendas_lista = []
    for i in range(1, 4):
        val = ft.TextField(label=f"Valor Venda {i}", prefix=ft.Text("R$ "), color=PALETA["texto_preto"])
        perc = ft.Slider(min=0, max=20, divisions=20, label="Comissão: {value}%", value=3, active_color=PALETA["primaria"])
        vendas_lista.append({"val": val, "perc": perc})

    # --- CONTAINER DE RESULTADO ---
    res_txt = ft.Text("", color=PALETA["texto_preto"], size=15)
    ia_txt = ft.Text("", color=PALETA["ia_cor"], weight="bold", italic=True)
    
    res_container = ft.Container(
        visible=False, 
        padding=25, 
        border_radius=15, 
        bgcolor=PALETA["card_fundo"], 
        border=ft.border.all(1, ft.Colors.GREY_400),
        content=ft.Column([res_txt, ft.Divider(), ia_txt])
    )

    def processar(e):
        try:
            base = float(salario_in.value or 0)
            extras = float(extra_in.value or 0)
            
            # Cálculo de Comissões
            comissao_total = 0
            for item in vendas_lista:
                v = float(item["val"].value or 0)
                p = item["perc"].value / 100
                comissao_total += (v * p)

            bruto = base + extras + comissao_total
            aviso_previo = 0
            
            # Lógica de Rescisão (Simulação de Aviso Prévio)
            if modo_calc.value == "rescisao":
                aviso_previo = base
                bruto += aviso_previo

            inss, irrf = calcular_impostos(bruto)
            liquido = bruto - inss - irrf

            # Relatório Detalhado (O que acrescentou vs O que descontou)
            tipo_label = "MENSAL (HOLERITE)" if modo_calc.value == "mensal" else "RESCISÃO DE CONTRATO"
            
            res_txt.value = (
                f"📋 TIPO: {tipo_label}\n"
                f"-------------------------------------------\n"
                f"✅ ACRESCENTADO (PROVENTOS):\n"
                f"   • Salário Base: R$ {base:.2f}\n"
                f"   • Comissões: R$ {comissao_total:.2f}\n"
                f"   • Extras/Prêmios: R$ {extras:.2f}\n"
                + (f"   • Aviso Prévio: R$ {aviso_previo:.2f}\n" if aviso_previo > 0 else "") +
                f"\n❌ DESCONTADO (DEDUÇÕES):\n"
                f"   • INSS: R$ {inss:.2f}\n"
                f"   • IRRF: R$ {irrf:.2f}\n"
                f"-------------------------------------------\n"
                f"💰 VALOR LÍQUIDO: R$ {liquido:.2f}"
            )

            ia_txt.value = f"🤖 IA PINK: Análise de {modo_calc.value} pronta. Tudo certo para o fechamento!"
            res_container.visible = True
            page.update()
        except:
            page.snack_bar = ft.SnackBar(ft.Text("Erro: Verifique os campos de valor."))
            page.snack_bar.open = True
            page.update()

    # --- MONTAGEM DO LAYOUT ---
    page.add(
        ft.Text("PINK SYSTEM V4.2", size=28, weight="bold", color=PALETA["primaria"]),
        ft.Text("Tipo de Cálculo", color=PALETA["texto_preto"], weight="w500"),
        modo_calc,
        salario_in,
        extra_in,
        ft.ExpansionTile(
            title=ft.Text("🛒 Lançar Vendas Individualmente", color=PALETA["texto_preto"]),
            controls=[ft.Container(content=ft.Column([i["val"], i["perc"]]), padding=10) for i in vendas_lista]
        ),
        ft.ElevatedButton(
            "CALCULAR EXTRATO COMPLETO", 
            on_click=processar, 
            bgcolor=PALETA["primaria"], 
            color="white", 
            height=55, 
            width=float("inf")
        ),
        res_container
    )

if __name__ == "__main__":
    # Configuração de porta para o Render
    port = int(os.getenv("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
