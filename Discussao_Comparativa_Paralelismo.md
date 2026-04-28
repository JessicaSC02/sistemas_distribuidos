# Discussão Comparativa: Processamento Sequencial vs. Paralelo

## 1. Comparação entre Versão Sequencial e Paralela

Com base nos logs de execução gerados para as Partes A (Sequencial) e B (Paralela) processando o dataset `yellow_tripdata_2016-02.csv` (11.382.049 corridas particionadas em 114 blocos de 100.000 linhas), observamos os seguintes tempos na máquina de teste:

*   **Versão Sequencial (Parte A):** ~50,89 segundos.
*   **Versão Paralela (Parte B):** ~86,24 segundos.

Em uma primeira análise, pode parecer contraintuitivo que a versão paralela, utilizando múltiplos processos de CPU, tenha levado **mais tempo** que a versão sequencial de thread única. No entanto, este resultado é extremamente comum no processamento de dados e serve como uma vitrine perfeita para compreendermos o peso do overhead na computação distribuída.

---

## 2. Discussão de Vantagens, Overhead e Escalabilidade

### 2.1. O Problema do Overhead (Custo Extra)
A razão pela qual a versão paralela apresentou desempenho inferior à sequencial reside no alto **overhead de comunicação (IPC)** em contraste com o baixo custo das operações matemáticas da nossa função, somado ao limite de leitura de disco:
*   **Serialização de Dados (Pickle no IPC):** A arquitetura do `multiprocessing` no Python emula a paralelização rodando múltiplos interpretadores independentes. Para que o processo principal envie um "chunk" (100.000 listas de strings) para um *worker*, o Python precisa converter esses dados em fluxo de bytes (*pickling*) e trafegá-los entre espaços de memória dos processos. O tempo gasto serializando, enviando, recebendo e desserializando esse volume gigantesco de dados brutos foi maior do que o tempo que a CPU levaria para simplesmente fazer as somas matemáticas na thread principal.
*   **Gargalo de I/O (I/O Bound):** A extração do arquivo do disco está sendo feita sequencialmente em apenas um processo (na função geradora de leitura que divide os chunks). O disco só consegue entregar as informações a uma certa velocidade limite (gargalo de I/O). Dividir os dados após passarem pelo gargalo de leitura nem sempre melhora a vazão total, especialmente quando o processamento desses dados já é suficientemente rápido e não "segura" a leitura.

### 2.2. Vantagens do Paralelismo
Se neste cenário específico não obtivemos ganho de tempo, por que utilizamos computação paralela? 
*   **Capacidade de Processamento Massivo:** Permite destrancar o processamento atrelado a um único core (núcleo) da CPU, aproveitando 100% dos recursos modernos de hardware.
*   **Desacoplamento de Tarefas:** Aplica isolamento de memória, o que garante que cálculos sendo computados em pacotes diferentes não interfiram ou manipulem variáveis de forma conflituosa (evitando *Race Conditions* e a necessidade custosa de uso de *Locks*).

### 2.3. Escalabilidade
O uso do modelo "Divisão e Conquista" com paralelismo apresenta uma **escalabilidade fantástica** apenas quando a aplicação é de fato **CPU Bound** (ou seja, quando as limitações são derivadas do "esforço" do processador, e não da busca de dados no disco).

*   **Quando o cenário seria diferente?** Se, para cada corrida de táxi (linha do CSV), tivéssemos que calcular a rota mais curta via API do Google Maps, rodar um processamento pesado em Linguagem Natural (NLP) sobre eventuais comentários da viagem ou realizar treinamento e predições com algoritmos complexos de Machine Learning, o tempo de *Pickling* (Overhead) passaria a ser irrelevante se comparado ao custo do processamento matemático. Em tal contexto, a versão paralela esmagaria a versão sequencial.
*   **Melhorando a escalabilidade com dados:** Para escalar melhor com Dataframes e I/O, seria ideal que o paralelismo se iniciasse *antes* da leitura (com cada processo lendo uma fatia em bytes paralela do mesmo arquivo ou de arquivos separados em um cluster/HDFS distribuído). Em ecossistemas modernos (como PySpark ou Dask), as ferramentas otimizam automaticamente o gerenciamento de blocos mantendo-os nativamente próximos à CPU, minimizando significativamente o overhead que enfrentamos com o módulo padrão de `multiprocessing`.
