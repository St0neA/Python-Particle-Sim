import numpy as np
import random as rand
from datetime import datetime


class Environment:
    def __init__(self, width, height, gravity=(np.pi, 0)): #initialisation function
        
        
        self.width = width #dimensions of env
        self.height = height
        self.particles = [] #list of particles in env
        self.colour = (0,0,0) #color (default)
        self.mass_of_air = 0 
        self.elasticity = 1
        self.gravity = gravity
        
        #### create grid for collision detection
        self.cols = 128
        self.rows = 96
        
        
        self.squarewidth = self.width / self.cols #size of cells
        self.squareheight = self.height / self.rows
        
        self.cells = [ [] for i in range(self.rows*self.cols)] #list of cells
        
        
        matrix = np.zeros((self.rows, self.cols)) #pointer array 
        k = -1
        num = 0
        for i in range(self.rows):
            for k in range(self.cols):
                matrix[i,k] = num
                num += 1
                
        self.squarepointers = matrix 
       
    def restrictcols(self, colnumA, colnumB, rownumA, rownumB): #restricts the col and row number so that particles do not go out of bounds
        if colnumA < 0:
            colnumA = 0
        if colnumB >= self.cols:
            colnumB = self.cols - 1
        if rownumA < 0:
            rownumA = 0
        if rownumB >= self.rows:
            rownumB = self.rows - 1
        return colnumA, colnumB, rownumA, rownumB
    
        
    def allocateSquares(self): #function to allocate squares

        for p in self.particles:
            

            ####
            colnumA = int((p.x - p.size)/self.squarewidth) #finds the col and row number
            colnumB = int((p.x + p.size)/self.squarewidth)
        
            rownumA = int((p.y - p.size)/self.squarewidth)
            rownumB = int((p.y + p.size)/self.squarewidth)
                

            colnumA, colnumB, rownumA, rownumB = self.restrictcols(colnumA, colnumB, rownumA, rownumB)
            
            cells = [] 
            
            #creates list of cells that particle occupies
            
            [cells.append(int(self.squarepointers[row, column])) for column in range(colnumA, colnumB+1) for row in range(rownumA, rownumB+1)]
            

            """ #what the above list comprehension does
            for column in range(colnumA, colnumB + 1):
                for row in range(rownumA, rownumB + 1):
                    
                    squarenum = int(self.squarepointers[row, column])
                    cells.append(int(squarenum))
            """

            if set(p.cells) != set(cells): #if not the same as previously
                
                #then update the cells by removing old cells and adding new cell list
                
                [self.cells[i].remove(p) for i in p.cells]
                [self.cells[i].append(p) for i in cells]
                p.cells = cells

            ###

    def initialSquare(self, p): #cells init
        
            colnumA = int((p.x - p.size)/self.squarewidth)
            colnumB = int((p.x + p.size)/self.squarewidth)
            rownumA = int((p.y - p.size)/self.squarewidth)
            rownumB = int((p.y + p.size)/self.squarewidth)
            
            colnumA, colnumB, rownumA, rownumB = self.restrictcols(colnumA, colnumB, rownumA, rownumB)
            
            for column in range(colnumA, colnumB + 1):
                for row in range(rownumA, rownumB + 1):
                    squarenum = int(self.squarepointers[row, column])
                    p.cells.append(squarenum)
                    self.cells[int(squarenum)].append(p)
            
    
        
    def addParticles(self, n=1, **kargs):
        #kargs are size, mass, x, y, speed, angle, color
        density = 100
        for i in range(n):

            size = kargs.get('size', int(np.random.normal(10, 3)))
            mass = kargs.get('mass', density*size)
            x = kargs.get('x', rand.uniform(size, self.width-size))
            y = kargs.get('y', rand.uniform(size, self.height-size))
            
            p = Particle(x, y, size, mass, self.gravity)
            
            p.speed = kargs.get('speed', rand.uniform(5, 20))
            p.angle = kargs.get('angle', rand.uniform(0, np.pi*2))
            
            p.colour = kargs.get('colour', (0, 0, 255))
            p.drag = (p.mass/(p.mass + self.mass_of_air)) ** p.size
            p.gravity = self.gravity
            
            
            self.initialSquare(p)
            self.particles.append(p)
            
    def update(self):
        
        [p.move() for p in self.particles]

        [self.bounce(p) for p in self.particles]

        self.allocateSquares()
        
       

        
        [collide(particle, n) for cell in self.cells for particle in cell for n in cell[cell.index(particle)+1:]]
        """
        #what the above list comprehension does
        for cell in self.cells:
            for particle in cell:
                i = cell.index(particle)
                #particle.move()
                #self.bounce(particle)
                [collide(particle, n) for n in cell[i+1:]]
        """ 
       
        
        
        """
        
        ################################## OLD COLLISION
        i = 0
        for n in self.particles: #iterates through all particles
            i = self.particles.index(n)
            
            n.move() #moves
            self.bounce(n) #bounces (if applicable)
            #for n2 in self.particles[i+1:]:
             #   collide(n, n2)
            [collide(n, n2) for n2 in self.particles[i+1:]]
            
            i+=1
        
        
        """
    def bounce(self, particle): #bounce function
        
        if particle.x > self.width - particle.size: #finds whether the ball has crossed boundaries (x4)
            particle.x = 2 * (self.width - particle.size) - particle.x #corrects the position back to boundary
            particle.angle = - particle.angle #reflects angle
            particle.speed *= self.elasticity #reduces speed
        elif particle.x < particle.size:
            particle.x = 2 * particle.size - particle.x
            particle.angle = - particle.angle
            particle.speed *= self.elasticity
        if particle.y > self.height - particle.size:
            particle.y = 2 * (self.height - particle.size) - particle.y
            particle.angle = np.pi - particle.angle
            particle.speed *= self.elasticity
        elif particle.y < particle.size:
            particle.y = 2 * particle.size - particle.y
            particle.angle = np.pi - particle.angle
            particle.speed *= self.elasticity      
            
        


class Particle: #particle class
    
    def __init__(self, x, y, size, mass = 1, gravity = 0, square=None): #initialisation function, takes x, y, size
        
        self.speed = 0 #angle and speed zero by default
        self.angle = 0
        self.x = x
        self.y = y
        self.size = size
        self.color = (0, 0, 225) #color blue by default
        self.thickness = 0 #thickness 0 by default (means filled)
        self.mass = mass
        self.drag = 1
        self.elasticity = 1
        self.gravity = gravity
        self.square = square
        self.cells = []
        
    def move(self): #move function, updates location and velocity
        self.x += np.sin(self.angle) * self.speed
        self.y -= np.cos(self.angle) * self.speed
        #(self.angle, self.speed) = addVectors(self.angle, self.speed, self.gravity[0], self.gravity[1]) #uses add-vector function to add gravity
        self.speed *= self.drag #speed multiplier (drag)
        


def addVectors(angle1, length1, angle2, length2): #add vector function 
    x  = np.sin(angle1) * length1 + np.sin(angle2) * length2 #adds the two horizontal/vertical vectors
    y  = np.cos(angle1) * length1 + np.cos(angle2) * length2
    length = np.hypot(x, y) #finds new vector length
    angle = 0.5 * np.pi - np.arctan2(y, x) #finds the new angle
    return (angle, length) #returns new vector
    
def findParticle(particles, x, y): #finds particle
    for p in particles: 
        if np.hypot(p.x-x, p.y-y) <= p.size: #if x and y given within size of particle
            return p #return that particle
    return None #else return none

def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    distance = np.hypot(dx, dy)

    if distance < p1.size + p2.size:
    
        correction = p1.size + p2.size - distance + 1
        
        total_mass = p1.mass + p2.mass
        
        tangent = np.arctan2(dy , dx)
        angle = 0.5 * np.pi + tangent
        
        #for p1
        theta1 = angle - p1.angle
        V1par = -p1.speed*np.sin(theta1)
        V1perp = p1.speed*np.cos(theta1)
        
        #for p2
        theta2 = angle - p1.angle
        V2par = -p2.speed*np.sin(theta2)
        V2perp = p2.speed*np.cos(theta2)
    
        #############
        V1perpAfter = -(V1perp*((p1.mass-p2.mass)/total_mass) + 2*V2perp*(p2.mass/total_mass))
        V2perpAfter = -(V2perp*((p2.mass-p1.mass)/total_mass) + 2*V1perp*(p1.mass/total_mass))
    
        speed1After = np.hypot(V1perpAfter, V1par)
        speed2After = np.hypot(V2perpAfter, V2par)

        
        #storing variables so they can be used in the next lines
        speed1 = p1.speed
        angle1 = p1.angle
        speed2 = p2.speed
        angle2 = p2.angle
        

        #new way where momentum appears to be conserved but doesn't get distributed properly
        p1.angle, _ = addVectors(angle1, speed1*((p1.mass-p2.mass)/total_mass), angle, 2*speed2*(p2.mass/total_mass))
        p2.angle, _= addVectors(angle2, speed2*((p2.mass-p1.mass)/total_mass), angle+np.pi, 2*speed1*(p1.mass/total_mass))    
        
        p1.speed = speed1After
        p2.speed = speed2After
        
        elasticity = p1.elasticity * p2.elasticity
        p1.speed *= elasticity
        p2.speed *= elasticity
        
        p1.x += correction*np.sin(angle)
        p1.y -= correction*np.cos(angle)
        p2.x -= correction*np.sin(angle)
        p2.y += correction*np.cos(angle)
     
    #print("collide: " + str((datetime.now() - startTime).microseconds))        


