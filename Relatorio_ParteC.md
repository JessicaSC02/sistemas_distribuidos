# Relatório Parte C: Análise de Desempenho e Processamento Paralelo

## 1. Objetivo
Analisar os resultados obtidos nas Partes A (Versão Sequencial) e B (Versão Paralela) do trabalho de Processamento Distribuído, focando em avaliar o impacto do paralelismo no processamento de uma grande base de dados (arquivo `yellow_tripdata_2016-02.csv`), discutindo os tempos de execução, a influência de parâmetros como tamanho de *chunk* e o custo de uso de múltiplos processos.

## 2. Resumo de Tempos de Execução

Os testes foram realizados em uma máquina padrão utilizando o script fornecido. O arquivo possui aproximadamente 11,3 milhões de registros. A versão sequencial processou o arquivo em cerca de 50.89 segundos. Em seguida, diferentes configurações da versão paralela foram testadas:

| Versão | Nº de Processos | Tamanho do *Chunk* | Tempo de Execução |
| --- | :---: | :---: | :---: |
| **Sequencial (Parte A)** | **1** | **100.000** | **~50.89 s** |
| Paralela (Parte B) | 2 | 100.000 | 85.32 s |
| Paralela (Parte B) | 4 | 100.000 | 84.21 s |
| Paralela (Parte B) | 8 | 100.000 | 83.80 s |
| Paralela (Parte B) | 10 | 100.000 | 79.40 s |
| Paralela (Parte B) | 20 | 100.000 | 84.88 s |
| Paralela (Parte B) | 8 | 10.000 | 64.43 s |
| Paralela (Parte B) | 8 | 500.000 | 110.11 s |

## 3. Interpretação dos Resultados e Comparação

**A versão paralela foi mais rápida?**
Não. Contrariando a intuição inicial, a versão paralela foi consideravelmente **mais lenta** que a versão sequencial para o mesmo cenário base. A execução sequencial levou ~50.89 segundos, enquanto os tempos paralelos variaram entre 64.43s e 110.11s. 

**Por que a versão sequencial teve melhor desempenho?**
A leitura de um arquivo CSV e a soma simples de seus valores são operações muito rápidas para a CPU. Este problema é tipicamente caracterizado como **I/O Bound** (limitado pela leitura do disco) e não **CPU Bound** (limitado por processamento).
Na implementação atual da Parte B, um único processo principal lê o arquivo inteiro, agrupa as linhas em *chunks* e as envia para os processos trabalhadores por meio de canais de comunicação (`multiprocessing.Pool.imap_unordered`). Isso exige que cada linha lida seja **serializada (Pickling)**, enviada para outro processo, desserializada, processada e depois os resultados são re-serializados e enviados de volta ao processo principal. 
Esse gargalo de *Inter-Process Communication* (IPC) superou enormemente o tempo de processamento em si. A CPU gasta mais tempo gerenciando a passagem de dados entre processos do que efetivamente somando os números.

**O tamanho do *chunk* influenciou?**
Sim, o tamanho do *chunk* mostrou influência substancial no desempenho:
* Quando o *chunk* foi muito grande (500.000 linhas), o tempo subiu consideravelmente (110.11s). Isso ocorre pois blocos massivos estouram a memória de cache local do processador (e exigem alocações massivas em RAM do processo worker de uma só vez), além de desequilibrar a divisão de tarefas (menos *chunks* disponíveis para serem pegos dinamicamente pelos workers).
* Quando o *chunk* foi menor (10.000 linhas), o tempo caiu para 64.43s. Um *chunk* menor provou ter um impacto de alocação/serialização menor ou preencheu o *pipeline* de despacho para os workers de modo mais responsivo, diminuindo o uso de pico de memória de um único worker. Contudo, *chunks* exageradamente pequenos eventualmente aumentariam ainda mais o *overhead* de comunicação.

**Houve custo extra de criação de processos?**
Sim. No teste em que configuramos 20 processos, o tempo aumentou para 84.88s (pior que com 10 processos, que foi 79.40s). Criar processos em sistemas operacionais consome processamento (alocação de espaço de memória separado, overhead do S.O. para escalonamento). Além disso, múltiplos processos começaram a competir pelo uso do sistema sem conseguir se manter ocupados (já que todos aguardavam o gerador central ler o CSV na *thread* principal). 

## 4. Conclusão: Em que cenário a paralelização compensa?

A paralelização usando `multiprocessing` compensa quando a tarefa é primariamente **CPU Bound** (com alta complexidade computacional associada a cada fatia de dados) ou quando não há a necessidade de repassar enormes quantidades de dados através do IPC. 

Se o processo das corridas de táxi envolvesse aplicar rotinas complexas de *machine learning*, criptografia pesada, renderização de vídeo para cada viagem, ou conversão profunda em texto, o custo de IPC seria irrisório em comparação ao ganho com CPUs simultâneas computando intensamente. 
Para manipulação direta de texto grande sem carga na CPU (I/O Bound), paralelizar dessa forma adiciona *overhead* desnecessário. Como alternativa, estratégias que envolvam as próprias fatias independentes (*workers*) abrirem o arquivo diretamente do disco e pularem (via comando `seek`) para sua parte de leitura resultariam em desempenho melhor, aliviando o processo principal da leitura centralizada.
