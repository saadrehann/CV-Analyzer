"""
CV Parser Service
Extracts text from PDF and DOCX files
"""
import PyPDF2
import docx
import io
import re


class CVParser:
    """Service to parse CV files and extract text"""
    
    @staticmethod
    def parse_pdf(file):
        """Extract text from PDF file"""
        try:
            # Read file content
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            text = ""
            
            # Extract text from all pages
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    @staticmethod
    def parse_docx(file):
        """Extract text from DOCX file"""
        try:
            # Read file content
            doc = docx.Document(io.BytesIO(file.read()))
            text = ""
            
            # Extract text from all paragraphs
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Error parsing DOCX: {str(e)}")
    
    @staticmethod
    def parse_cv(file, file_type):
        """
        Parse CV file based on its type
        
        Args:
            file: Uploaded file object
            file_type: 'pdf' or 'docx'
        
        Returns:
            Extracted text as string
        """
        if file_type.lower() == 'pdf':
            return CVParser.parse_pdf(file)
        elif file_type.lower() in ['docx', 'doc']:
            return CVParser.parse_docx(file)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    @staticmethod
    def extract_email(text):
        """Extract email address from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None
    
    @staticmethod
    def extract_phone(text):
        """Extract phone number from text"""
        # Simple phone pattern (customize based on region)
        phone_pattern = r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}'
        phones = re.findall(phone_pattern, text)
        return phones[0] if phones else None
    
    @staticmethod
    def extract_sections(text):
        """
        Extract common CV sections
        Returns a dictionary with section names as keys
        """
        sections = {}
        text_lower = text.lower()
        
        # Common section headers
        section_keywords = {
            'experience': ['experience', 'work history', 'employment', 'professional experience'],
            'education': ['education', 'academic', 'qualifications'],
            'skills': ['skills', 'technical skills', 'competencies'],
            'certifications': ['certifications', 'certificates', 'licenses'],
            'summary': ['summary', 'objective', 'profile', 'about'],
        }
        
        for section_name, keywords in section_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    sections[section_name] = True
                    break
            if section_name not in sections:
                sections[section_name] = False
        
        return sections
