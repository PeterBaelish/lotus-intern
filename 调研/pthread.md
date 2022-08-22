### 一、Pthread

- 是POSIX规定的thread协议
- 现在唯一略成熟的实现是NPTL

### 二、内容

##### 1、线程信息

- 进程内共享：进程指令、全局数据、信号及信号处理、当前工作目录、打开的文件
- 单个线程独有：线程ID、寄存器集合、栈指针SP、存放局部变量的栈、返回地址、signal mask（被调用者阻塞的一组信号）、优先级、guard size、返回值

##### 2、线程操作

- 创建pthread_create( )，在这里设置线程attributes，可设置的包括是否可join、调度策略、调度常数、是否使用优先级继承、栈大小
- 终止pthread_exit( )
  - 在进程内最后一个线程释放后终止进程
- 同步
  - pthead_join( )，使线程等待直到某些进程完成或终止
  - mutex，用于保护线程间的竞争区，只能同时被一个线程占用
    - pthread_mutex_t variable，用于初始化mutex
    - pthread_mutex_unlock，用于解锁mutex
    - pthread_mutex_lock，用于给mutex上锁
    - pthread_mutex_destroy，用于销毁mutex
    - 可设置mutex种类，包括normal（包含错误检查）、recursive（normal基础上支持递归调用mutex，有计数器记录递归层数）
  - condition variable，用于在线程被阻塞（竞争mutex）时等待另一个线程发送信号来被唤醒
    - pthread_cond_t (condition) ，用于初始化条件变量
    - pthread_cond_wait(condition，mutex)，用于阻塞调用mutex的线程，直到收到某个信号，线程wait期间将脱离就绪列表，不占用任何CPU cycle
    - pthread_cond_signal(condition)，告诉被条件变量阻塞的线程结束阻塞状态
    - pthread_cond_broadcast(condition)，告诉所有被该条件变量阻塞的线程结束阻塞状态

- 调度
  - 支持normal优先级（100-139）、实时优先级（0-99）
  - normal支持CFS调度，其他优化调度方式待定
  - set-priority() 运行时进程优先级修改
- 数据管理
- 进程通信

##### 3、优化内容

- 评估线程运行操作量级，分析堆栈大小分布图，为平台设置最佳线程stack size，以达到的最大线程数量
- 更好的改进CFS调度策略，参考《实时系统》

