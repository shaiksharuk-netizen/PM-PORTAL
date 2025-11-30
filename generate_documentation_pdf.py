"""
Script to convert TECHNICAL_DOCUMENTATION.md to PDF
Requires: pip install markdown2 pdfkit (or use reportlab)
"""
import os
import sys

def convert_markdown_to_pdf():
    """Convert markdown documentation to PDF"""
    try:
        # Try using markdown2 and pdfkit
        import markdown2
        import pdfkit
        
        # Read markdown file
        with open('TECHNICAL_DOCUMENTATION.md', 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convert markdown to HTML
        html_content = markdown2.markdown(markdown_content, extras=['fenced-code-blocks', 'tables'])
        
        # Add CSS styling
        html_with_style = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    line-height: 1.6;
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #34495e;
                    margin-top: 30px;
                    border-bottom: 2px solid #ecf0f1;
                    padding-bottom: 5px;
                }}
                h3 {{
                    color: #7f8c8d;
                    margin-top: 20px;
                }}
                code {{
                    background-color: #f4f4f4;
                    padding: 2px 6px;
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                }}
                pre {{
                    background-color: #f4f4f4;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 20px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }}
                th {{
                    background-color: #3498db;
                    color: white;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
        {html_content}
        </body>
        </html>
        """
        
        # Convert HTML to PDF
        pdfkit.from_string(html_with_style, 'TECHNICAL_DOCUMENTATION.pdf', options={
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None
        })
        
        print("✅ PDF generated successfully: TECHNICAL_DOCUMENTATION.pdf")
        
    except ImportError:
        print("❌ Required packages not installed.")
        print("Install with: pip install markdown2 pdfkit")
        print("\nOr use alternative method with reportlab...")
        
        # Alternative: Use reportlab (simpler, no external dependencies)
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
            from reportlab.lib.enums import TA_LEFT, TA_CENTER
            import re
            
            # Read markdown file
            with open('TECHNICAL_DOCUMENTATION.md', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create PDF
            pdf = SimpleDocTemplate('TECHNICAL_DOCUMENTATION.pdf', pagesize=A4,
                                   rightMargin=72, leftMargin=72,
                                   topMargin=72, bottomMargin=18)
            
            styles = getSampleStyleSheet()
            story = []
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor='#2c3e50',
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading1_style = ParagraphStyle(
                'CustomHeading1',
                parent=styles['Heading1'],
                fontSize=18,
                textColor='#34495e',
                spaceAfter=12,
                spaceBefore=20
            )
            
            heading2_style = ParagraphStyle(
                'CustomHeading2',
                parent=styles['Heading2'],
                fontSize=14,
                textColor='#7f8c8d',
                spaceAfter=10,
                spaceBefore=15
            )
            
            # Parse markdown and convert to PDF
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    story.append(Spacer(1, 12))
                elif line.startswith('# '):
                    story.append(Paragraph(line[2:], title_style))
                elif line.startswith('## '):
                    story.append(Paragraph(line[3:], heading1_style))
                elif line.startswith('### '):
                    story.append(Paragraph(line[4:], heading2_style))
                elif line.startswith('```'):
                    continue  # Skip code block markers
                else:
                    # Escape HTML and create paragraph
                    escaped = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    story.append(Paragraph(escaped, styles['Normal']))
                    story.append(Spacer(1, 6))
            
            pdf.build(story)
            print("✅ PDF generated successfully: TECHNICAL_DOCUMENTATION.pdf")
            
        except Exception as e:
            print(f"❌ Error generating PDF: {e}")
            print("\nAlternative: Use online markdown to PDF converter:")
            print("1. Open TECHNICAL_DOCUMENTATION.md")
            print("2. Copy content")
            print("3. Use: https://www.markdowntopdf.com/")
            print("   or: https://dillinger.io/ (export as PDF)")

if __name__ == '__main__':
    if not os.path.exists('TECHNICAL_DOCUMENTATION.md'):
        print("❌ TECHNICAL_DOCUMENTATION.md not found!")
        sys.exit(1)
    
    convert_markdown_to_pdf()

