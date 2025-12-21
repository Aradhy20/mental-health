from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
import base64
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        pass
    
    def generate_pdf_report(self, report_data: dict) -> bytes:
        """
        Generate a PDF report with analysis results
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title = Paragraph("Mental Health Analysis Report", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 12))

        # Report generation date
        date_paragraph = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
        story.append(date_paragraph)
        story.append(Spacer(1, 12))

        # User information
        user_info = Paragraph(f"User: {report_data.get('username', 'N/A')} (ID: {report_data.get('user_id', 'N/A')})", styles['Heading2'])
        story.append(user_info)
        story.append(Spacer(1, 12))

        # Text Analysis Section
        text_header = Paragraph("Text Analysis Results", styles['Heading3'])
        story.append(text_header)
        
        text_analysis = report_data.get('text_analysis', {})
        if text_analysis:
            text_data = [
                ['Metric', 'Value'],
                ['Emotion', text_analysis.get('emotion_label', 'N/A')],
                ['Score', f"{text_analysis.get('emotion_score', 0.0):.2f}"],
                ['Confidence', f"{text_analysis.get('confidence', 0.0):.2f}"]
            ]
            
            text_table = Table(text_data)
            text_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(text_table)
        else:
            story.append(Paragraph("No text analysis data available", styles['Normal']))
        story.append(Spacer(1, 12))

        # Voice Analysis Section
        voice_header = Paragraph("Voice Analysis Results", styles['Heading3'])
        story.append(voice_header)
        
        voice_analysis = report_data.get('voice_analysis', {})
        if voice_analysis:
            voice_data = [
                ['Metric', 'Value'],
                ['Stress Level', voice_analysis.get('voice_label', 'N/A')],
                ['Score', f"{voice_analysis.get('voice_score', 0.0):.2f}"],
                ['Confidence', f"{voice_analysis.get('confidence', 0.0):.2f}"]
            ]
            
            voice_table = Table(voice_data)
            voice_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(voice_table)
        else:
            story.append(Paragraph("No voice analysis data available", styles['Normal']))
        story.append(Spacer(1, 12))

        # Face Analysis Section
        face_header = Paragraph("Face Analysis Results", styles['Heading3'])
        story.append(face_header)
        
        face_analysis = report_data.get('face_analysis', {})
        if face_analysis:
            face_data = [
                ['Metric', 'Value'],
                ['Emotion', face_analysis.get('emotion_label', 'N/A')],
                ['Score', f"{face_analysis.get('face_score', 0.0):.2f}"],
                ['Confidence', f"{face_analysis.get('confidence', 0.0):.2f}"]
            ]
            
            face_table = Table(face_data)
            face_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(face_table)
        else:
            story.append(Paragraph("No face analysis data available", styles['Normal']))
        story.append(Spacer(1, 12))

        # Fusion Result Section
        fusion_header = Paragraph("Overall Assessment", styles['Heading3'])
        story.append(fusion_header)
        
        fusion_result = report_data.get('fusion_result', {})
        if fusion_result:
            fusion_data = [
                ['Metric', 'Value'],
                ['Risk Level', fusion_result.get('risk_level', 'N/A').capitalize()],
                ['Final Score', f"{fusion_result.get('final_score', 0.0):.2f}"]
            ]
            
            fusion_table = Table(fusion_data)
            fusion_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(fusion_table)
        else:
            story.append(Paragraph("No fusion result data available", styles['Normal']))
        story.append(Spacer(1, 12))

        # Recommendations
        rec_header = Paragraph("Recommendations", styles['Heading3'])
        story.append(rec_header)
        
        risk_level = fusion_result.get('risk_level', 'low') if fusion_result else 'low'
        if risk_level == 'high':
            recommendation = "Immediate professional consultation recommended. Please contact a mental health specialist as soon as possible."
        elif risk_level == 'medium':
            recommendation = "Consider scheduling a consultation with a mental health professional in the near future."
        else:
            recommendation = "Your mental health appears stable. Continue practicing healthy habits and self-care."
        
        rec_content = Paragraph(recommendation, styles['Normal'])
        story.append(rec_content)

        # Build PDF
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def generate_summary(self, report_data: dict) -> str:
        """
        Generate a text summary of the report
        """
        fusion_result = report_data.get('fusion_result', {})
        if fusion_result:
            risk_level = fusion_result.get('risk_level', 'unknown')
            final_score = fusion_result.get('final_score', 0.0)
            
            summary = f"Overall Risk Level: {risk_level.capitalize()} "
            summary += f"(Score: {final_score:.2f}). "
            
            if risk_level == 'high':
                summary += "Immediate professional consultation recommended."
            elif risk_level == 'medium':
                summary += "Professional consultation suggested."
            else:
                summary += "Mental health appears stable."
        else:
            summary = "No assessment data available."
        
        return summary
    
    def generate_base64_pdf(self, report_data: dict) -> str:
        """
        Generate a base64 encoded PDF report
        """
        pdf_bytes = self.generate_pdf_report(report_data)
        return base64.b64encode(pdf_bytes).decode('utf-8')

# Global instance
generator = ReportGenerator()