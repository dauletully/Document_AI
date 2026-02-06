import streamlit as st
import os
import asyncio
from document_parser import extract_text_from_pdf, extract_text_from_docx
from llm import analyze_document

# Настройка страницы
st.set_page_config(page_title="Document AI Analysis", layout="wide")

st.title("📄 Document AI: Анализ Регуляторных Актов")
st.write("Загрузите документы для автоматического анализа и назначения задач.")

# --- БЛОК 1: Загрузка файлов ---
uploaded_files = st.file_uploader(
    "Выбрать файлы", 
    type=['pdf', 'docx'], 
    accept_multiple_files=True
)

# --- БЛОК 2: Кнопка действия ---
if st.button("Назначить исполнителя"):
    if uploaded_files:
        all_text = ""
        
        # Анимация загрузки (Spinner)
        with st.spinner('ИИ анализирует документы, пожалуйста, подождите...'):
            try:
                # Обработка каждого файла
                for uploaded_file in uploaded_files:
                    # Сохраняем временно во временный файл
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    if uploaded_file.name.endswith('.pdf'):
                        text = extract_text_from_pdf(temp_path)
                    else:
                        text = extract_text_from_docx(temp_path)
                    
                    all_text += f"\nFILE: {uploaded_file.name}\n{text}\n"
                    os.remove(temp_path) # Удаляем временный файл

                # Запуск ИИ (ваша функция из llm.py)
                # Streamlit работает синхронно, поэтому используем run_until_complete или просто await
                result = asyncio.run(analyze_document(all_text))

                st.success("✅ Анализ завершен!")
                st.subheader("📊 Отчет для исполнителя")
                
                # Красивое отображение в контейнере
                st.markdown(f"""
                <div style="background-color: #4A4A4A; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b;">
                    {result}
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Произошла ошибка: {e}")
    else:
        st.warning("⚠️ Пожалуйста, сначала выберите файлы.")

# --- СТРАНИЦА ИСПОЛНИТЕЛЯ ---
st.sidebar.markdown("### Панель навигации")
if st.sidebar.button("Просмотр архива задач"):
    st.sidebar.write("Здесь будет список всех обработанных документов.")