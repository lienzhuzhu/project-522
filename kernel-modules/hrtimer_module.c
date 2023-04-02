#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/hrtimer.h>
#include <linux/ktime.h>
#include <linux/time.h>
// #include <sys/time.h>
#include <linux/timekeeping.h>


static struct hrtimer test_hrtimer;
static u64 sampling_period_ms = 1000; // 1000ms
static u32 loop = 0;

// struct timespec {
//     time_t  tv_sec;     /* seconds */
//     long    tv_nsec;    /* nanoseconds */
// };

static enum hrtimer_restart test_hrtimer_handler(struct hrtimer *timer)
{
    // pr_info("test_hrtimer_handler: %u\n", ++loop);
        /* get monotonic clock time */
    //  = current_kernel_time();
    unsigned long long  cur_tsc;
    cur_tsc = ktime_get_ns();
    printk("Current time count : %llu \n", cur_tsc);
    hrtimer_forward_now(&test_hrtimer, ms_to_ktime(sampling_period_ms));
    return HRTIMER_RESTART;
}

static int __init test_hrtimer_init(void)
{
    hrtimer_init(&test_hrtimer, CLOCK_MONOTONIC, HRTIMER_MODE_REL);
    test_hrtimer.function = &test_hrtimer_handler;
    hrtimer_start(&test_hrtimer, ms_to_ktime(sampling_period_ms), HRTIMER_MODE_REL);
    pr_info("init test_hrtimer\n");

    return 0;
}

static void __exit test_hrtimer_exit(void)
{
    hrtimer_cancel(&test_hrtimer );
    pr_info("exit test_hrtimer\n");
    return;
}

module_init(test_hrtimer_init);
module_exit(test_hrtimer_exit);

MODULE_LICENSE("GPL");
