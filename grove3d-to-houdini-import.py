filename = "F:/projects/005_renderTests/grove3d/tree01/twigs.pckl"
twigLib = "/obj/twig_lib/" 
twigsApical = ["ScotsPineTwigApical"]
twigsLateral = ["ScotsPineTwig","ScotsPineTwigA","ScotsPineTwigB","ScotsPineTwigC"]
scaleRandom = 0.2

#===================================================================================

import pickle, random
node = hou.pwd()
geo = node.geometry()

def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]

fixRM = hou.hmath.buildRotate(-90, 0, 0) # builds rotation Matrix to fix blender coordinates       

infile = open(filename,'rb')
sys_dict = pickle.load(infile)
infile.close()

geo.addAttrib(hou.attribType.Point, "typ", "")
geo.addAttrib(hou.attribType.Point, "orient", (0.0,0.0,0.0,0.0))
geo.addAttrib(hou.attribType.Point, "rotD", (0.0,0.0,0.0))
geo.addAttrib(hou.attribType.Point, "instance", "")
geo.addAttrib(hou.attribType.Point, "pscale", 1.0)
geo.addAttrib(hou.attribType.Point, "id", 0.0)

idC = 0.0
for sysName in sys_dict.keys():
    psys = sys_dict[sysName] # extract particle system name 
    locs = chunks(psys[0],3) # extract locations
    rots = chunks(psys[1],3) # extract rotations

    for p,r in zip(locs,rots):
        np = geo.createPoint()
        
        #set postion
        pM = hou.hmath.buildTranslate(p) #convert to translation matrix4
        fp = (pM*fixRM).extractTranslates() #rotate by fixRM 
        np.setPosition(fp)        
        
        #set rotation
        rE = (hou.hmath.radToDeg(r[0]),hou.hmath.radToDeg(r[2]),hou.hmath.radToDeg(r[1])) #convert to degrees
        rQ = hou.Quaternion(hou.hmath.buildRotate(rE, "xyz"))
        np.setAttribValue("orient", rQ)
        
        #set twig instance path
        if sysName == "Lateral Twigs":
             np.setAttribValue("instance", twigLib + random.choice(twigsLateral))
        elif sysName == "Apical Twigs":
             np.setAttribValue("instance", twigLib + random.choice(twigsApical))
             
        #set pscale
        np.setAttribValue("pscale", random.uniform(1-scaleRandom, 1+scaleRandom))
        
        #set id
        np.setAttribValue("id", idC)
        idC = idC+1.0
