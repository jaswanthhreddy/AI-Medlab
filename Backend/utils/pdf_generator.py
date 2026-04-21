"""
PDF Report Generator for Health Reports
Generates professional PDF documents with patient health information,
doctor guidance, and nurse clinical reports.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os

class HealthReportPDF:
    """Generate professional health reports in PDF format"""
    
    def __init__(self, filename):
        """Initialize PDF generator with filename"""
        self.filename = filename
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        if 'CustomTitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1f77b4'),
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            ))
        
        # Section heading style
        if 'SectionHead' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='SectionHead',
                parent=self.styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#2980b9'),
                spaceAfter=12,
                spaceBefore=12,
                fontName='Helvetica-Bold'
            ))
        
        # Body paragraph style
        if 'BodyText' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='BodyText',
                parent=self.styles['Normal'],
                fontSize=11,
                alignment=TA_JUSTIFY,
                spaceAfter=12,
                leading=14
            ))
        
        # Info text style
        if 'InfoText' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='InfoText',
                parent=self.styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor('#555555'),
                spaceAfter=6
            ))
    
    def generate(self, patient_data):
        """
        Generate PDF report
        
        Args:
            patient_data (dict): Dictionary containing:
                - patient_name (str)
                - patient_email (str)  
                - age (int)
                - gender (str)
                - disease (str)
                - symptoms (list)
                - appointment_date (str)
                - doctor_name (str)
                - doctor_guidance (str)
                - nurse_name (str)
                - nurse_report (str)
                - report_date (str)
        
        Returns:
            str: Path to generated PDF file
        """
        
        # Create PDF document
        doc = SimpleDocTemplate(
            self.filename,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Container for PDF elements
        elements = []
        
        # ===== Header Section =====
        elements.append(Paragraph("🏥 HEALTH REPORT", self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Patient Information Table
        patient_info = [
            ['Patient Name:', patient_data.get('patient_name', 'N/A')],
            ['Email:', patient_data.get('patient_email', 'N/A')],
            ['Age:', str(patient_data.get('age', 'N/A'))],
            ['Gender:', patient_data.get('gender', 'N/A')],
            ['Report Date:', patient_data.get('report_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))],
        ]
        
        patient_table = Table(patient_info, colWidths=[2*inch, 4*inch])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
        ]))
        
        elements.append(patient_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # ===== Diagnosis Section =====
        elements.append(Paragraph("📋 DIAGNOSIS", self.styles['SectionHead']))
        
        diagnosis_info = [
            ['Predicted Disease:', patient_data.get('disease', 'N/A')],
            ['Symptoms:', ', '.join(patient_data.get('symptoms', []))],
            ['Appointment Date:', patient_data.get('appointment_date', 'N/A')],
        ]
        
        diagnosis_table = Table(diagnosis_info, colWidths=[2*inch, 4*inch])
        diagnosis_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fff3e0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#fffaf0')])
        ]))
        
        elements.append(diagnosis_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # ===== Doctor's Guidance Section =====
        if patient_data.get('doctor_name') or patient_data.get('doctor_guidance'):
            elements.append(Paragraph("💊 DOCTOR'S HEALTH GUIDANCE", self.styles['SectionHead']))
            
            if patient_data.get('doctor_name'):
                elements.append(Paragraph(
                    f"<b>Doctor:</b> {patient_data.get('doctor_name')}",
                    self.styles['InfoText']
                ))
            
            if patient_data.get('doctor_guidance'):
                guidance_text = patient_data.get('doctor_guidance', '').replace('\n', '<br/>')
                elements.append(Paragraph(guidance_text, self.styles['BodyText']))
            
            elements.append(Spacer(1, 0.2*inch))
        
        # ===== Nurse's Clinical Report Section =====
        if patient_data.get('nurse_name') or patient_data.get('nurse_report'):
            elements.append(Paragraph("👩‍⚕️ NURSE'S CLINICAL REPORT", self.styles['SectionHead']))
            
            if patient_data.get('nurse_name'):
                elements.append(Paragraph(
                    f"<b>Nurse:</b> {patient_data.get('nurse_name')}",
                    self.styles['InfoText']
                ))
            
            if patient_data.get('nurse_report'):
                nurse_text = patient_data.get('nurse_report', '').replace('\n', '<br/>')
                elements.append(Paragraph(nurse_text, self.styles['BodyText']))
            
            elements.append(Spacer(1, 0.2*inch))
        
        # ===== Footer with disclaimer =====
        elements.append(Spacer(1, 0.3*inch))
        disclaimer = """<i>This is an official health report generated by AI MedLab. 
        It contains predictions and recommendations from healthcare professionals. 
        Please consult with your doctor for any medical concerns.</i>"""
        elements.append(Paragraph(disclaimer, self.styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        
        return self.filename
    
    @staticmethod
    def ensure_directory(directory):
        """Ensure directory exists, create if needed"""
        if not os.path.exists(directory):
            os.makedirs(directory)


def generate_health_report_pdf(patient_email, patient_data, output_dir='Backend/reports'):
    """
    Convenience function to generate health report PDF
    
    Args:
        patient_email (str): Patient email address
        patient_data (dict): Patient health data
        output_dir (str): Output directory for PDF
    
    Returns:
        str: Path to generated PDF file
    """
    
    # Ensure output directory exists
    HealthReportPDF.ensure_directory(output_dir)
    
    # Generate filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(output_dir, f'health_report_{patient_email.split("@")[0]}_{timestamp}.pdf')
    
    # Generate PDF
    pdf_generator = HealthReportPDF(filename)
    pdf_generator.generate(patient_data)
    
    return filename
