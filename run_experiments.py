import subprocess
import re
import csv

tests = [
    (2, 100000),
    (4, 100000),
    (8, 100000),
    (10, 100000),
    (20, 100000),
    (8, 10000),
    (8, 500000)
]

with open("resultados_experimento.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Processos", "ChunkSize", "Tempo(s)"])

for p, c in tests:
    print(f"Executando com {p} processos e chunk {c}...")
    result = subprocess.run(["python", "parte_b.py", str(p), str(c)], capture_output=True, text=True)
    match = re.search(r"Tempo total de execu[cç][aã]o:\s*([\d\.]+)", result.stdout, re.IGNORECASE)
    if match:
        tempo = match.group(1)
        print(f"  -> {tempo} segundos")
        with open("resultados_experimento.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([p, c, tempo])
    else:
        print("  -> Tempo não encontrado.")
        print(result.stdout)
