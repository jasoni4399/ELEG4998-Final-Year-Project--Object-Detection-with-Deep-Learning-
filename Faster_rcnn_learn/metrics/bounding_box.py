import logging 
from typing import Optional

from metrics.enumerators import(
    BBFormat,
    BBType,
    CoordinatesType,
)
from metrics.general_utils import(
    convert_to_absolute_values,
    convert_to_relative_values,
)

logger: logging.Logger=logging.getLogger(__name__)

class Boundingbox:
    def __init__(
            self,
            image_name:str,
            class_id:Optional[str]=None,
            coordinates:Optional[tuple]=None,
            type_coordinates:CoordinatesType=CoordinatesType.ABSOLUTE,
            img_size: Optional[tuple]=None,
            bb_type:BBType=BBType.GROUND_TRUTH,
            confidence:Optional[float]=None,
            format:BBFormat=BBFormat.XYWH,
            ):
        self._image_name=image_name
        self._type_coordinates=type_coordinates
        self._confidence=confidence
        self._class_id=class_id
        self._format=format
        if (bb_type==BBType.DETECTED and confidence is not None):
            raise IOError(
                "For bb_type='Detected', it is necessary to inform the confidence value."
            )
        self._bb_type=bb_type

        if img_size is None:
            self._width_img=None
            self._height_img=None
        else:
            self._width_img=img_size[0]
            self._height_img=img_size[1]

        self.set_coordinates(
            coordinates,
            img_size=img_size,
            type_coordinates=type_coordinates
        )

    def set_coordinates(self, coordinates, type_coordinates, img_size=None):
        self._type_coordinates=type_coordinates
        if(type_coordinates==CoordinatesType.RELATIVE and img_size is None):
            raise IOError(
                "Parameter 'img_size' is required. It is necessary to inform the image size."
            )
        
        if(type_coordinates==CoordinatesType.RELATIVE):
            #(x,y,w,h)=(X_center/img_width , Y_center/img_height)
            self._width_img=img_size[0]
            self._height_img=img_size[1]
            if self._format==BBFormat.XYWH:
                (self._x,self._y,self._w,self._h)=convert_to_absolute_values(img_size,coordinates)
                self._x2=self._w
                self._y2=self._h
                self._w=self._x2-self._x
                self._h=self._y2-self._y
            elif self._format==BBFormat.XYX2Y2:
                x1,y1,x2,y2=coordinates
                self._x=round(x1*self._width_img)
                self._x2=round(x2*self._width_img)
                self._y=round(y1*self._height_img)
                self._y2=round(y2*self._height_img)
                self._w=self._x2-self._x
                self._h=self._y2-self._y
            else:
                raise IOError(
                    "For relative coordinates, the format must be XYWH (x,y,width,height)"
                )
        else:
            #(x,y,w,h)=real bb coords
            self._x=coordinates[0]
            self._y=coordinates[1]
            if self._format==BBFormat.XYWH:
                self._w=coordinates[2]
                self._h=coordinates[3]
                self._x2=self._x+self._w
                self._y2=self._y+self._h
            else:
                self._x2=coordinates[2]
                self._y2=coordinates[3]
                self._w=self._x2-self._x
                self._h=self._y2-self._y
        self._x=float(self._x)
        self._y=float(self._y)
        self._w=float(self._w)
        self._h=float(self._h)
        self._x2=float(self._x2)
        self._y2=float(self._y2)

    def get_absolute_bounding_box(self,format=BBFormat.XYWH):
        if format==BBFormat.XYWH:
            return self._x,self._y,self._w,self._h
        elif format==BBFormat.XYX2Y2:
            return self._x,self._y,self._x2,self._y2
        
    def get_relative_bounding_box(self,img_size=None):
        if img_size is None and self._width_img is None and self._height_img is None:
            raise IOError(
                "Parameter 'img_size' is required. It is necessary to inform the image size."
            )
        if img_size is not None:
            return convert_to_relative_values(
                (img_size[0],img_size[1]),
                (self._x,self._x2,self._y,self._y2)
            )
        else:
            if img_size is None and self._width_img is None and self._height_img is None:
                raise IOError(
                "Parameter 'img_size' is required. It is necessary to inform the image size."
            )
            if img_size is not None:
                return convert_to_relative_values(
                    (self._width_img,self._height_img),
                    (self._x,self._x2,self._y,self.y2),
                )
            
    def get_image_name(self):
        return self._image_name
    
    def get_confidence(self):
        return self._confidence
    
    def get_format(self):
        return self._format
    
    def set_class_id(self,class_id):
        self._class_id=class_id

    def set_bb_type(self,bb_type):
        self._bb_type=bb_type
    
    def get_class_id(self):
        return self._class_id
    
    def get_image_size(self):
        return self._width_img,self._height_img
    
    def get_area(self):
        assert self._x2>self._x
        assert self._y2>self._y
        return (self._x2-self._x+1)*(self._y2-self._y+1)
    
    def get_coordinates_type(self):
        