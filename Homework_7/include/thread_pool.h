#pragma once
#include <pthread.h>
#include <stdbool.h>

struct Task {
    void (*f)(void *);
    void* arg;
    pthread_cond_t cond;
    pthread_mutex_t mutex;
    bool done;
    struct ThreadPool* pool;
    struct Task *l, *r;
};

struct Query{
    unsigned int l, r, depth;
    int *a;
    struct Task* t;
    unsigned int MaxRecLimit;
};

struct Node{
    struct Node *next;
    struct Task *t;
};

struct List{
    struct Node *head;
};

struct ThreadPool {
    struct List tasks;
    unsigned int num;
    bool deleted;
    pthread_cond_t done; //condition working == 0
    volatile unsigned int working; //number of working threads
    pthread_mutex_t list_lock; //mutex for list
    pthread_cond_t list_cond; //cond for informing of new elements in list
};

void thpool_init(struct ThreadPool* pool, unsigned int threads_nm);
void thpool_submit(struct ThreadPool* pool, struct Task* task);
void thpool_wait(struct Task* task);
void thpool_finit(struct ThreadPool* pool);
struct Task* new_task(int l, int r, int *a, int depth, int mx, void (*f)(void *), struct ThreadPool *pool);
void sort_arr(void *arg);
