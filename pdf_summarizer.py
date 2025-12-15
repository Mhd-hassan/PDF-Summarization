import PyPDF2
from transformers import pipeline
import argparse
from tqdm import tqdm

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Get number of pages
            num_pages = len(pdf_reader.pages)
            
            # Extract text from each page
            for page_num in tqdm(range(num_pages), desc="Extracting text"):
                # Get the page object
                page = pdf_reader.pages[page_num]
                # Extract text from page
                text += page.extract_text() + "\n"
                
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return None

def summarize_text(text, max_length=150, min_length=50):
    """
    Generate a summary of the input text using transformers
    """
    try:
        # Initialize the summarization pipeline
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        # Split text into chunks if it's too long (BART has a max input length)
        max_chunk_length = 1024
        chunks = [text[i:i + max_chunk_length] for i in range(0, len(text), max_chunk_length)]
        
        # Summarize each chunk
        summaries = []
        for chunk in tqdm(chunks, desc="Generating summaries"):
            if len(chunk.strip()) > 100:  # Only summarize chunks with substantial content
                summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
                summaries.append(summary[0]['summary_text'])
        
        # Combine summaries
        final_summary = " ".join(summaries)
        return final_summary
    
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return None

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='PDF Summarizer Tool')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('--max_length', type=int, default=150, help='Maximum length of the summary')
    parser.add_argument('--min_length', type=int, default=50, help='Minimum length of the summary')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Extract text from PDF
    print("\nExtracting text from PDF...")
    text = extract_text_from_pdf(args.pdf_path)
    
    if text:
        print("\nGenerating summary...")
        summary = summarize_text(text, args.max_length, args.min_length)
        
        if summary:
            print("\nSummary:")
            print("-" * 80)
            print(summary)
            print("-" * 80)
        else:
            print("Failed to generate summary.")
    else:
        print("Failed to extract text from PDF.")

if __name__ == "__main__":
    main()
