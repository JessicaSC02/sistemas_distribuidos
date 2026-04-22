# Relatório da Atividade: Processamento Distribuído com Divisão e Conquista

## Contexto da Prática
Este projeto lida com o processamento massivo de dados empregando um dataset público de viagens de táxi amarelo em Nova York (NYC Taxi and Limousine Commission - TLC). O arquivo utilizado (`yellow_tripdata_2016-02.csv`) possui características de Big Data, contendo aproximadamente 2GB e mais de 11 milhões de registros de corridas de táxi.

Diante do volume expressivo de informações, a estratégia aplicada é o modelo de **Divisão e Conquista** (Divide and Conquer), onde o problema maior é quebrado em frações menores e mais fáceis de processar.

## Objetivo da Atividade
O objetivo central da atividade é capacitar os alunos a trabalharem com técnicas que viabilizam o processamento de grandes volumes de dados através de estratégias eficientes de particionamento e computação paralela. 

Ao final da prática, espera-se que o aluno seja capaz de:

- **Aplicar o paradigma Divisão e Conquista:** estruturar a resolução de um problema de dados em etapas menores.
- **Particionar um arquivo CSV grande em blocos (chunks):** realizar leituras fatiadas (chunking) para evitar o esgotamento da memória RAM.
- **Executar processamento paralelo com Python:** implementar workers concorrentes para acelerar o processamento dos blocos.
- **Implementar a etapa de agregação (Combine):** juntar os resultados parciais obtidos por cada worker de forma a construir o resultado global e final.
- **Comparar versões Sequencial e Paralela:** estabelecer um baseline (Parte A) executado de forma sequencial para confrontar as métricas de tempo contra o processamento assíncrono e distribuído em múltiplos núcleos (Parte B).
- **Discutir vantagens, overhead e escalabilidade:** analisar criticamente em quais cenários o paralelismo de fato compensa, levando em consideração o custo atrelado à criação e gerenciamento de processos (overhead).

## Implementação - Parte A (Sequencial)
Como passo inicial, desenvolvemos a versão de referência (**Parte A**). O script `parte_a.py` foi programado para varrer todo o CSV utilizando a leitura segmentada em chunks. Neste momento:

1. **Dividir:** Lê o arquivo CSV segmentando-o em pequenos blocos (ex: 100 mil linhas).
2. **Conquistar:** Processa os dados iterativamente para extrair as métricas necessárias (distância total, valor total, maior e menor corrida, contagens de tipo de pagamento e agrupamento por dias).
3. **Combinar:** Unifica as informações computadas em cada bloco, alimentando um acumulador global.

Isso garante uma solução escalável na restrição de memória, gerando as métricas corretas e o log de execução, estabelecendo a base confiável para a avaliação posterior do paralelismo.
