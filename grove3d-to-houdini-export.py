filename = "F:/projects/005_renderTests/grove3d/tree01/twigs.pckl"

#================================================================

import bpy
import pickle
import numpy as numpy
import mathutils, math

def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]

outsys= dict()
ob = bpy.context.active_object
depsgraph = bpy.context.evaluated_depsgraph_get()
eval_ob = ob.evaluated_get(depsgraph)

for psys in eval_ob.particle_systems:
    
    #postions
    par_loc = [0,0,0]*len(psys.particles)
    psys.particles.foreach_get("location", par_loc) #gets postions in one long list 
    
    #rotations
    par_rot = [0,0,0,0]*len(psys.particles)
    psys.particles.foreach_get("rotation", par_rot) #gets rotation quaterions in one long list 
    
    par_locE = []
    par_rotE = []
    locs = chunks(par_loc,3)
    rots = chunks(par_rot,4)
    
    for l,r in zip(locs,rots):

        mtx4_z90 = mathutils.Matrix.Rotation(math.pi / 2.0, 4, 'Z') # stolen from blender fbx export
        
        #reorient locations
        mtx = mathutils.Matrix.Translation(l).to_4x4()@ mtx4_z90
        loc, rot, sca = mtx.decompose()
        
        par_locE.append(loc[0])
        par_locE.append(loc[1])
        par_locE.append(loc[2])
        
        #reorient rotations
        bq = mathutils.Quaternion(r) #convert to blender quaterion    
        eu = bq.to_euler() #convert to radians ??
        mtx =  eu.to_matrix().to_4x4()@ mtx4_z90 
        loc, rot, sca = mtx.decompose()
        
        par_rotE.append(rot.to_euler()[0])
        par_rotE.append(rot.to_euler()[1])
        par_rotE.append(rot.to_euler()[2])
        
        

    #add to final dict
    outsys[psys.name] = [par_locE,par_rotE]




outfile = open(filename,'wb')
pickle.dump(outsys,outfile, protocol=2)
outfile.close()
