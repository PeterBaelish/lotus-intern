# 零、休眠唤醒机制 #

- 休眠：task被放入阻塞队列，并存储一个唤醒回调函数autoremove_wake_function函数并挂起当前进程；其次不断事件触发轮询检查当前任务task执行的condition是否满足，不满足则进入休眠，满足则进入就绪队列

```
#define ___wait_event(wq_head, condition, state, exclusive, ret, cmd)		
({										
	__label__ __out;							
	struct wait_queue_entry __wq_entry;					
	long __ret = ret;	/* explicit shadow */				
										
	init_wait_entry(&__wq_entry, exclusive ? WQ_FLAG_EXCLUSIVE : 0);	
	for (;;) {								
		long __int = prepare_to_wait_event(&wq_head, &__wq_entry, state);
										
		if (condition)							
			break;							
										
		if (___wait_is_interruptible(state) && __int) {			
			__ret = __int;						
			goto __out;						
		}								
										
		cmd;				/* schedule()*/				
	}									
	finish_wait(&wq_head, &__wq_entry);					
__out:	__ret;									
})
```

```
int autoremove_wake_function(struct wait_queue_entry *wq_entry, unsigned mode, int sync, void *key)
{
	int ret = default_wake_function(wq_entry, mode, sync, key);
	/*default_wake_function的唤醒回调函数主要是将task添加到cpu就绪队列中等待cpu调度执行任务*/
	if (ret)
		list_del_init_careful(&wq_entry->entry);

	return ret;
}
```

- 唤醒：在等待队列中循环遍历所有的entry节点,并执行回调函数,直到当前entry为独占节点的时候退出循环遍历

# 一、互斥锁

### 1、互斥锁的特性及应用场景 ###

​		互斥锁一次只能一个线程拥有互斥锁，其他线程只有等待。互斥锁是在抢锁失败的情况下主动放弃CPU进入睡眠状态直到锁的状态改变时再唤醒，而操作系统负责线程调度，为了实现锁的状态发生改变时唤醒阻塞的线程或者进程，需要把锁交给操作系统管理，所以互斥锁在加锁操作时涉及上下文的切换。在并发运算的时候使用互斥锁会比自旋锁性能更优。互斥锁适用于被长时间持有的情况，且不会禁止内核抢占。

### 2、互斥锁的种类

- 普通锁（PTHREAD_MUTEX_NORMAL）：当一个线程对一个普通锁加锁以后，其余请求该锁的线程将形成一个 等待队列，并在该锁解锁后按照优先级获得它。普通锁不能处理对已经加锁的锁再次加锁，或解锁一个被其他线程加锁的锁，或对一个已经解锁的锁再次解锁
- 检错锁（PTHREAD_MUTEX_ERRORCHECK）：实现普通锁的功能基础上，增加了对上述违法操作的报错功能
- 递归锁（PTHREAD_MUTEX_RECURSIVE）：允许一个线程在释放锁之前多次对它加锁而不发生死锁，开辟一个变量记录递归层数。当解锁一个被其他线程加锁的锁，或对一个已经解锁的锁再次解锁时会报错

### 3、互斥锁的问题

​		一次只能一个线程拥有互斥锁，其他线程只有等待，当占用锁的线程耗费大量时间，阻塞线程又有实时性要求时，会有问题。



# 二、自旋锁

### 1、自旋锁的特性及应用场景 ###

​		自旋锁最多只能被一个线程持有。如果一个线程试图获取被使用的自旋锁，那么该线程就会一直进行忙循环——旋转（占用很多时间）——等待锁重新可用。自旋锁不可递归，禁止抢占。适用于短时间的轻量级加锁，如中断处理，但是必须要禁用本地中断以防止递归。

### 2、自旋锁的问题 ###

​		如果进线程无法取得锁，进线程不会立刻放弃CPU时间片，而是一直循环尝试获取锁，直到获取为止。如果别的线程长时期占有锁那么自旋就是在浪费CPU做无用功。



# 三、读写锁 #

### 1、读写锁的特性及应用场景 ###

​		对某个数据结构的操作可以被划分为读写两种类别时，可以使用读写锁。一个或多个读任务可以并发的持有读者锁；用于写的锁最多只能被一个写任务持有，而且此时不能有并发的读操作；读任务持有锁时，写操作必须等待。多个读者可以安全地获得同一个读锁，也可以线程递归地获得同一个读锁，这一特性使得读操作使用锁时不用禁用本地中断。

### 2、读写锁的操作 ###

- pthread_rwlock_rdlock(&mr_rwlock)
- pthread_rwlock_wrlock(&mr_rwlock)
- pthread_rwlock_unlock(&mr_rwlock)
- 注：读写锁函数调用的是一个锁，但是读锁、写锁操作应归于安全分隔开的代码分支中。如果试图读锁升级写锁，如

​		pthread_rwlock_rdlock(&mr_rwlock)；

​		pthread_rwlock_wrlock(&mr_rwlock)；

​		则会带来死锁，因为写锁会不断自旋等待读者锁释放锁

### 3、读写锁的问题 ###

​		读任务持有锁时，写操作会自旋等待，所以有大量读操作时，写操作会浪费CPU资源。



# 四、信号量 #

### 1、信号量的特性及应用场景 ###

​		信号量是一个计数器，用于控制访问有限共享资源的线程数。信号量的特性与互斥锁相同当有限共享线程数为1时，信号量退化为互斥锁。



# 五、条件变量 #

### 1、条件变量的特性及应用场景 ###

​		互斥锁一个明显的缺点是他只有两种状态：锁定和非锁定。而条件变量通过允许线程阻塞和等待另一个线程发送信号的方法弥补了互斥锁的不足，他常和互斥锁一起使用，以免出现竞态条件。当条件不满足时，线程往往解开相应的互斥锁并阻塞线程然后等待条件发生变化。一旦其他的某个线程改变了条件变量，他将通知相应的条件变量唤醒一个或多个正被此条件变量阻塞的线程。通过缓冲区隔离生产者和消费者，与二者直连相比，避免相互等待，提高运行效率。生产快于消费，缓冲区满，撑死。消费快于生产，缓冲区空，饿死。条件变量可以让调用线程在满足特定条件的情况下暂停。

### 2、条件变量的操作 ###

- pthread_cond_t (condition) ，用于初始化条件变量
- pthread_cond_wait(condition，mutex)，用于阻塞调用mutex的线程，直到收到某个信号，线程wait期间将脱离就绪列表，不占用任何CPU cycle
- pthread_cond_signal(condition)，告诉被条件变量阻塞的线程结束阻塞状态
- pthread_cond_broadcast(condition)，告诉所有被该条件变量阻塞的线程结束阻塞状态



# 六、Preempt_RT优化内容 #

### 1、中断处理变为可抢占内核线程

​		在内核初始化创建 init 线程时，中断线程化的中断在 init() 函数中还将调用 init_hardirqs，来为每一个 IRQ 创建一个内核线程，最高实时优先级为 50，依次类推直到 25，因此任何 IRQ 线程的最低实时优先级为 25。调用 wake_up_process() 函数唤醒中断处理线程，并开始运行。

```
void __init init_hardirqs(void){
……
    for (i = 0; i < NR_IRQS; i++) {
        irq_desc_t *desc = irq_desc + i;
        if (desc->action && !(desc->status & IRQ_NODELAY))
            desc->thread = kthread_create(do_irqd, desc, "IRQ %d", irq);
    ……
    }
}
static int do_irqd(void * __desc){
    `……`
    /*     * Scale irq thread priorities from prio 50 to prio 25     */
    param.sched_priority = curr_irq_prio;
    if (param.sched_priority > 25)`
        curr_irq_prio = param.sched_priority - 1;
   ……
}
```

```
fastcall notrace unsigned int __do_IRQ(unsigned int irq, struct pt_regs *regs)
{
……
    if (redirect_hardirq(desc))
        goto out_no_end;
……
action_ret = handle_IRQ_event(irq, regs, action);
……
}
int redirect_hardirq(struct irq_desc *desc){
……
    if (!hardirq_preemption || (desc->status & IRQ_NODELAY) || !desc->thread)
        return 0;
……
    if (desc->thread && desc->thread->state != TASK_RUNNING)
        wake_up_process(desc->thread);
……
}
```

### 2、自旋锁优先级继承

​		这种技术要求低优先级任务继承它们共享的资源上任何高优先级任务的优先级。一旦高优先级的任务开始等待，这个优先级的改变就应该发生;它应该在资源被释放时结束。用rt_mutex实现。注：信号量进行计数没有所有者的概念，没有优先级继承。（自旋锁spinlock转化为rt_mutex，仍然需要独占资源的使用raw_spinlock）

![](.\image-20220402142334379.png)

​        在struct rt_mutex中记录了owner和所有的waiters（进程），使用红黑树实现，称为Mutex Waiter List，优先级最高的那一个叫top waiter。

​        struct rt_mutex_waiter是用来链接rt_mutex和task_struct的数据结构，保存了waiter是哪个进程（task_struct）在等待哪个lock（rt_mutex）

​        struct task_struct中同样有一个waiters列表，使用红黑树实现，称为Task PI List列表中包含此进程持有所有rt_mutex的top waiter，称作top pi waiter。