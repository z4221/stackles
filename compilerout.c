
#include "stackmachine.c"

void cf_test() {
stackPush(3, 42, 2, 42);
stackPush(2, 2, 42);
stackPush(1, 42);
stackDiv();
dumpStack();
}
void cf_add() {
stackAdd();
}
void cf_fib() {
cf_if();
cf_<=();
stackPush(1, 0);
cf_then();
cf_return();
stackPush(1, 1);
cf_end();
cf_dup();
stackPush(1, 1);
stackSub();
cf_fib();
stackPush(1, 2);
stackSub();
cf_fib();
stackAdd();
}
void cf_main() {
stackPush(2, 10, 20);
stackPush(1, 20);
stackAdd();
popPrint();
stackPush(2, 10, 20);
stackPush(1, 20);
stackSub();
popPrint();
stackPush(2, 10, 20);
stackPush(1, 20);
stackDiv();
popPrint();
stackPush(2, 10, 20);
stackPush(1, 20);
stackMul();
popPrint();
stackPush(2, 10, 10);
stackPush(1, 10);
stackSub();
cf_if();
cf_!=();
stackPush(1, 0);
cf_then();
stackPush(1, 4221);
popPrint();
cf_else();
stackPush(1, 1224);
popPrint();
cf_end();
cf_test();
stackPush(2, 10, 10);
stackPush(1, 10);
cf_add();
popPrint();
}

int main() {
    initRuntime(1024);
    cf_main();
}
