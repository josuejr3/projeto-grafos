### APLICAÇÃO DE TEORIA DOS GRAFOS PARA COMPREENSÃO EPIDEMIOLÓGICA 📊🧬🔵🟢🟡

### Avalição retrospectiva dos casos de Leishmaniose Visceral na Paraíba no período de 2015 a 2024
---

Projeto final da disciplina "Teoria dos Grafos" como requisito parcial para conslusão da disciplina.

Este projeto teve como objetivo utilizar as técnicas adquiridas durante a disciplina para compreender
quadro de Leishmaniose Visceral no estado da Paraíba e nas regiões que à compõe durante o período de **2015-2024**

> TECNOLOGIAS UTILIZADAS
- Python
- NetworkxX
- Matplotlib
- Pandas
- Chardet

> REQUISITOS PARA EXECUÇÃO
- Instalação das bibliotecas
- mesoregioes.json
- Dataset em formato csv no diretorio data/processed/
- Exemplos de dataset: https://datasus.saude.gov.br/transferencia-de-arquivos/

<p align="center">
<img src="https://github.com/user-attachments/assets/0872fec0-81d3-40f8-81c5-730dcfb734a3" alt="Download dataset" width=500 height=500/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/b1334c34-073c-4c97-9571-f3de622a3645" alt="Tabwin" width=700 height=200>
</p>

- A formatação de cada arquivo csv deve ser do tipo (identifição_da_doenca)(útimos dígitos do ano).csv
  - **Ex: LEIV22.csv**
    
- As tabelas devem estar com codificação utf-8

> OBJETIVOS
- Construir um grafo com todas as cidades da Paraíba que tiveram casos notificados de LV no período de **2015-2024**;
  <p align="center">
    <img src="https://github.com/user-attachments/assets/74fffdf2-742e-4ff0-b2b8-63e47d9112a9" alt="Grafo da Paraíba" width=500 height=500/>
  </p>
- Construir um grafo para cada uma das quatro regiões: Agreste, Borborema, Sertão e Zona da Mata, no intervalo de análise do estudo;
<p align="center">
  <img src="https://github.com/user-attachments/assets/b99dcdd4-f5db-4580-9688-c5e26e4cfb14" alt="Grafo do Agreste" width=500 height=500/>
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/36fe5fcb-0db0-4010-820d-66ed6c92a8e5" alt="Grafo da Borborema" width=500 height=500/>
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/6f342c79-f120-4e64-b937-4a4ca418a8eb" alt="Grafo do Sertão" width=500 heigh=500/>
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/60210008-90e6-4f1b-9c27-836b560fa547" alt="Grafo da Zona da Mata" width=500 height=500/>
</p>

- Identificar os anos mais influentes para prevalência e incidência da doença no estado através da centralidade de autovetor;

<p align="center">
  <img src="https://github.com/user-attachments/assets/f25654ae-b1cd-4f95-869a-398f83f78307" alt="Gráfico de Barras - CA" width=500 height=500/>
</p>

- Detectar por região se durante algum período de tempo não houve casos notificados da doença utilizando centralidade de proximidade;

<p align="center">
  <img src="https://github.com/user-attachments/assets/28377ed6-c70d-4803-a3e8-205c1c1d3a4d" alt="Gráfico de Barras - CP" width=500 height=500/>
</p>

- Verificar como cada uma das regiões contribuiu para o percentual de casos notificados na Paraíba durante o tempo determinado no estudo utilizando
  a cardinalidade de grau.

  <p align="center">
    <img src="https://github.com/user-attachments/assets/009ab851-c93e-402b-bbcf-af831bee1d05" alt="Gráfico de Setor - CD" width=500 height=500/>
  </p>



