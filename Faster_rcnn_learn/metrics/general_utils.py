import logging

logger: logging.Logger=logging.getLogger(__name__)

def convert_to_relative_values(size:tuple,box:tuple):
    dw=1.0/size[0]
    dh=1.0/size[1]
    cx=(box[1]+box[0])/2.0
    cy=(box[3]+box[2])/2.0
    w=box[1]-box[0]
    h=box[3]-box[2]
    x=cx*dw
    y=cy*dh
    w=w*dw
    h=h*dh
    return x,y,w,h

def convert_to_absolute_values(size:tuple,box:tuple):
    w_box=size[0]*box[2]
    h_box=size[1]*box[3]

    x1=(float(box[0])*float(size[0]))-(w_box/2)
    y1=(float(box[1])*float(size[1]))-(h_box/2)
    x2=x1+w_box
    y2=y1+h_box
    return round(x1),round(y1),round(x2),round(y2)