#!/usr/bin/env python3
"""Script para gerar ícones PWA básicos com a letra E"""
from PIL import Image, ImageDraw, ImageFont
import os

def criar_icone(tamanho, caminho_saida):
    # Criar imagem com fundo gradiente simulado (azul esverdeado)
    img = Image.new('RGB', (tamanho, tamanho), color='#020617')
    draw = ImageDraw.Draw(img)
    
    # Desenhar um círculo no fundo (cor emerald-600)
    margin = int(tamanho * 0.05)
    draw.ellipse([margin, margin, tamanho-margin, tamanho-margin], fill='#059669')
    
    # Adicionar a letra "E" centralizada
    try:
        # Tentar usar uma fonte do sistema
        fonte_tamanho = int(tamanho * 0.5)
        fonte = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", fonte_tamanho)
    except:
        # Fallback para fonte padrão
        fonte = ImageFont.load_default()
    
    letra = "E"
    bbox = draw.textbbox((0, 0), letra, font=fonte)
    texto_largura = bbox[2] - bbox[0]
    texto_altura = bbox[3] - bbox[1]
    
    x = (tamanho - texto_largura) // 2
    y = (tamanho - texto_altura) // 2 - int(tamanho * 0.05)
    
    draw.text((x, y), letra, fill='white', font=fonte)
    
    # Salvar
    img.save(caminho_saida, 'PNG')
    print(f"Ícone criado: {caminho_saida}")

if __name__ == "__main__":
    public_dir = "/home/IEC/ilailsonrocha/Imagens/EmprestimofuncionalTela/emprestimo/frontend/public"
    
    # Criar ícones
    criar_icone(192, os.path.join(public_dir, "icon-192x192.png"))
    criar_icone(512, os.path.join(public_dir, "icon-512x512.png"))
    
    print("Ícones PWA gerados com sucesso!")
