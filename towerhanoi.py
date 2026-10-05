#!/usr/bin/env python3
"""towerhanoi - 终端汉诺塔: 手动挑战 + 最优解自动求解.

玩法: A/B/C 三根柱子, 一次只能移动一个盘子, 大盘不能压小盘.
目标: 把 A 柱上的盘子全部搬到 C 柱.
"""
from __future__ import annotations

import argparse
import sys
import time

PEGS = ("A", "B", "C")


def solve_moves(n: int, src: str = "A", dst: str = "C", aux: str = "B"):
    """返回最优递归解法的走法列表, 每项为 (from, to)."""
    moves = []

    def rec(k, s, d, a):
        if k == 0:
            return
        rec(k - 1, s, a, d)
        moves.append((s, d))
        rec(k - 1, a, d, s)

    rec(n, src, dst, aux)
    return moves


class Hanoi:
    def __init__(self, n: int):
        if not 1 <= n <= 12:
            raise ValueError("盘子数必须在 1~12 之间")
        self.n = n
        self.pegs = {p: [] for p in PEGS}
        self.pegs["A"] = list(range(n, 0, -1))  # 大在下
        self.moves = 0

    def move(self, src: str, dst: str) -> tuple[bool, str]:
        src, dst = src.upper(), dst.upper()
        if src not in PEGS or dst not in PEGS:
            return False, "柱子只能是 A / B / C。"
        if src == dst:
            return False, "起点和终点不能是同一根柱子。"
        if not self.pegs[src]:
            return False, f"{src} 柱是空的, 无子可移。"
        disk = self.pegs[src][-1]
        if self.pegs[dst] and self.pegs[dst][-1] < disk:
            return False, f"非法: 大盘({disk}) 不能压在小盘({self.pegs[dst][-1]}) 上。"
        self.pegs[src].pop()
        self.pegs[dst].append(disk)
        self.moves += 1
        return True, f"把盘 {disk} 从 {src} 移到 {dst}。"

    def won(self) -> bool:
        return self.pegs["C"] == list(range(self.n, 0, -1))

    def render(self) -> str:
        w = self.n * 2 + 1
        lines = []
        for level in range(self.n - 1, -1, -1):
            row = []
            for p in PEGS:
                stack = self.pegs[p]
                if level < len(stack):
                    d = stack[level]
                    s = "#" * (d * 2 - 1)
                    row.append(s.center(w))
                else:
                    row.append("|".center(w))
            lines.append("  ".join(row))
        lines.append("  ".join(p.center(w) for p in PEGS))
        return "\n".join(lines)


def play_interactive(n: int, delay: float = 0.0):
    game = Hanoi(n)
    opt = 2 ** n - 1
    print(f"汉诺塔({n} 盘) | 最优解 {opt} 步 | 输入如 `A C`, q 退出")
    print(game.render())
    while True:
        try:
            cmd = input("移动(起点 终点): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n已退出。")
            return 1
        if cmd.lower() in ("q", "quit", "exit"):
            print(f"已退出, 共走 {game.moves} 步。")
            return 0
        parts = cmd.upper().replace("-", " ").split()
        if len(parts) != 2:
            print("格式不对, 请输两个字母, 如 `A C`。")
            continue
        ok, msg = game.move(parts[0], parts[1])
        print(msg)
        if ok:
            print(game.render())
            if delay:
                time.sleep(delay)
            if game.won():
                print(f"🎉 成功! 共用 {game.moves} 步(最优 {opt} 步)。")
                return 0


def run_solve(n: int, animate: bool):
    moves = solve_moves(n)
    game = Hanoi(n)
    print(f"{n} 盘最优解: {len(moves)} 步(2^{n}-1)")
    for i, (s, d) in enumerate(moves, 1):
        ok, msg = game.move(s, d)
        assert ok, f"求解器走法非法: {s}->{d} ({msg})"
        if animate:
            print(f"第 {i} 步: {msg}")
            print(game.render())
            time.sleep(0.15)
    assert game.won(), "求解器走完后未达胜利状态"
    if not animate:
        for i, (s, d) in enumerate(moves, 1):
            print(f"第 {i} 步: {s} -> {d}")
    print("✓ 按最优解完成, 到达目标状态。")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="towerhanoi", description="终端汉诺塔: 手动挑战 + 最优解求解器")
    ap.add_argument("--disks", "-n", type=int, default=3, help="盘子数(1-12, 默认 3)")
    ap.add_argument("--solve", action="store_true", help="输出最优解走法")
    ap.add_argument("--animate", action="store_true", help="--solve 时逐步动画展示")
    args = ap.parse_args(argv)
    if not 1 <= args.disks <= 12:
        print("error: --disks 必须在 1~12 之间", file=sys.stderr)
        return 2
    if args.solve:
        run_solve(args.disks, args.animate)
        return 0
    return play_interactive(args.disks)


if __name__ == "__main__":
    raise SystemExit(main())
