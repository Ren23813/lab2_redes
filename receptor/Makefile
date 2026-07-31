CC = gcc
CFLAGS = -Wall -O2

OBJS = main_receptor.o transmision.o enlace.o fletcher.o viterbi.o presentacion.o aplicacion.o

receptor: $(OBJS)
	$(CC) $(CFLAGS) -o receptor $(OBJS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f *.o receptor
