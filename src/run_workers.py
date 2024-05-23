import multiprocessing
import subprocess
import time


def run_arq():
    """Run arq workers with the specified configuration in remote_worker.WorkerSettings."""
    subprocess.run(["arq", "src.remote_worker.WorkerSettings"])


def monitor_processes(processes: list[multiprocessing.Process]):
    """Check if one of the process died and restart it."""
    while True:
        for i, p in enumerate(processes):
            if not p.is_alive():
                print(f"Worker {i} died. Restarting.")
                new_p = multiprocessing.Process(target=run_arq)
                new_p.start()
                processes[i] = new_p
        time.sleep(2)


if __name__ == "__main__":
    num_cores = multiprocessing.cpu_count()
    processes = [multiprocessing.Process(target=run_arq) for _ in range(num_cores - 1)]

    for p in processes:
        p.start()

    monitor_processes(processes)
