#include "../include/thread_pool.h"
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

static pthread_mutex_t mw; //mutex for int working
static pthread_cond_t done; //condition working == 0
static volatile unsigned int working = 0; //number of working threads
static pthread_mutex_t list_lock; //mutex for list
static pthread_cond_t list_cond; //cond for informing of new elements in list
static struct ThreadPool *cur_pool = NULL;
static struct List* tasks;

static int cmpr(const void* a, const void *b){
    return (*(int*)a - *(int*)b);
}

struct Task* new_task(int l, int r, int *a, int depth, int mx, void (*f)(void *)){
    struct Task *res = malloc(sizeof(struct Task));
    struct Query *q = malloc(sizeof(struct Query));
    q -> l = l;
    q -> r = r;
    q -> a = a;
    q -> depth = depth;
    q -> MaxRecLimit = mx;
    q -> t = res;
    res -> f = f;
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
        make_done(t);
        return;
    }
    int l = q -> l, r = q -> r;
    if (l >= r){
        make_done(t);
        return;
    }
    int *a = q -> a;
    int x = a[l + rand() % (r - l + 1)];
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
    struct Task *t1 = new_task(l, j, a, q -> depth + 1, q -> MaxRecLimit, sort_arr);
    struct Task *t2 = new_task(i, r, a, q -> depth + 1, q -> MaxRecLimit, sort_arr);
    t -> l = t1;
    t -> r = t2;
    pthread_mutex_lock(&list_lock);
    thpool_submit(cur_pool, t1);
    thpool_submit(cur_pool, t2);
    pthread_mutex_unlock(&list_lock);
    make_done(t);
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
    pthread_mutex_lock(&list_lock);
    pthread_mutex_lock(&mw);
    working++;
    pthread_mutex_unlock(&mw);
    while (true){
        if (!pool -> tasks.head){
            pthread_mutex_lock(&mw);
            working--;
            if (!working)
                pthread_cond_signal(&done);
            pthread_mutex_unlock(&mw);
            while (!pool -> tasks.head)
                pthread_cond_wait(&list_cond, &list_lock);
            pthread_mutex_lock(&mw);
            working++;
            pthread_mutex_unlock(&mw);
        }
        struct Task *t = pool -> tasks.head -> t;
        delete_node(&pool -> tasks);
        pthread_mutex_unlock(&list_lock);
        t -> f((void*)t -> arg);
        pthread_mutex_lock(&list_lock);
    }
}

void thpool_init(struct ThreadPool* pool, unsigned int threads_nm){
    tasks = &pool -> tasks;
    cur_pool = pool;
    pool -> num = threads_nm;
    pthread_mutex_init(&list_lock, NULL);
    pthread_cond_init(&done, NULL);
    pthread_mutex_init(&mw, NULL);
    pthread_cond_init(&list_cond, NULL);
    struct ThreadNode *last = NULL;
    for (unsigned int i = 0; i < threads_nm; i++){
        struct ThreadNode *n = malloc(sizeof(struct ThreadNode));
        n -> next = last;
        last = n;
        pthread_create(&n -> t, NULL, worker, (void*)pool);
        pthread_detach(n -> t);
    }
    pool -> head = last;
}

void thpool_finit(struct ThreadPool* pool){
    pthread_mutex_lock(&mw);
    while (true){
        if (working != 0)
            pthread_cond_wait(&done, &mw);
        else
            break;
    }
    pthread_mutex_unlock(&mw);
    struct ThreadNode *cur = pool -> head, *n;
    while (cur){
        pthread_cancel(cur -> t);
        n = cur -> next;
        free(cur);
        cur = n;
    }

    pthread_mutex_destroy(&list_lock);
    pthread_mutex_destroy(&mw);
    pthread_cond_destroy(&list_cond);
    pthread_cond_destroy(&done);
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
    add_node(&pool -> tasks, n);
    if (cur_pool != NULL)
        pthread_cond_signal(&list_cond);
}
