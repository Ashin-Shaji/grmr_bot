import streamlit as st, base64, chardet, google.generativeai as gem, os
from langdetect import detect;from langdetect.lang_detect_exception import LangDetectException

os.environ["GOOGLE_API_KEY"] = 'AIzaSyBbepUh8x3CqpkxNFnJ1IX0dFc0UNTwwbU'
# gem.configure(api_key='AIzaSyBbepUh8x3CqpkxNFnJ1IX0dFc0UNTwwbU')

# o = gem.GenerativeModel('gemini-1.5-pro-latest')
o = gem.GenerativeModel('gemini-pro')
language_dict = {
    "Arabic": "ar", "Bengali": "bn", "Chinese": "zh",
    "Czech": "cs", "Danish": "da", "Dutch": "nl", "English": "en",
    "Finnish": "fi", "French": "fr", "German": "de", "Greek": "el",
    "Hebrew": "he", "Hindi": "hi", "Hungarian": "hu", "Indonesian": "id",
    "Italian": "it", "Japanese": "ja", "Korean": "ko", "Malay": "ms",
     "Polish": "pl", "Portuguese": "pt",
    "Romanian": "ro", "Russian": "ru", "Spanish": "es", "Swedish": "sv",
    "Tagalog": "tl", "Thai": "th", "Turkish": "tr","Urdu": "ur", "Vietnamese": "vi"
}

def translate_text(input_text, target_language):
    try:
        # Detect the input language
        detected_language = detect(input_text)
        detected_language_name = [lang for lang, abbrev in language_dict.items() if abbrev == detected_language]

        if not detected_language_name:
            return f"Detected language {detected_language} is not supported."

        detected_language_name = detected_language_name[0]

        if detected_language_name not in language_dict:
            return f"Detected language {detected_language_name} is not supported."

        # Ensure the target language is supported
        if target_language not in language_dict:
            return f"Target language {target_language} is not supported."

        # Define the translation prompt
        prompt = f"You are a translator who translates from {detected_language_name} to {target_language}. " \
                 "Never answer any queries irrelevant to this context. Here is the text to translate:\n\n"
        text = prompt + input_text

        # Generate the translation
        response = o.generate_content(text)
        return response.text
    except LangDetectException:
        return "Could not detect the language. Please provide a valid text."

# # Streamlit UI
# st.title("Language Translator Bot")
# st.markdown("""<style>.stButton > button {display: block;margin: 0 auto;}</style>""", unsafe_allow_html=True)

# input_method = st.radio("Select input method:", ("Text input box", "Upload txt input file"))
# input_text = ""
# if input_method == "Text input box":
#     # Input text box
#     input_text = st.text_area("Enter text to translate:", height=200)
# elif input_method == "Upload txt input file":
#     # File uploader
#     uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
#     if uploaded_file is not None:
#         raw_data = uploaded_file.read()
#         result = chardet.detect(raw_data)
#         input_text = raw_data.decode(result['encoding'])
#         with st.expander("Uploaded File Content"):
#             st.write(input_text)

# target_language = st.selectbox("Select target language:", list(language_dict.keys()))

# if st.button("Translate"):
#     if not input_text.strip():
#         st.error("Please enter some text to translate.")
#     else:
#         translation = translate_text(input_text, target_language)
#         st.write("**Translation:**")
#         st.write(translation)
#         st.markdown(f"""<div style="display: flex; justify-content: center;">
#                 <a href="data:file/txt;base64,{base64.b64encode(translation.encode()).decode()}"
#                    download="translation.txt">
#                     <button style="padding: 10px 20px; font-size: 16px;">Download Translation</button>
#                 </a></div>""",unsafe_allow_html=True)

def main1():
    st.title("Language Translator Bot")
    st.markdown("""<style>.stButton > button {display: block;margin: 0 auto;}</style>""", unsafe_allow_html=True)
    
    input_method = st.radio("Select input method:", ("Text input box", "Upload txt input file"))
    input_text = ""
    if input_method == "Text input box":
        # Input text box
        input_text = st.text_area("Enter text to translate:", height=200)
    elif input_method == "Upload txt input file":
        # File uploader
        uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
        if uploaded_file is not None:
            raw_data = uploaded_file.read()
            result = chardet.detect(raw_data)
            input_text = raw_data.decode(result['encoding'])
            with st.expander("Uploaded File Content"):
                st.write(input_text)
    
    target_language = st.selectbox("Select target language:", list(language_dict.keys()))
    
    if st.button("Translate"):
        if not input_text.strip():
            st.error("Please enter some text to translate.")
        else:
            translation = translate_text(input_text, target_language)
            st.write("**Translation:**")
            st.write(translation)
            st.markdown(f"""<div style="display: flex; justify-content: center;">
                    <a href="data:file/txt;base64,{base64.b64encode(translation.encode()).decode()}"
                       download="translation.txt">
                        <button style="padding: 10px 20px; font-size: 16px;">Download Translation</button>
                    </a></div>""",unsafe_allow_html=True)

#main 2
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import json

# Initialize the ChatGoogleGenerativeAI model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

# Define the mode_prompt_map outside of the functions
mode_prompt_map = {
    "Standard Mode": "Paraphrase the text while preserving the original meaning",
    "Fluency Mode": "Paraphrase the text to make it grammatically correct and natural",
    "Creative Mode": "Paraphrase the text creatively and diversely",
    "Shorten Mode": "Paraphrase the text to make it shorter",
    "Expand Mode": "Paraphrase the text to add more details and make it longer",
    "Formal Mode": "Paraphrase the text to make it sound more professional and formal",
    "Simple Mode": "Paraphrase the text to make it easier to understand",
    "Academic Mode": "Paraphrase the text to make it more academic",
    "Optimistic Mode": "Paraphrase the text with an optimistic tone",
    "Witty Mode": "Paraphrase the text with a witty and humorous tone"
}

def paraphrase_text(mode, text, synonyms=None):
    prompt = mode_prompt_map[mode] + " " + text

    if synonyms:
        prompt += f"\nUse these synonyms: {json.dumps(synonyms)}"

    message = HumanMessage(content=prompt)
    response = llm.invoke([message])
    return response.content

def generate_citation(text, style):
    citation_prompt_map = {
        "APA": "Generate an APA style citation for the following text:",
        "MLA": "Generate an MLA style citation for the following text:",
        "Chicago": "Generate a Chicago style citation for the following text:",
        "Harvard": "Generate a Harvard style citation for the following text:"
    }

    prompt = citation_prompt_map[style] + " " + text
    message = HumanMessage(content=prompt)
    response = llm.invoke([message])
    return response.content

def main2():
    st.title("Paraphrasing and Citation Generator")

    option = st.radio("Select an option:", ("Paraphrase Text", "Generate Citation"))

    if option == "Paraphrase Text":
        text = st.text_area("Enter text to paraphrase:")
        mode = st.selectbox(
            "Select paraphrasing mode:",
            ["Standard Mode", "Fluency Mode", "Creative Mode", "Shorten Mode", "Expand Mode", "Formal Mode", "Simple Mode", "Academic Mode",
            "Optimistic Mode", "Witty Mode"])

        # Display the mode-specific prompt as a caption
        st.caption(mode_prompt_map[mode])

        synonyms_input = st.text_area("Enter custom synonyms in JSON format (optional):")
        synonyms = None

        if synonyms_input:
            try:
                synonyms = json.loads(synonyms_input)
            except json.JSONDecodeError:
                st.error("Invalid JSON format for synonyms.")

        if st.button("Paraphrase"):
            if text:
                output = paraphrase_text(mode, text, synonyms)
                st.subheader("Paraphrased Text:")
                st.write(output)
            else:
                st.error("Please enter text to paraphrase.")

    elif option == "Generate Citation":
        text = st.text_area("Enter text to generate citation:")
        style = st.selectbox(
            "Select citation style:",
            ["APA", "MLA", "Chicago", "Harvard"]
        )

        if st.button("Generate Citation"):
            if text:
                output = generate_citation(text, style)
                st.subheader("Citation:")
                st.write(output)
            else:
                st.error("Please enter text to generate citation.")

#main 3
def summarize_text(text):
    llm = ChatGoogleGenerativeAI(model="Gemini 1.5 Pro")
    
    prompt = """You are a content summarizer. Your task is to carefully read the input text and provide a concise and accurate summary of the main points. Ensure the summary captures the essence of the content without losing important details. Do not add any personal opinions or external information."""
    
    # Combine prompt and input text
    full_text = prompt + " " + text
    response = llm.invoke([HumanMessage(content=full_text)])
    return response.content

def main3():
    st.title("Content Summarizer")
    
    st.markdown("""<style>.stButton > button {display: block;margin: 0 auto;}</style>""", unsafe_allow_html=True)
    
    input_text = st.text_area("Enter text to be summarized:", height=200)
    
    if st.button("Summarize"):
        if not input_text.strip():
            st.error("Please enter some text to summarize.")
        else:
            summary = summarize_text(input_text)
            st.subheader("Summary:")
            st.write(summary)

selected_option = st.radio("Select an option:",
      ["Paraphrasing and Citation Generator", "Language Translator Bot", "Content Summarizer"])

if selected_option == "Language Translator Bot":
    main1()
elif selected_option == "Paraphrasing and Citation Generator":
    main2()
elif selected_option == "Content Summarizer":
    main3()
