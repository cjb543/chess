CC := gcc
CFLAGS := -Wall -Wextra -std=c11

SRC := visualizer.c 
OUT := visualizer

all: $(OUT)

$(OUT): $(SRC)
		$(CC) $(CFLAGS) -o $@ $< 

clean:
		rm -f $(OUT)

.PHONY: all clean
