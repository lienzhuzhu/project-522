#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>

static int test_init(void) {
	printk(KERN_INFO "loaded test module\n");
	return 0;
}

static void test_exit(void) {
	printk(KERN_INFO "unloaded test module\n");
	return;
}

module_init(test_init);
module_exit(test_exit);

MODULE_LICENSE("GPL");
