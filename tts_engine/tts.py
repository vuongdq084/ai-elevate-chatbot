from transformers import VitsModel, AutoTokenizer
import torch
import soundfile as sf
import os
from dotenv import load_dotenv
from langdetect import detect, LangDetectException
 
load_dotenv()
 
# --- Integrated Language Detector ---
def detect_language(text):
    """
    Detects the language of a given text.
    Returns 'vi' for Vietnamese or 'en' for English.
    Defaults to 'en' if detection fails or the language is not supported.
    """
    try:
        lang = detect(text)
        if lang == 'vi':
            return 'vi'
        # Default to English for any other detected language
        return 'en'
    except LangDetectException:
        # If detection fails (e.g., for very short/ambiguous text), default to English
        print("Language detection failed, defaulting to English.")
        return 'en'
 
# --- TTS Model Cache and Loader ---
tts_models = {}
tts_tokenizers = {}
device = "cuda" if torch.cuda.is_available() else "cpu"
 
def get_tts_model(lang='en'):
    """
    Loads and returns a TTS model and tokenizer for the specified language.
    Caches the models to avoid reloading them on every call.
    """
    model_name_env_var = f"TTS_MODEL_NAME_{lang.upper()}"
    model_name = os.getenv(model_name_env_var)
 
    if not model_name:
        print(f"TTS model for language '{lang}' is not configured in .env. Expected variable: {model_name_env_var}")
        return None, None
 
    if model_name in tts_models:
        return tts_models[model_name], tts_tokenizers[model_name]
 
    print(f"Loading TTS model for language '{lang}': {model_name}...")
    try:
        model = VitsModel.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model.to(device)
 
        tts_models[model_name] = model
        tts_tokenizers[model_name] = tokenizer
       
        print(f"TTS model for '{lang}' loaded and cached successfully.")
        return model, tokenizer
    except Exception as e:
        print(f"Error loading TTS model {model_name}: {e}")
        tts_models[model_name] = None
        tts_tokenizers[model_name] = None
        return None, None
 
def text_to_speech(text, output_file="answer.wav"):
    """
    Detects the language of the input text, converts it to speech using the
    appropriate model, and saves it to an audio file.
   
    Args:
        text (str): The text to convert.
        output_file (str): The path to save the output audio file.
 
    Returns:
        str or None: The path of the saved file if successful, otherwise None.
    """
    # Detect language internally
    lang = detect_language(text)
    print(f"🔍 Detected language: {'Vietnamese' if lang == 'vi' else 'English'}")
   
    tts_model, tts_tokenizer = get_tts_model(lang)
 
    if not tts_model or not tts_tokenizer:
        print("TTS model is not available. Skipping speech generation.")
        return None
 
    try:
        inputs = tts_tokenizer(text, return_tensors="pt").to(device)
        with torch.no_grad():
            output_tensor = tts_model(**inputs).waveform
       
        waveform = output_tensor.squeeze().cpu().numpy()
       
        sf.write(output_file, waveform, tts_model.config.sampling_rate)
       
        print(f"Generated speech saved to: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error generating speech: {e}")
        return None