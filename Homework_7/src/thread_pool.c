#include "../include/thread_pool.h"
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

static int cmpr(const void* a, const void *b){
    return (*(int*)a - *(int*)b);
}

struct Task* new_task(int l, int r, int *a, int depth, int mx, void (*f)(void *), struct ThreadPool *pool){
    struct Task *res = malloc(sizeof(struct Task));
    struct Query *q = malloc(sizeof(struct Query));
    q -> l = l;
    q -> r = r;
    q -> a = a;
    q -> depth = depth;
    q -> MaxRecLimit = mx;
    q -> t = res;
    res -> f = f;
    res -> pool = pool;
    res -> arg = (void*)q;
    res -> done = false;
    res -> l = NULL;
    res -> r = NULL;
    pthread_cond_init(&res -> cond, NULL);
    pthread_mutex_init(&res -> mutex, NULL);
    return res;
}

static void make_done(struct Task *t){
    pthread_mutex_lock(&t -> mutex);
    t -> done = true;
    pthread_cond_signal(&t -> cond);
    pthread_mutex_unlock(&t -> mutex);
}

void sort_arr(void *arg){
    //fprintf(stderr, "%d\n", pthread_self());
    struct Query *q = (struct Query*)arg;
    struct Task *t = q -> t;
    if (q -> depth == q -> MaxRecLimit){
        qsort(q -> a + q -> l, q -> r - q -> l + 1, sizeof(int), cmpr);
        return;
    }
    int l = q -> l, r = q -> r;
    if (l >= r)
        return;
    int *a = q -> a;
    int x = a[l];
    int i = l, j = r, tmp;
    while (i <= j){
        while (a[i] < x) i++;
        while (a[j] > x) j--;
        if (i <= j){
            tmp = a[i];
            a[i++] = a[j];
            a[j--] = tmp;
        }
    }
    struct Task *t1 = new_task(l, j, a, q -> depth + 1, q -> MaxRecLimit, sort_arr, t -> pool);
    struct Task *t2 = new_task(i, r, a, q -> depth + 1, q -> MaxRecLimit, sort_arr, t -> pool);
    t -> l = t1;
    t -> r = t2;
    thpool_submit(t -> pool, t1);
    thpool_submit(t -> pool, t2);
}

static void add_node(struct List *l, struct Node *n){
    if (!l -> head){
        l -> head = n;
        return;
    }
    n -> next = l -> head;
    l -> head = n;
}

static void delete_node(struct List *l){
    struct Node *v = l -> head -> next;
    free(l -> head);
    l -> head = v;
}

static void* worker(void* arg){
    //fprintf(stderr, "%d\n", pthread_self());
    struct ThreadPool *pool = (struct ThreadPool*)arg;
    if (pool -> deleted)
        pthread_exit(0); //Sorry, thread, you are late
    pthread_mutex_lock(&pool -> list_lock);
    ++pool -> working;
    while (true){
        if (!pool -> tasks.head){
            --pool -> working;
            if (!pool -> working)
                pthread_cond_signal(&pool -> done);
            while (!pool -> tasks.head)
                pthread_cond_wait(&pool -> list_cond, &pool -> list_lock);
            ++pool -> working;
        }
        struct Task *t = pool -> tasks.head -> t;
        delete_node(&pool -> tasks);
        if (t == NULL){
            --pool -> working;
            if (!pool -> working)
                pthread_cond_signal(&pool -> done);
            pthread_mutex_unlock(&pool -> list_lock);
            pthread_exit(0);
        }
        pthread_mutex_unlock(&pool -> list_lock);
        t -> f((void*)t -> arg);
        make_done(t);
        pthread_mutex_lock(&pool -> list_lock);
    }
}

void thpool_init(struct ThreadPool* pool, unsigned int threads_nm){
    pool -> num = threads_nm;
    pool -> working = 0;
    pool -> deleted = false;
    pthread_mutex_init(&pool -> list_lock, NULL);
    pthread_cond_init(&pool -> done, NULL);
    pthread_cond_init(&pool -> list_cond, NULL);
    for (unsigned int i = 0; i < threads_nm; i++){
        pthread_t t;
        pthread_create(&t, NULL, worker, (void*)pool);
        pthread_detach(t);
    }
}

static void wait_empty(struct ThreadPool* pool){
    pthread_mutex_lock(&pool -> list_lock);
    while (pool -> working != 0){
        pthread_cond_wait(&pool -> done, &pool -> list_lock);
    }
    pthread_mutex_unlock(&pool -> list_lock);

}

void thpool_finit(struct ThreadPool* pool){
    wait_empty(pool);
    for (unsigned int i = 0; i < pool -> num; i++)
        thpool_submit(pool, NULL);
    wait_empty(pool);

    pool -> deleted = true;
    pthread_mutex_destroy(&pool -> list_lock);
    pthread_cond_destroy(&pool -> list_cond);
    pthread_cond_destroy(&pool -> done);
}

void thpool_wait(struct Task* task){
    pthread_mutex_lock(&task -> mutex);
    while (!task -> done)
        pthread_cond_wait(&task -> cond, &task -> mutex);
    pthread_mutex_unlock(&task -> mutex);
}

void thpool_submit(struct ThreadPool* pool, struct Task* task){
    struct Node *n = malloc(sizeof(struct Node));
    n -> t = task;
    n -> next = NULL;
    pthread_mutex_lock(&pool -> list_lock);
    add_node(&pool -> tasks, n);
    pthread_cond_signal(&pool -> list_cond);
    pthread_mutex_unlock(&pool -> list_lock);
}
