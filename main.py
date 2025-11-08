from pathlib import Path
from src.document_scanner import scan_and_summarize
import os
import time



def main():
    # Direct input configuration
    input_paths = [r"F:\ASKITLOUD\OpenCVProjects\Document_Scanner_Summerisation\sample-image"]
    
    # Options
    output_dir = os.mkdir("output_dir") if not os.path.exists("output_dir") else "output_dir"
    print("Output directory:", output_dir)
    use_preprocess = False  # Set to True to enable image preprocessing
    model_name = "gemini-2.5-flash"
    save_text = os.path.join(output_dir,f"text_{int(time.time()*1000)}.txt") # Set to filename to save extracted text
    save_summary = os.path.join(output_dir,f"summary_{int(time.time()*1000)}.txt")  # Set to filename to save summary
    try:
        print(f"Processing: {input_paths}")
        
        # Run the document scanner pipeline
        extracted_text, summary = scan_and_summarize(
            input_paths=input_paths,
            use_preprocess=use_preprocess,
            model_name=model_name,
            save_text=save_text,
            save_summary=save_summary
        )
        
        # Display results
        print("\n" + "="*50)
        print("EXTRACTED TEXT VIA OCR MODEL")
        print("="*50)
        print(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
        
        print("\n" + "="*50)
        print("SUMMARY OF DOCUMENT CONTENT VIA LLMs")
        print("="*50)
        print(summary)
        print("="*50 + "\n")
        print("Document scanning completed successfully")
        
    except Exception as e:
        print(f"Document scanning failed: {e}")
        raise


if __name__ == '__main__':
    main()
