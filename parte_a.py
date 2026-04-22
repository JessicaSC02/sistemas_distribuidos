import csv
import time
from collections import defaultdict

CHUNK_SIZE = 100000

def process_chunk(chunk):
    """
    Processa um bloco de dados e retorna os resultados parciais (locais).
    """
    metrics = {
        'total_trips': 0,
        'total_distance': 0.0,
        'total_amount': 0.0,
        'total_passengers': 0,
        'max_amount': float('-inf'),
        'min_amount': float('inf'),
        'payment_types': defaultdict(int),
        'pickup_days': defaultdict(int)
    }

    for row in chunk:
        try:
            # Pula linhas mal formatadas
            if len(row) < 19:
                continue

            # Índices das colunas baseados no cabeçalho:
            # 1: tpep_pickup_datetime
            # 3: passenger_count
            # 4: trip_distance
            # 11: payment_type
            # 18: total_amount

            pickup_datetime = row[1]
            # Extrai apenas a data (ignorando a hora) assumindo formato "YYYY-MM-DD HH:MM:SS"
            pickup_day = pickup_datetime.split(' ')[0] 
            
            passenger_count = int(row[3]) if row[3] else 0
            trip_distance = float(row[4]) if row[4] else 0.0
            payment_type = row[11]
            total_amount = float(row[18]) if row[18] else 0.0

            # Atualiza métricas
            metrics['total_trips'] += 1
            metrics['total_distance'] += trip_distance
            metrics['total_amount'] += total_amount
            metrics['total_passengers'] += passenger_count
            
            if total_amount > metrics['max_amount']:
                metrics['max_amount'] = total_amount
            if total_amount < metrics['min_amount']:
                metrics['min_amount'] = total_amount
                
            metrics['payment_types'][payment_type] += 1
            metrics['pickup_days'][pickup_day] += 1
            
        except ValueError:
            # Ignora erros de conversão nesta linha
            continue

    # Ajusta os infinitos se o chunk não teve valores numéricos válidos
    if metrics['max_amount'] == float('-inf'):
        metrics['max_amount'] = 0.0
    if metrics['min_amount'] == float('inf'):
        metrics['min_amount'] = 0.0

    return metrics

def combine_results(global_metrics, local_metrics):
    """
    Combina os resultados locais de um chunk com os resultados globais.
    """
    if global_metrics is None:
        return local_metrics

    global_metrics['total_trips'] += local_metrics['total_trips']
    global_metrics['total_distance'] += local_metrics['total_distance']
    global_metrics['total_amount'] += local_metrics['total_amount']
    global_metrics['total_passengers'] += local_metrics['total_passengers']
    
    global_metrics['max_amount'] = max(global_metrics['max_amount'], local_metrics['max_amount'])
    global_metrics['min_amount'] = min(global_metrics['min_amount'], local_metrics['min_amount'])
    
    for pt, count in local_metrics['payment_types'].items():
        global_metrics['payment_types'][pt] += count
        
    for pd, count in local_metrics['pickup_days'].items():
        global_metrics['pickup_days'][pd] += count

    return global_metrics

def main():
    print("Iniciando processamento da Parte A (Sequencial)...")
    start_time = time.time()
    
    filepath = 'yellow_tripdata_2016-02.csv'
    
    global_metrics = None
    
    with open(filepath, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        try:
            header = next(reader)
        except StopIteration:
            print("Arquivo vazio.")
            return
            
        chunk = []
        chunk_count = 0
        
        # Leitura em blocos
        for row in reader:
            chunk.append(row)
            if len(chunk) >= CHUNK_SIZE:
                chunk_count += 1
                print(f"Processando chunk {chunk_count} ({CHUNK_SIZE} linhas)...")
                
                # Processamento independente
                local_metrics = process_chunk(chunk)
                
                # Agregação global
                global_metrics = combine_results(global_metrics, local_metrics)
                
                chunk = []
                
        # Processa as linhas restantes
        if chunk:
            chunk_count += 1
            print(f"Processando chunk final {chunk_count} ({len(chunk)} linhas)...")
            local_metrics = process_chunk(chunk)
            global_metrics = combine_results(global_metrics, local_metrics)

    end_time = time.time()
    execution_time = end_time - start_time
    
    if global_metrics is None or global_metrics['total_trips'] == 0:
        print("Nenhum dado válido encontrado.")
        return

    # Cálculos finais
    avg_passengers = global_metrics['total_passengers'] / global_metrics['total_trips']
    
    # Top 5 dias com mais corridas
    top_5_days = sorted(global_metrics['pickup_days'].items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Apresentação dos Resultados
    print("\n" + "="*40)
    print("           RESULTADOS GLOBAIS           ")
    print("="*40)
    print(f"Quantidade total de corridas: {global_metrics['total_trips']:,}")
    print(f"Distância total percorrida: {global_metrics['total_distance']:,.2f} milhas")
    print(f"Valor total arrecadado: ${global_metrics['total_amount']:,.2f}")
    print(f"Média de passageiros por corrida: {avg_passengers:.2f}")
    print(f"Maior valor de corrida: ${global_metrics['max_amount']:,.2f}")
    print(f"Menor valor de corrida: ${global_metrics['min_amount']:,.2f}")
    
    print("\nQuantidade de corridas por forma de pagamento (payment_type):")
    for pt, count in sorted(global_metrics['payment_types'].items()):
        print(f"  Tipo {pt}: {count:,}")
        
    print("\nTop 5 dias com mais corridas:")
    for i, (day, count) in enumerate(top_5_days, 1):
        print(f"  {i}º: {day} ({count:,} corridas)")
        
    print(f"\nTempo total de execução: {execution_time:.2f} segundos")
    print("="*40)

    # Geração do log
    with open('log_execucao_ParteA.txt', 'w', encoding='utf-8') as log:
        log.write("--- Log de Execucao Parte A (Sequencial) ---\n")
        log.write(f"Tempo total de execucao: {execution_time:.2f} segundos\n")
        log.write(f"Total de blocos (chunks) processados: {chunk_count}\n")
        log.write(f"Tamanho de cada bloco (chunksize): {CHUNK_SIZE} linhas\n")
        log.write(f"Total de corridas lidas: {global_metrics['total_trips']}\n")

if __name__ == '__main__':
    main()
