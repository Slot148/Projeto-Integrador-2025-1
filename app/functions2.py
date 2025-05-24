from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
import os

def gerar_pdf_simples(data, filtros=None, output_path="app/data/relatorios/relatorio.pdf"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Relatório de Atestados")
        
        c.setFont("Helvetica", 10)
        y = height - 80
        if filtros:
            c.drawString(50, y, "Filtros aplicados:")
            y -= 15
            for key, value in filtros.items():
                if value:  # Só mostra filtros com valores
                    c.drawString(60, y, f"{key.capitalize()}: {value}")
                    y -= 15
            y -= 10

        total_atestados = len(data)
        aprovados = sum(1 for item in data if item.get('estado', '').lower() == 'aprovado')
        reprovados = sum(1 for item in data if item.get('estado', '').lower() == 'reprovado')
        pendentes = sum(1 for item in data if item.get('estado', '').lower() not in ['aprovado', 'reprovado'])
        
        alunos_unicos = len({item.get('ra', '') for item in data if item.get('ra')})
        
        c.drawString(50, y, f"Total de atestados: {total_atestados}")
        y -= 15
        c.drawString(50, y, f"Atestados aprovados: {aprovados} ({aprovados/total_atestados*100:.1f}%)" if total_atestados else "Atestados aprovados: 0")
        y -= 15
        c.drawString(50, y, f"Atestados reprovados: {reprovados} ({reprovados/total_atestados*100:.1f}%)" if total_atestados else "Atestados reprovados: 0")
        y -= 15
        c.drawString(50, y, f"Atestados pendentes: {pendentes} ({pendentes/total_atestados*100:.1f}%)" if total_atestados else "Atestados pendentes: 0")
        y -= 30

        headers = ["RA", "Nome", "Data Envio", "Início", "Fim", "Status"]
        col_widths = [60, 100, 70, 60, 60, 60]

        table_data = [headers]
        for item in data:
            table_data.append([
                item.get("ra", ""),
                item.get("nome_aluno", ""),
                item.get("data_envio", ""),
                item.get("inicio_periodo", ""),
                item.get("fim_periodo", ""),
                item.get("estado", "")
            ])

        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        table.wrapOn(c, width - 100, height)
        table.drawOn(c, 50, y - len(data)*15 - 30)

        c.showPage()
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Estatísticas Detalhadas")

        from collections import defaultdict
        atestados_por_aluno = defaultdict(int)
        for item in data:
            if item.get('ra'):
                atestados_por_aluno[item['ra']] += 1
        
        if atestados_por_aluno:
            top_alunos = sorted(atestados_por_aluno.items(), key=lambda x: x[1], reverse=True)[:5]
            
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, height - 80, "Alunos com mais atestados:")
            c.setFont("Helvetica", 10)
            y = height - 100
            for ra, count in top_alunos:
                aluno = next((item for item in data if item.get('ra') == ra), None)
                if aluno:
                    c.drawString(60, y, f"{aluno.get('nome_aluno', 'N/A')} (RA: {ra}): {count} atestados")
                    y -= 15

        c.save()
        return True
    except Exception as e:
        print(f"Erro ao gerar PDF: {str(e)}")
        return False