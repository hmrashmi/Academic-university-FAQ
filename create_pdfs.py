from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime

# Create Hostel Manual PDF
hostel_pdf = SimpleDocTemplate("Hostel_Manual.pdf", pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)

styles = getSampleStyleSheet()
story = []

# Title
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1f77b4'),
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

story.append(Paragraph("🏢 UNIVERSITY HOSTEL MANUAL", title_style))
story.append(Spacer(1, 0.2*inch))

# Subtitle
subtitle_style = ParagraphStyle(
    'CustomSubtitle',
    parent=styles['Normal'],
    fontSize=12,
    textColor=colors.grey,
    alignment=TA_CENTER,
    spaceAfter=20
)
story.append(Paragraph(f"Last Updated: {datetime.now().strftime('%B %d, %Y')}", subtitle_style))
story.append(Spacer(1, 0.3*inch))

# Content sections
heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#1f77b4'),
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

normal_style = ParagraphStyle(
    'CustomNormal',
    parent=styles['Normal'],
    fontSize=11,
    alignment=TA_JUSTIFY,
    spaceAfter=10
)

# Section 1: Overview
story.append(Paragraph("1. HOSTEL OVERVIEW", heading_style))
story.append(Paragraph(
    "Our university provides comfortable and safe hostel accommodation for students. The hostel facilities are designed to provide a home-like environment with modern amenities. Total capacity is 2000 beds with separate facilities for boys (1200 beds) and girls (800 beds).",
    normal_style
))
story.append(Spacer(1, 0.15*inch))

# Section 2: Room Types
story.append(Paragraph("2. ROOM TYPES & PRICING", heading_style))

room_data = [
    ['Room Type', 'Capacity', 'Price/Semester', 'Facilities'],
    ['Single Occupancy', '1 student', '$3000', 'AC, Bathroom, WiFi, Wardrobe, Study Table'],
    ['Double Occupancy', '2 students', '$2000', 'AC, Bathroom, WiFi, Wardrobes, Study Tables'],
    ['Triple Occupancy', '3 students', '$1500', 'AC, Bathroom, WiFi, Wardrobes, Study Tables']
]

room_table = Table(room_data, colWidths=[1.5*inch, 1.2*inch, 1.3*inch, 1.8*inch])
room_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
]))

story.append(room_table)
story.append(Spacer(1, 0.2*inch))

# Section 3: Hostel Rules
story.append(Paragraph("3. HOSTEL RULES & REGULATIONS", heading_style))

rules_text = """
<b>General Rules:</b><br/>
• Check-in time: 11:00 PM (Late check-in requires prior permission)<br/>
• Quiet hours: 11:00 PM to 7:00 AM<br/>
• Visitor hours: 10:00 AM to 8:00 PM<br/>
• No smoking or alcohol allowed in hostel premises<br/>
• Guests and visitors must register at the hostel office<br/>
• Monthly room inspection mandatory - 24 hours notice provided<br/>
• All residents must maintain cleanliness of common areas<br/>
• Unauthorized absence for more than 7 days may result in room cancellation<br/>
"""
story.append(Paragraph(rules_text, normal_style))
story.append(Spacer(1, 0.15*inch))

# Section 4: Services
story.append(Paragraph("4. HOSTEL SERVICES", heading_style))

services_text = """
<b>Available Services:</b><br/>
• Free laundry service: Twice per week<br/>
• Iron service: Available at nominal charge<br/>
• WiFi: 24/7 high-speed internet in all rooms<br/>
• Utilities: Electricity, water included in room fee<br/>
• Housekeeping: Daily cleaning of common areas<br/>
• Security: 24/7 security with CCTV surveillance<br/>
• Guest rooms: Available for visiting parents/relatives ($500/night)<br/>
• Common kitchen: Available for students to prepare meals<br/>
"""
story.append(Paragraph(services_text, normal_style))
story.append(Spacer(1, 0.15*inch))

# Section 5: Safety & Security
story.append(Paragraph("5. SAFETY & SECURITY", heading_style))

security_text = """
• Biometric access system at hostel gates<br/>
• CCTV cameras in all common areas<br/>
• 24/7 security personnel on duty<br/>
• Emergency services accessible at all times<br/>
• Fire extinguishers and emergency exits clearly marked<br/>
• Regular safety drills conducted monthly<br/>
"""
story.append(Paragraph(security_text, normal_style))
story.append(Spacer(1, 0.2*inch))

# Section 6: Fees & Payment
story.append(Paragraph("6. FEES & PAYMENT DETAILS", heading_style))

fees_text = """
All room fees must be paid by the 5th of each month. Payment can be made through:<br/>
• Online portal: student.university.edu/hostel-payment<br/>
• Direct bank transfer (details provided at hostel office)<br/>
• Cash payment at hostel office (Monday-Friday, 9 AM - 5 PM)<br/>
<br/>
<b>Late Payment:</b> Rs. 200 penalty per day after due date<br/>
"""
story.append(Paragraph(fees_text, normal_style))
story.append(Spacer(1, 0.15*inch))

# Section 7: Grievances
story.append(Paragraph("7. GRIEVANCE REDRESSAL", heading_style))

grievance_text = """
For any complaints or issues:<br/>
• Submit complaint form at hostel office<br/>
• Email: hostel@university.edu<br/>
• Contact: +1-800-HOSTEL-1<br/>
• Grievances resolved within 7 business days<br/>
"""
story.append(Paragraph(grievance_text, normal_style))

# Build PDF
hostel_pdf.build(story)
print("✅ Hostel_Manual.pdf created successfully!")

# Create College Handbook PDF
college_pdf = SimpleDocTemplate("College_Handbook.pdf", pagesize=letter,
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)

story = []

# Title
story.append(Paragraph("🎓 UNIVERSITY COLLEGE HANDBOOK", title_style))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph(f"Student Guide & Information Portal", subtitle_style))
story.append(Paragraph(f"Academic Year 2025-2026", subtitle_style))
story.append(Spacer(1, 0.3*inch))

# Table of Contents
story.append(Paragraph("TABLE OF CONTENTS", heading_style))
contents = [
    "1. Welcome to Our University<br/>",
    "2. Academic Calendar<br/>",
    "3. Courses & Programs<br/>",
    "4. Enrollment Procedures<br/>",
    "5. Campus Facilities<br/>",
    "6. Financial Information<br/>",
    "7. Student Support Services<br/>",
    "8. Code of Conduct<br/>",
    "9. Important Contacts<br/>"
]
story.append(Paragraph("".join(contents), normal_style))
story.append(Spacer(1, 0.2*inch))

# Section 1
story.append(Paragraph("1. WELCOME TO OUR UNIVERSITY", heading_style))
story.append(Paragraph(
    "Welcome to our vibrant academic community! This handbook contains essential information about our college programs, policies, and procedures. We are committed to providing quality education and comprehensive support services to all our students.",
    normal_style
))
story.append(Spacer(1, 0.15*inch))

# Section 2: Academic Calendar
story.append(Paragraph("2. ACADEMIC CALENDAR 2025-2026", heading_style))

calendar_data = [
    ['Semester', 'Important Dates'],
    ['Fall 2025', 'Start: Aug 25 | Registration: Aug 1-24 | Midterm: Oct 13-17 | Final: Dec 8-18'],
    ['Spring 2026', 'Start: Jan 12 | Registration: Dec 15-Jan 11 | Midterm: Mar 2-6 | Final: Apr 27-May 7'],
    ['Summer 2026', 'Start: Jun 1 | Registration: May 15-31 | End: Jul 24']
]

calendar_table = Table(calendar_data, colWidths=[1.5*inch, 4.5*inch])
calendar_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))

story.append(calendar_table)
story.append(Spacer(1, 0.2*inch))

# Section 3: Programs
story.append(Paragraph("3. ACADEMIC PROGRAMS", heading_style))

programs_text = """
<b>Undergraduate Programs (4 Years):</b><br/>
• Bachelor of Science (B.S.) in Computer Science<br/>
• Bachelor of Science (B.S.) in Engineering<br/>
• Bachelor of Business Administration (BBA)<br/>
• Bachelor of Arts (BA) in Liberal Arts<br/>
<br/>
<b>Postgraduate Programs (2 Years):</b><br/>
• Master of Technology (M.Tech)<br/>
• Master of Business Administration (MBA)<br/>
• Master of Science (M.S.)<br/>
"""
story.append(Paragraph(programs_text, normal_style))
story.append(Spacer(1, 0.15*inch))

# Section 4: Facilities
story.append(Paragraph("4. CAMPUS FACILITIES & SERVICES", heading_style))

facilities_text = """
<b>Academic Resources:</b> Library (500K+ books), 8 Computer Labs, Seminar Halls<br/>
<b>Sports & Recreation:</b> Olympic Pool, Gym, Tennis Courts, Soccer Field, Basketball Courts<br/>
<b>Health & Wellness:</b> 24/7 Medical Center, Counseling Services, Fitness Programs<br/>
<b>Dining & Accommodation:</b> 3 Cafeterias, Hostel (2000 beds), Guest Rooms<br/>
<b>Administrative:</b> Registrar Office, Financial Aid Office, Student Affairs, Career Services<br/>
"""
story.append(Paragraph(facilities_text, normal_style))
story.append(Spacer(1, 0.15*inch))

# Section 5: Fees
story.append(Paragraph("5. TUITION & FEES", heading_style))

fees_data = [
    ['Program', 'Per Semester', 'Annual'],
    ['Undergraduate', '$3,000', '$6,000'],
    ['Postgraduate', '$4,000', '$8,000'],
    ['International (UG)', '$6,000', '$12,000'],
    ['International (PG)', '$7,500', '$15,000']
]

fees_table = Table(fees_data, colWidths=[2*inch, 1.8*inch, 1.8*inch])
fees_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))

story.append(fees_table)
story.append(Spacer(1, 0.2*inch))

# Section 6: Support Services
story.append(Paragraph("6. STUDENT SUPPORT SERVICES", heading_style))

support_text = """
<b>Academic Support:</b> Peer Tutoring, Academic Advising, Writing Center<br/>
<b>Career Services:</b> Resume Building, Interview Prep, Job Placement, Internship Programs<br/>
<b>Counseling & Wellness:</b> Mental Health Counseling, Stress Management, Disability Services<br/>
<b>International Students:</b> Visa Assistance, Cultural Programs, Adaptation Support<br/>
<b>Financial Aid:</b> Scholarships, Grants, Student Loans, Work-Study Programs<br/>
"""
story.append(Paragraph(support_text, normal_style))
story.append(Spacer(1, 0.15*inch))

# Section 7: Important Contacts
story.append(Paragraph("7. IMPORTANT CONTACTS", heading_style))

contacts_text = """
<b>Main Administration:</b> admin@university.edu | 1-800-UNI-HELP<br/>
<b>Registrar Office:</b> registrar@university.edu | Ext. 2001<br/>
<b>Financial Aid:</b> finaid@university.edu | Ext. 2002<br/>
<b>Student Affairs:</b> studentaffairs@university.edu | Ext. 2003<br/>
<b>Hostel Office:</b> hostel@university.edu | Ext. 2004<br/>
<b>Career Services:</b> careers@university.edu | Ext. 2005<br/>
<b>Counseling Services:</b> counseling@university.edu | Ext. 2006<br/>
<b>Emergency Services:</b> Campus Security | Ext. 911<br/>
"""
story.append(Paragraph(contacts_text, normal_style))

# Build PDF
college_pdf.build(story)
print("✅ College_Handbook.pdf created successfully!")

print("\n📁 Both PDF files have been created in your project directory!")
print("📥 Hostel_Manual.pdf")
print("📥 College_Handbook.pdf")
