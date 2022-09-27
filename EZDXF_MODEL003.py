## This is a hard coded dxf model of the angle bracket

from ctypes import Union
from ssl import VERIFY_X509_PARTIAL_CHAIN, PROTOCOL_TLSv1_1
import ezdxf 
#add new entities to the modelspace

import matplotlib.pyplot as plt
from ezdxf import recover, entities, math
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.properties import Properties, LayoutProperties
from ezdxf.math import Vec3
import csv
import math 

def printVIEW(doc):
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    layout_properties = LayoutProperties.from_layout(doc.modelspace())
    layout_properties.set_colors(bg='#FFFFFF')
    ctx = RenderContext(doc)
    out = MatplotlibBackend(ax)
    Frontend(ctx, out).draw_layout(doc.modelspace(), layout_properties=layout_properties, finalize=True)
    plt.show() #Image to show the new model
    # fig.savefig('your.png', dpi=300)
    return


def modelView(msp, doc, viewPlane, toolDims, partDims):
    
    """ Determine the view plane"""
    # IF ISO, X rotation of arcsin(tan(30deg)) and y rotation of -45 degrees"""
    if viewPlane == "Front": #+X+Y
        xval = math.radians(0)
        yval = math.radians(0)
    if viewPlane == "Back": #-Y+X
        xval = math.radians(0)
        yval = math.radians(180)
    if viewPlane == "Top": #-Y+X
        xval = math.radians(90)
        yval = math.radians(0)
    if viewPlane == "Bottom": #-Y+X
        xval = math.radians(-90)
        yval = math.radians(0)
    if viewPlane == "Left": #-Y+X
        xval = math.radians(0)
        yval = math.radians(90)
    if viewPlane == "Right": #-Y+X
        xval = math.radians(0)
        yval = math.radians(270)
    if viewPlane == "Isometric": #ISO
        xval = 0.61549709
        yval = math.radians(-45)
    # # Change the view plane
    ucs = ezdxf.math.UCS(origin = (0,0,0)).rotate_local_x(xval).rotate_local_y(yval)




    # # TOOL VERTICES ASSOCIATIONS WITH DIMENSIONS
    # toolDims = [view, t_1, t_2, t_3, t_4, t_5, t_6, t_7]
    v1 = [0, 0, 0]
    v2 = [0, toolDims[2]+toolDims[3]+toolDims[5], 0]
    v3 = [toolDims[4], toolDims[2]+toolDims[3]+toolDims[5], 0]
    v4 = [toolDims[4], toolDims[3]+toolDims[5],0]
    v5 = [toolDims[1]+toolDims[4]+toolDims[5], 0, 0]
    v6 = [toolDims[1]+toolDims[4]+toolDims[5], toolDims[3], 0]
    v7 = [toolDims[4]+toolDims[5], toolDims[3], 0]
    v8 = [toolDims[4]+toolDims[5], toolDims[3]+toolDims[5],0]

    v1d = [0, 0, toolDims[6]]
    v2d = [0, toolDims[2]+toolDims[3]+toolDims[5],toolDims[6]]
    v3d = [toolDims[4], toolDims[2]+toolDims[3]+toolDims[5], toolDims[6]]
    v4d = [toolDims[4], toolDims[3]+toolDims[5],toolDims[6]]
    v5d = [toolDims[1]+toolDims[4]+toolDims[5], 0, toolDims[6]]
    v6d = [toolDims[1]+toolDims[4]+toolDims[5], toolDims[3], toolDims[6]]
    v7d = [toolDims[4]+toolDims[5], toolDims[3],toolDims[6]]
    v8d = [toolDims[4]+toolDims[5], toolDims[3]+toolDims[5],toolDims[6]]




    # # # Add Tool Layer 
    layerTool = doc.layers.add("Tool")

    # Z=0, back face
    msp.add_line(v1, v2, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) # vert 1, 2 (leg base)
    msp.add_line(v2, v3, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) #vert 2, 3 (leg thickness)
    msp.add_line(v3, v4, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) #vert 3, 4 (leg inner)
    msp.add_line(v5, v1, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) #vert 5, 1 (leg base)
    msp.add_line(v6, v7, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) #vert 6, 7 (leg inner)
    msp.add_line(v6, v5, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) #vert 6, 5 (leg thickness)
    msp.add_arc(center=v8, radius=toolDims[5], 
        start_angle=180, end_angle=270, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) #vert 8

    # # Z=+0, front face
    msp.add_line(v1d,v2d, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) # vert 1, 2 (leg base)
    msp.add_line(v2d, v3d, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) #vert 2, 3 (leg thickness)
    msp.add_line(v3d, v4d, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) #vert 3, 4 (leg inner)
    msp.add_line(v5d, v1d, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) #vert 5, 1 (leg base)
    msp.add_line(v6d, v7d, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) #vert 6, 7 (leg inner)
    msp.add_line(v6d, v5d, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) #vert 6, 5 (leg thickness)
    msp.add_arc(center=v8d, radius=toolDims[5], 
        start_angle=180, end_angle=270, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) #vert 8

    # # Add Tool Layer DEPTH
    msp.add_line(v1,v1d, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) # vert 1
    msp.add_line(v2,v2d, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) # vert 2
    msp.add_line(v3,v3d, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) # vert 3
    msp.add_line(v4,v4d, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) # vert 4
    msp.add_line(v5,v5d, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) # vert 5
    msp.add_line(v6,v6d, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) # vert 6
    msp.add_line(v7,v7d, dxfattribs={'layer': 'Tool'}).transform(ucs.matrix) # vert 7

    """TOOL DIMENSIONS EZDXF"""
    dim = msp.add_aligned_dim(p1=(v1), p2=(v2), distance=.05, override={"dimtsz": 0,"dimtxt": 0.01, "dimdec" : 4, "dimdsep":ord('.'), "dimexo" :0.005, "dimexe":0.005}, dxfattribs={ 'layer': 'Tool'})
    dim2 = msp.add_aligned_dim(p1=(v1), p2=(v5), distance=-.05, override={"dimtsz": 0,"dimtxt": 0.01, "dimdec" : 4, "dimdsep":ord('.'), "dimexo" :0.005, "dimexe":0.005}, dxfattribs={ 'layer': 'Tool'})
    
    dim.set_arrows(size=0.02)
    dim2.set_arrows(size=0.02)


    dim.render(ucs)
    dim2.render(ucs)


    # # # Add Part Layer
    layerPart = doc.layers.add("Part")

    # # PART VERTICES ASSOCIATIONS WITH DIMENSIONS
    v9 = [toolDims[4],toolDims[5]+toolDims[3]+partDims[2], 0]
    v10 = [toolDims[5]+toolDims[4]+partDims[1], toolDims[3], 0]
    v11 = [toolDims[3]+partDims[3], toolDims[5]+toolDims[3]+partDims[2], 0]
    v12 = [toolDims[5]+toolDims[4]+partDims[1], toolDims[4]+partDims[3],0]
    v13 = [toolDims[3]+partDims[3], toolDims[5]+toolDims[3], 0]
    v14 = [toolDims[5]+toolDims[4], toolDims[3]+partDims[3], 0]

    v9d = [toolDims[4],toolDims[5]+toolDims[3]+partDims[2], partDims[5]+partDims[4]]
    v10d = [toolDims[5]+toolDims[4]+partDims[1], toolDims[3], partDims[5]+partDims[4]]
    v11d = [toolDims[3]+partDims[3], toolDims[5]+toolDims[3]+partDims[2], partDims[5]+partDims[4]]
    v12d = [toolDims[5]+toolDims[4]+partDims[1], toolDims[4]+partDims[3],partDims[5]+partDims[4]]
    v13d = [toolDims[3]+partDims[3], toolDims[5]+toolDims[3], partDims[5]+partDims[4]]
    v14d = [toolDims[5]+toolDims[4], toolDims[3]+partDims[3], partDims[5]+partDims[4]]

    # dim3 = msp.add_aligned_dim(p1=(v11), p2=(v13), distance=.05, override={"dimjust": 3, "dimtsz": 0,"dimtxt": 0.01, "dimdec" : 4, "dimdsep":ord('.'), "dimexo" :0.005, "dimexe":0.005}, dxfattribs={ 'layer': 'Tool'})
    # dim3.set_arrows(size=0.02)
    # dim3.render(ucs)
    # # Z=0, back face    
    msp.add_line(v9, v4, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) #vert 9, 4 (leg base)
    msp.add_line(v7, v10, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) #vert 7, 10 (leg base)
    msp.add_line(v9, v11, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) #vert 9, 11 (leg thickness)
    msp.add_line(v10, v12, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) #vert 10, 12 (leg thickness)
    msp.add_line(v11, v13, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) #vert 11, 13 (leg inner))
    msp.add_line(v12, v14, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) #vert 12, 14 (leg inner))
    msp.add_arc(center=v8, radius=toolDims[5], 
        start_angle=180, end_angle=270, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) #vert 8, radius base
    msp.add_arc(center=v8, radius=toolDims[5]-partDims[3], 
        start_angle=180, end_angle=270, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) #vert 8, radius inner
    
    # # Z = +, front face
    msp.add_line(v9d, v4d, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) #vert 9, 4 (leg base)
    msp.add_line(v7d, v10d, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) #vert 7, 10 (leg base)
    msp.add_line(v9d, v11d, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) #vert 9, 11 (leg thickness)
    msp.add_line(v10d, v12d, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) #vert 10, 12 (leg thickness)
    msp.add_line(v11d, v13d, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) #vert 11, 13 (leg inner))
    msp.add_line(v12d, v14d, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) #vert 12, 14 (leg inner))
    msp.add_arc(center=v8d, radius=toolDims[5], 
        start_angle=180, end_angle=270, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) #vert 8, radius base
    msp.add_arc(center=v8d, radius=toolDims[5]-partDims[3], 
        start_angle=180, end_angle=270, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) #vert 8, radius inner

    # # PART Layer DEPTH
    msp.add_line(v9,v9d, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) # vert 9
    msp.add_line(v10,v10d, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) # vert 10
    msp.add_line(v11,v11d, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) # vert 11
    msp.add_line(v12,v12d, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) # vert 12
    msp.add_line(v13,v13d, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) # vert 13
    msp.add_line(v14,v14d, dxfattribs={'layer': 'Part'}).transform(ucs.matrix) # vert 14

    """PART DIMENSIONS"""
    
    if toolDims[0] == "X":
        layerTool.off() 
    if partDims[0] == "X":
        layerPart.off() 


    return (doc)


def importDims(msp, doc):
    #import from csv
    with open('Dims.csv', mode='r') as f:
        csv_reader = csv.reader(f)
        importList = list(csv_reader)
        importDict = {}
        for row in importList:
            importDict[row[0]] = row[1:]

    ## Importing Tool Dim Values
    toolShow = importDict["T"][1] #supress tool value
    t_1 = float(importDict["T-1"][2])
    t_2 = float(importDict["T-2"][2])
    t_3 = float(importDict["T-3"][2])
    t_4 = float(importDict["T-4"][2])
    t_5 = float(importDict["T-5"][2])
    t_6 = float(importDict["T-6"][2])
    t_7 = float(importDict["T-7"][2]) 
    toolDims = [toolShow, t_1, t_2, t_3, t_4, t_5, t_6, t_7]

    ## Importing Part Dim Values
    partShow = importDict["P"][1]
    p_1 = float(importDict["P-1"][2])
    p_2 = float(importDict["P-2"][2])
    p_3 = float(importDict["P-3"][2])
    p_4 = float(importDict["P-4"][2])
    p_5 = float(importDict["P-5"][2])
    partDims = [partShow, p_1, p_2, p_3, p_4, p_5]
    viewPlane = importDict["V"][2]

    doc = modelView(msp, doc, viewPlane, toolDims, partDims)
    return (doc)

def main():
    doc = ezdxf.new(dxfversion="R2010", setup=False, units=6) 
    doc.header['$INSUNITS'] = 6
    msp = doc.modelspace() 
    doc = importDims(msp, doc)
    
    ## If we wanted to save and reopen
    # doc.saveas("ExampleModel.dxf")
    # docs, auditor = recover.readfile("ExampleModel.dxf")

    # # Print new model view
    printVIEW(doc)

if __name__ == '__main__':
    main()
