### Nvidia GPU对CPU的通信方式:UVM

评估orin平台性能，主要基于数据传输和发送通知时延，构造CPU&GPU任务

使用UVM怎么接收数据已发送的信号？



orin: unified memory(UVM)有多种使用方式，需要调研，跑一个网络。跟踪具体任务模块的子任务时延

orin内部GPU的运行方式流水线or序列化，CPU执行GPU任务时是否忙等待

用户层的GPU调度程序实现（可能有性能问题）

内核层的GPU调度程序实现（考虑抓取中断的callback）

目前解决优先级反转的方法有哪些，不同方法的对比