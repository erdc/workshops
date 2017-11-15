from pythreejs import *
from IPython.display import set_matplotlib_formats,display
from matplotlib import pyplot, collections
import mpl_toolkits.mplot3d as a3
import matplotlib.colors as colors
import pylab as pl
from matplotlib import pyplot as plt
import pylab
from proteus import SpatialTools as st
import numpy as np

def plot_domain(domain, elev=0, azim=0, segmentFlags=None, vertexFlags=None, regionFlags=None):
    bc = domain.shape_list[0].BC_class
    st._assembleGeometry(domain, bc)
    if domain.nd == 2:
        lines = []
        cmap = pylab.get_cmap("jet")
        c = []
        shape_nb = float(len(domain.shape_list))
        annotate_coords_seg = []
        annotate_label_seg = []
        annotate_coords_ver = []
        annotate_label_ver = []
        annotate_coords_reg = []
        annotate_label_reg = []
        start_global_flag = 0
        if segmentFlags=='global': shapes_s = [domain];
        elif segmentFlags=='local' or segmentFlags is None: shapes_s = domain.shape_list
        if vertexFlags=='global': shapes_v = [domain];
        elif vertexFlags=='local' or vertexFlags is None: shapes_v = domain.shape_list
        if regionFlags=='global': shapes_r = [domain];
        elif regionFlags=='local' or regionFlags is None: shapes_r = domain.shape_list
        for i, shape in enumerate(shapes_s):
            for s,sF in zip(shape.segments, shape.segmentFlags):
                lines.append([shape.vertices[s[0]], shape.vertices[s[1]]])
                c.append(cmap(float(i/shape_nb)))
                annotate_coords_seg += [np.array((np.array(shape.vertices[s[0]])+np.array(shape.vertices[s[1]]))/2.).tolist()]
                annotate_label_seg += [sF]
        for i, shape in enumerate(shapes_v):
            for v, vF in zip(shape.vertices, shape.vertexFlags):
                annotate_coords_ver += [v]
                annotate_label_ver += [vF]
        for i, shape in enumerate(shapes_r):
            for r, rF in zip(shape.regions, shape.regionFlags):
                annotate_coords_reg += [r]
                annotate_label_reg += [rF]
        lc = collections.LineCollection(lines,colors=c,linewidths=3)
        fig, ax = pyplot.subplots()
        if segmentFlags is not None:
            for i, label in enumerate(annotate_label_seg):
                ax.annotate(str(label), size=10, xy=annotate_coords_seg[i], xycoords='data',
                bbox=dict(boxstyle="round", edgecolor='green', facecolor=(0,0,0,0)))
        if vertexFlags is not None:
            for i, label in enumerate(annotate_label_ver):
                ax.annotate(str(label), size=10, xy=annotate_coords_ver[i], xycoords='data',
                bbox=dict(boxstyle="round", edgecolor='blue', facecolor=(0,0,0,0)))
        if regionFlags is not None:
            for i, label in enumerate(annotate_label_reg):
                ax.annotate(str(label), size=10, xy=annotate_coords_reg[i], xycoords='data',
                bbox=dict(boxstyle="round", edgecolor='red', facecolor=(0,0,0,0)))
        ax.add_collection(lc)
        ax.margins(0.1)
        ax.set_aspect('equal')
        #pylab.savefig("pslg.pdf")
    if domain.nd == 3:
        ax = a3.Axes3D(pl.figure(),elev=elev,azim=azim)
        cmap = pylab.get_cmap("hsv")
        fN_max = float(max(domain.facetFlags))
        verts=[]
        c=[]
        for f,fN in zip(domain.facets,domain.facetFlags):
            verts.append([domain.vertices[vN] for vN in f[0]])
            #c.append(cmap(fN/fN_max))
        ply = a3.art3d.Poly3DCollection(verts)
        #ply.set_facecolors(c)
        ax.add_collection3d(ply)
        ax.margins(0.1,0.1,0.1)
        ax.set_aspect('equal')
        ax.set_xlim(domain.x[0],max(domain.L))
        ax.set_ylim(domain.x[1],max(domain.L))
        ax.set_zlim(domain.x[2],max(domain.L))
        pylab.savefig("plc.pdf")

def plot_js(domain):
    bc = domain.shape_list[0].BC_class
    st._assembleGeometry(domain, bc)
    faces3=[]
    facesn=[]
    vertices=[]
    va = np.array(domain.vertices)
    cg = va.mean(0)
    for v in domain.vertices:
        vertices+=(np.array(v)-cg).tolist()
    for facet in domain.facets:
        for face in facet:
            facesn.append(face)
            for i in range(len(face)-2):
                faces3.append([face[0],face[i+1],face[i+2]])
    p  = FaceGeometry(face3=[],face4=[],facen=facesn,vertices=vertices)
    mat = BasicMaterial(side='DoubleSide',color='red')
    m = Mesh(geometry=p, material=mat)
    scene = Scene(children=[m, AmbientLight(color=0x777777)])
    scene.background=0x777777
    c = PerspectiveCamera(position=[0,domain.x[1]+1.5*domain.L[1],domain.x[2]+1.5*domain.L[2]], up=[0,0,1], 
                          children=[DirectionalLight(color=0x777777, position=[3,5,1], intensity=0.6)])
    renderer = Renderer(camera=c, scene = scene, controls=[OrbitControls(controlling=c)],background="grey")
    display(renderer)