pqsort: ./bin/main.o ./bin/thread_pool.o
	gcc ./bin/main.o ./bin/thread_pool.o -o pqsort -lpthread -g

./bin/main.o: bin ./src/main.c 
	gcc -c -o ./bin/main.o ./src/main.c -g

./bin/thread_pool.o: bin ./src/thread_pool.c ./include/thread_pool.h
	gcc -c -o ./bin/thread_pool.o ./src/thread_pool.c -g

clean: 
	rm -rf ./bin
	rm -rf pqsort

bin:
	mkdir bin -p