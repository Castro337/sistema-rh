import flet as ft
import os

# PADRÕES DE DESIGN
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
    page.title = "PINK Calculo Salarial V3.9 | By Jean Castro"
    page.bgcolor = PALETA["fundo"]
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 30

    # MOTOR CLT (INSS + IRRF PROGRESSIVO)
    def calcular_clt(bruto):
        if bruto <= 1518: inss = bruto * 0.075
        elif bruto <= 2793: inss = (bruto * 0.09) - 22.77
        elif bruto <= 4190: inss = (bruto * 0.12) - 106.56
        else: inss = (bruto * 0.14) - 190.36
        
        base_ir = bruto - inss
        if base_ir <= 2259: irrf = 0
        elif base_ir <= 2826: irrf = (base_ir * 0.075) - 169.44
        elif base_ir <= 3751: irrf = (base_ir * 0.15) - 381.44
        else: irrf = (base_ir * 0.225) - 662.77
        
        return round(inss, 2), round(irrf, 2)

    # CORREÇÃO DO ERRO: Removido 'weight' direto do TextField
    salario_in = ft.TextField(
        label="Salário Base", 
        prefix=ft.Text("R$ "), 
        border_color=PALETA["primaria"],
        text_style=ft.TextStyle(weight="bold") # Forma correta de usar negrito
    )

    extra_in = ft.TextField(
        label="Benefícios e Extras", 
        prefix=ft.Text("R$ "), 
        border_color=PALETA["primaria"]
    )

    vendas_lista = []
    for i in range(1, 6):
        qtd = ft.TextField(label="Qtd", value="1", width=65)
        mat = ft.TextField(label=f"Material {i}", expand=True)
        val = ft.TextField(label="Valor Un.", prefix=ft.Text("R$ "), width=110)
        perc = ft.Slider(min=0, max=100, divisions=100, label="Comissão: {value}%", value=3)
        
        ui = ft.Container(
            content=ft.Column([ft.Row([qtd, mat, val], spacing=10), perc, ft.Divider(color=ft.Colors.PINK_100)]),
            padding=15, bgcolor=PALETA["card"], border_radius=15
        )
        vendas_lista.append({"qtd": qtd, "mat": mat, "val": val, "perc": perc, "ui": ui})

    res_container = ft.Container(visible=False, padding=25, border_radius=20, bgcolor="#F8F9FA", border=ft.border.all(2, PALETA["primaria"]))
    
    def calcular(e):
        try:
            sal_base = float(salario_in.value or 0)
            beneficios = float(extra_in.value or 0)
            
            total_comissao = 0
            for v in vendas_lista:
                q = float(v["qtd"].value or 0)
                vu = float(v["val"].value or 0)
                p = v["perc"].value / 100
                total_comissao += (q * vu) * p

            bruto_total = sal_base + beneficios + total_comissao
            inss, irrf = calcular_clt(bruto_total)
            liquido = bruto_total - inss - irrf

            res_container.content = ft.Column([
                ft.Text("📑 EXTRATO DE PAGAMENTO", size=20, weight="bold", color=ft.Colors.PINK_900),
                ft.Text("➕ ACRESCENTADO (PROVENTOS):", weight="bold", color=PALETA["positivo"]),
                ft.Text(f"   • Salário + Extras: R$ {sal_base + beneficios:.2f}"),
                ft.Text(f"   • Comissões: R$ {total_comissao:.2f}"),
                ft.Divider(),
                ft.Text("➖ DESCONTADO (DEDUÇÕES):", weight="bold", color=PALETA["negativo"]),
                ft.Text(f"   • INSS: R$ {inss:.2f}"),
                ft.Text(f"   • IRRF: R$ {irrf:.2f}"),
                ft.Container(
                    content=ft.Text(f"💰 LÍQUIDO: R$ {liquido:.2f}", size=20, weight="bold", color=PALETA["primaria"]),
                    padding=10, bgcolor=ft.Colors.PINK_50, border_radius=10
                ),
                ft.Divider(),
                ft.Row([ft.Icon(ft.Icons.AUTO_AWESOME, color=PALETA["ia_cor"]), ft.Text("IA PINK ANALISA:", weight="bold", color=PALETA["ia_cor"])]),
                ft.Text("🤖 IA PINK: Cálculo processado com as regras CLT vigentes. Seu saldo líquido está disponível!", italic=True)
            ])
            
            res_container.visible = True
            page.update()
        except Exception as ex:
            print(f"Erro no calculo: {ex}")
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Use apenas números nos campos de valor!"))
            page.snack_bar.open = True
            page.update()

    page.add(
        ft.Text("PINK SYSTEM V3.9", size=28, weight="bold", color=ft.Colors.PINK_900),
        salario_in,
        extra_in,
        ft.ExpansionTile(
            title=ft.Text("🛒 Detalhar Vendas", weight="bold"),
            controls=[item["ui"] for item in vendas_lista]
        ),
        ft.ElevatedButton("GERAR EXTRATO CLT", on_click=calcular, bgcolor=PALETA["primaria"], color="white", height=60, width=float("inf")),
        res_container
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
