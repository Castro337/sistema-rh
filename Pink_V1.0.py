import flet as ft
import os

# 1. PADRÕES DE DESIGN (Alto Contraste e Rosa Vibrante)
PALETA = {
    "primaria": ft.Colors.PINK_600,
    "fundo": ft.Colors.WHITE,
    "card": "#FFF0F5",
    "ia_cor": ft.Colors.DEEP_PURPLE_500,
    "texto_preto": ft.Colors.BLACK,
    "positivo": ft.Colors.GREEN_700,
    "negativo": ft.Colors.RED_700
}

def main(page: ft.Page):
    page.title = "PINK Cálculo Salarial V3.8 Com I.A Integrada | By Jean Castro"
    page.bgcolor = PALETA["fundo"]
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 30

    # --- MOTOR CLT (Cálculo Oficial Progressivo) ---
    def calcular_clt(bruto):
        # INSS 2026
        if bruto <= 1518: inss = bruto * 0.075
        elif bruto <= 2793: inss = (bruto * 0.09) - 22.77
        elif bruto <= 4190: inss = (bruto * 0.12) - 106.56
        else: inss = (bruto * 0.14) - 190.36
        
        # IRRF
        base_ir = bruto - inss
        if base_ir <= 2259: irrf = 0
        elif base_ir <= 2826: irrf = (base_ir * 0.075) - 169.44
        elif base_ir <= 3751: irrf = (base_ir * 0.15) - 381.44
        else: irrf = (base_ir * 0.225) - 662.77
        
        return round(inss, 2), round(irrf, 2)

    # --- ENTRADAS DE DADOS ---
    salario_in = ft.TextField(label="Salário Base", prefix=ft.Text("R$ "), border_color=PALETA["primaria"], color=PALETA["texto_preto"], weight="bold")
    extra_in = ft.TextField(label="Benefícios e Extras (Prêmios/Gratificações)", prefix=ft.Text("R$ "), border_color=PALETA["primaria"], color=PALETA["texto_preto"])

    vendas_lista = []
    for i in range(1, 6):
        qtd = ft.TextField(label="Qtd", value="1", width=65, color=PALETA["texto_preto"])
        mat = ft.TextField(label=f"Material {i}", expand=True, color=PALETA["texto_preto"])
        val = ft.TextField(label="Valor Un.", prefix=ft.Text("R$ "), width=110, color=PALETA["texto_preto"])
        perc = ft.Slider(min=0, max=100, divisions=100, label="Comissão: {value}%", value=3)
        
        ui = ft.Container(
            content=ft.Column([ft.Row([qtd, mat, val], spacing=10), perc, ft.Divider(color=ft.Colors.PINK_100)]),
            padding=15, bgcolor=PALETA["card"], border_radius=15
        )
        vendas_lista.append({"qtd": qtd, "mat": mat, "val": val, "perc": perc, "ui": ui})

    # --- ÁREA DE RESULTADO DETALHADO ---
    res_container = ft.Container(visible=False, padding=25, border_radius=20, bgcolor="#F8F9FA", border=ft.border.all(2, PALETA["primaria"]))
    
    def calcular(e):
        try:
            # 1. ACRESCENTADOS (Proventos)
            sal_base = float(salario_in.value or 0)
            beneficios = float(extra_in.value or 0)
            
            total_comissao = 0
            detalhe_vendas = ""
            for v in vendas_lista:
                q = float(v["qtd"].value or 0)
                vu = float(v["val"].value or 0)
                p = v["perc"].value / 100
                if q > 0 and vu > 0:
                    sub = (q * vu) * p
                    total_comissao += sub
                    detalhe_vendas += f"   • {v['mat'].value}: R$ {sub:.2f}\n"

            bruto_total = sal_base + beneficios + total_comissao

            # 2. DESCONTADOS (Deduções)
            inss, irrf = calcular_clt(bruto_total)
            liquido = bruto_total - inss - irrf

            # 3. MONTAGEM DO RELATÓRIO DE TRANSPARÊNCIA
            res_container.content = ft.Column([
                ft.Text("📑 EXTRATO DETALHADO", size=20, weight="bold", color=ft.Colors.PINK_900),
                
                ft.Text("➕ O QUE FOI ACRESCENTADO (PROVENTOS):", weight="bold", color=PALETA["positivo"]),
                ft.Text(f"   • Salário Base: R$ {sal_base:.2f}"),
                ft.Text(f"   • Benefícios/Extras: R$ {beneficios:.2f}"),
                ft.Text(f"   • Total Comissões: R$ {total_comissao:.2f}"),
                ft.Text(detalhe_vendas, size=12, italic=True),
                
                ft.Divider(),
                
                ft.Text("➖ O QUE FOI DESCONTADO (DEDUÇÕES):", weight="bold", color=PALETA["negativo"]),
                ft.Text(f"   • INSS (Previdência): R$ {inss:.2f}"),
                ft.Text(f"   • IRRF (Imposto de Renda): R$ {irrf:.2f}"),
                
                ft.Container(
                    content=ft.Row([
                        ft.Text("💰 LÍQUIDO A RECEBER:", size=18, weight="bold"),
                        ft.Text(f"R$ {liquido:.2f}", size=18, weight="bold", color=PALETA["primaria"])
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=10, bgcolor=ft.Colors.PINK_50, border_radius=10
                ),
                
                ft.Divider(),
                ft.Row([ft.Icon(ft.Icons.AUTO_AWESOME, color=PALETA["ia_cor"]), ft.Text("ANÁLISE DA IA PINK", weight="bold", color=PALETA["ia_cor"])]),
                ft.Text(
                    "🤖 IA PINK: " + (
                        "Uau! Suas comissões turbinaram seu salário. Excelente gestão de vendas!" if total_comissao > sal_base else
                        "Os descontos CLT estão altos, mas seu saldo líquido permanece saudável." if inss+irrf > 500 else
                        "Cálculo finalizado. Tudo pronto para o fechamento do mês!"
                    ),
                    color=PALETA["ia_cor"], italic=True
                )
            ])
            
            res_container.visible = True
            page.update()
        except:
            page.snack_bar = ft.SnackBar(ft.Text("Erro: Use apenas números nos valores!"))
            page.snack_bar.open = True
            page.update()

    # --- LAYOUT ---
    page.add(
        ft.Text("PINK SYSTEM V3.8", size=28, weight="bold", color=ft.Colors.PINK_900),
        ft.Text("Configuração de Ganhos", weight="bold"),
        salario_in,
        extra_in,
        ft.ExpansionTile(
            title=ft.Text("🛒 Lançar Vendas Detalhadas", weight="bold", color=ft.Colors.PINK_700),
            controls=[item["ui"] for item in vendas_widgets]
        ),
        ft.ElevatedButton("GERAR EXTRATO COMPLETO", on_click=calcular, bgcolor=PALETA["primaria"], color="white", height=60, width=500),
        res_container
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)

