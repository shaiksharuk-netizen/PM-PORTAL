# services/indexing.py

def index_file_background(file_id, text, source_filename, file_type, uploaded_by, uploaded_at):
    print(f"[INDEXING] Queued file {file_id} ({source_filename}) for Pinecone indexing")
