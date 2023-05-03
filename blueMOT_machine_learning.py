# -*- coding: utf-8 -*-
"""
Created on Wed May  3 14:58:21 2023

@author: Korak
"""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

#Imports for M-LOOP
import mloop.interfaces as mli
import mloop.controllers as mlc
import mloop.visualizations as mlv

# Importing other modules
import os
import numpy as np
import time


DataPath = 'XXXX'  # Address of the directory where user wants to save tha data
if not os.path.exists(DataPath): os.makedirs(DataPath) # Creates the directory if it doesn't exist
SubDirs = [x[0] for x in os.walk(DataPath)]
RunFilePath = DataPath + '\\' + 'Run' + str(len(SubDirs))
os.makedirs(RunFilePath)
 
# Method Names : {'random','nelder_mead','gaussian_process','differential_evolution','neural_net'}
# Param List   : {'TC AOM','ZS AOM', 'ZSCoil1', 'ZSCoil2','MOTCoil'}

# Optimization Method
Method = 'neural_net'
MaxRun = 150
ParamNum = 5

# Param ranges
Mins = [150,65,1.5,1.5,0.2]   # expected minia of ranges of parameres
Maxs = [210,85,3,3,0.41]      # expected maxima of ranges of parameres

# Target Photodiode voltage
PDV = 10
TargetCost = 0


# Saving params
file = open(RunFilePath + '//' + 'mlParams.txt', "a")  # append mode
file.write("Param List   : {TC AOM,ZS AOM,ZSCoil1,ZSCoil2,MOTCoil} \n")
file.write(f"Method: {Method} \n")
file.write(f"ParamNum: {ParamNum} \n")
file.write(f"Min Value : {Mins} \n")
file.write(f"Max Value : {Maxs} \n")
file.write(f"Target Photodiode voltage (V) : {PDV} \n")
file.write(f"Target Cost : {TargetCost} \n")
file.close()


#<action starts>
  # Initialize AOM driver to control TC AOM and ZS AOM. 
  # Initialize power supplies to control ZSCoil1, ZSCoil2, MOTCoil.
  # Initialize photodiode to take the reading for calculating the cost function
#<action ends>


class Optimizer(mli.Interface):
       
    def get_next_cost_dict(self,params_dict):
       
        params = params_dict['params']
       
    #<system specific action starts>
          # Feed TC AOM  with the value params[0]
          # Feed ZS AOM  with the value params[1]
          # Feed ZSCoil1 with the value params[2]
          # Feed ZSCoil2 with the value params[3]
          # Feed MOTCOIL with the value params[4]
    #<system specific action ends>

        # Allowingg system to settle down
        time.sleep(6)
       
    #<action starts>
        # Collect sufficient datapoints from the photodiode and 
          #save the mean and standard deviation in variables 
           # named cost and uncer. The examole is as follows.   
        cost,uncer = MEAN_PHOTODIODE_VOLTAGE, STD_PHOTODIODE_VOLTAGE  
    #<action ends>
       
        print('INFO  \t Photodiode signal (V):',round(cost,3)) # print photodiode voltage for tracking
        print('*********************************') # demarcation line between printed values of different iterations
       
        cost = PDV-cost  # calculating the cost fuction
        bad = False
        cost_dict = {'cost':cost, 'uncer':uncer, 'bad':bad}
       
        return cost_dict
   
def main():   
    global controller
    interface = Optimizer()
    controller = mlc.create_controller(interface, max_num_runs = MaxRun, target_cost = TargetCost, num_params = ParamNum,
                                       min_boundary = Mins, max_boundary = Maxs)
    controller.optimize()
    
    # saving parameter values and the corresponding costs and uncertainties 
    np.savetxt(RunFilePath + '\\AllCosts.txt',controller.in_costs)
    np.savetxt(RunFilePath + '\\AllUncres.txt',controller.in_uncers)
    np.savetxt(RunFilePath + '\\AllParams.txt',controller.out_params)
   
if __name__ == '__main__': main()