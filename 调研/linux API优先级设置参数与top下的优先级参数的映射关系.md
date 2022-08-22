## linux API优先级设置参数与top下的优先级参数的映射关系

linux进程调度优先级分为两种：实时优先级、静态优先级。实时优先级对应的调度策略只能是：FIFO、RR，静态优先级对应的调度策略几乎都是：OTHER。



#### 用户、top命令优先级表示法

- 用户优先级表示法
  - 设置实时优先级：设置RT参数，范围[0,99]，值越高优先级越高。
  - 设置静态优先级：设置NICE值，范围[-20,19]，值越低优先级越高。

- top优先级表示法

![image-20220523155820487](C:\Users\Ziyang.Tao\AppData\Roaming\Typora\typora-user-images\image-20220523155820487.png)

上图中涉及优先级的有两个参数：PR、NI。PR代表进程优先级，NI代表进程的NICE值，由用户态设置，NI值是对PR值的修正。PR值的范围是[-100,39]



#### 用户、top命令优先级的转换关系

拥有静态优先级的进程中，PR、NI的关系式为：
$$
PR=20+NI
$$
拥有实时优先级的进程中，NI恒等于0，PR的计算方式为：
$$
PR=-1-RT
$$
特别地，RT=99，即为最高实时优先级时，top中的PR显示为rt。



观察到NICE值的范围[-20,19]，所以静态优先级进程的PR值的范围是[0,39]；RT值的范围[0,99]，所以实时优先级进程的PR值的范围是[-100,-1]。所以PR值大于0时，这是个静态优先级进程；PR值小于0时，这是个实时优先级进程。



以下是例子：

用户态：设置实时优先级RT为50，调度策略为SCHED_FIFO。top下显示：PR=-51，NI=0

![image-20220523155650559](C:\Users\Ziyang.Tao\AppData\Roaming\Typora\typora-user-images\image-20220523155650559.png)

用户态：设置静态优先级NICE为5，调度策略为SCHED_OTHER。top下显示：PR=25，NI=5

![image-20220523164915444](C:\Users\Ziyang.Tao\AppData\Roaming\Typora\typora-user-images\image-20220523164915444.png)

