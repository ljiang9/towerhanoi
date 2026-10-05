# towerhanoi — 终端汉诺塔

三柱汉诺塔: 手动挑战 + 最优解自动求解器。纯标准库, 无依赖。

## 玩法

```bash
python -m towerhanoi            # 手动玩(默认 3 盘)
python -m towerhanoi --disks 5  # 5 盘挑战
python -m towerhanoi --solve    # 打印最优解走法
python -m towerhanoi --solve --animate  # 逐步动画演示
```

交互: 输入 `A C` 把 A 柱顶盘移到 C 柱; `q` 退出。
规则: 一次移一个盘, 大盘不能压小盘; 目标是把 A 柱全部盘子搬到 C 柱。

## 设计取舍

- 最优解是经典递归(2^n − 1 步), `--solve` 会用断言校验"每一步合法且终局获胜"。
- 盘子数限制 1–12: 盘子太多画不下, 12 盘最优解 4095 步也足够演示。
- 行输入模式(每步回车), 不需要终端 raw 模式。

## 已知局限

- 无悔棋、记分; 求解器只输出 A→C 的标准最优解, 无其他目标柱选项。
