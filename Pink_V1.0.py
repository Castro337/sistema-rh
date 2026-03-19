mport flet as ft
import os

# 1. PADRÕES DE DESIGN (Alto Contraste e Rosa Vibrante)
PALETA = {
    "primaria": ft.Colors.PINK_600,
    "fundo": ft.Colors.WHITE,
    "card": "#FFF0F5",
    "ia_cor": ft.Colors.DEEP_PURPLE_500,
    "texto": ft.Colors.BLACK,
    "positivo": ft.Colors.GREEN_700,
    "negativo": ft.Colors.RED_700
}

def main(page: ft.Page):
    page.title = "PINK Calculo Salarial |By Jean"
    page.bgcolor = PALETA["fundo"]
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 30

    # --- MOTOR DE CÁLCULO CLT (INSS + IRRF 2026) ---
    def calcular_clt(bruto):
        # INSS Progressivo 2026
        if bruto <= 1518: inss = bruto * 0.075
        elif bruto <= 2793: inss = (bruto * 0.09) - 22.77
        elif bruto <= 4190: inss = (bruto * 0.12) - 106.56
        else: inss = (bruto * 0.14) - 190.36
        
        # IRRF Progressivo
        base_ir = bruto - inss
        if base_ir <= 2259: irrf = 0
        elif base_ir <= 2826: irrf = (base_ir * 0.075) - 169.44
        elif base_ir <= 3751: irrf = (base_ir * 0.15) - 381.44
        else: irrf = (base_ir * 0.225) - 662.77
        
        return round(inss, 2), round(irrf, 2)

    # --- CAMPOS DE ENTRADA ---
    # Correção: weight movido para text_style para evitar erro de inicialização
    salario_in = ft.TextField(
        label="Salário Base", 
        prefix=ft.Text("R$ "), 
        border_color=PALETA["primaria"],
        text_style=ft.TextStyle(weight="bold", color=PALETA["texto"])
    )

    extra_in = ft.TextField(
        label="Benefícios e Extras (Outros Ganho)", 
        prefix=ft.Text("R$ "), 
        border_color=PALETA["primaria"],
        value="0"
    )

    # Lista para Vendas Detalhadas
    vendas_lista = []
    for i in range(1, 6):
        qtd = ft.TextField(label="Qtd", value="1", width=70)
        mat = ft.TextField(label=f"Material {i}", expand=True)
        val = ft.TextField(label="Valor Un.", prefix=ft.Text("R$ "), width=110)
        perc = ft.Slider(min=0, max=100, divisions=100, label="Comissão: {value}%", value=3)
        
        container_venda = ft.Container(
            content=ft.Column([
                ft.Row([qtd, mat, val], spacing=10),
                perc,
                ft.Divider(color=ft.Colors.PINK_100)
            ]),
            padding=15, bgcolor=PALETA["card"], border_radius=15
        )
        vendas_lista.append({"qtd": qtd, "mat": mat, "val": val, "perc": perc, "ui": container_venda})

    # --- ÁREA DE RESULTADOS ---
    res_txt = ft.Text("", color=PALETA["texto"], size=16)
    ia_txt = ft.Text("", color=PALETA["ia_cor"], italic=True, weight="bold")
    
    res_container = ft.Container(
        visible=False, 
        padding=25, 
        border_radius=20, 
        bgcolor="#F8F9FA", 
        border=ft.border.all(2, PALETA["primaria"])
    )

    def realizar_calculo(e):
        try:
            # 1. PROVENTOS (O que foi acrescentado)
            sal_fixo = float(salario_in.value or 0)
            beneficios = float(extra_in.value or 0)
            
            total_comissao = 0
            for item in vendas_lista:
                q = float(item["qtd"].value or 0)
                v = float(item["val"].value or 0)
                p = item["perc"].value / 100
                total_comissao += (q * v) * p

            bruto = sal_fixo + beneficios + total_comissao
            
            # 2. DEDUÇÕES (O que foi descontado)
            inss, irrf = calcular_clt(bruto)
            liquido = bruto - inss - irrf

            # 3. EXTRATO DETALHADO (Conforme solicitado)
            res_txt.value = (
                f"➕ ACRESCENTADO (PROVENTOS):\n"
                f"   • Salário Base: R$ {sal_fixo:.2f}\n"
                f"   • Extras/Benefícios: R$ {beneficios:.2f}\n"
                f"   • Comissões: R$ {total_comissao:.2f}\n\n"
                f"➖ DESCONTADO (DEDUÇÕES CLT):\n"
                f"   • INSS: R$ {inss:.2f}\n"
                f"   • IRRF: R$ {irrf:.2f}\n\n"
                f"💰 LÍQUIDO FINAL: R$ {liquido:.2f}"
            )

            # 4. INTELIGÊNCIA IA
            if total_comissao > (bruto * 0.3):
                ia_txt.value = "🤖 IA PINK: Sensacional! Suas comissões representam uma fatia forte do seu ganho. Continue assim!"
            else:
                ia_txt.value = "🤖 IA PINK: Cálculo finalizado. Os descontos seguem a tabela progressiva oficial."

            res_container.content = ft.Column([
                ft.Text("📑 EXTRATO DETALHADO", size=20, weight="bold", color=ft.Colors.PINK_900),
                res_txt,
                ft.Divider(),
                ft.Row([ft.Icon(ft.Icons.AUTO_AWESOME, color=PALETA["ia_cor"]), ft.Text("ANÁLISE DA IA", weight="bold", color=PALETA["ia_cor"])]),
                ia_txt
            ])
            
            res_container.visible = True
            page.update()

        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text("Erro: Verifique se usou pontos em vez de vírgulas."))
            page.snack_bar.open = True
            page.update()

    # --- MONTAGEM DO APP ---
    page.add(
        ft.Text("PINK SYSTEM V4.0", size=28, weight="bold", color=ft.Colors.PINK_900),
        ft.Text("Dados de Contrato e Benefícios", weight="bold"),
        salario_in,
        extra_in,
        ft.ExpansionTile(
            title=ft.Text("🛒 Lançar Vendas e Produtos", weight="bold", color=ft.Colors.PINK_700),
            controls=[item["ui"] for item in vendas_lista]
        ),
        ft.ElevatedButton(
            "GERAR EXTRATO E CONSULTAR IA", 
            on_click=realizar_calculo, 
            bgcolor=PALETA["primaria"], 
            color="white", 
            height=60, 
            width=500
        ),
        res_container
    )

if __name__ == "__main__":
    # Configuração de porta para o Render
    port = int(os.getenv("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
