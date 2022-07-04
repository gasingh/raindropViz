"""
raindrop simulator_v0

19:47 02/11/2021

REFERENCE NOTE:
The code here is derived from an algorithm discussed in the following publication from Harvard GSD:    
    vb-workshop-harvard-gsd-woojsung-com1.pdf
    https://woojsung.com/2011/11/24/vb-workshop-harvard-gsd/
"""

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import scriptcontext
import math

srfID = rs.GetObject("sel SRF",rs.filter.surface)
srfRC = rs.coercesurface(srfID)

ptRC = rs.GetPointOnSurface(srfRC,"please select a point on the SRF: to simulate a water drop!")
print type(ptRC)

def getRainDropPt(srfRC,ptRC,scaleVal):
    """
    retrieves raindrop next location based on input params
    19:52 02/11/2021
    """
    u,v = srfRC.ClosestPoint(ptRC)[1:]
    vN = srfRC.NormalAt(u,v)
    vZ = rg.Plane.WorldXY.ZAxis
    vX = rg.Vector3d.CrossProduct(vN,vZ)
    vX.Unitize()
    vX.Reverse()
    #print vX
    
    vX.Rotate(math.radians(-90),vN)
    vec2Ln = lambda v1,v2 : rg.Line(v1,v2)
    if scaleVal == None:
         scaleVal = 0.005
    vecScale = lambda v1, v2 : rg.Vector3d.Multiply(v2,v1)  #input vec, num
    vX = vecScale(vX,scaleVal)
    lnRC = vec2Ln(ptRC,vX)
    ptRC_future = rg.Point3d.Add(ptRC,vX)
    
    #srfNearPt = lambda *srfRC.ClosestPoint(ptRC)[1:]
    u_future,v_future = srfRC.ClosestPoint(ptRC_future)[1:]
    ptRC_futureStuck = srfRC.PointAt(u_future,v_future)
    
    #scriptcontext.doc.ActiveDoc.Objects.AddLine(lnRC)
    return [ptRC_futureStuck,vX,lnRC]

scaleVal = 0.005
ptLstRC = []
for i in range(5000):
    if i == 0:
        ptLast = getRainDropPt(srfRC,ptRC,scaleVal)[0]
    else:
        ptLast = getRainDropPt(srfRC,ptLast,scaleVal)[0]
        ptLstRC.append(ptLast)
#ptLst = map(scriptcontext.doc.ActiveDoc.Objects.AddPoint,ptLstRC)
#rs.AddObjectsToGroup(ptLst,rs.AddGroup())
crvRC = rg.Curve.CreateInterpolatedCurve(ptLstRC,3)
crvID = scriptcontext.doc.ActiveDoc.Objects.AddCurve(crvRC)
