# PDF Summarizer Tool

This is a Python tool that extracts text from PDF files and generates concise summaries using state-of-the-art natural language processing. It provides both a web interface and command-line interface.

## Features

- Web interface for easy PDF upload and summary generation
- PDF text extraction using PyPDF2
- Text summarization using the BART model from Hugging Face Transformers
- Progress bars for long-running operations
- Configurable summary length
- Download summaries as text files
- Command-line interface (optional)

## Installation

1. First, ensure you have Python 3.7 or later installed.

2. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   ```
   Note: If you get a PowerShell execution policy error, run PowerShell as administrator and execute:
   ```powershell
   Set-ExecutionPolicy RemoteSigned
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Web Interface (Recommended)

Run the Streamlit app:

```
streamlit run streamlit_app.py
```

This will open a web browser where you can:
1. Upload your PDF file using drag-and-drop or file selection
2. Adjust summary length settings using sliders
3. View the extracted text and generated summary
4. Download the summary as a text file

### Command Line Interface (Optional)

You can also run the script from the command line:

```
python pdf_summarizer.py path/to/your/file.pdf [--max_length MAX_LENGTH] [--min_length MIN_LENGTH]
```

Arguments:
- `path/to/your/file.pdf`: Path to the PDF file you want to summarize
- `--max_length`: Maximum length of the summary (default: 150)
- `--min_length`: Minimum length of the summary (default: 50)

Example:
```
python pdf_summarizer.py document.pdf --max_length 200 --min_length 100
```

## Note

The first time you run the script, it will download the BART model, which may take a few minutes depending on your internet connection.

## Dependencies

- PyPDF2: For PDF text extraction
- transformers: For text summarization using BART
- torch: Required by transformers
- tqdm: For progress bars
- numpy: Required by transformers
