import numpy as np 
from scipy import signal
import subprocess
import os
import math
import skimage.measure

def fp_to_float(s,integer_precision,fraction_precision):       #s = input binary string
    number = 0.0
    i = integer_precision - 1
    j = 0
    if(s[0] == '1'):
        s_complemented = twos_comp((s[1:]),integer_precision,fraction_precision)
    else:
        s_complemented = s[1:]
    while(j != integer_precision + fraction_precision -1):
        number += int(s_complemented[j])*(2**i)
        i -= 1
        j += 1
    if(s[0] == '1'):
        return (-1)*number
    else:
        return number

def float_to_fp(num,integer_precision,fraction_precision):   
    if(num<0):
        sign_bit = 1                                          #sign bit is 1 for negative numbers in 2's complement representation
        num = -1*num
    else:
        sign_bit = 0
    precision = '0'+ str(integer_precision) + 'b'
    integral_part = format(int(num),precision)
    fractional_part_f = num - int(num)
    fractional_part = []
    for i in range(fraction_precision):
        d = fractional_part_f*2
        fractional_part_f = d -int(d)        
        fractional_part.append(int(d))
    fraction_string = ''.join(str(e) for e in fractional_part)
    if(sign_bit == 1):
        binary = str(sign_bit) + twos_comp(integral_part + fraction_string,integer_precision,fraction_precision)
    else:
        binary = str(sign_bit) + integral_part+fraction_string
    return str(binary)

def twos_comp(val,integer_precision,fraction_precision):
    flipped = ''.join(str(1-int(x))for x in val)
    length = '0' + str(integer_precision+fraction_precision) + 'b'
    bin_literal = format((int(flipped,2)+1),length)
    return bin_literal

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

def get_rand():
	e = np.random.randint(0,11)%2
	n = np.random.uniform(-0.5,-0.006,1)
	p = np.random.uniform(0.006,0.5,1)
	if(e == 0):
		return n
	else:
		return p
		
N = 16           #Total bitwidth of each number
Q = 12           #Number of bits allotted to represent the fractonal part
I = N-Q-1        #Number of bits allotted to represent the integral part
NoT = 1#0000

for i in range(NoT):
    a = get_rand() #np.random.uniform(-0.5,0.5,1) #
    b = get_rand() #np.random.uniform(-0.5,0.5,1) #
    c = get_rand() #np.random.uniform(-0.5,0.5,1) #

    p_golden = a[0]*b[0] + c[0]
    p_golden_trunc = truncate(p_golden,2)

    a_fp = float_to_fp(a[0],I,Q)
    b_fp = float_to_fp(b[0],I,Q)
    c_fp = float_to_fp(c[0],I,Q)

    ip_file = open('input.txt','w')
    ip_file.write(format(a_fp)+"\n")
    ip_file.write(format(b_fp)+"\n")
    ip_file.write(format(c_fp)+"\n")
    ip_file.close()

    os.system("iverilog -o mac_manual.vvp mac_manual_tb.v qadd.v qmult.v")
    os.system("vvp mac_manual.vvp ")

    op_file = open('output.txt','r')
    p_practical = op_file.readline()
    p_practical_trunc = truncate(fp_to_float(p_practical[:-1],I,Q),2) #round(fp_to_float(p_practical[:-1],3,12),2)
    op_file.close()

    if(abs(abs(p_golden_trunc) - abs(p_practical_trunc)) < 0.05): #p_golden_trunc == p_practical_trunc):
    	print('test_passed')
    else:
    	print('test_failed')
    	print(' a =',a_fp, '=', a[0])
    	print(' b =',b_fp, '=', b[0])
    	print(' c =',c_fp, '=', c[0])
    	print('p_golden =' ,p_golden_trunc)
    	print('p_practical =' ,p_practical_trunc) #fp_to_float(p_practical[:-1],3,12))
    	print(abs(abs(p_golden_trunc) - abs(p_practical_trunc)))
    	break

