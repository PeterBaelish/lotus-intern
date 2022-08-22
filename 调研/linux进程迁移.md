linux内核中每个CPU都会有一个迁移守护进程，他们在内核启动时被初始化，在调用sched_setaffinity时被唤醒（可能有其他调用方式唤醒）

sched_setaffinity(pid_t pid, const struct cpumask *in_mask)（系统调用）

以下为内核态

- __set_cpus_allowed_ptr

  - 设置线程/进程亲和度

  - 检查进程/线程是否在运行，或准备运行（TASK_WAKING态）

    - 是 -> 调用stop_one_cpu

      - 调用cpu_stop_queue_work

        - 获取源CPU的stopper thread

        - 调用__cpu_stop_queue_work

          - 迁移任务放入stopprt thread的任务队列

          - 唤醒stopper_thread执行迁移

    - 否 -> 检查进程/线程是否在源CPU（调用sched_setaffinity的CPU）的运行队列
      - 是 -> 在执行sched_setaffinity的CPU上做将进程从源CPU迁移到目标CPU的运行队列的动作
      - 否 -> 改变源CPU的亲和度



stopper_thread工作过程

- 在源CPU上调用migration_cpu_stop，并设置为高优先级

  - 调用__migrate_task

    - 测试进程/线程亲和度是否被设置

    - 调用move_queued_task 

      - 进程/线程从源CPU运行队列中移除

      - 调用enqueue_task移动进程到目的CPU运行队列

        