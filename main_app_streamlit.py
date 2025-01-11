import streamlit as st
import os
import pandas as pd
from mainapp import extract_text_from_url, load_dictionaries, calculate_sentiment, calculate_readability, calculate_other_metrics, process_urls

# Load dictionaries for sentiment analysis
def load_dictionaries_for_app():
    folder_path = "dictionaries"  # Change to your actual dictionary folder
    stop_words, positive, negative = load_dictionaries(folder_path)
    return stop_words, positive, negative

# Streamlit App UI
st.title("Text Analysis from URL")

# Choose between single URL input or multiple URLs input from Excel file
input_choice = st.radio("Choose Input Method", ["Single URL", "Multiple URLs from Excel"])

if input_choice == "Single URL":
    # Get URL input from the user
    url = st.text_input("Enter URL for analysis")

    # Button to trigger the extraction and analysis
    if st.button('Analyze URL'):
        if url:
            folder_name = "extracted_texts"
            # Extract text from the URL
            extracted_file_path = extract_text_from_url(url, folder_name)
            
            if extracted_file_path:
                # Load stop words and sentiment words
                stop_words, positive_words, negative_words = load_dictionaries_for_app()

                with open(extracted_file_path, 'r', encoding='utf-8') as file:
                    text = file.read()

                # Sentiment analysis
                positive_score, negative_score, polarity_score, subjectivity_score = calculate_sentiment(text, stop_words, positive_words, negative_words)
                # Readability analysis
                fog_index, avg_sentence_length, complex_words = calculate_readability(text)
                # Other text metrics
                word_count, syllable_count, personal_pronouns, avg_word_length = calculate_other_metrics(text)

                # Display Results
                st.subheader("Analysis Results")
                st.write(f"**Positive Score**: {positive_score}")
                st.write(f"**Negative Score**: {negative_score}")
                st.write(f"**Polarity Score**: {polarity_score}")
                st.write(f"**Subjectivity Score**: {subjectivity_score}")
                st.write(f"**Fog Index**: {fog_index}")
                st.write(f"**Average Sentence Length**: {avg_sentence_length}")
                st.write(f"**Complex Word Count**: {complex_words}")
                st.write(f"**Word Count**: {word_count}")
                st.write(f"**Syllable Count**: {syllable_count}")
                st.write(f"**Personal Pronouns Count**: {personal_pronouns}")
                st.write(f"**Average Word Length**: {avg_word_length}")

                # Save the results to an Excel file
                result_df = pd.DataFrame({
                    "Positive Score": [positive_score],
                    "Negative Score": [negative_score],
                    "Polarity Score": [polarity_score],
                    "Subjectivity Score": [subjectivity_score],
                    "Fog Index": [fog_index],
                    "Avg Sentence Length": [avg_sentence_length],
                    "Complex Word Count": [complex_words],
                    "Word Count": [word_count],
                    "Syllable Count": [syllable_count],
                    "Personal Pronouns Count": [personal_pronouns],
                    "Avg Word Length": [avg_word_length]
                })
                
                # Save to Excel
                output_file = "url_analysis_results.xlsx"
                result_df.to_excel(output_file, index=False)

                # Provide download link
                with open(output_file, "rb") as f:
                    st.download_button(
                        label="Download Analysis Results",
                        data=f,
                        file_name=output_file,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.error("Failed to extract text from the URL.")
        else:
            st.warning("Please enter a valid URL.")

elif input_choice == "Multiple URLs from Excel":
    # File uploader for the Excel file
    uploaded_file = st.file_uploader("Upload Excel File with URLs", type=["xlsx"])

    if uploaded_file:
        # Read the Excel file
        df = pd.read_excel(uploaded_file)
        if 'URL' in df.columns:
            # Get the output file name
            output_file = st.text_input("Enter output Excel file name", "output.xlsx")
            
            # Button to trigger the multiple URL analysis
            if st.button('Analyze Multiple URLs'):
                folder_name = "extracted_texts"
                dictionaries_folder = "dictionaries"
                process_urls(uploaded_file, output_file, dictionaries_folder, folder_name)

                # Provide download link for the output file
                with open(output_file, "rb") as f:
                    st.download_button(
                        label="Download Analysis Results",
                        data=f,
                        file_name=output_file,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                st.success(f"Analysis completed! Results saved to {output_file}.")
        else:
            st.error("Excel file must contain a column named 'URL'.")
    else:
        st.warning("Please upload an Excel file containing URLs.")
