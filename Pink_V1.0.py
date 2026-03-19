import flet as ft
import os

# 1. ESTILOS E PALETA
PALETA = {
    "primaria": ft.Colors.PINK_400,
    "ia": ft.Colors.DEEP_PURPLE_400,
    "fundo_res": ft.Colors.GREY_50
}

# 2. LÓGICA DE CÁLCULO
def calcular_rh_avancado(salario, lista_vendas, perc_comissao, lista_bens, lista_percs_ben, tipo_calc, ferias_venc):
    # Soma de todas as vendas dos 5 produtos
    total_vendas_bruto = sum(lista_vendas)
    comissao_total = total_vendas_bruto * (perc_comissao / 100)
    
    # Soma dos 5 benefícios calculados por suas respectivas porcentagens
    total_beneficios = sum([v * (p / 100) for v, p in zip(lista_bens, lista_percs_ben)])
    
    total_bruto = salario + comissao_total + total_beneficios
    
    # INSS e IRRF (Tabelas 2026 Simuladas)
    inss = total_bruto * 0.14 if total_bruto > 4000 else total_bruto * 0.11
    irrf = (total_bruto - inss) * 0.075 if total_bruto > 2250 else 0
    
    liquido = total_bruto - inss - irrf
    
    # Lógica de Férias
    valor_ferias = (salario + (salario/3)) if tipo_calc == "Férias" else 0
    if ferias_venc and tipo_calc == "Férias": valor_ferias *= 2
        
    return inss, irrf, total_bruto, liquido, valor_ferias, comissao_total

def main(page: ft.Page):
    page.title = "Pink V2.6 | Multi-Produtos & Procentagens"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- CAMPOS DE ENTRADA ---
    salario_in = ft.TextField(label="Salário Base", prefix=ft.Text("R$ "), border_color="pink", value="0")
    comissao_geral_perc = ft.Slider(min=0, max=20, divisions=20, label="Comissão Geral: {value}%", value=3)

    # Listas para 5 Produtos
    vendas_inputs = [ft.TextField(label=f"Valor Venda Produto {i+1}", prefix=ft.Text("R$ "), value="0") for i in range(5)]
    
    # Listas para 5 Benefícios e suas Porcentagens
    ben_inputs = [ft.TextField(label=f"Valor Base Benefício {i+1}", prefix=ft.Text("R$ "), value="0") for i in range(5)]
    ben_percs = [ft.Slider(min=0, max=100, divisions=20, label="Cálculo: {value}%", value=100) for i in range(5)]

    tipo_op = ft.Dropdown(label="Tipo de Cálculo", options=[ft.dropdown.Option("Mensal"), ft.dropdown.Option("Férias")], value="Mensal")
    check_ferias = ft.Checkbox(label="Férias Vencidas?", value=False)

    # --- RESULTADOS E IA ---
    res_txt = ft.Text("", color="black", weight="bold")
    container_res = ft.Container(content=res_txt, visible=False, padding=15, bgcolor=PALETA["fundo_res"], border_radius=10)
    chat_ia = ft.Column(height=200, scroll=ft.ScrollMode.ALWAYS)
    pergunta_ia = ft.TextField(hint_text="Pergunte à Aurora...", expand=True)

    def processar(e):
        try:
            # Converte valores das listas, tratando vazios como 0
            vendas = [float(v.value or 0) for v in vendas_inputs]
            beneficios = [float(b.value or 0) for b in ben_inputs]
            percentuais = [float(p.value) for p in ben_percs]
            
            inss, irrf, bruto, liquido, ferias, com_final = calcular_rh_avancado(
                float(salario_in.value or 0), vendas, comissao_geral_perc.value, 
                beneficios, percentuais, tipo_op.value, check_ferias.value
            )

            res_txt.value = (
                f"✅ RESULTADO FINAL\n"
                f"💰 Total Bruto: R$ {bruto:.2f}\n"
                f"📈 Comissão Total (5 prod): R$ {com_final:.2f}\n"
                f"📉 INSS/IRRF: R$ {inss+irrf:.2f}\n"
                f"💵 LÍQUIDO: R$ {liquido if tipo_op.value == 'Mensal' else ferias:.2f}"
            )
            container_res.visible = True
            page.update()
        except Exception as err:
            res_txt.value = f"Erro nos dados: {err}"
            container_res.visible = True
            page.update()

    def responder_aurora(e):
        p = pergunta_ia.value.lower()
        resp = "Aurora: "
        if "oi" in p: resp += "Olá! Como Vai Você?"
        elif "lei" in p or "clt" in p: resp += "Sim, os cálculos de comissão e benefícios seguem as normas da CLT brasileira."
        elif "errado" in p: resp += "Manual: 1. Verifique as porcentagens; 2. Confira o valor base; 3. Consulte seu RH."
        else: resp += "Estou aqui para tirar dúvidas sobre seus direitos e descontos!"
        
        chat_ia.controls.append(ft.Text(f"Você: {pergunta_ia.value}", italic=True))
        chat_ia.controls.append(ft.Text(resp, color=PALETA["ia"], weight="bold"))
        pergunta_ia.value = ""
        page.update()

    # --- UI LAYOUT ---
   # --- UI LAYOUT ---
    page.add(
        ft.Text("PINK V2.6 - Gestão Avançada", size=24, weight="bold", color="pink"),
        salario_in,
        ft.ExpansionTile(
            title=ft.Text("Vendas (5 Produtos)"), 
            controls=[comissao_geral_perc] + vendas_inputs
        ),
        ft.ExpansionTile(
            title=ft.Text("Benefícios (Valor + %)"), 
            controls=[ft.Column([ben_inputs[i], ben_percs[i]]) for i in range(5)]
        ),
        tipo_op, 
        check_ferias,
        ft.ElevatedButton("Calcular Tudo", on_click=processar, bgcolor="pink", color="white"),
        container_res,
        ft.Divider(),
        ft.Text("Aurora IA", size=18, weight="bold", color=PALETA["ia"]),
        ft.Container(content=chat_ia, bgcolor="#eeeeee", padding=10, border_radius=10),
        ft.Row([pergunta_ia, ft.IconButton(ft.Icons.SEND, on_click=responder_aurora)])
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
