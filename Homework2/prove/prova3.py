import multiprocessing
import time

def slow_function():
    print("Starting slow function...")
    time.sleep(1)  # Simulating a slow operation
    print("Slow function completed.")

if __name__ == '__main__':
    print("Main program started.")
    
    process = multiprocessing.Process(target=slow_function, args=())
    print("Process created.")
    
    process.start()  # This starts the slow_function in a new process
    print("Process started.")
    
    time.sleep(5)  # Simulating a slow operation
    process.join()  # This will block the main process until the child process finishes
    print(f"Process finished with exit code {process.exitcode}.")
    
    print("Main program continues after the process has finished.")
