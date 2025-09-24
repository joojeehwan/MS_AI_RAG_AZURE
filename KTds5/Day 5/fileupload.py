# # pip install azure-identity azure-storage-blob
# import os
# from azure.identity import DefaultAzureCredential
# from azure.storage.blob import BlobClient

# account = os.getenv("STORAGE_ACCOUNT")          # <storacc>
# container = "uploads"
# blob_name = "hello.txt"

# cred = DefaultAzureCredential()  # Managed Identity 사용
# blob = BlobClient(
#     account_url=f"https://{account}.blob.core.windows.net",
#     container_name=container,
#     blob_name=blob_name,
#     credential=cred,
# )

# blob.upload_blob(b"Hello Azure Storage!", overwrite=True)
import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
AZURE_STORAGE_CONTAINER_NAME = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
#LOCAL_PATH = r"D:\ms_ai_azure\KTds5\Day 5\3fc7bbd12946c37021896a8e90d842a2.jpg"

print(AZURE_STORAGE_CONNECTION_STRING)
print(AZURE_STORAGE_CONTAINER_NAME)

st.title("Azure Blob Storage에 파일 업로드")
uploaded_file = st.file_uploader("업로드할 파일 선택", type=["txt", "pdf", "csv", "png", "jpg", "jpeg"])

if uploaded_file is not None :
  try:
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER_NAME)
    blob_container = container_client.get_blob_client(uploaded_file.name)

    # with open(LOCAL_PATH, "rb") as data:  # ★ 반드시 'rb'
    #      blob_container.upload_blob(data, overwrite = True)
    blob_container.upload_blob(uploaded_file, overwrite = True)

    print("파일 업로드 성공")
    st.success("파일 업로드 성공")

  except Exception as e:
    print(f"파일 업로드 실패 : {e}")
    st.error(f"파일 업로드 실패 {e}") 



