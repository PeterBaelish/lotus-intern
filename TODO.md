#### 项目推进汇报任务

- 遗留问题
  - IO对时延影响大的原因，IO&CPU同时负载效果较好的原因
- 短期目标
  - 基本负载下，调度优先级、调度策略影响测试
    - 在单核上cyclictest增加线程数，测量负载的瓶颈，负载任务也需要安排实时优先级
    - CPU、IO负载下，不同调度策略、优先级配置的cyclictest测试，研究100、300、500、700、1000线程，负载任务也需要安排实时优先级
    - CPU、IO负载下，不同调度策略、优先级配置的数据链时延测试，负载任务也需要安排实时优先级（Linux 本身如何做进程间通信？IPC共享内存；Linux本身做信号通信的机制调研）
    - ROS2_PiCAS tracing on **Reference System**
  - CPU、GPU调度器实现
    - orin对GPU到CPU的通信方式为unified memory。评估orin平台性能，主要基于数据传输和发送通知时延，构造CPU&GPU任务。unified memory(UWA)有多种使用方式，需要调研，跑一个网络。跟踪具体任务模块的子任务时延 https://docs.nvidia.com/cuda/cuda-for-tegra-appnote/index.html
    - 安装Nsight，跑不同内存和异步机制下的任务
    - orin内部GPU的运行方式流水线or序列化，CPU执行GPU任务时忙等待or睡眠
    - orin内部GPU任务是否不可抢占？进程不可抢占，线程内可抢占并且可以被赋予优先级（xavier只有三个优先级，orin有七个）
    - 用户层的GPU调度程序实现（可能有性能问题）
    - 内核层的GPU调度程序实现（考虑抓取中断的callback）
    - 目前解决优先级反转的方法有哪些，不同方法的对比
    - 线程调度管理算法设计（基于EDF）
    - 进程挂起预测算法设计
    - 可调度性算法分析
    - MIG？
    - TensorRT劫持？
- 长远目标
  - 比较 在中间件层面（比如Cyber RT）调度进程 与 分配进程优先级、调度策略之后在内核内调度 的性能优劣



注：测量结果应该标注上 平均处理时间、WCET、WBET

附：叶工的任务

1 整理一个调度实现过程的场景梳理  看论文
2 你们产品的底层实现技术，A到B的响应，B的响应触发是什么 怎么实现数据流的先后顺序 pub-sub
3 基于信号触发和时间触发的差异和影响，是否有负载高等情况，引起无法正常工作 （时钟中断）
	基于事件（基于少量数据），基于时间（适用于快速大量数据）
做实验观察
4 可抢占内核线程本质的编排实现
5 ros调度的问题，是什么原因引起



----

针对CPU加压的种类，加压的差异，对CPU的影响，加压具体的操作命令，自己先在板子上验证可行性，有什么指标可以评估。给出加压的方案，可能有多个加压方式结合的加压方案等。（近期需完成）

GPU任务通信模型和时延分析

CPU-GPU调度算法调研

----

打卡找考勤员王月