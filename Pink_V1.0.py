import flet as ft
import os
from datetime import datetime

# 1. CONSTANTES E ESTILOS
PALETA = {
    "primaria": ft.Colors.PINK_400,
    "secundaria": ft.Colors.PINK_50,
    "ia": ft.Colors.DEEP_PURPLE_400,
    "fundo_res": ft.Colors.GREY_50
}

# 2. LÓGICA DE CÁLCULO
def calcular_folha_completa(salario, comissao, outros_ben, tipo_calculo, ferias_vencidas):
    total_bruto = salario + comissao + sum(outros_ben)
    
    # INSS 2026 (Simulado)
    if total_bruto <= 1512: inss = total_bruto * 0.075
    elif total_bruto <= 2800: inss = total_bruto * 0.09
    elif total_bruto <= 4000: inss = total_bruto * 0.12
    else: inss = total_bruto * 0.14
    
    # IRRF (Simulado)
    base_irrf = total_bruto - inss
    irrf = 0 if base_irrf <= 2259 else (base_irrf * 0.075) - 169
    
    liquido = total_bruto - inss - irrf
    
    # Adicional de Férias (1/3)
    valor_ferias = (salario + (salario/3)) if tipo_calculo == "Férias" else 0
    if ferias_vencidas and tipo_calculo == "Férias":
        valor_ferias *= 2 # Dobra se vencida
        
    return inss, irrf, total_bruto, liquido, valor_ferias

# 3. INTERFACE PRINCIPAL
def main(page: ft.Page):
    page.title = "Pink V2.5 Pro | Gestão RH"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.window_width = 500

    # --- CAMPOS DE ENTRADA ---
    tipo_op = ft.Dropdown(
        label="O que deseja calcular?",
        options=[
            ft.dropdown.Option("Mensal"),
            ft.dropdown.Option("Rescisão"),
            ft.dropdown.Option("Férias")
        ], value="Mensal"
    )

    salario_in = ft.TextField(label="Salário Base", prefix=ft.Text("R$ "), border_color="pink")
    
    # Área de Produto/Comissão
    prod_nome = ft.TextField(label="Produto Vendido", hint_text="Ex: Pendrive")
    prod_val = ft.TextField(label="Valor Total Vendido", prefix=ft.Text("R$ "), value="0")
    comissao_perc = ft.Slider(min=0, max=100, divisions=100, label="Comissão: {value}%", value=3)

    # Benefícios (Até 5 opcionais)
    ben_inputs = [ft.TextField(label=f"Benefício/Extra {i+1}", prefix=ft.Text("R$ "), value="0") for i in range(5)]
    check_ferias = ft.Checkbox(label="Possui férias vencidas?", value=False)

    # --- RESULTADOS ---
    res_txt = ft.Text("", color="black", size=14)
    container_res = ft.Container(content=res_txt, visible=False, padding=15, border_radius=10, bgcolor=PALETA["fundo_res"])

    # --- AURORA IA ---
    chat_ia = ft.Column(height=250, scroll=ft.ScrollMode.ALWAYS)
    pergunta_ia = ft.TextField(hint_text="Dúvidas sobre CLT ou descontos?", expand=True)

    def responder_aurora(e):
        if not pergunta_ia.value: return
        p = pergunta_ia.value.lower()
        res = "Aurora: "
        
        if any(x in p for x in ["oi", "tudo bem", "como vai"]):
            res += "Olá! Tudo ótimo por aqui. Como posso ajudar seu RH hoje?"
        elif "desconto" in p or "obrigatório" in p:
            res += "Sim, descontos de INSS, IRRF e faltas são previstos pela CLT e obrigatórios."
        elif "clt" in p or "lei" in p:
            res += "Sim, todos os cálculos deste sistema seguem as normas da CLT brasileira vigente."
        elif "errado" in p or "manual" in p:
            res += ("MANUAL DE DIVERGÊNCIA:\n1. Peça seu holerite detalhado.\n2. Confira a tabela do INSS/IRRF do ano atual.\n"
                    "3. Verifique se houve faltas ou atrasos.\n4. Caso persista, procure o RH ou seu sindicato.")
        else:
            res += "Como sua assistente, recomendo verificar se todos os adicionais e comissões foram lançados corretamente."

        chat_ia.controls.append(ft.Text(f"Você: {pergunta_ia.value}", italic=True))
        chat_ia.controls.append(ft.Text(res, color=PALETA["ia"], weight="bold"))
        pergunta_ia.value = ""
        page.update()

    def calcular(e):
        try:
            s_base = float(salario_in.value)
            v_vendas = float(prod_val.value)
            perc = comissao_perc.value / 100
            comis_total = v_vendas * perc
            
            outros = [float(b.value) for b in ben_inputs if b.value]
            
            inss, irrf, bruto, liquido, ferias = calcular_folha_completa(
                s_base, comis_total, outros, tipo_op.value, check_ferias.value
            )

            res_txt.value = (
                f"📊 RESUMO {tipo_op.value.upper()}\n"
                f"💰 Bruto Total: R$ {bruto:.2f}\n"
                f"📈 Comissão ({comissao_perc.value}%): R$ {comis_total:.2f}\n"
                f"📉 INSS: R$ {inss:.2f} | IRRF: R$ {irrf:.2f}\n"
            )
            
            if tipo_op.value == "Férias":
                res_txt.value += f"🏖️ Total a receber nas Férias: R$ {ferias:.2f}"
            else:
                res_txt.value += f"💵 LÍQUIDO FINAL: R$ {liquido:.2f}"

            container_res.visible = True
            page.update()
        except:
            res_txt.value = "⚠️ Erro: Insira valores numéricos válidos."
            container_res.visible = True
            page.update()

    # --- MONTAGEM DA PÁGINA ---
    page.add(
        ft.Text("PINK V2.5 - Gestão de Vendas & RH - By Jean Castro", size=24, weight="bold", color="pink"),
        tipo_op,
        salario_in,
        ft.ExpansionTile(
            title=ft.Text("Vendas e Comissão"),
            controls=[prod_nome, prod_val, comissao_perc]
        ),
        ft.ExpansionTile(
            title=ft.Text("Benefícios e Extras (Até 5)"),
            controls=ben_inputs
        ),
        check_ferias,
        ft.ElevatedButton("Gerar Simulação", on_click=calcular, bgcolor="pink", color="white"),
        container_res,
        ft.Divider(),
        ft.Text("Aurora IA - Consultoria CLT", size=18, weight="bold", color=PALETA["ia"]),
        ft.Container(content=chat_ia, bgcolor="#f0f0f7", padding=10, border_radius=10),
        ft.Row([pergunta_ia, ft.IconButton(ft.Icons.SEND, on_click=responder_aurora)])
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
