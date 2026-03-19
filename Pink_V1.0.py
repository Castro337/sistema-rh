import flet as ft
import os

# 1. PADRÕES DE DESIGN (Foco em Contraste e Legibilidade)
PALETA = {
    "primaria": ft.Colors.DEEP_PURPLE_600,
    "fundo": ft.Colors.WHITE,
    "card": "#F3E5F5",
    "ia_cor": ft.Colors.PINK_600,
    "texto": ft.Colors.BLACK, # Letras sempre pretas
    "positivo": ft.Colors.GREEN_700,
    "negativo": ft.Colors.RED_700
}

def main(page: ft.Page):
    page.title = "PINK Calculo Salarial V4.2 | By Jean Castro"
    page.bgcolor = PALETA["fundo"]
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 30

    # --- MOTOR DE CÁLCULO (CLT + RESCISÃO) ---
    def calcular_impostos(valor):
        # INSS 2026 Progressivo
        if valor <= 1518: inss = valor * 0.075
        elif valor <= 2793: inss = (valor * 0.09) - 22.77
        elif valor <= 4190: inss = (valor * 0.12) - 106.56
        else: inss = (valor * 0.14) - 190.36
        
        # IRRF Simples
        base_ir = valor - inss
        irrf = (base_ir * 0.075) - 169.44 if base_ir > 2259 else 0
        return round(inss, 2), round(max(0, irrf), 2)

    # --- CAMPOS DE ENTRADA ---
    # Seletor de Modo (Mensal ou Rescisão)
    modo_calc = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="mensal", label="Mensal (Holerite)", label_style=ft.TextStyle(color=PALETA["texto"])),
            ft.Radio(value="rescisao", label="Rescisão (Saída)", label_style=ft.TextStyle(color=PALETA["texto"]))
        ]), 
        value="mensal"
    )

    salario_in = ft.TextField(
        label="Salário Base", 
        label_style=ft.TextStyle(color=PALETA["texto"]),
        prefix=ft.Text("R$ ", color=PALETA["texto"]), 
        border_color=PALETA["primaria"],
        color=PALETA["texto"], # Texto digitado em preto
        text_style=ft.TextStyle(weight="bold")
    )

    extra_in = ft.TextField(
        label="Benefícios / Extras / Prêmios", 
        label_style=ft.TextStyle(color=PALETA["texto"]),
        prefix=ft.Text("R$ ", color=PALETA["texto"]), 
        border_color=PALETA["primaria"],
        color=PALETA["texto"],
        value="0"
    )

    # Vendas Detalhadas
    vendas_lista = []
    for i in range(1, 4):
        val = ft.TextField(label=f"Valor Venda {i}", label_style=ft.TextStyle(color=PALETA["texto"]), prefix=ft.Text("R$ "), color=PALETA["texto"], expand=True)
        perc = ft.Slider(min=0, max=20, divisions=20, label="Comissão: {value}%", value=3)
        vendas_lista.append({"val": val, "perc": perc})

    # --- RESULTADOS ---
    res_container = ft.Container(visible=False, padding=25, border_radius=20, bgcolor="#F8F9FA", border=ft.border.all(2, PALETA["primaria"]))
    res_txt = ft.Text("", color=PALETA["texto"], size=16)
    ia_txt = ft.Text("", color=PALETA["ia_cor"], italic=True, weight="bold")

    def processar(e):
        try:
            base = float(salario_in.value or 0)
            extras = float(extra_in.value or 0)
            
            comissao_total = 0
            for item in vendas_lista:
                v = float(item["val"].value or 0)
                p = item["perc"].value / 100
                comissao_total += (v * p)

            bruto = base + extras + comissao_total
            
            # Lógica de Rescisão (Adiciona Proporcionais Simples)
            aviso_previo = 0
            if modo_calc.value == "rescisao":
                aviso_previo = base # Simulação de 1 salário de aviso
                bruto += aviso_previo

            inss, irrf = calcular_impostos(bruto)
            liquido = bruto - inss - irrf

            # Relatório de Transparência
            tipo = "MENSAL" if modo_calc.value == "mensal" else "RESCISÃO"
            res_txt.value = (
                f"📊 TIPO DE CÁLCULO: {tipo}\n"
                f"--------------------------------\n"
                f"✅ PROVENTOS (O QUE ENTROU):\n"
                f"   • Salário Base: R$ {base:.2f}\n"
                f"   • Comissões: R$ {comissao_total:.2f}\n"
                f"   • Extras: R$ {extras:.2f}\n"
                + (f"   • Aviso Prévio: R$ {aviso_previo:.2f}\n" if aviso_previo > 0 else "") +
                f"\n❌ DEDUÇÕES (O QUE SAIU):\n"
                f"   • INSS: R$ {inss:.2f}\n"
                f"   • IRRF: R$ {irrf:.2f}\n"
                f"--------------------------------\n"
                f"💰 VALOR LÍQUIDO FINAL: R$ {liquido:.2f}"
            )

            ia_txt.value = f"🤖 IA PINK: Cálculo de {tipo} realizado. Tudo pronto para o fechamento!"
            res_container.visible = True
            page.update()
        except:
            page.snack_bar = ft.SnackBar(ft.Text("Erro: Verifique os valores digitados."))
            page.snack_bar.open = True
            page.update()

    # --- LAYOUT ---
    page.add(
        ft.Text("PINK SYSTEM V4.2", size=28, weight="bold", color=PALETA["primaria"]),
        ft.Text("Escolha o Modo:", color=PALETA["texto"], weight="bold"),
        modo_calc,
        salario_in,
        extra_in,
        ft.ExpansionTile(
            title=ft.Text("🛒 Comissões de Vendas", weight="bold", color=PALETA["texto"]),
            controls=[ft.Column([i["val"], i["perc"], ft.Divider()]) for i in vendas_lista]
        ),
        ft.ElevatedButton("GERAR EXTRATO DETALHADO", on_click=processar, bgcolor=PALETA["primaria"], color="white", height=55, width=float("inf")),
        res_container
    )
    res_container.content = ft.Column([res_txt, ft.Divider(), ia_txt])

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
