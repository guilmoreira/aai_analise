import streamlit as st

def display_creator_info():
    st.title("Sobre o Criador")
    
    # Profile Information
    st.write("Olá! Meu nome é Guilherme, e desenvolvi esta página para facilitar a busca pelos escritórios e assessores de investimento cadastrados no Brasil.")
    st.write("Sinta-se à vontade para conectar-se comigo no LinkedIn para mais atualizações e projetos:")

    # Larger LinkedIn Button using HTML
    linkedin_button = """
    <a href="https://www.linkedin.com/in/guilmoreira/" target="_blank" style="text-decoration: none;">
        <div style="
            display: inline-block;
            padding: 15px 25px;
            margin-top: 20px;
            font-size: 20px;
            font-weight: bold;
            color: white;
            background-color: #0077b5;
            border-radius: 8px;
            text-align: center;
            ">
            Conectar no LinkedIn
        </div>
    </a>
    """
    st.markdown(linkedin_button, unsafe_allow_html=True)

    # Email Button using HTML
    email_button = """
    <a href="mailto:guilmoreira@outlook.com" style="text-decoration: none;">
        <div style="
            display: inline-block;
            padding: 15px 25px;
            margin-top: 20px;
            font-size: 20px;
            font-weight: bold;
            color: white;
            background-color: #34a853;
            border-radius: 8px;
            text-align: center;
            ">
            Enviar Email
        </div>
    </a>
    """
    st.markdown(email_button, unsafe_allow_html=True)

if __name__ == "__main__":
    display_creator_info()
