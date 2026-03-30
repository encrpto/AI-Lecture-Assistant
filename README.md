# AI-Lecture-Assistant
Problem Statement There are a lot of problems that modern learners and professionals have to deal with: Hard to find specific ideas in long videos. Not having interactive tools to ask questions about lecture content. Static summaries are not very useful. • Privacy rules that stop people from using AI tools in the cloud

# How to Run

# 1st way Simple
Directly upload the VideoParser.ipynb file in googlecolab and run on GPU runtime for better performance.

# 2nd way for continous chat about your lectures
install and setup ffmpeg essentials into your pc first

copy paste this code to install necessary libraries:

pip install torch torchvision torchaudio
pip install fastapi uvicorn streamlit
pip install transformers sentencepiece accelerate
pip install sentence-transformers
pip install faiss-cpu
pip install faster-whisper


run these commands in 2 different terminals and wait for models to load...
uvicorn api:app --reload
streamlit run app.py


# important! for better output and response change model from model="google/flan-t5-large" to any big model like mistral 7b
