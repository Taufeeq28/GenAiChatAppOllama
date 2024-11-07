from PyPDF2 import PdfReader
import docx
import json
from pathlib import Path
from typing import List, Dict, Any
import streamlit as st

class DocumentProcessor:
    SUPPORTED_TYPES = {
        "application/pdf": "PDF",
        "text/plain": "Text",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "Word",
        "application/json": "JSON"
    }

    @staticmethod
    def get_pdf_text(file) -> str:
        text = ""
        pdf_reader = PdfReader(file)
        for page_num, page in enumerate(pdf_reader.pages, 1):
            content = page.extract_text()
            if content:
                text += f"\nPage {page_num}:\n{content}"
        return text

    @staticmethod
    def get_docx_text(file) -> str:
        doc = docx.Document(file)
        text = ""
        for para_num, para in enumerate(doc.paragraphs, 1):
            if para.text:
                text += f"\nParagraph {para_num}:\n{para.text}"
        return text

    @staticmethod
    def get_text_file_content(file) -> str:
        return file.getvalue().decode('utf-8')

    @staticmethod
    def get_json_content(file) -> str:
        content = json.loads(file.getvalue().decode('utf-8'))
        return json.dumps(content, indent=2)

    def process_document(self, file) -> Dict[str, Any]:
        """Process a single document and return its content with metadata"""
        try:
            file_type = file.type
            if file_type not in self.SUPPORTED_TYPES:
                raise ValueError(f"Unsupported file type: {file_type}")

            if file_type == "application/pdf":
                text = self.get_pdf_text(file)
            elif file_type == "text/plain":
                text = self.get_text_file_content(file)
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text = self.get_docx_text(file)
            elif file_type == "application/json":
                text = self.get_json_content(file)

            return {
                "content": text,
                "metadata": {
                    "filename": file.name,
                    "type": self.SUPPORTED_TYPES[file_type],
                    "size": file.size
                }
            }
        except Exception as e:
            st.error(f"Error processing {file.name}: {str(e)}")
            return None

    def process_documents(self, files: List[Any]) -> List[Dict[str, Any]]:
        """Process multiple documents and return their contents with metadata"""
        processed_docs = []
        for file in files:
            doc = self.process_document(file)
            if doc:
                processed_docs.append(doc)
        return processed_docs