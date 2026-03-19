import flet as ft
import os

# 1. CONSTANTES E TABELAS (Valores de Referência 2026)
PALETA_CORES = {
    "primaria": ft.Colors.PINK_400,
    "secundaria": ft.Colors.PINK_50,
    "texto": ft.Colors.PINK_900,
    "ia": ft.Colors.DEEP_PURPLE_400
}

def calcular_clt(salario_bruto, comissao):
    total_proventos = salario_bruto + comissao
    
    # Cálculo Simplificado INSS (Tabela Progressiva)
    if total_proventos <= 1500: inss = total_proventos * 0.075
    elif total_proventos <= 2800: inss = total_proventos * 0.09
    elif total_proventos <= 4000: inss = total_proventos * 0.12
    else: inss = total_proventos * 0.14 # Teto simplificado
    
    # Cálculo Simplificado IRRF
    base_irrf = total_proventos - inss
    if base_irrf <= 2250: irrf = 0
    else: irrf = base_irrf * 0.075 # Alíquota inicial
    
    salario_liquido = total_proventos - inss - irrf
    return inss, irrf, salario_liquido

# 2. INTERFACE
def main(page: ft.Page):
    page.title = "Pink V2.0 | RH & Aurora IA"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.window_width = 450

    # --- CAMPOS DE ENTRADA ---
    salario_in = ft.TextField(label="Salário Base", prefix=ft.Text("R$ "), border_color="pink")
    vendas_in = ft.TextField(label="Total Vendas", prefix=ft.Text("R$ "), value="0")
    faltas_in = ft.TextField(label="Faltas no Mês", value="0")

    # --- EXIBIÇÃO DE RESULTADOS ---
    res_detalhe = ft.Text("", color="black")
    container_res = ft.Container(content=res_detalhe, visible=False, padding=10, border_radius=10)

    # --- CHAT COM A AURORA ---
    chat_ia = ft.Column(height=200, scroll=ft.ScrollMode.ALWAYS)
    pergunta_ia = ft.TextField(hint_text="Pergunte à Aurora sobre seus direitos...", expand=True)

    def responder_aurora(e):
        if not pergunta_ia.value: return
        
        pergunta = pergunta_ia.value.lower()
        # Lógica de resposta "Simulada" da Aurora
        resposta = "Olá! Eu sou a Aurora. "
        if "desconto" in pergunta:
            resposta += "Os descontos de INSS e IRRF são obrigatórios por lei na CLT. Verifique se as alíquotas batem com sua faixa salarial."
        elif "escala" in pergunta or "5x2" in pergunta:
            resposta += "Na escala 5x2, você trabalha 5 dias e folga 2. O DSR já está incluso no seu salário mensal fixo."
        else:
            resposta += "Como sua assistente de RH, recomendo sempre conferir sua convenção coletiva para detalhes específicos."
        
        chat_ia.controls.append(ft.Text(f"Você: {pergunta_ia.value}", italic=True))
        chat_ia.controls.append(ft.Text(f"Aurora: {resposta}", color=PALETA_CORES["ia"], weight="bold"))
        pergunta_ia.value = ""
        page.update()

    def processar_calculo(e):
        try:
            s_base = float(salario_in.value)
            comissao = float(vendas_in.value) * 0.03
            inss, irrf, liquido = calcular_clt(s_base, comissao)
            
            res_detalhe.value = (
                f"✅ Escala 5x2: DSR Incluso\n"
                f"💰 Comissão: R$ {comissao:.2f}\n"
                f"📉 INSS: R$ {inss:.2f} ({(inss/(s_base+comissao)*100):.1f}%)\n"
                f"📉 IRRF: R$ {irrf:.2f}\n"
                f"💵 LÍQUIDO A RECEBER: R$ {liquido:.2f}"
            )
            container_res.bgcolor = ft.Colors.GREEN_50
            container_res.visible = True
            page.update()
        except:
            res_detalhe.value = "Erro: Preencha os valores corretamente."
            container_res.visible = True
            page.update()

    # --- CONSTRUÇÃO DA PÁGINA ---
    page.add(
        ft.Text("PINK - SISTEMA DE RH - By Jean Castro", size=25, weight="bold", color="pink"),
        ft.Divider(),
        salario_in,
        vendas_in,
        faltas_in,
        ft.ElevatedButton("Calcular Holerite", on_click=processar_calculo, bgcolor="pink", color="white"),
        container_res,
        ft.Divider(),
        ft.Text("Fale com a Aurora (IA)", size=18, weight="bold", color=PALETA_CORES["ia"]),
        ft.Container(content=chat_ia, bgcolor="grey-100", padding=10, border_radius=10),
        ft.Row([pergunta_ia, ft.IconButton(ft.Icons.SEND, on_click=responder_aurora)])
    )

if __name__ == "__main__":
    # Ajuste para o Render (Host 0.0.0.0 e porta do sistema)
    port = int(os.getenv("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
