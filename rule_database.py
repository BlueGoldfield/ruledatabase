from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import sys
import sqlite3

conn = sqlite3.connect('rule.db')
c = conn.cursor()

class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.UI()
        self.get_data()
        if self.index < 1:
            self.index = -1

    def UI(self) -> None:
        TitleLabel = QLabel()
        TitleLabel.setText("Booru Artists Database")
        TitleLabel.adjustSize()
        self.TableView = QTableWidget()
        self.TableView.setColumnCount(2)
        self.TableView.setRowCount(0)
        self.TableView.setHorizontalHeaderLabels(['Artist username', 'Booru URL'])
        self.TableView.setShowGrid(True)
        self.TableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.TableView.resizeColumnsToContents()
        ButtonAdd = QPushButton('Add')
        ButtonAdd.clicked.connect(self.add_data)
        ButtonDel = QPushButton('Delete')
        ButtonDel.clicked.connect(self.del_data)
        ButtonEdit = QPushButton('Edit')
        ButtonEdit.clicked.connect(self.edit_data)
         
        grid = QGridLayout()
        grid.addWidget(TitleLabel, 0, 1)
        grid.addWidget(self.TableView, 1, 0, 1, 3)
        grid.addWidget(ButtonAdd, 2, 0)
        grid.addWidget(ButtonDel, 2, 2)
        grid.addWidget(ButtonEdit, 2, 1)
 
        self.setLayout(grid)
        self.setGeometry(300, 300, 200, 200)
        self.setWindowTitle('BooruADB')
        self.show()
        
    def get_data(self) -> None:
        self.TableView.setRowCount(0)
        c.execute("SELECT * FROM artists")
        all = c.fetchall()
        self.index = 0
        self.TableView.setRowCount(len(all))
        for row in all:
            self.TableView.setItem(self.index, 0, QTableWidgetItem(row[1]))
            self.TableView.setItem(self.index, 1, QTableWidgetItem(row[2]))
            self.index += 1

    def add_data(self) -> None:
        new, done = QInputDialog.getText(self, 'New artist', 'Enter new artist\'s url:')
        self.TableView.setRowCount(self.TableView.rowCount()+1)
        self.TableView.setItem(self.index, 0, QTableWidgetItem(new.split("tags=",1)[1]))
        self.TableView.setItem(self.index, 1, QTableWidgetItem(new))
        self.index += 1
        c.execute("INSERT INTO artists VALUES(:id, :name, :link)", {'id': None, 'name': new.split("tags=",1)[1], 'link': new})
        conn.commit()

    def del_data(self) -> None:
        try:
            curr = self.TableView.currentItem()
            c.execute(f"DELETE FROM artists WHERE name='{curr.text()}' OR link='{curr.text()}'")
            conn.commit()
            self.get_data()
        except Exception as e:
            print(e)
    
    def edit_data(self) -> None:
        try:
            curr = self.TableView.currentItem()
            new, done = QInputDialog.getText(self, 'Edit artist', f'Current artist: {curr.text()}\nEnter new artist\'s url:')
            c.execute(f"UPDATE artists SET name = :name, link = :link WHERE name = '{curr.text()}' OR link = '{curr.text()}'", {'name': new.split("tags=",1)[1], 'link': new})
            conn.commit()
            self.get_data()
        except Exception as e:
            print(e)

def main() -> None:
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()