import streamlit as st 
from gtts import gTTS
import os
from langdetect.lang_detect_exception import LangDetectException
from googletrans import Translator
import pycountry
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
import nltk
import asyncio

# Download NLTK data
nltk.download('punkt')
nltk.download('words')

# functions to read text aloud
def read_aloud(text, language='en'):  
    tts = gTTS(text =text, lang = language)
    tts.save("temp1.mp3")
    os.system("start temp.mp3")
    
# Function to generate word cloud
def generate_wordcloud(text):
    english_words = set(nltk.corpus.Words.Words())
    Words = word_tokenize(text)
    english_words_in_text = [Word for Word in Words if Word.lower() in english_words]
    english_text = ' '.join(english_words_in_text)

    WordCloud = WordCloud(width=800, height=400, background_color = 'White').generate(english_text)
    fig, ax = plt.subplots()
    ax.imshow(WordCloud, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout()
    return fig

# Main streamlit app
st.title("Globalize")

# Set background image using custom CSS
background_image = "back.jpg"   
st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:streamlit_env\back.jpg;base64,{background_image});
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Create a two -column layout
col1,col2 = st.columns(2)

# Get user input
with col1:
    paragraph = st.text_area("Enter one paragraph:")
    
with col2:
    # get list of all languages
    all_languages = [lang.name for lang in pycountry.languages]
    
    # Get user input for target languages
    target_language_input = st.multiselect("Select the desired languages for translation:", all_languages)
    
# Button to read aloud
if st.button("Read Aloud"):
    read_aloud(paragraph)
    
# Detect the language of the input paragraph
paragraph_language = None
if paragraph.strip():
    try:
        paragraph_language = detect(paragraph)
        language_name = pycountry.languages.get(alpha_2=paragraph_language).name
        st.write("Detected language:",language_name)
    except langdetect_lang_detect_ecpection.LangDetectException as e:
        st.error("Language detection failed: {}".format(e))
        paragraph_language = 'en'
        language_name='English'
    except KeyError:
        st.error("Language code not found in pypcountry")
        language_name = 'Unknown'
    except Exception as e:
        st.error("Error occurred during language detection: {}".format(e))
        
# Translate the paragraph  to English  if it's not already in english
translator = Translator()
if paragraph_language and paragraph_language != 'en':
    translated_paragraph =asyncio.run (translator.translate(paragraph, dest='en')).text
    st.write("Translated to universal language English:",translated_paragraph)
else:
    translated_paragraph = paragraph
    
# Generated and display word cloud
if translated_paragraph.strip():
    try:
        # Encode text to UTF-8 to handle non-Unicode characters
        translated_paragraph=translated_paragraph.encode('Utf-8','ignore').decode('Utf-8')
        WordCloud_fig = generate_wordcloud(translated_paragraph)
        st.sidebar.Subheader("Word Cloud")
        st.sidebar.pyplot(WordCloud_fig)
    except Exception as e:
        st.Error(f"Error generating word cloud: {e}")
     
# Add image below  the word cloud
st.sidebar.subheader("Image")  

# Translate and read Aloud
if st.button("Translate and Read Aloud"):
    target_languages = []
    for lang_name in target_language_input:
        lang_code = pycountry.languages.lookup(lang_name).alpha_2
        target_languages.append(lang_code)
        
# Translate the paragraph into each target language, print , and read aloud
target_languages = ['fr', 'es', 'de']  # Add this before line 119

for target_language in target_languages:
    try:
        translated_paragraph= asyncio.run(translator.translate(paragraph, dest = target_languages)).text
        language_name = pycountry.languages.get(alpha_2 = target_languages).name
        st.write(f"\nTranslated paragraph in {language_name}:")
        st.write(translated_paragraph)
        
        # Read  Translated text aloud
        read_aloud(translated_paragraph, target_languages)
    except Exception as e:
        st.error(f"Translation to {target_language} failed: {e}")

    
    