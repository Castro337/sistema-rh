import flet as ft
import os

# PALETA DE ALTO CONTRASTE
PALETA = {
    "primaria": ft.Colors.PINK_600,
    "fundo_tela": ft.Colors.WHITE,
    "fundo_card": "#FFF0F5",
    "texto_preto": ft.Colors.BLACK,
    "texto_destaque": ft.Colors.PINK_900
}

def main(page: ft.Page):
    page.title = "PINK Calculo Salarial | By Jean Castro"
    page.bgcolor = PALETA["fundo_tela"]
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 20
    page.spacing = 20

    # --- CAMPOS PRINCIPAIS ---
    salario_in = ft.TextField(
        label="Salário Base",
        prefix=ft.Text("R$ ", color=PALETA["texto_preto"]),
        color=PALETA["texto_preto"],
        border_color=PALETA["primaria"],
        border_radius=10,
        label_style=ft.TextStyle(color=PALETA["texto_destaque"], weight="bold")
    )

    # --- ESTRUTURA DE VENDAS (QUANTIDADE + MATERIAL + VALOR) ---
    vendas_lista = []
    
    def criar_linha_venda(index):
        qtd = ft.TextField(label="Qtd", value="1", width=70, color=PALETA["texto_preto"])
        material = ft.TextField(label=f"Material {index}", hint_text="Ex: Pendrive", expand=True, color=PALETA["texto_preto"])
        valor = ft.TextField(label="Valor Un.", prefix=ft.Text("R$ "), width=120, color=PALETA["texto_preto"])
        porcentagem = ft.Slider(min=0, max=100, divisions=100, label="Comissão: {value}%", thumb_color=PALETA["primaria"])
        
        return {
            "container": ft.Container(
                content=ft.Column([
                    ft.Row([qtd, material, valor], spacing=10),
                    porcentagem,
                    ft.Divider(color=ft.Colors.PINK_100)
                ]),
                padding=10
            ),
            "qtd": qtd, "mat": material, "val": valor, "perc": porcentagem
        }

    for i in range(1, 6):
        vendas_lista.append(criar_linha_venda(i))

    # --- BENEFÍCIOS ---
    ben_in = ft.TextField(label="Total Benefícios/Extras", prefix=ft.Text("R$ "), color=PALETA["texto_preto"], border_color=PALETA["primaria"])

    # --- RESULTADO ---
    res_txt = ft.Text("", color=PALETA["texto_preto"], weight="bold", size=16)
    res_container = ft.Container(content=res_txt, visible=False, padding=20, bgcolor=ft.Colors.AMBER_100, border_radius=15)

    def calcular(e):
        try:
            total_comissao = 0
            detalhes_vendas = ""
            
            for item in vendas_lista:
                q = float(item["qtd"].value or 0)
                v = float(item["val"].value or 0)
                p = item["perc"].value / 100
                
                subtotal = (q * v) * p
                total_comissao += subtotal
                
                if q > 0 and v > 0:
                    detalhes_vendas += f"• {item['mat'].value}: {q:.0f}x R$ {v:.2f} (Comissão: R$ {subtotal:.2f})\n"

            sal = float(salario_in.value or 0)
            extra = float(ben_in.value or 0)
            bruto = sal + total_comissao + extra
            
            res_txt.value = (
                f"📊 RESUMO FINAL\n\n"
                f"{detalhes_vendas}\n"
                f"💰 Salário Base: R$ {sal:.2f}\n"
                f"📈 Total Comissões: R$ {total_comissao:.2f}\n"
                f"🎁 Extras: R$ {extra:.2f}\n"
                f"🔥 TOTAL BRUTO: R$ {bruto:.2f}"
            )
            res_container.visible = True
            page.update()
        except:
            res_txt.value = "⚠️ Erro: Preencha os valores corretamente (apenas números)."
            res_container.visible = True
            page.update()

    # --- LAYOUT ---
    page.add(
        ft.Row([ft.Icon(ft.Icons.SETTINGS_SUGGEST, color=PALETA["primaria"]), 
                ft.Text("SISTEMA PINK V3.3", size=24, weight="bold", color=PALETA["texto_destaque"])]),
        
        ft.Text("Configurações Base", weight="bold", color=PALETA["texto_destaque"]),
        salario_in,
        ben_in,

        ft.ExpansionTile(
            title=ft.Text("📦 DETALHAMENTO DE VENDAS", weight="bold", color=PALETA["texto_destaque"]),
            subtitle=ft.Text("Quantidade, Material e Valor Unitário", size=12),
            controls=[item["container"] for item in vendas_lista]
        ),

        ft.ElevatedButton(
            "GERAR CÁLCULO DETALHADO",
            on_click=calcular,
            bgcolor=PALETA["primaria"],
            color=ft.Colors.WHITE,
            height=50,
            width=float("inf")
        ),
        
        res_container
    )

if __name__ == "__main__":
    # Suporte para o Render.com
    port = int(os.getenv("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port)
