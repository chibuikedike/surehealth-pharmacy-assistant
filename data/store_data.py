import os
import pandas as pd
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

all_chunks = []

# 1. PROCESS THE TEXT FILES (Guidelines, Hours, Policies)
print("Processing text guidelines...")
if os.path.exists("./documents"):
    text_loader = DirectoryLoader("./documents", glob="*.csv", loader_cls=TextLoader)
    text_docs = text_loader.load()
    
    # Split the long text file into smaller paragraphs
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    all_chunks.extend(text_splitter.split_documents(text_docs))

# 2. PROCESS THE EXCEL FILE (1,000 Inventory Records)
file_path = "./documents/pharmacy_inventory.csv"
if os.path.exists(file_path):
    print("Processing csv inventory records...")
    df = pd.read_csv(file_path)
    
    # Loop through each row and convert it into a clear sentence for the LLM
    for _, row in df.iterrows():
        sentence = (
            f"Medication: {row['Medication Name']} (SKU: {row['SKU']}). "
            f"Category: {row['Category']}. Price: ₦{row['Price (₦)']}. "
            f"Stock Level: {row['Current Stock']} units. Location: {row['Warehouse Location']}."
        )
        # Wrap the sentence into a LangChain Document format
        all_chunks.append(Document(page_content=sentence, metadata={"source": "inventory_csv"}))

# # 3. CONVERT TO MATH (EMBED) AND SAVE TO CHROMA
# print(f"Total compiled data blocks: {len(all_chunks)}")
# print("Turning data into math vectors (this may take a minute)...")
# print(all_chunks)

# Free local model to process the calculations
free_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Save to local Chroma database folder
db = Chroma.from_documents(all_chunks, free_embeddings, persist_directory="./free_pharmacy_db")

print("⚡ Success! Your database folder 'free_pharmacy_db' has been created and populated.")