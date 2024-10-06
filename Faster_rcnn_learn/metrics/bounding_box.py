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

class BoundingBox:
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
        return self._type_coordinates
    
    def get_bb_type(self):
        return self._bb_type
    
    def __str__(self):
        abs_bb_xywh=self.get_absolute_bounding_box(format=BBFormat.XYWH)
        abs_bb_xyx2y2=self.get_absolute_bounding_box(format=BBFormat.XYX2Y2)
        area=self.get_area()
        return(
            f"image name: {self._image_name}\n"
            f"image size: {self.get_image_size()}\n"
            f"class: {self._class_id}\n"
            f"bb (XYWH): {abs_bb_xywh}\n"
            f"bb (X1Y1X2Y2): {abs_bb_xyx2y2}\n"
            f"area: {area}\n"
            f"bb_type: {self._bb_type}"
        )
    
    def __eq__(self,other):
        if not isinstance(other, BoundingBox):
            return False
        return str(self)==str(other)

    def __repr__(self):
        abs_bb_xywh = self.get_absolute_bounding_box(format=BBFormat.XYWH)
        abs_bb_xyx2y2 = self.get_absolute_bounding_box(format=BBFormat.XYX2Y2)
        area=self.get_area()
        return f"{self._bb_type}(bb (XYWH): {abs_bb_xywh}, bb (X1Y1X2Y2): {abs_bb_xyx2y2},area: {area}), class: {self._class_id})"
    
    @staticmethod
    def iou(box_a,box_b):
        coords_a = box_a.get_absolute_bounding_box(format=BBFormat.XYX2Y2)
        coords_b = box_b.get_absolute_bounding_box(format=BBFormat.XYX2Y2)
        if BoundingBox.has_intersection_area(coords_a,coords_b)is False:
            return 0
        inter_area=BoundingBox.get_intersection_area(coords_a,coords_b)
        union=BoundingBox.get_union_areas(box_a,box_b,inter_area=inter_area)
        iou=inter_area/union
        assert iou>=0
        return iou
    
    @staticmethod
    def have_intersection(box_a,box_b):
        if isinstance(box_a,BoundingBox):
            box_a=box_a.get_absolute_bounding_box(BBFormat.XYX2Y2)
        if isinstance(box_b,BoundingBox):
            box_b=box_b.get_absolute_bounding_box(BBFormat.XYX2Y2)
        if box_a[0]>box_b[2]:
            return False
        if box_b[0]>box_a[2]:
            return False
        if box_a[3]<box_b[1]:
            return False
        if box_a[1]>box_b[3]:
            return False
        return True
    
    @staticmethod
    def get_intersection_area(box_a,box_b):
        if isinstance(box_a,BoundingBox):
            box_a=box_a.get_absolute_bounding_box(BBFormat.XYX2Y2)
        if isinstance(box_b,BoundingBox):
            box_b=box_b.get_absolute_bounding_box(BBFormat.XYX2Y2)
        x_a=max(box_a[0],box_b[0])
        y_a=max(box_a[1],box_b[1])
        x_b=min(box_a[2],box_b[2])
        y_b=min(box_a[3],box_b[3])

        return (x_b-x_a+1)*(y_b-y_a+1)
    
    @staticmethod
    def get_union_areas(box_a,box_b,inter_area=None):
        area_a=box_a.get_area()
        area_b=box_b.get_area()
        if inter_area is None:
            inter_area=BoundingBox.get_intersection_area(box_a,box_b)
        return float(area_a+area_b-inter_area)
    
    @staticmethod
    def get_amount_bounding_box_all_classes(bounding_boxes,reverse=False):
        classes=list(set([bb._class_id for bb in bounding_boxes]))
        ret={}
        for c in classes:
            ret[c]=len(BoundingBox.get_bounding_box_by_class(bounding_boxes,c))
        ret={
            k:v for k,v in sorted(ret.items(),key=lambda item:item[1],reverse=reverse)
        }
        return ret

    @staticmethod
    def get_bounding_box_by_class(bounding_boxes,class_id):
        return [bb for bb in bounding_boxes if bb.get_class_id()==class_id]
    
    @staticmethod
    def get_bounding_box_by_image_name(bounding_boxes,image_name):
        return [bb for bb in bounding_boxes if bb.get_image_name()==image_name]
    
    @staticmethod
    def get_total_images(bounding_boxes):
        return len(list(set([bb.get_image_name() for bb in bounding_boxes])))
    
    @staticmethod
    def get_average_area(bounding_boxes):
        areas=[bb.get_area() for bb in bounding_boxes]
        return sum(areas)/len(areas)