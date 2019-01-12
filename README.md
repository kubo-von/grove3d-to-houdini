# grove3d-to-houdini

Python scripts for exporting trees from grove3d to houdini with twing instancing.

Don't expect anything polished, I made these as my personal messy R&D.

This setup works for Renderman and Mantra, for Redshift or Arnold it migth need slight adjustments but I haven't tested it.<br>

<h2>Tutorial:</h2>

<h3>1.Blender</h3>
Open grove3d-to-houdini-export.py in the text editor, change the path on the first line to where you want the twig file to be exported. 
Select the tree trunk and Run the script<br>
Export the trunk as Alembic file (tick "Vertex Colors" if you want to use  grove3d attributtes like  thickness, Power etc..   )<br>
Export each twig you want to use as an alembic file.<br>

![alt text](https://github.com/kubo-von/grove3d-to-houdini/blob/master/help/scr01.JPG)


<h3>2.Houdini - scene preparation</h3>
Create geometry node for the trunk, load it with Alembic node. <br>
Create instance node, set it to "fast point instancing" and name it e.g. "twigs". <br>
Create Subnet called e.g. twig_lib", inside it create geometry node for each twig you exported from Blender. In the geometry node load the alembic files with alembic node and add transform node with Y rotation set to -90. <br>

![alt text](https://github.com/kubo-von/grove3d-to-houdini/blob/master/help/scr02.JPG)
![alt text](https://github.com/kubo-von/grove3d-to-houdini/blob/master/help/scr03.JPG)




<h3>3.Houdini - Reading the points</h3>
Go inside the instance node ("twigs") and delete the "add" node<br>

Create python node and paste content of grove3d-to-houdini-import.py as the node's Code<br>

![alt text](https://github.com/kubo-von/grove3d-to-houdini/blob/master/help/scr04.JPG)

Edit the varibles on the first few lines:<br>

filename = the .pckl file we exported from blender<br>
twigLib = "path to twing_lib subnet"<br>
twigsApical = array of geometry nodes from twig_lib that you want use as apical twigs<br>
twigsLateral = array of geometry nodes from twig_lib that you want use as lateral twigs<br>
scaleRandom = twing scale randomnes<br>

Jump out of the instance node and you should see the twigs being instanced in the viewport:
![alt text](https://github.com/kubo-von/grove3d-to-houdini/blob/master/help/scr05.JPG)

