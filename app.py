import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
import time


# Configuração da página
st.set_page_config(
    page_title="Painel de Monitoramento de Servidores",
    page_icon=r"C:\Users\gabriel_silva206\Downloads\weg.png",
    layout="wide"
)


def carregar_dados(limite):

    conn = sqlite3.connect("Servidores.db", timeout=10)

    query = f'''
        SELECT
            timestamp,
            servidor_id,
            uso_cpu,
            uso_memoria,
            latencia,
            temperatura_cpu

        FROM leituras_servidores

        ORDER BY id DESC

        LIMIT {limite}
    '''

    df = pd.read_sql_query(query, conn)

    conn.close()

    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')

    return df

st.image("weg_icone.png", width=80)
st.title(" Monitoramento de Servidores em Tempo Real")


# Barra lateral
st.sidebar.header("Filtros e Controles")

intervalo_atualizacao = st.sidebar.slider(
    "Frequência de Atualização (segundos)",
    1,
    10,
    2
)

quantidade_registros = st.sidebar.slider(
    "Histórico de Leituras",
    30,
    300,
    120
)


df = carregar_dados(limite=quantidade_registros)


if df.empty:

    st.info(
        "Aguardando dados... "
        "Certifique-se de que o arquivo 'simulador.py' está rodando."
    )

else:

    servidores_disponiveis = df['servidor_id'].unique().tolist()

    servidor_selecionado = st.sidebar.selectbox(
        "Filtrar por Servidor:",
        ["Todos"] + servidores_disponiveis
    )


    if servidor_selecionado != "Todos":

        df_filtrado = df[
            df['servidor_id'] == servidor_selecionado
        ]

    else:

        df_filtrado = df


    # Indicadores dos últimos valores
    st.subheader("Últimas leituras registradas")

    ultimos = (
        df_filtrado
        .groupby('servidor_id')
        .last()
        .reset_index()
    )


    cols = st.columns(len(ultimos))


    for idx, row in ultimos.iterrows():

        with cols[idx]:

            st.markdown(f"### {row['servidor_id']}")

            st.metric(
                "Uso de CPU",
                f"{row['uso_cpu']} %"
            )

            st.metric(
                "Uso de Memória RAM",
                f"{row['uso_memoria']} %"
            )

            st.metric(
                "Latência",
                f"{row['latencia']} ms"
            )

            st.metric(
                "Temperatura da CPU",
                f"{row['temperatura_cpu']} °C"
            )


    st.markdown("---")


    # Gráficos dinâmicos
    col_g1, col_g2 = st.columns(2)


    with col_g1:

        fig_cpu = px.line(
            df_filtrado,
            x='timestamp',
            y='uso_cpu',
            color='servidor_id',
            title="Uso de CPU ao longo do tempo",
            markers=True
        )

        fig_cpu.update_xaxes(
            title_text="Horário"
        )

        fig_cpu.update_yaxes(
            title_text="Uso de CPU (%)"
        )

        st.plotly_chart(
            fig_cpu,
            use_container_width=True
        )


    with col_g2:

        fig_memoria = px.line(
            df_filtrado,
            x='timestamp',
            y='uso_memoria',
            color='servidor_id',
            title="Uso de Memória RAM ao longo do tempo",
            markers=True
        )

        fig_memoria.update_xaxes(
            title_text="Horário"
        )

        fig_memoria.update_yaxes(
            title_text="Uso de Memória (%)"
        )

        st.plotly_chart(
            fig_memoria,
            use_container_width=True
        )


    # Visualização de dados brutos
    with st.expander("Visualização Tabela de Registros"):

        st.dataframe(
            df_filtrado.sort_values(
                'timestamp',
                ascending=False
            ),
            use_container_width=True
        )


# Loop de atualização automática
time.sleep(intervalo_atualizacao)

st.rerun()