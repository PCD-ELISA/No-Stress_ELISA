import streamlit as st
import pandas as pd
from processa_dados import layout_para_dataframe
from processa_dados import remove_celulas_vazias
from processa_dados import recebe_arquivo
from processa_dados import separa_namostra
from gera_graficos import plot_absorbancia
import traceback
import io
from PIL import Image

#Deixar barra de opções invisível
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Inicializa a sessão (se não existir)
if "pagina" not in st.session_state:
    st.session_state.pagina = "Início"

# Sidebar com botões
st.sidebar.button("Início", on_click=lambda: st.session_state.update({"pagina": "Início"}))
st.sidebar.button("Como usar", on_click=lambda: st.session_state.update({"pagina": "Como usar"}))
st.sidebar.button("Gráfico", on_click=lambda: st.session_state.update({"pagina": "Gráfico"}))
st.sidebar.button("Código", on_click=lambda: st.session_state.update({"pagina": "Código"}))


# Mostra conteúdo com base no estado
if st.session_state.pagina == "Início":
    #Cabeçalho
    st.markdown("<h1 style='text-align: center;'>No-Stress Elisa</h1>", unsafe_allow_html=True)
    st.subheader('Você poderá analisar com precisão dados do leitor de placas "Elisa" automaticamente')
    st.markdown("---", unsafe_allow_html=True)
    #Explicar sobre Elisa
    st.header(" 🡆 O que é um Leitor de placas Elisa?")
    col1, col2 = st.columns([1, 2])
    with col1:
            st.image(
            "images/elisa.png",
            caption="Leitor de placas ELISA moderno",
            width=200
            )
    with col2:
            st.markdown("")
            st.markdown("")
            st.markdown(
                """
                O leitor de Elisa (Enzyme-Linked Immunosorbent Assay) é um instrumento laboratorial
                que usa uma placa de 96 poços de microtitulação. Luz de um comprimento de onda específico
                incide em cada poço e, através da diferença entre a luz emitida e detectada, é medida
                a absorbância ou fluorescência com alta precisão.
                """)
    st.markdown("<h3 style='text-align: center;'>Aplicações</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1.28, 1, 1])
    with col1:
            st.markdown("""
                🔬 **Diagnóstico médico**  
                - Detecção de anticorpos e antígenos
                - Testes para HIV, hepatite, COVID-19
                - Diagnóstico de doenças autoimunes
                        """)
    with col2:
            st.markdown("""
                🧪 **Pesquisa científica**  
                - Quantificação de proteínas
                - Estudos imunológicos
                - Análise de sinalização celular
                        """)
    with col3:
            st.markdown("""
                🏭 **Controle de qualidade**  
                - Indústria farmacêutica
                - Segurança alimentar
                - Monitoramento ambiental                  
                """)
    
    st.markdown("---", unsafe_allow_html=True)
    #Falar sobre a equipe
    st.header("Equipe:")
    equipe = [
        {
            "nome": "Jõao Roberto B. K. Cruz",
            "resumo": "Resumo",
            "imagem": "images/matheus_velloso.jpg",
            "link": "https://github.com/RobertJbkc"
        },
        {
            "nome": "Lucas Candinho",
            "resumo": "Cursando bacharelado em ciência e tecnologia na Ilum - Escola de Ciência ",
            "imagem": "images/lucas_candinho.jpg",
            "link": "https://github.com/LucasCandinho"
        },
        {
            "nome": "Matheus P. Velloso da Silveira",
            "resumo": "Cursando bacharelado em ciência e tecnologia na Ilum - Escola de Ciência ",
            "imagem": "images/matheus_velloso.jpg",
            "link": "https://github.com/Velky2"
        }
    ]
    cols2 = st.columns(3)

    for col, pessoa in zip(cols2, equipe):
        with col:
            st.image(
                pessoa["imagem"], 
                width=250, 
                caption=None, 
                use_container_width=False
            )
            st.markdown(f"### {pessoa['nome']}")
            st.markdown(f"<p style='text-align: justify;'>{pessoa['resumo']}</p>", unsafe_allow_html=True)
            st.markdown(
    f'<a href="{pessoa["link"]}" target="_blank">'
    '<img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="50">'
    '</a>',
    unsafe_allow_html=True
)
            
elif st.session_state.pagina == "Como usar":
    st.markdown("<h1 style='text-align: center;'>Como usar</h1>", unsafe_allow_html=True)
    st.subheader("Aprenda a utilizar nossa ferramenta de forma simples")
    st.markdown("---", unsafe_allow_html=True)

elif st.session_state.pagina == "Gráfico":
    st.markdown("<h1 style='text-align: center;'>Gráfico</h1>", unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)
    radio_btn = st.radio("Qual tipo de gráfico?", options=("Barra", "Linha"))    
    file = st.file_uploader("**1)** Faça o upload de seu arquivo:", type=["xlsx"])
    st.markdown("**2)** Selecione o contido em cada poço")

    # Definindo as linhas e colunas da placa
    rows = list("ABCDEFGH")
    cols = [str(i) for i in range(1, 13)]

    # Inicializar a matriz se ainda não estiver na sessão
    if "elisa_matrix" not in st.session_state:
        st.session_state.elisa_matrix = pd.DataFrame("", index=rows, columns=cols)

    # Mostrar a matriz editável
    edited_matrix = st.data_editor(
        st.session_state.elisa_matrix,
        use_container_width=True,
        num_rows="fixed",
        hide_index=False
    )

    # Botão de salvar alterações
    if st.button("💾 Salvar alterações"):
        st.session_state.elisa_matrix = edited_matrix.fillna("")
        st.success("Concentrações atualizadas!")

    # Mostrar matriz salva
    with st.expander("📊 Ver matriz final"):
        st.dataframe(st.session_state.elisa_matrix, use_container_width=True)

    # Exportar como CSV
    st.download_button(
        label="📥 Baixar como CSV",
        data=st.session_state.elisa_matrix.to_csv().encode("utf-8"),
        file_name="matriz_elisa.csv",
        mime="text/csv"
    )
    st.markdown("Ou faça upload das informações:")
    dados = st.file_uploader("""Obs.: O Excel deverá ter informações de A a H representando as linhas da placa 
                             e de 1 a 12 representando as colunas""", type=["xlsx"])
    st.markdown("**3)** Veja o gráfico de barra do seu Elisa:")
    
    if st.button("📶 Plotar gráfico"):
        try:
            if file is None:
                st.error("⚠️ Por favor, envie o arquivo principal (leitor de placas)")
                raise ValueError("Arquivo principal não enviado")
            
            elif dados is not None:
                #Matriz do Excel
                try:
                    data = pd.read_excel(dados, header=None)
                    data.columns = list("ABCDEFGH")[:data.shape[1]]
                    data.index = range(1, data.shape[0] + 1)
                    layout = {}
                    for coluna in data.columns:
                        for linha in data.index:
                            valor = str(data.loc[linha, coluna]).strip()
                            if valor not in ["", "nan", "0", "None"]:
                                posicao = f"{coluna}{linha}"
                                if valor not in layout:
                                    layout[valor] = [posicao]
                                else:
                                    layout[valor].append(posicao)
                    
                    data_info = [[k] + v for k, v in layout.items()]
                    st.success("Dados processados com sucesso!")
        
                except Exception as e:
                    st.error(f"Erro ao processar arquivo: {str(e)}")
                
            else:
                # Matriz Analógica
                if st.session_state.elisa_matrix.empty:
                    st.error("⚠️ A matriz está vazia. Preencha ou envie um arquivo.")
                    raise ValueError("Matriz vazia")
                
                layout = {}
                for i in rows:
                    for j in cols:
                        tmp = st.session_state.elisa_matrix.loc[i, j]
                        if pd.isna(tmp) or str(tmp).strip() in ["", "0", "None", "-"]:
                            continue
                        if tmp not in layout:
                            layout[tmp] = [f"{i}{j}"]
                        else:
                            layout[tmp].append(f"{i}{j}")
                data_info = [[k] + v for k, v in layout.items()]
                st.success("Dados da Matriz carregados com sucesso!")
                
            #Processar dados

            layout = layout_para_dataframe(data_info)
            dados_amostrais = remove_celulas_vazias(recebe_arquivo(file))[1]
            dados_df = separa_namostra(layout, dados_amostrais)

            #Plotar gráficos
            if radio_btn == "Barra":
                imagem_grafico = plot_absorbancia(dados_df, "barra")
                st.image(
                        imagem_grafico,
                        width=800
                        )
                buf = io.BytesIO()
                imagem_grafico.save(buf, format="PNG")
                buf.seek(0)
    
                st.download_button(
                    label="📥 Baixar gráfico como PNG",
                    data=buf,
                    file_name="grafico_absorbancia_barra.png",
                    mime="image/png"
                )

            elif radio_btn == "Linha":
                imagem_grafico = plot_absorbancia(dados_df, "linha")
                st.image(
                        imagem_grafico,
                        width=800
                        )
                buf = io.BytesIO()
                imagem_grafico.save(buf, format="PNG")
                buf.seek(0)
    
                st.download_button(
                    label="📥 Baixar gráfico como PNG",
                    data=buf,
                    file_name="grafico_absorbancia_linha.png",
                    mime="image/png"
                )

        except Exception:
             st.markdown("Não foi possível plotar seu gráfico. Verifique se os arquivos correspondem ao solicitado")
             print(traceback.format_exc())
             

elif st.session_state.pagina == "Código":
    code = """
    #Colocar o código aqui

    """
    st.code(code, language="python")