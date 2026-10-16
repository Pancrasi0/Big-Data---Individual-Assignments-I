import os
import random
import subprocess
import time
import matplotlib.pyplot as plt  # Importado para generar el gráfico

# Tamaños de prueba
sizes = [50, 100, 150, 200, 250]

# Listas para almacenar los tiempos de cada lenguaje
times_python = []
times_c = []
times_java = []

print("Compilando C...", flush=True)
compile_c = subprocess.run(
    ["gcc", "-O3", "matrix.c", "-o", "matrix_c"], capture_output=True, text=True
)
if compile_c.returncode != 0:
  print("❌ Error crítico al compilar C:", flush=True)
  print(compile_c.stderr)
  exit(1)

print("Compilando Java...", flush=True)
compile_java = subprocess.run(
    ["javac", "main.java"], capture_output=True, text=True
)
if compile_java.returncode != 0:
  print("❌ Error crítico al compilar Java:", flush=True)
  print(compile_java.stderr)
  exit(1)

print("¡Compilación exitosa!\n", flush=True)


def multiply_python(n):
  matrix_a = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]
  matrix_b = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]
  result = [[0] * n for _ in range(n)]

  start = time.time()
  for i in range(n):
    for j in range(n):
      for k in range(n):
        result[i][j] += matrix_a[i][k] * matrix_b[k][j]
  return time.time() - start


print("Iniciando benchmarks...", flush=True)

for n in sizes:
  print(f"--- Probando tamaño N = {n} ---", flush=True)

  # 1. Python
  t_py = multiply_python(n)
  times_python.append(t_py)
  print(f"     Python tardó: {t_py:.4f}s", flush=True)

  # 2. C
  res_c = subprocess.run(["./matrix_c", str(n)], capture_output=True, text=True)
  t_c = float(res_c.stdout.strip())
  times_c.append(t_c)
  print(f"     C tardó: {t_c:.6f}s", flush=True)

  # 3. Java (Usa 'main' en minúscula para que coincida con main.java)
  res_java = subprocess.run(
      ["java", "main", str(n)], capture_output=True, text=True
  )
  try:
    t_java = float(res_java.stdout.strip())
  except ValueError:
    t_java = 0.0
  times_java.append(t_java)
  print(f"     Java tardó: {t_java:.6f}s", flush=True)

# --- GENERAR Y GUARDAR EL GRÁFICO ---
plt.figure(figsize=(10, 6))
plt.plot(
    sizes, times_python, marker="o", label="Python (Interpretado)", color="red"
)
plt.plot(sizes, times_java, marker="s", label="Java (JIT Compilado)", color="orange")
plt.plot(sizes, times_c, marker="^", label="C (Optimizado -O3)", color="blue")

plt.title("Comparativa de Rendimiento: Multiplicación de Matrices O(n^3)")
plt.xlabel("Tamaño de la Matriz (N x N)")
plt.ylabel("Tiempo de Ejecución (Segundos)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()

# Guarda el gráfico en la carpeta actual
plt.savefig("matrix_benchmark.png", dpi=300)
print(
    "\n¡Benchmark completado con éxito y gráfico guardado como"
    " 'matrix_benchmark.png'!",
    flush=True,
)