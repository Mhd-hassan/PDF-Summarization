import streamlit as st
import PyPDF2
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk
import tempfile
from io import BytesIO

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def create_summarizer():
    """Create a simple summarizer using sumy"""
    stemmer = Stemmer('english')
    summarizer = LsaSummarizer(stemmer)
    summarizer.stop_words = get_stop_words('english')
    return summarizer

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        # Read PDF file
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
                
        return text.strip()
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return None

def summarize_text(text, summarizer, num_sentences=3):
    """Generate a summary of the input text using sumy"""
    try:
        # Create a parser for the text
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        
        # Generate summary
        summary = summarizer(parser.document, num_sentences)
        
        # Join the sentences
        summary_text = " ".join([str(sentence) for sentence in summary])
        
        return summary_text
    
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="PDF Summarizer",
        page_icon="📄",
        layout="centered"
    )
    
    st.title("📄 PDF Summarizer")
    st.write("Upload your PDF file and get an AI-generated summary!")

    # Create the summarizer
    summarizer = create_summarizer()
    
    # File uploader
    pdf_file = st.file_uploader("Upload your PDF file", type=['pdf'])
      # Sidebar controls
    with st.sidebar:
        st.header("Summary Settings")
        num_sentences = st.slider("Number of sentences in summary", 1, 10, 3)
    
    if pdf_file is not None:
        with st.spinner("Extracting text from PDF..."):
            text = extract_text_from_pdf(pdf_file)
        
        if text:
            st.success("Text extracted successfully!")
            
            # Show extracted text in expander
            with st.expander("Show extracted text"):
                st.text_area("Extracted text", text, height=200)
            
            with st.spinner("Generating summary..."):
                summary = summarize_text(text, summarizer, num_sentences)
            
            if summary:
                st.header("Summary")
                st.write(summary)
                
                # Add download button for summary
                st.download_button(
                    label="Download Summary",
                    data=summary,
                    file_name="summary.txt",
                    mime="text/plain"
                )
        else:
            st.error("Failed to extract text from the PDF. Please try another file.")

if __name__ == "__main__":
    main()
