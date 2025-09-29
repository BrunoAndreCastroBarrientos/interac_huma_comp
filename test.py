# consume_sync.py
import requests
import time
import statistics

URL = "http://54.89.139.69:8085/api/files/1.png"
N = 1000
TIMEOUT = 10  # segundos por petición
DELAY = 0.05  # segundos entre peticiones (ajusta para no saturar)

headers = {
    "User-Agent": "monitoring-test/1.0"
}

success = 0
fail = 0
times = []

for i in range(1, N+1):
    try:
        t0 = time.perf_counter()
        r = requests.get(URL, headers=headers, timeout=TIMEOUT)
        elapsed = time.perf_counter() - t0
        times.append(elapsed)
        if r.status_code == 200:
            success += 1
        else:
            fail += 1
            print(f"[{i}] status {r.status_code}")
    except Exception as e:
        fail += 1
        print(f"[{i}] error: {e}")
    # pequeña espera para ser responsable con el servidor
    time.sleep(DELAY)

print("\n--- Resumen ---")
print(f"Total requests: {N}")
print(f"Successful (200): {success}")
print(f"Failed: {fail}")
if times:
    print(f"Avg: {statistics.mean(times):.3f}s")
    print(f"Median: {statistics.median(times):.3f}s")
    print(f"P95: {statistics.quantiles(times, n=100)[94]:.3f}s")
    print(f"Min: {min(times):.3f}s  Max: {max(times):.3f}s")
