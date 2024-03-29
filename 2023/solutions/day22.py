#!/usr/bin/env python3

from collections import defaultdict

from utils import advent

advent.setup(2023, 22)
fin = advent.get_input()

bricks = [
    ([int(num) for num in first], [int(num) for num in second])
    for line in fin.read().splitlines()
    if len(parts := line.split("~", maxsplit=1)) == 2
    and len(first := parts[0].split(",", maxsplit=2)) == 3
    and len(second := parts[1].split(",", maxsplit=2)) == 3
    and all(num.isdecimal() for num in first + second)
]
bricks.sort(key=lambda brick: brick[0][2])

heights = defaultdict(int)
for first, second in bricks:
    (x0, y0, z0), (x1, y1, z1) = first, second
    dz = (
        max(heights[(x, y)] for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
        + 1
        - z0
    )
    first[2], second[2] = z0, z1 = z0 + dz, z1 + dz
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            heights[(x, y)] = z1

bricks.sort(key=lambda brick: brick[0][2])
rdeps, deps = defaultdict(set), defaultdict(set)
for i, ((x0, y0, _), (x1, y1, z1)) in enumerate(bricks):
    for j, ((x2, y2, z2), (x3, y3, _)) in enumerate(bricks[i + 1 :]):
        if z2 <= z1:
            continue
        if z2 > z1 + 1:
            break
        if x0 <= x3 and x2 <= x1 and y0 <= y3 and y2 <= y1:
            rdeps[i].add(i + j + 1)
            deps[i + j + 1].add(i)
        j += 1

acc = 0
for item in rdeps.items():
    _deps = {above: set(belows) for above, belows in deps.items()}
    stack = [item]
    while stack:
        below, aboves = stack.pop()
        for above in aboves:
            belows = _deps[above]
            if below not in belows:
                continue
            belows.remove(below)
            if belows:
                continue
            acc += 1
            stack.append((above, rdeps.get(above, ())))

# Part 1
result_1 = len(bricks) - len(
    {next(iter(below)) for below in deps.values() if len(below) == 1}
)
advent.submit_answer(1, result_1)

# Part 2
result_2 = acc
advent.submit_answer(2, result_2)
