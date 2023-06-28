#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <cstring>
#include <semaphore.h>

struct SharedData {
    int var1 = 0;
    int var2 = 0;
};

int main() {
    const char *memname = "sample";
    const char *sem_ready_name = "sem_data_ready";
    const char *sem_consumed_name = "sem_data_consumed";
    const size_t region_size = sysconf(_SC_PAGE_SIZE);

    int fd = shm_open(memname, O_CREAT | O_TRUNC | O_RDWR, 0666);
    if (fd == -1) {
        // Handle error
    }

    if (ftruncate(fd, region_size) == -1) {
        // Handle error
    }

    void *ptr = mmap(0, region_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (ptr == MAP_FAILED) {
        // Handle error
    }

    sem_t *sem_ready = sem_open(sem_ready_name, O_CREAT, 0666, 0);
    if (sem_ready == SEM_FAILED) {
        // Handle error
    }

    sem_t *sem_consumed = sem_open(sem_consumed_name, O_CREAT, 0666, 1);
    if (sem_consumed == SEM_FAILED) {
        // Handle error
    }

    SharedData *data = reinterpret_cast<SharedData *>(ptr);

    // Main loop
    while (true) {
        sem_wait(sem_consumed);  // Wait until data has been consumed

        // Update the data
        ++data->var1;
        data->var2 += 2;

        sem_post(sem_ready);  // Indicate that new data is ready
    }

    return 0;
}