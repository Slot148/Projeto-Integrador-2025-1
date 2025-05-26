from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
import flask as f
import os
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def gerar_pdf_simples(data, filtros=None, output_path=None):

    if output_path is None:
        output_path = os.path.join(BASE_DIR, "app/data/relatorios/atestados.pdf")
    else:
        output_path = os.path.join(BASE_DIR, output_path)

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
                if value: 
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
        f.flash('Erro ao gerar relatório', 'error')
        print(f"Erro ao gerar PDF: {str(e)}")
        return False    

def gerar_csv_avaliacoes(data, output_path, filtros=None):
    output_path = os.path.join(BASE_DIR, output_path)
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            if filtros:
                writer.writerow(["Relatório de Avaliações - Filtros Aplicados"])
                for key, value in filtros.items():
                    if value: 
                        writer.writerow([f"{key.capitalize()}: {value}"])
                writer.writerow([])

            writer.writerow([
                "RA Avaliado", "Nome Avaliado", "RA Avaliador", "Nome Avaliador",
                "Equipe", "Sprint", "Curso", "Semestre",
                "Produtividade", "Autonomia", "Colaboração", "Entrega de Resultados",
                "Média", "Feedback", "Data de Avaliação"
            ])

            for item in data:
                
                media = (
                    item.get("produtividade", 0) + 
                    item.get("autonomia", 0) + 
                    item.get("colaboracao", 0) + 
                    item.get("entrega_resultados", 0)
                ) / 4

                writer.writerow([
                    item.get("ra_aluno", ""),
                    item.get("nome_aluno", ""),
                    item.get("avaliador_ra", ""),
                    item.get("nome_avaliador", ""),
                    item.get("equipe", ""),
                    item.get("sprint", ""),
                    item.get("curso", ""),
                    item.get("semestre", ""),
                    item.get("autonomia", ""),     
                    item.get("colaboracao", ""),   
                    item.get("entrega_resultados", ""),
                    round(media, 2), 
                    item.get("feedback", ""),
                    item.get("data_avaliacao", "")
                ])
        return True
    except Exception as e:
        f.flash('Erro ao gerar relatório', 'error')
        print(f"Erro ao gerar CSV: {str(e)}")
        return False
    
def gerar_csv_medias(data, output_path, filtros=None):
    output_path = os.path.join(BASE_DIR, output_path)
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            writer.writerow([
                "RA", "Nome", "Curso", "Semestre", "Equipe", "Turno",
                "Sprint", "Média Produtividade", "Média Autonomia", 
                "Média Colaboração", "Média Entrega", "Média Total",
                "Total Avaliações"
            ])

            alunos = {}
            for item in data:
                ra = item.get("ra_aluno")
                if not ra:
                    continue
                    
                sprint = item.get("sprint", "Geral")
                
        
                if ra not in alunos:
                    alunos[ra] = {
                        "nome": item.get("nome_aluno", ""),
                        "curso": item.get("curso", ""),
                        "semestre": item.get("semestre", ""),
                        "equipe": item.get("equipe", ""),
                        "turno": item.get("turno", ""),
                        "sprints": {},
                        "total_avaliacoes": 0,
                        "soma_produtividade": 0,
                        "soma_autonomia": 0,
                        "soma_colaboracao": 0,
                        "soma_entrega": 0,
                        "contador": 0
                    }
                

                if sprint not in alunos[ra]["sprints"]:
                    alunos[ra]["sprints"][sprint] = {
                        "soma_produtividade": 0,
                        "soma_autonomia": 0,
                        "soma_colaboracao": 0,
                        "soma_entrega": 0,
                        "contador": 0
                    }
                

                alunos[ra]["sprints"][sprint]["soma_produtividade"] += item.get("produtividade", 0)
                alunos[ra]["sprints"][sprint]["soma_autonomia"] += item.get("autonomia", 0)
                alunos[ra]["sprints"][sprint]["soma_colaboracao"] += item.get("colaboracao", 0)
                alunos[ra]["sprints"][sprint]["soma_entrega"] += item.get("entrega_resultados", 0)
                alunos[ra]["sprints"][sprint]["contador"] += 1
                
                alunos[ra]["soma_produtividade"] += item.get("produtividade", 0)
                alunos[ra]["soma_autonomia"] += item.get("autonomia", 0)
                alunos[ra]["soma_colaboracao"] += item.get("colaboracao", 0)
                alunos[ra]["soma_entrega"] += item.get("entrega_resultados", 0)
                alunos[ra]["contador"] += 1
                alunos[ra]["total_avaliacoes"] += 1

            for ra, aluno in alunos.items():

                if aluno["contador"] > 0:
                    media_geral_prod = aluno["soma_produtividade"] / aluno["contador"]
                    media_geral_auto = aluno["soma_autonomia"] / aluno["contador"]
                    media_geral_colab = aluno["soma_colaboracao"] / aluno["contador"]
                    media_geral_entrega = aluno["soma_entrega"] / aluno["contador"]
                    media_geral_total = (media_geral_prod + media_geral_auto + 
                                       media_geral_colab + media_geral_entrega) / 4
                    
                    writer.writerow([
                        ra, aluno["nome"], aluno["curso"], aluno["semestre"], 
                        aluno["equipe"], aluno["turno"],
                        "Geral",
                        round(media_geral_prod, 2),
                        round(media_geral_auto, 2),
                        round(media_geral_colab, 2),
                        round(media_geral_entrega, 2),
                        round(media_geral_total, 2),
                        aluno["total_avaliacoes"]
                    ])
                
                for sprint, dados in aluno["sprints"].items():
                    if dados["contador"] > 0:
                        media_prod = dados["soma_produtividade"] / dados["contador"]
                        media_auto = dados["soma_autonomia"] / dados["contador"]
                        media_colab = dados["soma_colaboracao"] / dados["contador"]
                        media_entrega = dados["soma_entrega"] / dados["contador"]
                        media_total = (media_prod + media_auto + media_colab + media_entrega) / 4
                        
                        writer.writerow([
                            ra, aluno["nome"], aluno["curso"], aluno["semestre"], 
                            aluno["equipe"], aluno["turno"],
                            sprint,
                            round(media_prod, 2),
                            round(media_auto, 2),
                            round(media_colab, 2),
                            round(media_entrega, 2),
                            round(media_total, 2),
                            dados["contador"]
                        ])
            
        return True
    except Exception as e:
        f.flash('Erro ao gerar relatório', 'error')
        print(f"Erro ao gerar CSV de médias: {str(e)}")
        return False
    
def gerar_pdf_avaliacoes(data, filtros=None, output_path=None):
    if output_path is None:
        output_path = os.path.join(BASE_DIR, "app/data/relatorios/avaliacoes.pdf")
    else:
        output_path = os.path.join(BASE_DIR, output_path)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Relatório de Avaliações")
        
        c.setFont("Helvetica", 10)
        y = height - 80
        if filtros:
            c.drawString(50, y, "Filtros aplicados:")
            y -= 15
            for key, value in filtros.items():
                if value: 
                    c.drawString(60, y, f"{key.capitalize()}: {value}")
                    y -= 15
            y -= 10

        headers = ["RA Aluno", "Nome", "Equipe", "Sprint", "Produtividade", 
                  "Autonomia", "Colaboração", "Entrega", "Média", "Feedback"]
        col_widths = [60, 100, 60, 40, 50, 50, 50, 50, 40, 100]

        table_data = [headers]
        for item in data:
            media = (item.get("produtividade", 0) + item.get("autonomia", 0) + 
                    item.get("colaboracao", 0) + item.get("entrega_resultados", 0)) / 4
            
            table_data.append([
                item.get("ra_aluno", ""),
                item.get("nome_aluno", ""),
                item.get("equipe", ""),
                item.get("sprint", ""),
                str(item.get("produtividade", "")),
                str(item.get("autonomia", "")),
                str(item.get("colaboracao", "")),
                str(item.get("entrega_resultados", "")),
                f"{media:.1f}",
                item.get("feedback", "")[:30] + "..." if item.get("feedback") else ""
            ])

        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 7)
        ]))

        table.wrapOn(c, width - 60, height)
        table.drawOn(c, 30, y - len(data)*10 - 30)

        c.showPage()
        c.save()
        return True
    except Exception as e:
        f.flash('Erro ao gerar relatório', 'error')
        print(f"Erro ao gerar PDF de avaliações: {str(e)}")
        return False

def gerar_pdf_medias(data, filtros=None, output_path=None):
    if output_path is None:
        output_path = os.path.join(BASE_DIR, "app/data/relatorios/medias.pdf")
    else:
        output_path = os.path.join(BASE_DIR, output_path)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Relatório de Médias")
        
        c.setFont("Helvetica", 10)
        y = height - 80
        if filtros:
            c.drawString(50, y, "Filtros aplicados:")
            y -= 15
            for key, value in filtros.items():
                if value: 
                    c.drawString(60, y, f"{key.capitalize()}: {value}")
                    y -= 15
            y -= 10

        headers = ["RA", "Nome", "Equipe", "Sprint", "Média Prod", "Média Aut", 
                  "Média Colab", "Média Entr", "Média Total", "Qtd Aval"]
        col_widths = [50, 100, 60, 40, 50, 50, 50, 50, 50, 40]

        table_data = [headers]
        for item in data:
            table_data.append([
                item.get("ra", ""),
                item.get("nome", ""),
                item.get("equipe", ""),
                item.get("sprint", "Geral"),
                f"{item.get('media_produtividade', 0):.1f}",
                f"{item.get('media_autonomia', 0):.1f}",
                f"{item.get('media_colaboracao', 0):.1f}",
                f"{item.get('media_entrega', 0):.1f}",
                f"{item.get('media_total', 0):.1f}",
                str(item.get("total_avaliacoes", ""))
            ])

        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 7)
        ]))

        table.wrapOn(c, width - 60, height)
        table.drawOn(c, 30, y - len(data)*10 - 30)

        c.showPage()
        c.save()
        return True
    except Exception as e:
        f.flash('Erro ao gerar relatório', 'error')
        print(f"Erro ao gerar PDF de médias: {str(e)}")
        return False
    
def gerar_csv_atestados(data, filtros=None, output_path=None):
    output_path = os.path.join(BASE_DIR, output_path)
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            if filtros:
                writer.writerow(["Relatório de Atestados - Filtros Aplicados"])
                for key, value in filtros.items():
                    if value: 
                        writer.writerow([f"{key.capitalize()}: {value}"])
                writer.writerow([])

            writer.writerow([
                "RA", "Nome Aluno", "Data Envio", "Início Período", 
                "Fim Período", "Status"
            ])

            for item in data:
                writer.writerow([
                    item.get("ra", ""),
                    item.get("nome_aluno", ""),
                    item.get("data_envio", ""),
                    item.get("inicio_periodo", ""),
                    item.get("fim_periodo", ""),
                    item.get("estado", ""),
                ])
        return True
    except Exception as e:
        f.flash('Erro ao gerar relatório', 'error')
        print(f"Erro ao gerar CSV de atestados: {str(e)}")
        return False