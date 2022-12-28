import peyemmv as pv
import os

os.system('cls')

fixations=pv.extract_fixations('demo_data.txt',0.3,0.12,80,'0')

for fix in fixations:
    print(fix)