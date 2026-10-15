# Monitoramento de Servidores em Tempo Real

## 1. Sobre o projeto

Este projeto é um dashboard de telemetria em tempo real para monitorar
servidores de TI. Ele foi desenvolvido com base na **Opção A ---
Monitoramento de Servidores de TI** do desafio prático.

A aplicação simula leituras de três servidores --- **Servidor A,
Servidor B e Servidor C** --- e registra os valores em um banco de dados
SQLite. O dashboard, desenvolvido com Streamlit, consulta esses
registros e apresenta indicadores e gráficos que ajudam a acompanhar as
variações das métricas ao longo do tempo.

## 2. Objetivo

Demonstrar uma arquitetura de monitoramento composta por dois processos
executados simultaneamente:

-   **Simulador (`simulador.py`):** gera leituras simuladas dos
    servidores e grava os dados no banco SQLite.
-   **Dashboard (`app.py`):** lê os dados armazenados e apresenta as
    informações em uma interface visual que se atualiza automaticamente.

> **Importante:** os valores apresentados são simulados pelo programa.
> Eles não são coletados de servidores físicos ou de uma infraestrutura
> real.

## 3. Tecnologias utilizadas

-   **Python:** linguagem utilizada para desenvolver o simulador e o
    dashboard.
-   **SQLite (`sqlite3`):** banco de dados local usado para armazenar as
    leituras.
-   **Streamlit:** framework utilizado para construir a interface web.
-   **Pandas:** biblioteca utilizada para carregar e organizar os dados
    em tabelas.
-   **Plotly Express:** biblioteca utilizada para criar os gráficos de
    linha.
-   **Bibliotecas padrão do Python:** `time`, `random` e `datetime`,
    utilizadas, respectivamente, para controlar os intervalos, gerar
    variações simuladas e registrar data e hora.

## 4. Estrutura do projeto

Os arquivos presentes no projeto são:

``` text
Monitoramento-de-Servidores-em-Tempo-Real/
├── app.py
├── simulador.py
├── Servidores.db
└── weg_icone.png
```

-   **`app.py`:** código do dashboard Streamlit.
-   **`simulador.py`:** código que gera as leituras e as grava no banco
    de dados.
-   **`Servidores.db`:** banco de dados SQLite utilizado pelo projeto.
-   **`weg_icone.png`:** imagem exibida na interface do dashboard.

O banco de dados e a imagem são referenciados por caminhos relativos no
código. Por isso, execute os comandos a partir da pasta do projeto.

## 5. Métricas monitoradas

O sistema registra quatro métricas para cada servidor:

  -----------------------------------------------------------------------
  Métrica                 Descrição               Unidade
  ----------------------- ----------------------- -----------------------
  Uso de CPU              Percentual simulado de  \%
                          utilização do           
                          processador             

  Uso de memória RAM      Percentual simulado de  \%
                          utilização da memória   

  Latência                Valor simulado de       ms
                          latência                

  Temperatura da CPU      Temperatura simulada do °C
                          processador             
  -----------------------------------------------------------------------

Os valores partem de referências iniciais definidas no simulador e
sofrem pequenas variações aleatórias a cada ciclo. Os valores de CPU e
memória são limitados ao intervalo de 0% a 100%.

## 6. Banco de dados

O banco SQLite utiliza a tabela `leituras_servidores`, com as seguintes
colunas:

  Coluna              Finalidade
  ------------------- ----------------------------------------------------
  `id`                Identificador único e incremental de cada registro
  `timestamp`         Data e hora da leitura
  `servidor_id`       Identificador do servidor monitorado
  `uso_cpu`           Uso simulado de CPU
  `uso_memoria`       Uso simulado de memória RAM
  `latencia`          Latência simulada
  `temperatura_cpu`   Temperatura simulada da CPU

O simulador configura o banco com `PRAGMA journal_mode=WAL;`. O modo WAL
permite que leituras e gravações ocorram com melhor concorrência,
reduzindo a possibilidade de o dashboard bloquear enquanto o simulador
grava novos dados. O código também utiliza um tempo limite de conexão e
trata ocorrências de `sqlite3.OperationalError`.

## 7. Funcionalidades do dashboard

### Indicadores por servidor

O painel apresenta os valores mais recentes de CPU, memória RAM,
latência e temperatura da CPU para cada servidor incluído no filtro.

### Filtro de servidor

A barra lateral permite escolher um servidor específico ou selecionar
**Todos**, alterando os indicadores, gráficos e registros apresentados.

### Controles da barra lateral

-   **Frequência de atualização:** permite definir o intervalo de
    atualização do dashboard entre 1 e 10 segundos.
-   **Histórico de leituras:** permite escolher a quantidade de
    registros consultados, entre 30 e 300.

### Gráficos temporais

O dashboard apresenta dois gráficos de linha com marcadores:

1.  Uso de CPU ao longo do tempo.
2.  Uso de memória RAM ao longo do tempo.

Os gráficos usam o horário como eixo horizontal e diferenciam os
servidores por cor quando mais de um está sendo exibido. Os eixos
possuem títulos para facilitar a leitura.

### Tabela de registros

A seção expansível **"Visualização Tabela de Registros"** apresenta os
dados carregados do banco, ordenados do mais recente para o mais antigo.

### Atualização automática

O dashboard aguarda o intervalo definido na barra lateral e executa
novamente a interface para consultar e exibir os dados atualizados. Para
que novos valores apareçam, o simulador precisa continuar em execução.

## 8. Instalação e execução

### Pré-requisitos

-   Python instalado.
-   Terminal ou prompt de comando.
-   Os arquivos do projeto reunidos na mesma pasta.

### Instalar as dependências

Abra o terminal na pasta do projeto e execute:

``` bash
python -m pip install streamlit pandas plotly
```

As bibliotecas `sqlite3`, `time`, `random` e `datetime` fazem parte da
biblioteca padrão do Python.

### Iniciar o simulador

Abra um terminal na pasta do projeto e execute:

``` bash
python simulador.py
```

O simulador cria a tabela caso ela ainda não exista, registra leituras
para os três servidores e repete o processo a cada dois segundos.

Mantenha esse terminal aberto enquanto estiver utilizando o dashboard.

### Iniciar o dashboard

Abra **outro terminal** na mesma pasta e execute:

``` bash
streamlit run app.py
```

O Streamlit disponibilizará o endereço local da aplicação no terminal.
Abra esse endereço no navegador.

**Os dois processos precisam permanecer em execução ao mesmo tempo:** o
simulador grava os dados e o dashboard os consulta.

## 9. Encerramento

Para encerrar o simulador, utilize `Ctrl + C` no terminal em que ele
está rodando. Para parar o dashboard, utilize `Ctrl + C` no terminal
correspondente.

## 10. Relação com os requisitos do desafio

O projeto foi desenvolvido para o tema **Opção A --- Monitoramento de
Servidores de TI** e contém os elementos previstos no desafio:

-   tabela SQLite com identificador, data/hora, servidor e métricas
    numéricas;
-   configuração do banco com `PRAGMA journal_mode=WAL;`;
-   simulação contínua de três servidores, com novas leituras a cada
    dois segundos;
-   dashboard Streamlit com título, imagem e layout `wide`;
-   controles na barra lateral para intervalo de atualização, quantidade
    de registros e filtro por servidor;
-   indicadores `st.metric` com os últimos valores;
-   dois gráficos temporais de linha feitos com Plotly Express;
-   seção expansível com os registros do banco;
-   atualização periódica com `time.sleep()` e `st.rerun()`.

O desafio também avalia a execução simultânea do simulador e do
dashboard, a interatividade dos filtros, a fluidez visual e a
organização do código. Esses aspectos devem ser verificados durante a
execução do projeto no ambiente utilizado.

## 11. Observação para execução em outro computador

No código atual de `app.py`, a configuração `page_icon` utiliza um
caminho absoluto de arquivo do computador em que o projeto foi
desenvolvido. Esse caminho pode não existir em outro computador. Caso o
Streamlit apresente erro nessa configuração, ajuste o caminho para um
arquivo de imagem disponível no ambiente ou utilize um ícone compatível
com a configuração do Streamlit.