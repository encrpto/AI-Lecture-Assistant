import os
import subprocess
import numpy as np
import faiss

from faster_whisper import WhisperModel
from sentence_transformers import SentenceTransformer
from transformers import pipeline


BASE_DIR = "data"
VIDEO_PATH = os.path.join(BASE_DIR, "lecture.mp4")
AUDIO_PATH = os.path.join(BASE_DIR, "lecture.mp3")


GLOBAL_CHUNKS = None
GLOBAL_INDEX = None
CHAT_HISTORY = []
generator = None  # lazy load


def convert_to_mp3():
    print("🔊 Converting video...")
    subprocess.run(
        f'ffmpeg -i "{VIDEO_PATH}" -q:a 0 -map a "{AUDIO_PATH}" -y',
        shell=True
    )

    if not os.path.exists(AUDIO_PATH):
        raise Exception(" MP3 conversion failed. Check ffmpeg installation.")


def transcribe():
    print("🎤 Transcribing...")
    model = WhisperModel("tiny")  # CPU optimized

    segments, _ = model.transcribe(AUDIO_PATH)

    data = []
    for seg in segments:
        data.append({
            "text": seg.text,
            "start": seg.start,
            "end": seg.end
        })

    return data

def chunk_segments(segments, size=3):
    chunks = []
    for i in range(0, len(segments), size):
        group = segments[i:i+size]

        chunks.append({
            "text": " ".join([g["text"] for g in group]),
            "start": group[0]["start"],
            "end": group[-1]["end"]
        })

    return chunks

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def build_index(chunks):
    print("Creating embeddings...")
    texts = [c["text"] for c in chunks]

    embeddings = embedder.encode(texts)

    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))

    return index

def retrieve(query, chunks, index, k=3):
    q_emb = embedder.encode([query])
    _, indices = index.search(np.array(q_emb), k)
    return [chunks[i] for i in indices[0]]


def get_model():
    global generator

    if generator is None:
        print("Loading flan-t5 model...")

        generator = pipeline(
            "text-generation",   
            model="google/flan-t5-large"
        )

    return generator

# ---------- GENERATE ----------
def generate(prompt):
    model = get_model()
    result = model(prompt, max_length=512, do_sample=True, temperature=0.7)
    return result[0]["generated_text"]

# ---------- RUN PIPELINE ----------
def run_pipeline():
    global GLOBAL_CHUNKS, GLOBAL_INDEX

    os.makedirs(BASE_DIR, exist_ok=True)

    convert_to_mp3()

    segments = transcribe()

    chunks = chunk_segments(segments)

    index = build_index(chunks)

    GLOBAL_CHUNKS = chunks
    GLOBAL_INDEX = index

    print("Pipeline ready!")

# ---------- CHAT ----------
def answer_question(query):
    global GLOBAL_CHUNKS, GLOBAL_INDEX, CHAT_HISTORY

    if GLOBAL_CHUNKS is None:
        return "Please process a lecture first."

    retrieved = retrieve(query, GLOBAL_CHUNKS, GLOBAL_INDEX)

    context = "\n".join([
        f"[{round(c['start'],1)}s-{round(c['end'],1)}s] {c['text']}"
        for c in retrieved
    ])

    history = "\n".join([
        f"User: {q}\nAssistant: {a}" for q, a in CHAT_HISTORY[-3:]
    ])

    prompt = f"""
Answer ONLY using this lecture context.

If answer is not found, say:
"Not mentioned in lecture."

History:
{history}

Context:
{context}

Question:
{query}
"""

    answer = generate(prompt)

    CHAT_HISTORY.append((query, answer))

    return answer
