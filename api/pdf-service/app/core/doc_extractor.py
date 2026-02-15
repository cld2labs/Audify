import io
import logging
import subprocess
import tempfile
import os
from docx import Document

logger = logging.getLogger(__name__)

class DocExtractor:
    """
    Extracts text from Microsoft Word documents (.docx and .doc).
    """

    def extract_docx(self, content: bytes) -> dict:
        """
        Extract text from .docx file using python-docx
        """
        try:
            # Load bytes into document
            doc = Document(io.BytesIO(content))
            
            # Extract text from paragraphs
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
                
            text = "\n".join(full_text)
            
            return {
                "text": text,
                "metadata": {
                    "page_count": len(doc.sections) if doc.sections else 1, # Approx
                    "format": "docx"
                },
                "method": "python-docx"
            }
        except Exception as e:
            logger.error(f"DOCX extraction failed: {str(e)}")
            raise

    def extract_doc(self, content: bytes) -> dict:
        """
        Extract text from .doc file using antiword (requires binary on system)
        """
        try:
            # Antiword works on files, not streams
            with tempfile.NamedTemporaryFile(suffix=".doc", delete=False) as temp:
                temp.write(content)
                temp_path = temp.name

            try:
                # Run antiword
                result = subprocess.run(
                    ['antiword', temp_path],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    raise Exception(f"Antiword failed: {result.stderr}")
                    
                return {
                    "text": result.stdout,
                    "metadata": {"format": "doc"},
                    "method": "antiword"
                }
            finally:
                # Cleanup
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            logger.error(f"DOC extraction failed: {str(e)}")
            raise
