import math; pi = math.pi;
import time;

class car():
    
    def __init__(self):
        self.position = (200,200); #meters
        self.rotation = (1,0); #2D vector
        self.turn_speed = 2*pi; #m/s
        self.velocity = 100; #2D vector m/s
        self.mass = 1000; #kg
        self.size = (20,30); #px
        
        self.normal_f = self.mass * 9.8; #Newtons
        self.drag_f = (0,0); #N
        self.fric_coeff = 0.7; #unitless
        self.friction_f = self.fric_coeff * self.normal_f; #N make vector
        self.drive_f = (0,0); #N
        self.is_gas = 0;
        self.is_turn = 0;
        
        self.wheels = (wheel(self.mass/4), wheel(self.mass/4), wheel(self.mass/4), wheel(self.mass/4));
        
        
    def gas(self, value):
        self.is_gas = value;
        pass;
    
    def brake(self):
        pass;
    
    def turn(self, direc): #https://stackoverflow.com/questions/4780119/2d-euclidean-vector-rotations
        #theta = self.turn_speed * (time.time()-last_tick);
        if(direc == 1):
            theta = pi/4;
            #self.is_turn = pi/4;
        elif(direc == 2):
            theta = -pi/4;
            #self.is_turn = -pi/4;
        #else:
            #theta = 0;
            #self.is_turn = 0;
        if(direc):
            self.rotation = (self.rotation[0] * math.cos(theta) - self.rotation[1] * math.sin(theta),
                            self.rotation[0] * math.sin(theta) + self.rotation[1] * math.cos(theta));
    
    def trans_temp(self, dx, dy):
        temp_speed = 5; #px/s
        if(self.position[0] + dx < 500 and self.position[0] + dx > 0 
           and self.position[1] + dy < 500 and self.position[1] + dy > 0):
            self.position = (self.position[0] + dx, self.position[1] + dy);
    
    
    def get_state(self):
        return (self.position, self.size, math.atan2(self.rotation[0],self.rotation[1])*180/pi); #self.is_turn*180/pi #https://stackoverflow.com/questions/6247153/angle-from-2d-unit-vector
        """
        rotation 2D vector is converted into angle for pil to rotate source image
        """
    
    def update(self, last_tick):
        #get average force to find acceleration
        #accel to velocity
        #vel and time since last frame to update pos
        #also rotation somehow
        if(self.is_gas):
            self.position = ( self.position[0]+(self.rotation[0]*(self.velocity*((time.time()-last_tick) ))) *self.is_gas  ,
                              self.position[1]+(self.rotation[1]*(self.velocity*((time.time()-last_tick) ))) *self.is_gas   );
            """
            old position plus rotation to get new pos but multiplied by velocity*frametime for framerate independant speed
            is_gas determines forward of backward
            """
        """if(self.is_turn):
            self.rotation = (self.rotation[0] * math.cos(self.is_turn) - self.rotation[1] * math.sin(self.is_turn),
                         self.rotation[0] * math.sin(self.is_turn) + self.rotation[1] * math.cos(self.is_turn));"""
        

class wheel():
    
    def __init__(self, load):
        self.diameter = 0.5; #meters
        self.rpm = 0;
        self.load = load;
        
    
    def get_friction(self, coeff):
        return load * coeff;
