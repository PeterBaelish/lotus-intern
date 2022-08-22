有无抢占补丁CPU性能对比，CPU核使用表格完善，并且输出CPU核的使用结论

----

怎么把某个中断固定到某个cpu, 怎么把进程固定到一某个cpu， 怎么样让某个进程独享某个cpu，怎么配置进程调度策略与优先级等



把某个进程/线程绑定到特定的cpu核上后，该进程就会一直在此核上运行，不会再被操作系统调度到其他核上。但绑定的这个核上还是可能会被调度运行其他应用程序的。



进程绑核：

```c
int sched_setaffinity(pid_t pid, size_t cpusetsize, cpu_set_t *mask);
/* 设定进程号为pid的进程运行在mask所设定的CPU上，第二个数cpusetsize是mask所指定的数的长度，通常为sizeof(cpu_set_t)。mask通常指向一个32位整数，整数的二进制下的每个位表示一个CPU，1表示pid使用该CPU，0相反。如果pid的值为0，则表示的是当前进程。*/
```

对cpu_set_t *mask的操作（其中a为CPU编号）：

CPU_ZERO(&mask) : 初始化

CPU_SET(a,&mask) : 设置a号CPU被选中



进程/线程独占：

分三步

1、CPU隔离

2、绑定中断到非隔离的CPU上

3、绑定线程到CPU上

