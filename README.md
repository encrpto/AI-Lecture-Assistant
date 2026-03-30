# AI-Lecture-Assistant
Problem Statement There are a lot of problems that modern learners and professionals have to deal with: Hard to find specific ideas in long videos. Not having interactive tools to ask questions about lecture content. Static summaries are not very useful. • Privacy rules that stop people from using AI tools in the cloud

#How to Run

#1st way
Directly upload the VideoParser.ipynb file in googlecolab and run on GPU runtime for better performance.

#2nd way
install and setup ffmpeg essentials into your pc first

copy paste this code to install necessary libraries:

pip install torch torchvision torchaudio
pip install fastapi uvicorn streamlit
pip install transformers sentencepiece accelerate
pip install sentence-transformers
pip install faiss-cpu
pip install faster-whisper


run these commands in 2 different terminals and wait for models to get loaded..
uvicorn api:app --reload
streamlit run app.py
