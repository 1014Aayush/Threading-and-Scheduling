import threading
import queue
import random
import time

# Define a queue for the customers
customer_queue = queue.Queue()

# Define a list of tellers
num_tellers = 3
tellers = [None] * num_tellers

# Lock for print statements
print_lock = threading.Lock()

# Define the time quantum for RR
time_quantum = 2

# Lists to store arrival, start, and completion times for each customer
arrival_times = []
start_times = []
completion_times = []

# Function to simulate teller service for RR
def teller_rr(teller_id):
    while True:
        customer_id, arrival_time, remaining_time = customer_queue.get()
        if customer_id is None:
            break
        start_time = time.time()  # Record start time
        with print_lock:
            print(f"Customer {customer_id} is in Teller {teller_id + 1} at time {start_time}")
        service_time = min(remaining_time, time_quantum)
        time.sleep(service_time)
        remaining_time -= service_time
        if remaining_time > 0:
            with print_lock:
                print(f"Customer {customer_id} re-enters the Queue with remaining time {remaining_time}")
            customer_queue.put((customer_id, arrival_time, remaining_time))
        else:
            with print_lock:
                print(f"Customer {customer_id} leaves the Teller {teller_id + 1} at time {time.time()}")

# Function to simulate customer arrivals for RR
def customer_arrival_rr():
    customer_id = 1
    while True:
        arrival_time = time.time()  # Record arrival time
        service_time = random.randint(1, 5)
        with print_lock:
            print(f"Customer {customer_id} enters the Queue with service time {service_time}")
        customer_queue.put((customer_id, arrival_time, service_time))
        customer_id += 1
        arrival_interval = random.randint(1, 3)
        time.sleep(arrival_interval)

# Function to run RR simulation and calculate metrics
def run_rr_simulation():
    # Create threads for tellers
    teller_threads = []
    for i in range(num_tellers):
        t = threading.Thread(target=teller_rr, args=(i,))
        t.start()
        teller_threads.append(t)

    # Create a thread for customer arrivals
    customer_thread = threading.Thread(target=customer_arrival_rr)
    customer_thread.start()

    # Let the simulation run for some time (e.g., 30 seconds)
    time.sleep(30)

    # Stop the threads
    for i in range(num_tellers):
        customer_queue.put((0, 0, None))
    for t in teller_threads:
        t.join()

    customer_thread.join()

    # Calculate metrics
    turnaround_times = [completion_times[i] - arrival_times[i] for i in range(len(arrival_times))]
    waiting_times = [start_times[i] - arrival_times[i] for i in range(len(arrival_times))]
    response_times = [start_times[i] - arrival_times[i] for i in range(len(arrival_times))]

    # Calculate averages
    avg_turnaround_time = sum(turnaround_times) / len(turnaround_times)
    avg_waiting_time = sum(waiting_times) / len(waiting_times)
    avg_response_time = sum(response_times) / len(response_times)

    # Print averages
    with print_lock:
        print("Average Turnaround Time:", avg_turnaround_time)
        print("Average Waiting Time:", avg_waiting_time)
        print("Average Response Time:", avg_response_time)

# Run RR simulation
run_rr_simulation()
