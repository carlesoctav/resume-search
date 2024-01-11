from pydantic import BaseModel
from datetime import datetime
from llama_index.program import OpenAIPydanticProgram
import json
from dotenv import load_dotenv
from llama_index.llms.cohere import Cohere
from llama_index.program import LLMTextCompletionProgram
import os
from typing import List, Dict, Optional, Union, Union
from pypdf import PdfReader
import re
import unicodedata

load_dotenv()


class Basic(BaseModel):
    """
    Basic profile information from resume
    name: name of the person
    title: title of the person or label
    email: email address
    phone: phone number
    summary: summary of the person
    location: location of the person
    """

    name: str = ""
    title: str = ""
    email: str = ""
    phone: str = ""
    summary: str = ""
    location: str = ""


class Profiles(BaseModel):
    class ProfileNetwork(BaseModel):
        """
        atomic information about each network of the person
        network: name of the network, like github, linkedin, etc
        username: username of the person
        url: url of the person
        """
        network: str = ""
        username: str = ""
        url: str = ""

    profiles: List[ProfileNetwork] = []


class Works(BaseModel):
    class WorkExp(BaseModel):
        """
        atomic information about each work experience of the person
        company: name of the company
        position: position of the person
        summary: summary of the work experience
        startDate: start date of the work experience
        endDate: end date of the work experience
        """
        company: str = ""
        position: str = ""
        summary: str = ""
        startDate: str = ""
        endDate: str = ""

    works: List[WorkExp] = []


class Educations(BaseModel):
    class Education(BaseModel):
        """
        atomic information about each education of the person
        institution: name of the institution
        major: major of the person
        studytype: type of study
        summary: summary of the education
        startDate: start date of the education
        endDate: end date of the education
        """
        institution: str = ""
        major: str = ""
        studytype: str = ""
        summary: str = ""
        startDate: str = ""
        endDate: str = ""

    educations: List[Education] = []


class Certificates(BaseModel):
    class Certificate(BaseModel):
        """
        atomic information about each certificate of the person
        name: name of the certificate
        issuer: issuer of the certificate
        date: date of the certificate
        """
        name: str = ""
        issuer: str = ""
        date: str = ""

    certificates: List[Certificate] = []


class Awards(BaseModel):
    class Award(BaseModel):
        """
        atomic information about each award of the person
        title: title of the award
        awarder: awarder of the award
        date: date of the award
        """
        title: str = ""
        awarder: str = ""
        date: str = ""

    awards: List[Award] = []


class Publications(BaseModel):
    class Publication(BaseModel):
        """
        atomic information about each publication of the person
        name: name of the publication
        publisher: publisher of the publication
        date: date of the publication
        """
        title: str = ""
        publisher: str = ""
        date: str = ""

    publications: List[Publication] = []


class Skills(BaseModel):
    """
    list of bunch of skills of the person (keywords)
    """
    skills: List[str] = []


class Languages(BaseModel):
    class Language(BaseModel):
        """
        atomic information about each language of the person
        language: name of the language
        fluency: fluency of the person 
        """
        language: str = ""
        fluency: str = ""

    languages: List[Language] = []


class References(BaseModel):
    class Reference(BaseModel):
        """
        atomic information about each reference of the person
        name: name of the reference
        reference: reference of the person
        """
        name: str = ""
        reference: str = ""

    references: List[Reference] = []


class FullProfile(BaseModel):
    basic: Basic = Basic()
    profiles: Profiles = Profiles()
    works: Works = Works()
    educations: Educations = Educations()
    certificates: Certificates = Certificates()
    awards: Awards = Awards()
    publications: Publications = Publications()
    skills: Skills = Skills()
    languages: Languages = Languages()
    references: References = References()


def convert_pdf_to_text(file_path):
    # Open the PDF file in read-binary mode
    with open(file_path, "rb") as file:
        # Create a PDF file reader object
        pdf_reader = PdfReader(file)

        # Initialize an empty string to store the extracted text
        text = ""

        # Get the number of pages in the PDF
        num_pages = len(pdf_reader.pages)

        # Loop through each page and extract the text
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    return text

def text_cleaning(input_string):
    lowercase = input_string.lower()
    remove_link = re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)', '', lowercase).replace("&amp;","&")
    remove_bullet = "\n".join([T for T in remove_link.split('\n') if '•' not in T and "baca juga:" not in T])
    remove_accented = unicodedata.normalize('NFKD', remove_bullet).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    remove_parentheses = re.sub("([\(\|]).*?([\)\|])", "\g<1>\g<2>", remove_accented)
    remove_punc = re.sub(r"[^\w\d.\s]+",' ', remove_parentheses)
    remove_num_dot = re.sub(r"(?<=\d)\.|\.(?=\d)|(?<=#)\.","", remove_punc)
    remove_extra_whitespace =  re.sub(r'^\s*|\s\s*', ' ', remove_num_dot).strip()
    return ".".join([s for s in remove_extra_whitespace.strip().split('.') if len(s.strip())>10]).replace("_","")


def OpenAiPDFParser(
    input_path: Optional[str] = None,
    input_folder: Optional[str] = None,
) -> Dict:
    prompt_template_str = """\
    Extract the FullProfile from a resume. Do not add, remove, or change any information.
    here is the resume:\
    {resume}
    """

    resume_text = convert_pdf_to_text(input_path)
    # resume_text = text_cleaning(resume_text)
    print(f"==>> resume_pdf: {resume_text}")
    llm = Cohere(api_key=os.getenv("COHERE_API_KEY"), max_tokens=4096, model="command")

    program = LLMTextCompletionProgram.from_defaults(
        output_cls=FullProfile,
        prompt_template_str=prompt_template_str,
        verbose=True,
        llm=llm,
    )

    output = program(resume=resume_text)
    print(f"==>> output: {output}")


if __name__ == "__main__":
    OpenAiPDFParser(input_path="html2pdf/gayatri.json.pdf")
