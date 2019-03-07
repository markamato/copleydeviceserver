import time
import serial


class CopleyRS232:
    
    
    
	nodeID = ""
	axisLetter = ""
	
	defaultBaud = 115200;
	defaultTimeout = .1;
	defaultPortID = '/dev/ttyUSB1'
	
	#parameter dictionary and values
	
	#position parameters
	param_commanded_position_ID = '0x3d'
	param_motor_position_ID = '0x32'
	param_load_position_ID = '0x17'
	param_trajectory_mode_ID = '0x24'
	param_following_error_ID = '0x35'
    
    #homing
	param_home_offset_ID = '0xc6'
    
    #trajectories
	param_trajectory_stop = 0
	param_trajectory_move = 1
	param_trajectory_home = 2

	
	#Programmed position mode params

	param_profile_ID = "0xc8"
	param_profile_absTrapMove = 0
	param_profile_absSMove = 1
	param_profile_veloMove = 2
	param_profile_relTrapMove = 256
	param_profile_relSMove = 257
	param_position_command_ID = "0xca"
	param_position_mode_posVelo = 1
	param_position_mode_negVelo = -1
	param_maxVelo_ID = "0xcb"
	param_maxAccel_ID = "0xcc"
	param_maxDecel_ID = "0xcd"
	param_maxJerk_ID = "0xce"
	param_abortDecel_ID = "0xcf"
	
	#in/out
	param_analogInVoltage_ID = "0x1d"
	param_inputs_ID = "0xa6"
	param_outputs_ID = "0xab"
	
	#faults/states
	param_statusRegister_ID = "0xa0"
	param_trajectoryRegister_ID = "0xc9"
	param_faultRegister_ID = "0xa4"
	
	
	#misc
	param_busVoltage_ID = "0x1E"
	param_ampTemp_ID = "0x20"
	param_baud_ID = "0x90"
	
	# memories
	ram = 'r'
	flash = 'f'
	
	
	# Defines, go do defines here
	
	
	# Init object
	def __init__(self):
		print "Init!"
	
	# Open serial object
	def StartSerial(self,baud=defaultBaud,serialPort=defaultPortID,timeout=defaultTimeout):
		self.CopleySerial = serial.Serial()
		self.CopleySerial.timeout=timeout
		self.CopleySerial.port=serialPort
		self.CopleySerial.baudrate=9600
		self.CopleySerial.open()
		self.CopleySerial.write('r \r')
		time.sleep(5)
		self.CopleySerial.close()
		self.CopleySerial.baudrate=9600
		self.CopleySerial.open()
		self.CopleySerial.write('r \r')		
		time.sleep(5)
		self.ChangeSerialSpeed(baud)
		print self.CopleySerial.name
		
		return self.CopleySerial
	
	# Close serial object
	def StopSerial(self):
		#self.ChangeSerialSpeed(9600)
		self.CopleySerial.close()
	
	
    # Change the serial speed
	def ChangeSerialSpeed(self,baud):
		commandstring = 's r'+str(self.param_baud_ID)+' '+str(baud) + '\r'
		#print commandstring
		self.CopleySerial.write(commandstring)
		self.CopleySerial.close()
		self.CopleySerial.baudrate=baud
		time.sleep(2)
		self.CopleySerial.open()
	
	# define parameters if required; if called with no values resets to default
#	def Config(self, nodeIDcmd, axisLettercmd):
#	    nodeID = nodeIDcmd
 #       axisLetter = axisLettercmd
	
	# Command structure
	def CopleyCommand(self,nodeID="",axisLetter="",commandCode="",commandParameters=""):
	    commandString = str(nodeID) + str(axisLetter) + '' + str(commandCode) + str(commandParameters).strip() +'\r' 
	    # print commandString
	    self.CopleySerial.write(commandString)
	    response = self.CopleySerial.read_until('\r')
	    response = response[0:(len(response)-1)]
	    #print response
	    return response


	# Set Command
	def Set(self,memoryBank,parameterID,value):
		
		return self.CopleyCommand(self.nodeID, self.axisLetter,'s ',(str(memoryBank) + str(parameterID) + ' ' + str(value)))
		
    # Get Command
	def Get(self,memoryBank,parameterID,optional=""):
	
		return self.CopleyCommand(self.nodeID, self.axisLetter,'g ',(str(memoryBank) + str(parameterID) + ' ' + str(optional)))
	
	def Reset(self):
    
		return self.CopleyCommand("","","r","")
        
	def Trajectory(self,commandCode):
    
		return self.CopleyCommand(self.nodeID, self.axisLetter,'t ',commandCode)
        
        
	def ClearEncoderErrors(encoder="both"):
		if encoder == "load":
			self.CopleySerial.write("ldenc clear\r")
		if encoder == "motor":
			self.CopleySerial.write("enc clear\r")
		else:
			self.CopleySerial.write("enc clear\r")
			self.CopleySerial.write("ldenc clear\r")
        
		return "ok"
