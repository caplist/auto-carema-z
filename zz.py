# -*- coding: utf-8 -*-
"""
Created on Thu Oct 01 11:52:44 2015
控制位移台的移动：通过写入命令=> 写入字符串
z轴 range: 0-100um
@author: lj
"""
from __future__ import print_function
from builtins import str
import serial

import nplab.instrument.serial_instrument as si

class Piezoconcept(si.SerialInstrument):
    '''A simple class for the Piezo concept FOC100 nanopositioning system'''
    
    def __init__(self, port=None):
        self.termination_character = '\n'
        self.port_settings = {
                    'baudrate':115200,
                    'bytesize':serial.EIGHTBITS,
                    'parity':serial.PARITY_NONE,
                    'stopbits':serial.STOPBITS_ONE,
                    'timeout':1, #wait at most one second for a response
          #          'writeTimeout':1, #similarly, fail if writing takes >1s
           #         'xonxoff':False, 'rtscts':False, 'dsrdtr':False,
                    }
        si.SerialInstrument.__init__(self,port=port)
        self.recenter()
        
    def move_rel(self,value,unit="n"):
        '''A command for relative movement, where the default units is nm'''
        if unit == "n":
            multiplier=1
        if unit == "u":
            multiplier=1E3
            
        if (value*multiplier+self.position) > 1E5 or (value*multiplier+self.position) < 0:
            print("The value is out of range! 0-100 um (0-1E8 nm) (Z)")
        elif (value*multiplier+self.position) < 1E5 and (value*multiplier+self.position) >= 0:
            self.write("MOVRZ "+str(value)+unit)
            self.position=(value*multiplier+self.position)
    
    def move(self,value,unit="n"):
        '''An absolute movement command, will print an error to the console 
        if you moveoutside of the range(100um) default unit is nm'''
        if unit == "n":
            multiplier=1
        if unit == "u":
            multiplier=1E3
            
        if value*multiplier >1E5 or value*multiplier <0:
            print("The value is out of range! 0-100 um (0-1E8 nm) (Z)")
            
        elif value*multiplier < 1E5 and value*multiplier >=0: 
            self.write("MOVEZ "+str(value)+unit)
            self.position = value*multiplier
            
    def move_step(self,direction):
        self.move_rel(direction*self.stepsize)
        
    def recenter(self):
        ''' Moves the stage to the center position'''
        self.move(50,unit = "u")
        self.position = 50E3
        
    def INFO(self):
        return self.query("INFOS",multiline=True,termination_line= "\n \n \n \n",timeout=.1,)
    
    def GetZ(self):
        # 得到当前上Z轴的位置
        # return self.write("Z")
        return self.query("Z")
    
    def PrintPosition(self):
        print(self.position)
    # 得到z轴的位置 用于
    def GetZPosition(self):
        return self.position
        

    
        
# if __name__ == "__main__":
#     '''Basic test, should open the Z stage and print its info before closing. 
#     Obvisouly the comport has to be correct!'''
#     Z = Piezoconcept(port = "COM3")
#     print(Z.PrintPosition())
#     # print(Z.GetZ())
#     Z.move(99, unit = "u")
#     print(Z.PrintPosition())
#     # print(Z.GetZ())
#     Z.close()
        
