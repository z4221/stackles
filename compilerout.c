#include "stackmachine.c"

int main() {
initRuntime(1024);
stackPush(2,42,100);
stackMul();
stackPush(1,21);
stackAdd();
popPrint();
return stack[stackPtr];
}
