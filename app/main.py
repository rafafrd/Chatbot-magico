import streamlit as st
from utils.gemini_client import GeminiClient

# Configuração inicial da página DEVE SER A PRIMEIRA COISA
st.set_page_config(
    page_title="🚀 Gemini 2.0 Flash",
    page_icon="⚡",
    layout="centered"
)

# Configuração do tema escuro com detalhes vermelhos
st.markdown("""
<style>
:root {
    --primary-color: #ff4b4b;
    --background-color: #0e1117;
    --secondary-background-color: #1a1d24;
    --text-color: #f0f0f0;
    --font: sans-serif;
}

.stApp {
    background-color: var(--background-color);
    color: var(--text-color);
    font-family: var(--font);
}

.stTextInput input {
    background-color: var(--secondary-background-color) !important;
    color: var(--text-color) !important;
    border: 1px solid var(--primary-color) !important;
}

.stTextInput label {
    color: var(--primary-color) !important;
}

.stChatMessage {
    border-radius: 10px;
    margin: 10px 0;
}

.stChatMessage.user {
    background-color: #1e2a38;
}

.stChatMessage.assistant {
    background-color: #2a1e38;
    border-left: 3px solid var(--primary-color);
}

h1 {
    color: var(--primary-color) !important;
    text-shadow: 0 0 8px rgba(255, 75, 75, 0.3);
}

.stMarkdown {
    color: var(--text-color) !important;
}

.stButton>button {
    background-color: var(--primary-color) !important;
    color: white !important;
    border: none !important;
}

.stError {
    border-left: 3px solid var(--primary-color);
}
</style>
""", unsafe_allow_html=True)

def main():
    # Título da aplicação com estilo moderno
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #ff4b4b; font-size: 2.5em; margin-bottom: 0;">GEMINI 2.0 FLASH</h1>
        <p style="color: #aaa; font-size: 0.9em; margin-top: 0;">Conectado à API mais rápida da Google • 2025</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Barra decorativa
    st.markdown("<hr style='border: 1px solid #ff4b4b; margin: 0 0 20px 0;'>", unsafe_allow_html=True)
    
    # Restante do código mantido igual...
    try:
        client = GeminiClient()
    except Exception as e:
        with st.container():
            st.error(f"🚨 Erro de configuração: {str(e)}")
            st.markdown("""
            <div style="background-color: #1a1d24; padding: 15px; border-radius: 8px; border-left: 3px solid #ff4b4b;">
                <h4 style="color: #ff4b4b; margin-top: 0;">Solução:</h4>
                <ol style="color: #f0f0f0;">
                    <li>Crie a pasta <code>/env/.env</code> na raiz do projeto</li>
                    <li>Adicione: <code>GEMINI_API_KEY=sua_chave_real</code></li>
                    <li>Reinicie o servidor</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
        st.stop()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(f"<div style='color: #f0f0f0;'>{message['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='color: #f0f0f0; border-left: 2px solid #ff4b4b; padding-left: 10px;'>{message['content']}</div>", unsafe_allow_html=True)
    
    input_container = st.container()
    with input_container:
        prompt = st.chat_input("Digite sua mensagem...", key="input")
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(f"<div style='color: #f0f0f0;'>{prompt}</div>", unsafe_allow_html=True)
        
        with st.chat_message("assistant"):
            try:
                with st.spinner("Processando..."):
                    response = client.generate_text(prompt)
                    st.markdown(f"<div style='color: #f0f0f0; border-left: 2px solid #ff4b4b; padding-left: 10px;'>{response}</div>", unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"🔴 Erro ao gerar resposta: {str(e)}")

if __name__ == "__main__":
    main()