import flet as ft
import os

# 1. PADRÕES DE DESIGN (Identidade Visual PINK)
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
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- MOTOR DE CÁLCULO CLT 2026 (ATUALIZADO) ---
    def calcular_impostos(valor):
        # Cálculo do INSS 2026 (Baseado nas faixas de 1.518,00 a 8.157,41)
        if valor <= 1518.00:
            inss = valor * 0.075
        elif valor <= 2793.88:
            inss = (valor * 0.09) - 22.77
        elif valor <= 4190.83:
            inss = (valor * 0.12) - 106.56
        elif valor <= 8157.41:
            inss = (valor * 0.14) - 190.38
        else:
            inss = 951.66  # Teto máximo de contribuição 2026
        
        # Cálculo do IRRF 2026 (Base de cálculo = Bruto - INSS)
        base_ir = valor - inss
        
        if base_ir <= 2259.20:
            irrf = 0
        elif base_ir <= 2826.65:
            irrf = (base_ir * 0.075) - 169.44
        elif base_ir <= 3751.05:
            irrf = (base_ir * 0.15) - 381.44
        elif base_ir <= 4664.68:
            irrf = (base_ir * 0.225) - 662.77
        else:
            irrf = (base_ir * 0.275) - 896.00
            
        return round(inss, 2), round(max(0, irrf), 2)

    # --- COMPONENTES DE INTERFACE ---
    modo_calc = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="mensal", label="Folha Mensal", label_style=ft.TextStyle(color=PALETA["texto"])),
            ft.Radio(value="rescisao", label="Rescisão (Aviso Prévio)", label_style=ft.TextStyle(color=PALETA["texto"]))
        ]), 
        value="mensal"
    )

    salario_in = ft.TextField(
        label="Salário Base", 
        prefix=ft.Text("R$ ", color=PALETA["texto"]), 
        border_color=PALETA["primaria"],
        color=PALETA["texto"],
        keyboard_type=ft.KeyboardType.NUMBER
    )

    extra_in = ft.TextField(
        label="Outros Benefícios", 
        prefix=ft.Text("R$ ", color=PALETA["texto"]), 
        border_color=PALETA["primaria"],
        color=PALETA["texto"],
        value="0",
        keyboard_type=ft.KeyboardType.NUMBER
    )

    # LISTA DINÂMICA DE PRODUTOS (Adaptado da lógica de contagem)
    vendas_lista = []
    for i in range(1, 4):
        qtd = ft.TextField(label="Qtd", value="1", width=70, color=PALETA["texto"])
        prod = ft.TextField(label=f"Produto {i}", expand=True, color=PALETA["texto"], hint_text="Nome do item")
        val_un = ft.TextField(label="Valor Un.", prefix=ft.Text("R$ "), width=110, color=PALETA["texto"])
        perc = ft.Slider(min=0, max=20, divisions=20, label="Comissão: {value}%", value=3)
        
        vendas_lista.append({"qtd": qtd, "prod": prod, "val": val_un, "perc": perc})

    res_container = ft.Container(
        visible=False, 
        padding=25, 
        border_radius=15, 
        bgcolor=PALETA["card_fundo"], 
        border=ft.border.all(1, ft.Colors.PINK_100)
    )
    res_txt = ft.Text("", color=PALETA["texto"], size=14, font_family="monospace")
    ia_txt = ft.Text("", color=PALETA["ia_cor"], italic=True, weight="bold")

    def processar(e):
        try:
            base = float(salario_in.value.replace(",", ".") or 0)
            extras = float(extra_in.value.replace(",", ".") or 0)
            
            comissao_total = 0
            detalhe_itens = ""
            
            # Lógica de processamento dos itens de venda
            for item in vendas_lista:
                q = float(item["qtd"].value or 0)
                v = float(item["val"].value.replace(",", ".") or 0)
                p = item["perc"].value / 100
                if q > 0 and v > 0:
                    subtotal = (q * v) * p
                    comissao_total += subtotal
                    nome = item["prod"].value or "Produto s/ nome"
                    detalhe_itens += f"   • {int(q)}x {nome}: R$ {subtotal:.2f}\n"

            bruto = base + extras + comissao_total
            
            if modo_calc.value == "rescisao":
                bruto += base  # Simulação simples de aviso prévio indenizado

            inss, irrf = calcular_impostos(bruto)
            liquido = bruto - inss - irrf

            res_txt.value = (
                f"📊 EXTRATO SALARIAL 2026 - {modo_calc.value.upper()}\n"
                f"{'='*40}\n"
                f"(+) Salário Base:    R$ {base:>10.2f}\n"
                f"(+) Comissões:       R$ {comissao_total:>10.2f}\n"
                f"(+) Outros Extras:   R$ {extras:>10.2f}\n"
                f"{detalhe_itens}"
                f"{'-'*40}\n"
                f"(-) INSS (2026):     R$ {inss:>10.2f}\n"
                f"(-) IRRF (2026):     R$ {irrf:>10.2f}\n"
                f"{'='*40}\n"
                f"💰 LÍQUIDO A RECEBER: R$ {liquido:>9.2f}\n"
            )

            ia_txt.value = "🤖 IA PINK: Cálculos realizados com as tabelas de 2026. Revisado!"
            res_container.visible = True
            page.update()
            
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Erro: Insira apenas números válidos nos valores."))
            page.snack_bar.open = True
            page.update()

    # --- CONSTRUÇÃO DO LAYOUT ---
    header = ft.Column([
        ft.Text("PINK Calculo Salarial", size=32, weight="bold", color=PALETA["primaria"]),
        ft.Text("By Jean Castro | v2.0-2026", size=14, color=ft.Colors.GREY_700),
    ], spacing=0)

    btn_calcular = ft.ElevatedButton(
        "GERAR RELATÓRIO COMPLETO", 
        on_click=processar, 
        bgcolor=PALETA["primaria"], 
        color="white", 
        height=50, 
        width=float("inf"),
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    page.add(
        header,
        ft.Divider(height=20, color="transparent"),
        ft.Text("Configurações de Salário", weight="bold", size=18),
        modo_calc,
        salario_in,
        extra_in,
        ft.ExpansionTile(
            title=ft.Text("🛒 Lançamento de Vendas e Comissões", color=PALETA["texto"], weight="bold"),
            subtitle=ft.Text("Clique para expandir e inserir produtos"),
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
        ft.Divider(height=10, color="transparent"),
        btn_calcular,
        res_container
    )
    res_container.content = ft.Column([res_txt, ft.Divider(), ia_txt])

if __name__ == "__main__":
    # Configuração para rodar no servidor ou localmente
    port = int(os.getenv("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
