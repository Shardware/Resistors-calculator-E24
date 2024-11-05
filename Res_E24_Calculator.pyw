import sys
from DATA.RES_E24 import init_res_table
import datatable


from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox,QWidget,QTableWidgetItem,QItemDelegate
)

from PyQt5 import QtCore, QtGui

from PyQt5.uic import loadUi
from GUI.RES_E24_ui import Ui_RES_E24_Calculator,Ui_Results

            


class Window(QMainWindow, Ui_RES_E24_Calculator):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

class WindowResults(QMainWindow,Ui_Results):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)    



def compute(Window,res_table):
    if Window.checkAll():


        # creates localcopy to not change original table
        table = res_table.copy()


        # removes useless columns
        if "R2" not in win.formula.text():
            del table[:, "R2"]
        if "R1_a" not in win.formula.text():
            del table[:, "R1_a"]
        if "R1_b" not in win.formula.text():
            del table[:, "R1_b"]



          #######################################
         #### Remove duplicate combinations ####
        #######################################
            
        # creates unique string to identify unique combinations
        col_num=len(table.names)

        # groups by combination to remove duplicates
        if col_num == 2:
            table=table[1,:,datatable.by(datatable.f[0],datatable.f[1])]
        elif col_num == 1:
            table=table[1,:,datatable.by(datatable.f[0])]
            
        elif col_num == 0:
                msgBox = QMessageBox()
                msgBox.setText("Please, use at least one resistor as variable in the Formula.")
                msgBox.exec()
                return False

          ######################################################
         #### Calculates result, deviation, sorts & filter ####
        ######################################################

        # computes results and stores it in a new column
        resultFormula=win.formula.text()
        resultFormula=resultFormula.replace("R","datatable.f.R")

        datatable.Frame.cbind(table,table[:,eval(resultFormula)])
        table.names={"C0": "Results"}

        # computes absolute deviation from target in % and stores it in a new column
        targetFormula="(datatable.f.Results-"+win.target.text()+")/"+win.target.text()+"*100"

        datatable.Frame.cbind(table,table[:,eval(targetFormula)])
        table.names={"C0": "Deviation from target [%]"}

        datatable.Frame.cbind(table,table[:,datatable.ifelse(eval(targetFormula) < 0, eval("-"+targetFormula), eval(targetFormula))])
        table.names={"C0": "Absolute deviation from target [abs(%)]"}


        # sorts by deviation from target
        table=table.sort("Absolute deviation from target [abs(%)]")

        filterFormula="("+win.res_select.currentText()+">="+win.res_min.text()+") & ("+win.res_select.currentText()+"<="+win.res_max.text()+")"
        filterFormula=filterFormula.replace("R","datatable.f.R")

        # applies filter
        if win.res_select.currentIndex()<3:
            table=table[eval(filterFormula),:]

            # if filtering gives no result, message box and abort
            if table.nrows == 0:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Oops...")
                msgBox.setText("No result found in allowed resistance range.")
                msgBox.exec()
                return False


          #####################################################
         #### Create results window & populate the table  ####
        #####################################################


        res = WindowResults()

        col_num=len(table.names)
        row_num=min(table.nrows,100)

        
        res.table.setColumnCount(col_num)
        res.table.setRowCount(row_num)
        res.table.setHorizontalHeaderLabels(table.names)

        # fill the QTableWidget
        for r in range(row_num):        #row
            for c in range(col_num):    #col
                current_cell = QTableWidgetItem(" ")
                if c < (col_num-3) :
                    current_cell.setText("{:10.1f}".format(table[r,c]))
                else :
                    current_cell.setText("{:10.3f}".format(table[r,c]))
                res.table.setItem(r,c,current_cell)
             

        # resisze to content
        res.table.resizeColumnsToContents()

        table_length=0

        for c in range(col_num):
            table_length=table_length+res.table.columnWidth(c)

        heigh=int(800)
        
        res.table.setGeometry(QtCore.QRect(10, 10, table_length+50, heigh-20))

        res.setMinimumSize(table_length+70, heigh)
        res.setMaximumSize(table_length+70, heigh)
        

          #################################################
         #### Open results window and wait for close  ####
        #################################################
        
        res.show()
    
        loop = QtCore.QEventLoop()
        res.destroyed.connect(loop.quit)
        loop.exec() # wait ...

        
        return True
    
    else:
        return False

        
if __name__ == "__main__":


    app = QApplication(sys.argv)
##    with open(".\GUI\Diffnes.qss", "r") as f:
##        _style = f.read()
##        app.setStyleSheet(_style)
  
    win = Window()
    win.show()

    #res = WindowResults()
    #res.show()

    main_table=init_res_table()

    win.short.activated.connect(lambda : compute(win,main_table))
    win.Go.clicked.connect(lambda: compute(win,main_table))



 

    sys.exit(app.exec())




