### autocore工程工作说明书

![image-20220510140807258](C:\Users\Ziyang.Tao\AppData\Roaming\Typora\typora-user-images\image-20220510140807258.png)



![image-20220510141022008](C:\Users\Ziyang.Tao\AppData\Roaming\Typora\typora-user-images\image-20220510141022008.png)

![image-20220510140849770](C:\Users\Ziyang.Tao\AppData\Roaming\Typora\typora-user-images\image-20220510140849770.png)

![image-20220510141117733](C:\Users\Ziyang.Tao\AppData\Roaming\Typora\typora-user-images\image-20220510141117733.png)

![image-20220510141546596](C:\Users\Ziyang.Tao\AppData\Roaming\Typora\typora-user-images\image-20220510141546596.png)



![image-20220510141741261](C:\Users\Ziyang.Tao\AppData\Roaming\Typora\typora-user-images\image-20220510141741261.png)

![image-20220510141920776](C:\Users\Ziyang.Tao\AppData\Roaming\Typora\typora-user-images\image-20220510141920776.png)



- autocore自己设计了DDS，但是路特斯已经谈好了DDS的供应商，商议后autocore决定使用路特斯提供的第三方DDS

- autocore的GPU调度应用程序不提供GPU调度，只有监控

- autocore针对不同触发情况处理机制
  - 事件触发：资源隔离、带宽保留
  - 周期触发：离线调度表

- autocore的调度器工作在最高优先级



