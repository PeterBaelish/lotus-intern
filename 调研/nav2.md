nav2用行为树（behavior tree）调用模块化server来执行action。action都是独立的节点，通过ROS action server与行为树(BT)通信。可以在每个server上使用匹配的BT插件。这可以用来创建上下文导航（contextual navigation）行为。

nav2的预期输入是 符合REP-105的TF 转换（transformation）（如果使用静态costmap层，则是一个map  source），一个行为树（BT） XML文件 和 任何相关的传感器数据。他的输出是 为机器人电机提供有效的速度指令。

nav2包含的组件有：

- Map Server：加载、存储地图
- AMCL：在地图上定位
- Nav2 Planner：点到点路径规划
- Nav2 Controller：控制机器人沿路径行走
- Nav2 Smoother：使路径增加连续性、可行性
- Nav2 Costmap 2D：将传感器数据转换为世界的costmap表示  （?）
- Nav2 Behavior Trees and BT Navigator：使用行为树构建复杂的机器人行为  
- Nav2 Recoveries：计算 出故障时的恢复行为

- Nav2 Waypoint Follower：按顺序描点
- Nav2 Lifecycle Manager：管理服务器的生命周期和watchdog
- Nav2 Core：插件，用来使用自定义算法和行为

![img](https://navigation.ros.org/_images/nav2_architecture.png)