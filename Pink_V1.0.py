import flet as ft
import os
from datetime import datetime

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
        if valor <= 1518.00:
            inss = valor * 0.075
        elif valor <= 2793.88:
            inss = (valor * 0.09) - 22.77
        elif valor <= 4190.83:
            inss = (valor * 0.12) - 106.56
        elif valor <= 8157.41:
            inss = (valor * 0.14) - 190.38
        else:
            inss = 951.66 
        
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

    # --- NOVOS COMPONENTES PARA RESCISÃO ---
    data_entrada = ft.TextField(label="Data de Entrada", hint_text="DD/MM/AAAA", width=200, color=PALETA["texto"])
    data_saida = ft.TextField(label="Data de Saída", hint_text="DD/MM/AAAA", width=200, color=PALETA["texto"])
    motivo_rescisao = ft.Dropdown(
        label="Motivo da Saída",
        options=[
            ft.dropdown.Option("sem_justa", "Sem Justa Causa"),
            ft.dropdown.Option("com_justa", "Com Justa Causa"),
            ft.dropdown.Option("pedido", "Pedido de Demissão"),
        ],
        width=410,
        color=PALETA["texto"]
    )

    # --- COMPONENTES ORIGINAIS ---
    modo_calc = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="mensal", label="Folha Mensal", label_style=ft.TextStyle(color=PALETA["texto"])),
            ft.Radio(value="rescisao", label="Rescisão Completa", label_style=ft.TextStyle(color=PALETA["texto"]))
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
            for item in vendas_lista:
                q = float(item["qtd"].value or 0)
                v = float(item["val"].value.replace(",", ".") or 0)
                p = item["perc"].value / 100
                if q > 0 and v > 0:
                    subtotal = (q * v) * p
                    comissao_total += subtotal
                    nome = item["prod"].value or "Produto s/ nome"
                    detalhe_itens += f"    • {int(q)}x {nome}: R$ {subtotal:.2f}\n"

            bruto_mensal = base + extras + comissao_total
            total_rescisao_adicional = 0
            detalhe_rescisao = ""

            if modo_calc.value == "rescisao":
                # Lógica de Datas
                d1 = datetime.strptime(data_entrada.value, "%d/%m/%Y")
                d2 = datetime.strptime(data_saida.value, "%d/%m/%Y")
                
                # 1. Saldo de Salário
                dias_trabalhados = d2.day
                saldo_salario = (base / 30) * dias_trabalhados
                
                # 2. 13º Proporcional (Meses com mais de 14 dias trabalhados)
                meses_13 = d2.month if d2.day >= 15 else d2.month - 1
                decimo_terceiro = (base / 12) * meses_13
                
                # 3. Férias Proporcionais + 1/3
                meses_ferias = ((d2 - d1).days // 30) % 12
                valor_ferias = (base / 12) * meses_ferias
                um_terco = valor_ferias / 3
                
                total_rescisao_adicional = saldo_salario + decimo_terceiro + valor_ferias + um_terco
                
                # Ajuste por motivo
                if motivo_rescisao.value == "sem_justa":
                    aviso_previo = base # Simulação simplificada de 1 mês
                    total_rescisao_adicional += aviso_previo
                    detalhe_rescisao = f"(+) Aviso Prévio:    R$ {aviso_previo:>10.2f}\n"
                elif motivo_rescisao.value == "com_justa":
                    total_rescisao_adicional = saldo_salario # Perde quase tudo
                    decimo_terceiro = valor_ferias = um_terco = 0
                
                detalhe_rescisao += (
                    f"(+) Saldo Salário:   R$ {saldo_salario:>10.2f}\n"
                    f"(+) 13º Proporc.:    R$ {decimo_terceiro:>10.2f}\n"
                    f"(+) Férias Proporc.: R$ {valor_ferias:>10.2f}\n"
                    f"(+) 1/3 Férias:      R$ {um_terco:>10.2f}\n"
                )
                bruto_final = total_rescisao_adicional + extras + comissao_total
            else:
                bruto_final = bruto_mensal

            inss, irrf = calcular_impostos(bruto_final)
            liquido = bruto_final - inss - irrf

            res_txt.value = (
                f"📊 EXTRATO PINK 2026 - {modo_calc.value.upper()}\n"
                f"{'='*40}\n"
                f"{detalhe_rescisao if modo_calc.value == 'rescisao' else f'(+) Salário Base:    R$ {base:>10.2f}'}\n"
                f"(+) Comissões:       R$ {comissao_total:>10.2f}\n"
                f"(+) Outros Extras:    R$ {extras:>10.2f}\n"
                f"{detalhe_itens}"
                f"{'-'*40}\n"
                f"(-) INSS (2026):     R$ {inss:>10.2f}\n"
                f"(-) IRRF (2026):     R$ {irrf:>10.2f}\n"
                f"{'='*40}\n"
                f"💰 TOTAL LÍQUIDO:    R$ {liquido:>9.2f}\n"
            )

            ia_txt.value = f"🤖 IA PINK: Rescisão calculada ({motivo_rescisao.value}). Revisado!"
            res_container.visible = True
            page.update()
            
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: Verifique os campos e datas (DD/MM/AAAA)."))
            page.snack_bar.open = True
            page.update()

    # --- LAYOUT ATUALIZADO ---
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
        ft.Text("Configurações de Cálculo", weight="bold", size=18),
        modo_calc,
        salario_in,
        extra_in,
        ft.ExpansionTile(
            title=ft.Text("📅 Detalhes da Rescisão (Obrigatório para Rescisão)", color=PALETA["texto"], weight="bold"),
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Row([data_entrada, data_saida]),
                        motivo_rescisao,
                        ft.Text("Obs: O saldo de salário considera o dia da saída.", size=12, italic=True)
                    ]), padding=15
                )
            ]
        ),
        ft.ExpansionTile(
            title=ft.Text("🛒 Lançamento de Vendas e Comissões", color=PALETA["texto"], weight="bold"),
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
    port = int(os.getenv("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
