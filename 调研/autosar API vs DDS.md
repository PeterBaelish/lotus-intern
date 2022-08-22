AUTOSAR的ara::com服务接口用ARXML定义，ARXML编译器分别为客户端和服务器proxy和skeleton生成代码，在客户端的应用程序实例化 绑定到在服务器端运行的服务实例的 代理。每个代理一次只能绑定到一个服务实例。![](D:\lotus\AUTOSAR_dds.PNG)

DDS解除AUTOSAR代理和服务实例的耦合方法：每个ara::com服务实例在以 service ID命名的特定分区上发布数据，每个代理使用以它们绑定的service ID命名的分区订阅数据。





ara::com提供以下资源：

events:通知客户端应用程序在服务器端触发的事件

methods:公开客户端应用程序可以调用的远程过程

fields:提供客户端应用程序可以使用远程getter和setter修改的数据值



映射到DDS：

events->DDS regular topics

![](D:\lotus\events.jpg)

methods->DDS service methods

![](D:\lotus\methods.jpg)

fields->DDS常规的getter和setter方法

![](D:\lotus\fields.jpg)



------

与普通DDS or RPC-DDS? 需要询问