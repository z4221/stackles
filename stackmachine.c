#include <stdlib.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>

int64_t* stack;
uint64_t stackPtr  = 0;
uint64_t stackSize = 1024;

typedef struct {
    int64_t a1;
    int64_t a2;
} arguments;

void initRuntime(uint64_t mainStackSize) {
    stack = (int64_t*)malloc(stackSize*sizeof(int64_t*));
    stackSize = mainStackSize;
}

void runtimeError(const char* error) {
    printf("Runtime error!\n");
    printf("%s",error);
    exit(1);
}

void checkSafety() {
    if (stackPtr > stackSize) {
        runtimeError("Stack overflow!\n");
    }
    if (stackPtr < 1) {
        runtimeError("Stack underflow!\n");
    }
}

void dumpStack() {
    int64_t oldStackPtr = stackPtr;
    printf("BEGIN DUMP\n");
    while (stackPtr != 0) {
        printf("S: %lu | V: %ld\n",stackPtr,stack[stackPtr]);
        stackPtr--;
    }
    printf("END DUMP\n\n");
    stackPtr = oldStackPtr;
}

void popPrint() {
    if (stackPtr == 0) {
        runtimeError("Stack underflow!\n");
    }
    printf("%ld\n",stack[stackPtr]);
    stackPtr--;
}

void noPopPrint() {
    printf("V: %ld\n",stack[stackPtr]);
}

arguments getArgs() {
    arguments args;
    args.a1 = stack[stackPtr];
    stackPtr--;
    checkSafety();
    args.a2 = stack[stackPtr];
    return args;
}

void stackAdd() {
    arguments args = getArgs();
    stack[stackPtr] = args.a1+args.a2;
}

void stackSub() {
    arguments args = getArgs();
    stack[stackPtr] = args.a1-args.a2;
}

void stackMul() {
    arguments args = getArgs();
    stack[stackPtr] = args.a1*args.a2;
}

void stackDiv() {
    arguments args = getArgs();
    stack[stackPtr] = args.a1/args.a2;
}

void stackSwap() {
    arguments args = getArgs();
    stack[stackPtr] = args.a1;
    stackPtr++;
    stack[stackPtr] = args.a2;
}

void stackDrop() {
    checkSafety();
    stackPtr--;
}

void stackDup() {
    int64_t a1 = stack[stackPtr];
    stackPtr++;
    checkSafety();
    stack[stackPtr] = a1;
}

void stackPush(uint64_t items, ...) {
    va_list ptr;
    va_start(ptr, items);
    for (int i = 0;i < items;i++) {
        stackPtr++;
        checkSafety();
        stack[stackPtr] = va_arg(ptr, int64_t);
    }
    va_end(ptr);
}

