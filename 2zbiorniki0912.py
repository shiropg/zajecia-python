import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPainterPath

class Zbiornik(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize (300, 400)
        
        self.top_trapez_h = 60
        self.rect_h = 200
        self.bot_trapez_h = 60
        
        self.width_top = 200
        self.width_mid = 140
        self.width_bot = 40
        self.total_tank_height = self.top_trapez_h + self.rect_h + self.bot_trapez_h
        
        self._poziom = 0.5
        
        self.draw_x = 50
        self.draw_y = 50
        
    def setPoziom(self, poziom):
        self._poziom = max(0.0, min(1.0, poziom))
        self.update()
        
    def setPolozenie(self, x, y):
        self.draw_x = x
        self.draw_y = y
        self.update()
        
    def getPoziom(self):
        return self._poziom
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint (QPainter.Antialiasing)
        
        cx = self.draw_x + (self.width_top/2) 
        start_y = self.draw_y
        
        path = QPainterPath()
        
        p1_tl = QPointF(cx - self.width_top/2, start_y)
        p1_tr = QPointF(cx + self.width_top/2, start_y)
        p2_ml = QPointF(cx - self.width_mid/2, start_y + self.top_trapez_h)
        p2_mr = QPointF(cx + self.width_mid/2, start_y + self.top_trapez_h)
        p3_bl = QPointF(cx - self.width_mid/2, start_y + self.top_trapez_h + self.rect_h)
        p3_br = QPointF(cx + self.width_mid/2, start_y + self.top_trapez_h + self.rect_h)
        p4_bl = QPointF(cx - self.width_bot/2, start_y + self.total_tank_height)
        p4_br = QPointF(cx + self.width_bot/2, start_y + self.total_tank_height)
        
        path.moveTo(p1_tl)
        path.lineTo(p1_tr); path.lineTo(p2_mr); path.lineTo(p3_br)
        path.lineTo(p4_br); path.lineTo(p4_bl); path.lineTo(p3_bl)
        path.lineTo(p2_ml); path.lineTo(p1_tl)
        path.closeSubpath()
        
        painter.save()
        painter.setClipPath(path)
        
        liquid_height_px = self.total_tank_height * self._poziom
        
        rect_liquid = QRectF(
            cx - self.width_top/2,
            start_y + self.total_tank_height - liquid_height_px,
            self.width_top,
            liquid_height_px
        )
        
        painter.fillRect(rect_liquid, QColor(0, 120, 255, 180))
        painter.restore()
        
        pen = QPen(Qt.gray, 4)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)
        
        
        
        
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Laboratorium: Dwa zbiorniki PyQt")
        self.resize(650, 650)
        
        layout0 = QHBoxLayout()
        self.setLayout(layout0)
        

        layout1 = QVBoxLayout()
        
        self.zbiornik1 = Zbiornik()
        self.zbiornik1.setStyleSheet("background-color: #222:")
        self.zbiornik1.setPolozenie(50,50)
        layout1.addWidget(self.zbiornik1)
        
        self.slider1 = QSlider(Qt.Horizontal)
        self.slider1.setRange(0, 100)
        self.slider1.valueChanged.connect(self.zmien_poziom1)
        
        self.label1 = QLabel("Poziom: 20%")
        self.label1.setAlignment(Qt.AlignCenter)
        
        self.slider1.setValue(20)
        
        layout1.addWidget(self.slider1)
        layout1.addWidget(self.label1)
        layout0.addLayout(layout1)
        

        layout2 = QVBoxLayout()
        
        self.zbiornik2 = Zbiornik()
        self.zbiornik2.setStyleSheet("background-color: #222:")
        self.zbiornik2.setPolozenie(50,50)
        layout2.addWidget(self.zbiornik2)
        
        self.slider2 = QSlider(Qt.Horizontal)
        self.slider2.setRange(0, 100)
        self.slider2.valueChanged.connect(self.zmien_poziom2)

        self.label2 = QLabel("Poziom: 80%")
        self.label2.setAlignment(Qt.AlignCenter)

        self.slider2.setValue(80)
        
        layout2.addWidget(self.slider2)
        layout2.addWidget(self.label2)
        layout0.addLayout(layout2)
        
    def zmien_poziom1(self, value):
        poziom_float = value/100.0
        self.zbiornik1.setPoziom(poziom_float)
        self.label1.setText(f"Poziom: {value}%")
        
    def zmien_poziom2(self, value):
        poziom_float = value/100.0
        self.zbiornik2.setPoziom(poziom_float)
        self.label2.setText(f"Poziom: {value}%")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
        
        
        
 