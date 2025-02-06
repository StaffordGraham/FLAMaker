import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from Person import Person
from CaseDetails import CaseDetails
from datetime import datetime
from tkcalendar import DateEntry
import os
import subprocess
from docx import Document
from docx.oxml import OxmlElement
from docx.shared import Cm
from docx.shared import Inches
import functions
from functions import article
import sys




def write_order(case_details):
        #if case_details.definitions:
            #family_home_def=case_details.definitions[0]
        court_name=f"In the Family Court\n sitting at {case_details.court_name}"
        case_number_text=f"Case No: {case_details.case_number}"
        appapp=case_details.application
        appo =f"{appapp} \n Family Law Act 1996"
            
      
         #CREATE DOCUMENT   
        doc=Document()
        #COURT AND CASE NUMBER
        heading_table=doc.add_table(1,3)
        coat_of_arms_cell =heading_table.cell(0,0)
        court_name_cell=heading_table.cell(0,1)
        case_number_cell=heading_table.cell(0,2)
        #coat_of_arms_cell.paragraphs[0].add_run().add_picture('Coat_of_arms.png',width=Inches(1.25))
        court_name_paragraph=court_name_cell.paragraphs[0]
        court_name_run=court_name_paragraph.add_run(court_name)
        court_name_run.bold=True
        
        case_number_paragraph=case_number_cell.paragraphs[0]
        case_number_run=case_number_paragraph.add_run(case_number_text)
        case_number_run.bold=True
        
        #LINE
        
        line_paragraph = doc.add_paragraph()
        line_paragraph.add_run('_'*100)
        #THE APPLICATION AND THE STATUTE
        paragraph=doc.add_paragraph()
        appo=case_details.application
        pprun=paragraph.add_run(appo)
        pprun.bold=True
        pparagraph=doc.add_paragraph()
        pprun=pparagraph.add_run("Family Law Act 1997")
        pprun.bold=True
        paragraph=doc.add_paragraph()
        
        #LINE
        line_paragrap=doc.add_paragraph()  # Adjust the number for length
        line_paragrap.add_run('_'*100)
        #TABLE FOR CHILDREN
        kidno =len(case_details.children)
        if kidno>1:
            label_children="The full names of the children"
            label_date="Dates of Birth"
        else:
            label_children="The full name of the child"
            label_date="Date of Birth"
        
        child_table=doc.add_table(rows=kidno+1,cols=3)
        child_table.columns[0].width=Cm(20)
        child_table.columns[1].width=Cm(3)
        child_table.columns[2].width=Cm(3)
       
        cell_00=child_table.cell(0,0)
        cell_00.text=label_children
        cell_01=child_table.cell(0,1)
        cell_01.text="Boy or Girl"
        cell_02=child_table.cell(0,2)
        cell_02.text=label_date
        
        #ADD CHILDREN INFO
        
        for i, child in enumerate(case_details.children, start=1):  # start=1 to fill rows below the header
            child_full_name =child.first_name + " "+child.last_name
            child_table.cell(i, 0).text = child_full_name  # Name
            child_table.cell(i, 1).text = child.gender # Gender
            child_table.cell(i, 2).text = child.full_date_of_birth  # Date of Birth (convert to string if necessary)
        
        doc.add_paragraph()
        
        #THE WARNING
        
        warning_text=[] 
        warning_text.append(f"IMPORTANT NOTICE TO THE RESPONDENT {case_details.respondent.first_name.upper()} ")
        warning_text.append(case_details.respondent.last_name.upper())
        warning_text.append(f" of {case_details.respondent.address_building_and_street.upper()}, ")
        warning_text.append(f"{case_details.respondent.address_second_line.upper()} ")
        warning_text.append(f"{case_details.respondent.address_town_or_city.upper()} ")
        warning_text.append(f"{case_details.respondent.address_postcode.upper()}.\n")
        warning_text.append("YOU MUST OBEY THIS ORDER. You should read it carefully .If you do not understand anything in this order you should go to a solicitor, Legal Advice Centre or Citizens Advice Bureau. You have the right to apply to the court to change or cancel the order.\n")
        warning_text.append("WARNING: ALTERNATIVELY, IF YOU DISOBEY THIS ORDER, YOU MAY BE HELD TO BE IN CONTEMPT OF COURT AND MAY BE IMPRISONED, FINED, OR HAVE YOUR ASSETS SEIZED")
        final_warning_text=' '.join(warning_text) 
        
        
        warning_table=doc.add_table(rows=1,cols=1)
        warning_table.autofit=True
        warning_table.style='Table Grid'
        
        warning_cell =warning_table.cell(0,0)
        warning_cell_paragraph=warning_cell.paragraphs[0]
        run = warning_cell_paragraph.add_run(final_warning_text)
        run.bold=True
        doc.add_paragraph()
        doc.add_paragraph()
        
        #THE JUDGE, HEARING DATE & TYPE
        judge_date_hearing_type=[]
        judge_date_hearing_type.append('Before')
        if case_details.judge_rank:
            judge_date_hearing_type.append(case_details.judge_rank)
            
        if case_details.judge_name:
            judge_date_hearing_type.append(case_details.judge_name)
          
        if case_details.hearing_date:
            judge_date_hearing_type.append(' in private on')        
            judge_date_hearing_type.append(case_details.hearing_date)
            
        if case_details.listed_for:
            judge_date_hearing_type.append(' at')
            judge_date_hearing_type.append(article(case_details.listed_for))
        
        judge_date_hearing_type.append('.')
        judge_and_hearing=" ".join(judge_date_hearing_type)
        doc.add_paragraph(judge_and_hearing)        
        #THE PARTIES
        
        
        parties_definitions_text=[]
        parties_definitions_text.append(f"The applicant is {case_details.applicant.first_name} {case_details.applicant.last_name}")
        reppo=case_details.app_rep
        beppo=case_details.resp_rep
        
        parties_definitions_text.append(f"represented by {case_details.app_rep.full_name}")
        parties_definitions_text.append(f"The respondent is {case_details.respondent.first_name} {case_details.respondent.last_name}")
        parties_definitions_text.append(f"represented by {case_details.resp_rep.full_name}")
        the_parties_defs=' '.join(parties_definitions_text)
        parties_table=doc.add_table(rows=2,cols=2)
        for row in parties_table.rows:
            row.cells[0].width = Cm(3.0)  # Adjust as needed
            row.cells[1].width = Cm(14.0)  # 
    
        parties_label=parties_table.cell(0,0)
        parties_para =parties_label.add_paragraph()
        run =parties_para.add_run("The Parties: ")
        run.bold=True
        parties_cell=parties_table.cell(0,1)
        parties_cell_para=parties_cell.add_paragraph()
        run=parties_cell_para.add_run(the_parties_defs)
        parties_cell_para.alignment = 0  # Left-aligned
               
         #DEFINITIONS - CHILDREN
        definitions_table=doc.add_table(rows=2,cols=2)
        definitions_label=definitions_table.cell(0,0)
        definit_head=definitions_label.add_paragraph()
        run=definit_head.add_run("Definitions")
        run.bold=True
        
        numb_children = len(case_details.children)
        
        
        
        if numb_children>1:
            chilo="The “relevant children” within the meaning of Family Law Act 1996 are:"
        else:
            chilo="The relevant child within the meaning of the Family Law Act 1995 is:"
        doc.add_paragraph(chilo,style="ListNumber")
        
        
        starting_char='a'
        for index, child_info in enumerate(case_details.children):
            sentence=child.sentence
            
            prefix =chr(ord(starting_char)+index)
            paragraph_text=f"\t{prefix}\t{sentence}"
            doc.add_paragraph(paragraph_text)
            
            #DEFINITIONS FAMILY HOME
            
        fam_home_stringbuilder =[]
        fam_home_stringbuilder.append('The "family home" is the property at')
        fam_home_stringbuilder.append(case_details.applicant.address_building_and_street)
        fam_home_stringbuilder.append(case_details.applicant.address_second_line)
        fam_home_stringbuilder.append(case_details.applicant.address_town_or_city)
        fam_home_stringbuilder.append(case_details.applicant.address_postcode)
        family_home_def=' '.join(fam_home_stringbuilder)
        doc.add_paragraph(family_home_def  ,style='ListNumber')
            
        #RECITALS

        if len(case_details.recitals) >0:
            recitals_para_head=doc.add_paragraph()
            rec_run=recitals_para_head.add_run("Recitals")
            rec_run.bold=True
        
            for recit_para in case_details.recitals:
                doc.add_paragraph(recit_para,style='ListNumber')
               
        
        #UNDERTAKINGS
        if len(case_details.undertakings)>0:
            undertakings_para_head=doc.add_paragraph()
            ut_rn=undertakings_para_head.add_run('Undertakings')
            ut_rn.bold=True
            for upara in case_details.undertakings:
                doc.add_paragraph(upara,style='ListNumber')
            
         #ORDERS
            
            if case_details.consent_order ==True:
                orders_para_head="IT IS ORDERED BY CONSENT"
            else:
                orders_para_head="IT IS ORDERED"
                
                
            oph=doc.add_paragraph()
            ord_head_run=oph.add_run(orders_para_head)
            ord_head_run.bold=True
            for opara in case_details.orders:
                doc.add_paragraph(opara,style='ListNumber')
            
            doc.add_paragraph("_" * 5)
            judge=case_details.judge_rank+" "+case_details.judge_name
            
            
            end=doc.add_paragraph()
            
            end_run =end.add_run(judge)
            doc.add_paragraph()
            date_end=doc.add_paragraph()
            run_date_end=date_end.add_run(case_details.hearing_date)


      
        
    
        
        
        
        
        
        # Save the document
        doc.save("family_court_document.docx")
        
        
        
        file_path='sample_document.docx'
        doc.save(file_path)
        os.name='nt'
        os.startfile(file_path)

    