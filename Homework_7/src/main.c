#include "../include/thread_pool.h"
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>

void wait_sort(struct ThreadPool *pool, struct Task *t){
    if (t == NULL)
        return;
    thpool_wait(t);
    wait_sort(pool, t -> l);
    wait_sort(pool, t -> r);
}

void free_sort(struct Task *t){
    if (t == NULL)
        return;
    free_sort(t -> l);
    free_sort(t -> r);
    free((struct Query*)t -> arg);
    pthread_mutex_destroy(&t -> mutex);
    pthread_cond_destroy(&t -> cond);
    free(t);
}

bool sorted(int *a, int n){
    for (int i = 1; i < n; i++)
        if (a[i - 1] > a[i])
            return false;
    return true;
}

int main(int argc, char **argv){
    if (argc != 4){
        printf("Wrong number of arguments!\n");
        return 1;
    }
    unsigned int num, n, mx;
    num = atoi(argv[1]);
    n = atoi(argv[2]);
    mx = atoi(argv[3]);
    int *a = malloc(n*sizeof(int));
    srand(42);
    for (int i = 0; i < n; i++)
        a[i] = rand();
    struct ThreadPool pool;
    pool.tasks.head = NULL;
    struct Task *t = new_task(0, n - 1, a, 0, mx, sort_arr);
    thpool_submit(&pool, t);
    thpool_init(&pool, num);
    wait_sort(&pool, t);
    free_sort(t);
    thpool_finit(&pool);
    if (sorted(a, n))
        printf("Well done!\n");
    else
        printf("Epic fail!\n");
    free(a);
    return 0;
}
