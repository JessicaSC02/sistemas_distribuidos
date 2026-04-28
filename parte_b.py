import csv
import time
from collections import defaultdict
import multiprocessing

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

            pickup_datetime = row[1]
            pickup_day = pickup_datetime.split(' ')[0] 
            
            passenger_count = int(row[3]) if row[3] else 0
            trip_distance = float(row[4]) if row[4] else 0.0
            payment_type = row[11]
            total_amount = float(row[18]) if row[18] else 0.0

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
            continue

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

def chunk_reader(filepath, chunk_size):
    with open(filepath, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            next(reader)
        except StopIteration:
            return
            
        chunk = []
        for row in reader:
            chunk.append(row)
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []
                
        if chunk:
            yield chunk

def main():
    print("Iniciando processamento da Parte B (Paralela)...")
    start_time = time.time()
    
    filepath = 'yellow_tripdata_2016-02.csv'
    
    global_metrics = None
    chunk_count = 0
    
    num_processes = multiprocessing.cpu_count()
    print(f"Utilizando {num_processes} processos paralelos.")
    
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Usa imap_unordered para iterar sobre os chunks paralelamente
        for local_metrics in pool.imap_unordered(process_chunk, chunk_reader(filepath, CHUNK_SIZE)):
            chunk_count += 1
            print(f"Chunk {chunk_count} processado e agregado.")
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
    with open('log_execucao_ParteB.txt', 'w', encoding='utf-8') as log:
        log.write("--- Log de Execucao Parte B (Paralela) ---\n")
        log.write(f"Tempo total de execucao: {execution_time:.2f} segundos\n")
        log.write(f"Total de blocos (chunks) processados: {chunk_count}\n")
        log.write(f"Tamanho de cada bloco (chunksize): {CHUNK_SIZE} linhas\n")
        log.write(f"Total de corridas lidas: {global_metrics['total_trips']}\n")
        log.write(f"Numero de processos utilizados: {num_processes}\n")

if __name__ == '__main__':
    main()
