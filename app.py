import streamlit as st
from docling.document_converter import DocumentConverter
import tempfile
import os

# Função para processar o upload do arquivo e conversão
def process_document(file):
    # Criação de um arquivo temporário para salvar o conteúdo enviado
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file.getvalue())
        temp_file_path = temp_file.name

    # Converter o arquivo usando o DocumentConverter
    converter = DocumentConverter()
    result = converter.convert(temp_file_path)

    # Remover o arquivo temporário após a conversão
    os.remove(temp_file_path)

    return result.document.export_to_markdown()

# Interface Streamlit
st.title("Conversor de Documentos")

st.write(
    "Envie um arquivo para ser convertido em Markdown. O arquivo será processado e convertido automaticamente."
)

# Criação do uploader de arquivos
uploaded_file = st.file_uploader("Arraste e solte o arquivo aqui", type=["pdf"])

# Espaço vazio para exibir a mensagem "Processando o arquivo..."
processing_message = st.empty()

# Se o usuário fizer o upload de um arquivo
if uploaded_file is not None:
    # Exibir a mensagem de processamento
    processing_message.text("Processando o arquivo...")

    # Chamada da função para converter o arquivo
    result = process_document(uploaded_file)

    # Remover a mensagem de processamento assim que o arquivo for processado
    processing_message.empty()

    # Exibição do conteúdo convertido
    st.subheader("Conteúdo em Markdown")
    st.code(result, language='markdown')

    # Botão para baixar o arquivo markdown
    st.download_button(
        label="Baixar arquivo Markdown",
        data=result,
        file_name="documento_convertido.md",
        mime="text/markdown"
    )
