# Orquestrador do pipeline
from pathlib import Path

raiz = Path(__file__).resolve().parent.parent
pasta_src = Path(__file__).resolve().parent

# Scripts na ordem de execução
scripts = [
    "00_carga_raw_vendas.py",
    "01_leitura_dados.py",
    "02_etl_vendas.py",
    "03_estatistica.py",
]

for script in scripts:
    print(f"\n>>> Executando {script}...")
    caminho = pasta_src / script
    codigo = caminho.read_text(encoding="utf-8")
    exec(compile(codigo, str(caminho), "exec"),
         {"__file__": str(caminho), "__name__": "__main__"})

print("\nPipeline finalizado com sucesso.")