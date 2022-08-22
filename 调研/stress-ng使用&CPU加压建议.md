针对CPU加压的种类，加压的差异，对CPU的影响，加压具体的操作命令，自己先在板子上验证可行性，有什么指标可以评估。给出加压的方案，可能有多个加压方式结合的加压方案等（加压配置算法）。

依靠stress-ng作为背景压力任务，然后对实际任务的时延进行测试。目的在于对供应商提供的调度程序实施压力，让他们的调度程序出现较大的时延。主要考虑中断负载。

----

#### stress-ng

--class name

​	类有很多种，如cpu cpu-cache device io os pipe vm memory等等。一些stressors只属于一个类，有些则属于多个类。选择一个特定的类 将只在使用顺序（sequential）选项运行时运行 只属于该类的 所有压力源。



--ionice-class class / --ionice-level level

​	设置和获取I/O类进程的优先级。可以被分为三个调度类：idle、best-effort（RR）、realtime。idle会当磁盘上没有任务时执行；best-effort有8个优先级，并且会默认情况继承CPU nice值（映射）；realtime会第一个获得磁盘的使用权，也有8个优先级，决定在每个调度窗口进程会被分到多大的可执行时间片。



--metrics

​	bogo ops、real time、usr time、sys time



--sched scheduler

​	选择调度器，包括rr，rt，fifo等



--sched-prio prio

​	选择调度器的优先级，默认为最高



--taskset list

​	设置被使用的CPU集合



-t N

​	设置运行时间（单位：秒）



--affinity N

​	开启N个stressors快速改变CPU的亲和性（应该会有大量的迁移），会对cache造成压力



--aio N

​	开启N个stressors产生大量异步I/O读写，读写操作针对相对较小的暂存文件。



--mq N

​	产生N个发送、接收进程，用POSIX消息队列持续的收发数据。



--cpu N

​	产生N个锻炼CPU的进程。



--cpu-load P

​	产生百分之P(0~100)的CPU负载。



--cpu-load-slice S

​	S<0：busy与idle之间穿插-S个stress loop

​	S=0：busy与idle之间穿插随机时间（0~0.5s）

​	S>0：busy与idle之间穿插S毫秒CPU busy time



--timer N (--timer-freq n) (--timer-rand)

​	产生N个频率为n的中断负载。rand范围为n +/- 12.5%



--timerfd N (--timerfd-freq n) (--timerfd-rand)

​	产生N个频率为n的等待文件描述符的中断负载。rand范围为n +/- 12.5%



--io N

​	产生N个持续调用sync 以 向磁盘提交缓存的进程（最好和--hdd结合使用）



---iomix N (--iomix-bytes N)

​	启动N个worker，混合执行顺序的、随机的和内存映射的读/写操作，以及强制同步和(如果作为root运行)缓存删除。生成的多个子进程共享同一个文件，并对同一个文件执行不同的I/O操作。用bytes设置每个iomix进程写内存大小，可以设置为总可用内存的百分比。



--hdd N (--hdd-bytes N)

​	产生N个持续读写、移除临时文件的进程。用bytes设置每个hdd进程写内存大小，可以设置为总可用内存的百分比。



--mcontend N

​	产生N个进程，产生读写竞争。每个进程会产生5个线程来读写同一块物理内存。这些线程也会随机的改变CPU亲和性。



--sleep N 

​	产生N个进程，每个进程都产生大量线程（默认1024个）随机睡眠1us到0.1s。



---schedpolicy N

​	产生N个进程随机分配调度策略，对于实时调度策略的进程，会被随机分配实时优先级。



软中断

由正在运行的代码产生I/O请求 或 yield请求，这些请求有些需要被立即处理，有些可以排队（如磁盘I/O）。软中断由硬件中断处理程序的下半部 或 内核自定义事件（如内核调度、RCU锁）产生。具体种类包括网络、定时中断、RCU锁中断、内核调度中断。



硬中断

由硬件产生，比如磁盘，网卡，键盘，时钟等等。当硬中断产生的时候，CPU会中断当前正在运行的任务（RT补丁可能不会）

----

cd ~/taoziyang/rt-tests-2.3 && sudo ./cyclictest -a 0-10 -d 0 --json=cyclicout --priospread -i 1000 -m --priority=99 --policy=fifo -q -t 49

cd ~/taoziyang/ipc-bench-master-crude/src && sudo chrt 30 ./unix_lat 4096 100000

----

## 一、CPU加压种类及影响  

#### 1、CPU密集型任务

#### 2 、I/O密集型任务

- 访存（磁盘换页引发中断）
- 硬中断

#### 3、密集上下文切换



## 二、调度器职能

#### 1、时间片

#### 2、中断响应

- 硬中断
- 软中断

#### 3、优先级

- 实时
- 普通

#### 4、负载均衡

- MC域内负载均衡



## 三、干扰调度器的加压方式

#### 1、自yield（软中断）

--sleep（实时优先级影响都不大）

#### 2、硬中断

--timer（实时优先级影响都不大）

#### 3、提交缓存

--io --hdd（io改成实时优先级后有明显效果）

#### 4、进程、I/O优先级

chrt

#### 5 、CPU负载率

--cpu --cpu-load（更改实时优先级之后有相当明显的效果）

#### 6、进程迁移

--affinity（更改实时优先级后有明显效果）

#### 7、内存竞争

--mcontend （更改实时优先级之后有相当明显的效果）（更改成实时优先级以后系统会炸，勿用！）

#### 8、读写

--aio （改成实时优先级后有明显效果）



## 四、干扰命令及效果展示

#### 1、背景任务 stress-ng

#### 2、单任务时延测试 cyclictest

#### 3、进程间通信时延测试 unix domain socket

​	./unix_lat <传输字节数> <测试次数>

​	如何设置优先级？需要设置吗？

----

8.28 +2000

8.28 +1000

9.1    -4000

9.13 +3500

9.28 +1000

