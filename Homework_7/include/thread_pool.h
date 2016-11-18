#pragma once
#include <pthread.h>
#include <stdbool.h>

struct Task {
    void (*f)(void *); // функция, которую требуется выполнить
    void* arg; // данные, передаваемые функции в качестве параметра
    pthread_cond_t cond; //cond for done
    pthread_mutex_t mutex; //mutex for done
    bool done;
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

struct ThreadNode{
    struct ThreadNode *next;
    pthread_t t;
};

struct List{
    struct Node *head;
};

struct ThreadPool {
    struct List tasks;
    struct ThreadNode *head;
    unsigned int num;
    //<как-то хранящиеся потоки>
    //<как-то хранящиеся таски>
	//<любые поля на усмотрение студента>
};

void thpool_init(struct ThreadPool* pool, unsigned int threads_nm);
void thpool_submit(struct ThreadPool* pool, struct Task* task);
void thpool_wait(struct Task* task);
void thpool_finit(struct ThreadPool* pool);
struct Task* new_task(int l, int r, int *a, int depth, int mx, void (*f)(void *));
void sort_arr(void *arg);
