import nemo.collections.asr as nemo_asr
import nemo.collections.nlp as nemo_nlp
import soundfile as sf
import torch
from transformers import pipeline

# ---------------- Load ASR Model ----------------
asr_model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained("nvidia/quisper_conformer")

# ---------------- Transcribe Audio ----------------
def transcribe(audio_file):
    transcript = asr_model.transcribe(paths2audio_files=[audio_file])[0]
    return transcript

# ---------------- Summarize Transcript ----------------
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text):
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
    return summary

# ---------------- Translate Summary ----------------
translator = pipeline("translation_en_to_es", model="Helsinki-NLP/opus-mt-en-es")

def translate_summary(text):
    translation = translator(text)[0]['translation_text']
    return translation

# ---------------- Main Workflow ----------------
if __name__ == "__main__":
    audio_path = "doctor_note.wav"  # Replace with your own recording

    print("🎧 Transcribing...")
    transcription = transcribe(audio_path)
    print(f"\n📝 Transcription:\n{transcription}")

    print("\n📚 Summarizing...")
    summary = summarize_text(transcription)
    print(f"\n✂️ Summary:\n{summary}")

    print("\n🌐 Translating to Spanish...")
    translation = translate_summary(summary)
    print(f"\n🗣️ Spanish Translation:\n{translation}")
