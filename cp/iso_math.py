

import sys, copy, math
import gfx



def isoProjection(pos3d,tile_size,iso_size, real_size):

    x,y,z = pos3d

    tx, ty = tile_size
    x = float(x) * float(tx)
    y = float(y) * float(ty)

    cx, cy = iso_size
    cx = float(cx)/2
    cy = float(cy)/2

    #translates de point to the center
    x = x - cx
    y = y - cy

    #rotates the point 45 degrees an divide y by 2 
    xpos, ypos = gfx.rotate45((x,y))

    cosx = -0.866
    ypos = z*cosx-(ypos/2)

    ncx,ncy = real_size

    xpos = xpos + (float(ncx)/2) 
    ypos = ypos + (float(ncy)/2) 

    return (xpos,ypos)

    
def getIsoPoint(pos,total_size,original_size, floor_size):

    x,y = pos

    ncx,ncy = total_size
    ncx = float(ncx)
    ncy = float(ncy)
    x = x-(ncx/2)
    y = y-(ncy/2)

    y = -y*2

    x,y = gfx.rotate45((x,y))
    
    cx, cy = original_size
    cx = float(cx)/2
    cy = float(cy)/2

    #translates de point to the center
    tx, ty = floor_size

    x = (x + cx)/tx
    y = (y + cy)/ty    
    
    return int(x),int(y)
