"""
    At a command prompt,run the following code to install the Azure AI Document Intelligence client library for Python with pip:
                                pip install azure-ai-documentintelligence --pre
"""
import os
from utility import client


def get_words(page, line):
    result = []
    for word in page.words:
        if _in_span(word, line.spans):
            result.append(word)
    return result


def _in_span(word, spans):
    for span in spans:
        if word.span.offset >= span.offset and (word.span.offset + word.span.length) <= (span.offset + span.length):
            return True
    return False


def analyze_read(directory_path, output_directory):
    from azure.ai.documentintelligence.models import DocumentAnalysisFeature, AnalyzeResult

    document_intelligence_client = client()

    # Iterate over all files in the given directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            print(f"\nBeginning text extraction of file: {filename}")
            with open(file_path, "rb") as f:
                poller = document_intelligence_client.begin_analyze_document(
                    "prebuilt-read",
                    analyze_request=f,
                    features=[DocumentAnalysisFeature.LANGUAGES],
                    content_type="application/octet-stream",
                )
            result: AnalyzeResult = poller.result()

            # Create a new text file to save the output
            output_file_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.txt")
            print(f"\nBeginning writing the text extraction of file: {filename}")
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                # Analyze pages.
                for page in result.pages:
                    print(f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}")
                    # Analyze lines.
                    if page.lines:
                        for line_idx, line in enumerate(page.lines):
                            # words = get_words(page, line)
                            output_file.write(f'{line.content}\n')
                            print(f'{line.content}')


if __name__ == "__main__":
    from azure.core.exceptions import HttpResponseError
    from dotenv import find_dotenv, load_dotenv

    try:
        load_dotenv(find_dotenv())
        directory_path = "C:/Users/Admin/Desktop/OCR/image/"
        output_directory = "C:/Users/Admin/Desktop/OCR/text/"
        analyze_read(directory_path, output_directory)

    except HttpResponseError as error:
        # Examples of how to check an HttpResponseError
        # Check by error code:
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(f"Received an invalid image error: {error.error}")
            if error.error.code == "InvalidRequest":
                print(f"Received an invalid request error: {error.error}")
            # Raise the error again after printing it
            raise
        # If the inner error is None and then it is possible to check the message to get more information:
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        # Raise the error again
        raise
