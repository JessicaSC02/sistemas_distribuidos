# Processamento Distribuído de Big Data - Divisão e Conquista (Parte A)

Este repositório contém a implementação da **Parte A** do trabalho da disciplina de **Armazenamento e Processamento Massivo e Distribuído de Dados** do curso de Engenharia de Dados.

## 📝 Descrição do Projeto

O objetivo deste projeto é processar um dataset massivo (base pública de viagens de táxi de Nova York - `yellow_tripdata_2016-02.csv`) aplicando o paradigma de **Divisão e Conquista**. 

Na **Parte A**, construímos a **versão sequencial** que serve como *baseline* (referência) de desempenho. O script lê o arquivo original em blocos menores (*chunks*), calcula agregações estatísticas e combina os resultados parciais em um resultado final, tudo de forma linear.

### Métricas Calculadas:
- Quantidade total de corridas
- Distância total percorrida
- Valor total arrecadado
- Média de passageiros por corrida
- Maior e menor valor de corrida
- Distribuição de corridas por forma de pagamento
- Top 5 dias com maior volume de corridas

## ⚙️ Pré-requisitos

Para rodar este projeto, você precisará apenas do **Python 3.x** instalado na sua máquina.
Nenhuma biblioteca externa de terceiros (como `pandas` ou `numpy`) é necessária. O código foi desenvolvido utilizando a biblioteca padrão `csv` do Python, garantindo máxima compatibilidade e leveza.

## 🚀 Como Executar

1. Certifique-se de que o arquivo de dados `yellow_tripdata_2016-02.csv` está na mesma pasta que o script.
2. Abra o terminal (PowerShell, CMD ou o terminal do VS Code) na pasta do projeto.
3. Execute o comando:
   ```bash
   python parte_a.py
   ```

## 📊 O que esperar da Execução

- **Console:** Durante a execução, o script exibirá o progresso da leitura (bloco a bloco de 100.000 linhas). Ao final (que leva cerca de 50 segundos dependendo da máquina), um relatório com todos os indicadores consolidados aparecerá na tela.
- **Log:** Um arquivo chamado `log_execucao_ParteA.txt` será gerado automaticamente. Nele constam informações vitais para a avaliação, como o tempo exato de processamento, tamanho dos blocos e quantidade de blocos lidos.

## 📄 Outros Arquivos
- `Relatorio_Atividade_Paralelismo.md`: Detalhamento teórico sobre o contexto da prática e os objetivos da técnica de Divisão e Conquista.

## 🔗 Link Útil
- [Acesso ao Arquivo no Google Drive](https://drive.google.com/file/d/1HLbygYQv6nhD6eYHwHk-5IAZrk1ZoqYr/view?usp=sharing)
