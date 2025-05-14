import streamlit as st
from utils.gemini_client import GeminiClient

# Configuração inicial da página
st.set_page_config(
    page_title="💼 Gemini Pro - Business Edition",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS - Design Profissional Corporativo
st.markdown("""
<style>
:root {
    --primary-color: #2563eb;
    --secondary-color: #1e40af;
    --background-color: #f8fafc;
    --card-color: #ffffff;
    --text-color: #1e293b;
    --light-text: #64748b;
    --border-color: #e2e8f0;
    --success-color: #10b981;
    --font: 'Segoe UI', Roboto, sans-serif;
}

.stApp {
    background-color: var(--background-color);
    color: var(--text-color);
    font-family: var(--font);
}

/* Header Estilizado */
.stMarkdown h1 {
    color: var(--primary-color) !important;
    font-weight: 600 !important;
    margin-bottom: 0.5rem !important;
    border-bottom: 2px solid var(--border-color);
    padding-bottom: 0.5rem;
}

/* Input Field Moderno */
.stTextInput input {
    background-color: var(--card-color) !important;
    color: var(--text-color) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);
}

.stTextInput label {
    color: var(--light-text) !important;
    font-weight: 500 !important;
}

/* Botão Primário */
.stButton>button {
    background-color: var(--primary-color) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}

.stButton>button:hover {
    background-color: var(--secondary-color) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
}

/* Mensagens de Chat Profissionais */
.stChatMessage {
    border-radius: 12px !important;
    margin: 12px 0 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    max-width: 85% !important;
}

.stChatMessage.user {
    background-color: var(--card-color) !important;
    border-left: 4px solid var(--light-text) !important;
    margin-left: auto !important;
}

.stChatMessage.assistant {
    background-color: var(--card-color) !important;
    border-left: 4px solid var(--primary-color) !important;
}

/* Container de Erro Estilizado */
.stAlert {
    border-radius: 8px !important;
    border-left: 4px solid var(--primary-color) !important;
}

/* Efeitos de Foco */
.stTextInput input:focus {
    border-color: var(--primary-color) !important;
    box-shadow: 0 0 0 2px rgba(37,99,235,0.2) !important;
}

/* Layout Responsivo */
@media (max-width: 768px) {
    .stChatMessage {
        max-width: 100% !important;
    }
}
</style>
""", unsafe_allow_html=True)

def main():
    # Header Corporativo
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
            <h1 style="margin: 0; color: #2563eb;">Gemini Pro</h1>
            <span style="background-color: #e0e7ff; color: #2563eb; padding: 0.25rem 0.75rem; 
                        border-radius: 9999px; font-size: 0.875rem; font-weight: 500;">Business Edition</span>
        </div>
        <p style="color: #64748b; margin: 0;">Powered by Google AI • Enterprise-ready solution</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Barra de Status
    st.markdown("""
    <div style="background-color: #ffffff; padding: 0.75rem 1rem; border-radius: 8px; 
                margin-bottom: 1.5rem; display: flex; justify-content: space-between;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-left: 4px solid #2563eb;">
        <div>
            <span style="font-weight: 500;">Status:</span>
            <span style="color: #10b981; font-weight: 500;"> Operational</span>
        </div>
        <div>
            <span style="font-weight: 500;">Version:</span>
            <span> 2.1.0</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        client = GeminiClient()
    except Exception as e:
        with st.container():
            st.error(f"Configuration Error: {str(e)}")
            st.markdown("""
            <div style="background-color: #ffffff; padding: 1rem; border-radius: 8px; 
                        margin-top: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                        border-left: 4px solid #2563eb;">
                <h4 style="color: #2563eb; margin-top: 0;">Troubleshooting Guide:</h4>
                <ol style="color: #1e293b;">
                    <li>Create <code>/env/.env</code> in project root</li>
                    <li>Add: <code>GEMINI_API_KEY=your_api_key_here</code></li>
                    <li>Restart the server</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
        st.stop()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Container de Conversação
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.markdown(f"<div style='color: #1e293b;'>{message['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='color: #1e293b; padding-left: 12px;'>
                        {message['content']}
                        <div style='margin-top: 8px; font-size: 0.875rem; color: #64748b; 
                                    display: flex; align-items: center; gap: 4px;'>
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="#64748b" stroke-width="2"/>
                                <path d="M12 6V12L16 14" stroke="#64748b" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                            Generated by Gemini Pro
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Input Field com Estilo Profissional
    input_container = st.container()
    with input_container:
        col1, col2 = st.columns([6, 1])
        with col1:
            prompt = st.chat_input("Type your business query here...", key="input")
        with col2:
            st.markdown("""
            <style>
                .stChatInputContainer {
                    margin-top: 1rem;
                }
            </style>
            """, unsafe_allow_html=True)
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(f"<div style='color: #1e293b;'>{prompt}</div>", unsafe_allow_html=True)
        
        with st.chat_message("assistant"):
            try:
                with st.spinner("Analyzing..."):
                    response = client.generate_text(prompt)
                    st.markdown(f"""
                    <div style='color: #1e293b; padding-left: 12px;'>
                        {response}
                        <div style='margin-top: 8px; font-size: 0.875rem; color: #64748b; 
                                    display: flex; align-items: center; gap: 4px;'>
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M9 12L11 14L15 10M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="#64748b" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                            Verified by Google AI
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")

if __name__ == "__main__":
    main()