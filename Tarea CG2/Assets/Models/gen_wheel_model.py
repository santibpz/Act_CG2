# Santiago Benitez Perez - A01782813
# script to generate the wheel model for unity
import math 
import sys 

# list to store vertices
vertices = []
# list to store faces
faces = []
# list to store normal vector
normal_vectors = []

def create_wheel_model(numSides=8, radius=1, width=0.5):
    # guard clauses
    if numSides <= 3 or numSides > 360:
        sys.exit("ERROR: Invalid number of sides of the wheel")
    elif radius <= 0:
        sys.exit("ERROR: Radius must be positive")
    elif width <= 0:
        sys.exit("ERROR: Width must be positive")
        
    gen_vertices(numSides, radius, width) # generate vertices
    gen_faces(vertices) # generate faces and normal vectors given the vertices calculated
    create_obj_file(vertices, faces, normal_vectors) # create the obj file
    return {"result": "done"}

def gen_vertices(numSides, radius, width):
    cx = width/2 # width 
    
    #adding centers of both sides to the vertex list
    vertices.append((-cx, 0, 0))
    vertices.append((cx, 0, 0))
    
    # initial value of the angle
    angle = 0
    
    # increase of the angle on each iteration
    angleIncrease = 360/numSides
    
    
    while angle < 360:
        # calculate coordinates of the vertex given the current angle and the radius
        cz = radius * round(math.cos(math.radians(angle)), 4)
        cy = radius * round(math.sin(math.radians(angle)), 4)
        
        vertices.append((-cx, cy, cz)) # front side vertex
        vertices.append((cx, cy, cz)) # back side vertex 
        angle+=angleIncrease # increase the angle

    
    
def gen_faces(vertices):
    n = len(vertices) # length of the vertex list
    i = 2 # initialize i at 2
    last_frontside = i + 1 # store the vertex id for use when calculating last face of the wheel's frontside
    last_backside = i + 2 # store the vertex id for use when calculating last face of the wheel's backside
    
    # iterate over the vertices list
    while i < n:
        # if current index is even, determine the face of the front side of the weel
        if i%2==0:
            # determine last face of the front side of the wheel
            if i + 1 == n - 1:
                face = (1, i + 1, last_frontside)
            else:
            # determine the face based on the index
                face = (1, i + 1, i + 3)
            
            # obtaining lateral faces
            gen_lateral_faces(i, n - 2, last_frontside, last_backside)
            
        else:
            # if current index is odd, determine the face of the back side of the weel
            if i + 1 == n:
                #determine last face of the back side of the wheel
                face = (2, last_backside, i + 1)
            else:
                #determine the face based on the index
                face = (2, i + 3, i + 1)
                    
        # calculate the normal vector based on current face
        vn = gen_vn(face) # normal vector of the current face
            
        # append the new face with its normal vector id tag to the faces list
        faces.append((face, normal_vectors.index(vn) + 1))
        
        #increment i
        i+=1
        
def gen_lateral_faces(current, n, last_frontside, last_backside):
    # determine the faces of the lateral sides of the wheel that connect the frontside of the wheel with the backside of the wheel
    if current != n: # determine the 2 lateral faces 
        first = (current + 1, current + 2, current + 4)
        second = (current + 1, current + 4, current + 3)
    else: # determine last 2 lateral faces
        first = (current + 1, current + 2, last_backside)
        second = (current + 1, last_backside, last_frontside)
    
    # calculate the normal vector based on current face
    vn = gen_vn(first)
        
    # append the new faces with their normal vector id tag to the faces list
    faces.append((first, normal_vectors.index(vn) + 1))
    faces.append((second, normal_vectors.index(vn) + 1))
    
    
def gen_vn(face):
    # obtain indices of the face and create a points list which will have the vertices of the current face
    v1, v2, v3 = face
    points = [vertices[v1-1], vertices[v2-1], vertices[v3-1]]
    
    p1, p2, p3 = points #obtaining vertices from the points list
    
    # vector 1 will be calculated by doing p2 - p1
    v1 = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
    
    # vector 2 will be calculated by doing p3 - p1
    v2 = (p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2])
    
    #obtain the cross product of v1 and v2
    vn = cross_product(v1, v2)
    
    # add normal vector only if it is not present in the normal vectors list
    if vn not in normal_vectors:
        normal_vectors.append(vn)
    
    return vn #return normal vector


def cross_product(v1, v2):
    # obtaining the components of each vector
    vx1, vy1, vz1 = v1
    vx2, vy2, vz2 = v2
    
    # calculating the cross product of 2 vectors to obtain the normal vector 
    vn = (round(vy1*vz2 - vz1*vy2,4), round(-(vx1*vz2 - vz1*vx2),4), round(vx1*vy2 - vy1*vx2,4))
    
    # calculamos la magnitud del vector normal
    magnitude = math.sqrt(math.pow(vn[0],2) + math.pow(vn[1],2) + math.pow(vn[2],2))
    
    # normalizamos el vector normal
    normalized_vector = (round((vn[0] / magnitude), 4), round((vn[1] / magnitude), 4), round((vn[2] / magnitude), 4))
    
    return normalized_vector #retornamos el vector normalizado
    
    
def create_obj_file(V, F, VN):
    # Open a .obj file for writing
    with open('car_wheel.obj', 'w') as file:
        # Write the data to the file
        # vertices
        file.write(f'# Vertices: {len(V)}\n')
        for vertex in V:
            (x,y,z) = vertex
            file.write(f'v {x} {y} {z}\n')
        
        #normals
        file.write(f'# Normals: {len(VN)}\n')
        for vn in VN:
            (x,y,z) = vn
            file.write(f'vn {x} {y} {z}\n')
        
        #faces
        file.write(f'# Faces: {len(F)}\n')
        for tuple in F:
            (face, vn_id) = tuple
            x,y,z = face
            file.write(f'f {x}//{vn_id} {y}//{vn_id} {z}//{vn_id}\n')
    
        
def main():
    # argumentos via terminal
    args = sys.argv[1:]
    
    # validamos cuantos argumentos se pasan
    if len(args) == 0:
        create_wheel_model()
    elif len(args) == 1:
        numSides = args[0]
        create_wheel_model(int(numSides))
    elif len(args) == 2:
        numSides, radius = args
        create_wheel_model(int(numSides), float(radius))
    elif len(args) == 3:
        numSides, radius, width = args
        create_wheel_model(int(numSides), float(radius), float(width))
    else:
        sys.exit(f"ERROR, ONLY 3 ARGUMENTS EXPECTED, {len(args)} GIVEN")
        
    
main()
    
    