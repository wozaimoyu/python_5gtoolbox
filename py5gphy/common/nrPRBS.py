# -*- coding:utf-8 -*-
"""NR 伪随机序列（PRBS）生成工具。

本模块实现 3GPP TS 38.211 Section 5.2.1 定义的 Gold 序列，
用于 DMRS、扰码等多个链路处理环节。
"""

import numpy as np

# TS 38.211 Section 5.2.1
def gen_nrPRBS(c_init, N):
    """ generate pseudo-random sequences refer to 38.211 5.2.1
    seq = gen_nrPRBS(c_init, N)
    input:
        c_init: init value
        N: output seq bit length
    output:
        seq: N length [0,1] sequence
    """
    assert N > 0
    Nc = 1600
    # 初始化 x1 / x2 两个 m-sequence 寄存器。
    # x1 的初始状态固定为 [1,0,0,...]，x2 由 c_init 的低 31 bit 决定。
    x1_seq = np.zeros(Nc + N,'i1')
    x1_seq[0] = 1
    x2_seq = np.zeros(Nc + N,'i1')
    x2_seq[0:31] = [c_init >> i & 1 for i in range(31)]
    
    # 按标准定义递推，先生成 Nc+N 长度，后续丢弃前 Nc 位。
    for m in range(Nc+N-31):
        x1_seq[m+31] = (x1_seq[m+3]+x1_seq[m]) % 2
        x2_seq[m+31] = (x2_seq[m+3]+x2_seq[m+2]+x2_seq[m+1]+x2_seq[m]) % 2
    
    # Gold 序列：c(n) = x1(n+Nc) + x2(n+Nc) (mod 2)
    seq = (x1_seq[1600:]+x2_seq[1600:]) % 2
    
    return seq


if __name__ == "__main__":
    from scipy import io
    import os
    
    print("test nr PBRS encoding")
    from tests.common import test_nrPRBS
    testcases = test_nrPRBS.get_testvectors()
    count = 1
    for ins,  expected in testcases:
        test_nrPRBS.test_nrPRBS(ins,  expected)
