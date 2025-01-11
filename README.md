# URLInsights: Text Analysis from URLs

URLInsights is a powerful tool that allows users to analyze the content of URLs by extracting the text and performing various analyses such as sentiment analysis, readability scores, and more. Users can either analyze a single URL or upload an Excel file containing multiple URLs for batch processing.
webapp link: https://urlinsights.streamlit.app/

## Features

- **Single URL Analysis**: Enter a URL, extract its text, and analyze it for sentiment, readability, and other metrics.
- **Multiple URL Analysis**: Upload an Excel file containing multiple URLs and get the analysis results for each URL.
- **Excel Output**: Results are displayed in the app and can be downloaded as an Excel file for further use.
- **Text Metrics**:
  - Sentiment Analysis (Positive/Negative Score, Polarity, Subjectivity)
  - Readability Analysis (Fog Index, Average Sentence Length, Complex Words)
  - Additional Metrics (Word Count, Syllable Count, Personal Pronouns, Average Word Length)

## Technologies Used

- Python
- Streamlit
- Pandas
- BeautifulSoup (for text extraction)
- NLP Libraries for Sentiment and Readability Analysis

## Usage

### Single URL Analysis:
- Enter the URL into the input field and click the "Analyze URL" button.
- The extracted text will be analyzed, and the results will be displayed.
- Results can be downloaded as an Excel file.

### Multiple URL Analysis:
- Upload an Excel file with a column named `URL` containing URLs to analyze.
- Click the "Analyze Multiple URLs" button to process the URLs.
- Download the results as an Excel file.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository, make your changes, and submit a pull request.

