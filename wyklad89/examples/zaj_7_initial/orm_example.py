from orm import *

from sqlalchemy.orm import relationship

class TabA(Base): 
    
    __tablename__ = "TAB_A"
    
    id = Column(Integer(), primary_key = True)
    foo = Column(String())
    
class TabB(Base): 
    
    __tablename__ = "TAB_B"
    
    id = Column(Integer(), primary_key = True)
    bar = Column(String())    
    a = Column(Integer(), ForeignKey("TAB_A.id"))
    a_inst = relationship("TabA", backref ="b_inst")