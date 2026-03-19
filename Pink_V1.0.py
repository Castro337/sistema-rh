import flet as ft
import os

# 1. ESTILOS (Voltando para o Rosa Vibrante)
PALETA = {
    "primaria": ft.Colors.PINK_400,
    "fundo": ft.Colors.WHITE,
    "card_bg": ft.Colors.PINK_50,
    "texto": ft.Colors.PINK_900
}

def main(page: ft.Page):
    page.title = "Pink V3.1 | Gestão Completa"
    page.bgcolor = PALETA["fundo"]
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 30
    page.spacing = 20

    # --- FUNÇÃO AUXILIAR PARA CRIAR CARDS ---
    def criar_card(titulo, controles, cor_borda=PALETA["primaria"]):
        return ft.Container(
            content=ft.Column([
                ft.Text(titulo, weight="bold", size=16, color=PALETA["texto"]),
                *controles
            ], spacing=15),
            padding=20,
            border=ft.border.all(1, cor_borda),
            border_radius=15,
            bgcolor=PALETA["card_bg"]
        )

    # --- ENTRADAS PRINCIPAIS ---
    salario_in = ft.TextField(label="Salário Base", prefix=ft.Text("R$ "), border_color=PALETA["primaria"], border_radius=10)
    
    # 5 PRODUTOS: Valor + % Individual
    vendas_inputs = []
    for i in range(5):
        v = ft.TextField(label=f"Valor Produto {i+1}", prefix=ft.Text("R$ "), value="0")
        p = ft.Slider(min=0, max=100, divisions=100, label="Comissão: {value}%", value=3)
        vendas_inputs.append({"valor": v, "perc": p})

    # 5 BENEFÍCIOS: Valor + % Individual
    ben_inputs = []
    for i in range(5):
        v = ft.TextField(label=f"Valor Base Benefício {i+1}", prefix=ft.Text("R$ "), value="0")
        p = ft.Slider(min=0, max=100, divisions=100, label="Pagar: {value}%", value=100)
        ben_inputs.append({"valor": v, "perc": p})

    # --- OPÇÕES DE CÁLCULO ---
    tipo_calc = ft.Dropdown(
        label="Tipo de Cálculo",
        options=[ft.dropdown.Option("Mensal"), ft.dropdown.Option("Férias"), ft.dropdown.Option("Rescisão")],
        value="Mensal"
    )
    
    ferias_venc_radio = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="sim", label="Sim"),
            ft.Radio(value="nao", label="Não")
        ]), value="nao"
    )

    meses_rescisao = ft.TextField(label="Meses Trabalhados", value="0", visible=False)

    def mudar_tipo(e):
        meses_rescisao.visible = (tipo_calc.value == "Rescisão")
        page.update()
    
    tipo_calc.on_change = mudar_tipo

    # --- RESULTADO ---
    res_txt = ft.Text("", weight="bold", size=16)
    container_res = ft.Container(content=res_txt, visible=False, padding=20, bgcolor=ft.Colors.GREEN_50, border_radius=15)

    def calcular(e):
        try:
            sal = float(salario_in.value or 0)
            
            # Cálculo Vendas Individuais
            total_comissao = sum([float(x["valor"].value or 0) * (x["perc"].value / 100) for x in vendas_inputs])
            
            # Cálculo Benefícios Individuais
            total_ben = sum([float(x["valor"].value or 0) * (x["perc"].value / 100) for x in ben_inputs])
            
            bruto = sal + total_comissao + total_ben
            
            # Impostos (Simulados)
            inss = bruto * 0.11 if bruto < 4000 else bruto * 0.14
            irrf = (bruto - inss) * 0.075 if bruto > 2250 else 0
            liquido = bruto - inss - irrf

            msg = f"💰 Bruto: R$ {bruto:.2f}\n📈 Comissões: R$ {total_comissao:.2f}\n📉 Descontos: R$ {inss+irrf:.2f}\n"
            
            if tipo_calc.value == "Rescisão":
                meses = int(meses_rescisao.value or 0)
                decimo = (sal / 12) * meses
                ferias_prop = ((sal + (sal/3)) / 12) * meses
                total_rec = liquido + decimo + ferias_prop
                msg += f"📅 Décimo Proporcional: R$ {decimo:.2f}\n🏖️ Férias Proporcionais: R$ {ferias_prop:.2f}\n🔥 TOTAL RESCISÃO: R$ {total_rec:.2f}"
            else:
                msg += f"💵 LÍQUIDO FINAL: R$ {liquido:.2f}"

            res_txt.value = msg
            container_res.visible = True
            page.update()
        except Exception as ex:
            res_txt.value = f"Erro: Verifique os números preenchidos."
            container_res.visible = True
            page.update()

    # --- MONTAGEM FINAL ---
    page.add(
        ft.Text("PINK SYSTEM V3.1", size=30, weight="bold", color=PALETA["primaria"]),
        
        criar_card("💼 Salário Base", [salario_in]),
        
        ft.ExpansionTile(
            title=ft.Text("📦 Vendas Individuais (Valor e %)", weight="bold"),
            controls=[ft.Container(content=ft.Column([ft.Column([x["valor"], x["perc"], ft.Divider()]) for x in vendas_inputs]), padding=10)]
        ),
        
        ft.ExpansionTile(
            title=ft.Text("🎁 Benefícios Individuais (Valor e %)", weight="bold"),
            controls=[ft.Column([ft.Container(content=ft.Column([x["valor"], x["perc"]]), padding=10) for x in ben_inputs])]
        ),
        
        criar_card("⚙️ Configurações e Rescisão", [
            tipo_calc,
            ft.Text("Possui férias vencidas?"),
            ferias_venc_radio,
            meses_rescisao
        ]),
        
        ft.ElevatedButton("CALCULAR TUDO", on_click=calcular, bgcolor=PALETA["primaria"], color="white", height=50),
        container_res
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
