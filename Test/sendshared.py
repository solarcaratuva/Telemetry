import os
import mmap
import posix_ipc
import ctypes

class SharedData(ctypes.Structure):
    _fields_ = [('var1', ctypes.c_int),
                ('var2', ctypes.c_int)]

memname = "sample"
sem_ready_name = "sem_data_ready"
sem_consumed_name = "sem_data_consumed"
region_size = os.sysconf('SC_PAGE_SIZE')

# Open the shared memory object
fd = os.open("/dev/shm/" + memname, os.O_RDONLY)

# Memory-map the file
mm = mmap.mmap(fd, region_size, access=mmap.ACCESS_READ)

# Map the data structure
data = SharedData.from_buffer(mm)

# Open semaphores
sem_ready = posix_ipc.Semaphore(sem_ready_name)
sem_consumed = posix_ipc.Semaphore(sem_consumed_name)

# Main loop
while True:
    sem_ready.acquire()  # Wait for data to be ready

    # Read the data
    val1 = data.var1
    val2 = data.var2
    print(f'var1: {val1}, var2: {val2}')

    sem_consumed.release()  # Indicate that data has been consumed
