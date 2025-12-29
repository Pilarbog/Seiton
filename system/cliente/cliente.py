
import sqlite3
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox
from tools.DBCrud import CRUD
from PyQt5.QtCore import QDate

class Cliente():
    """Clase específica de Clientes"""

    def cargarLocalidades(self, main_window):
        try:
            conexion_BD = sqlite3.connect("pedidos.sqlite3")
            cursor = conexion_BD.cursor()
            cursor.execute("SELECT nombreloc FROM localidad ORDER BY nombreloc ASC;")
            localidades = cursor.fetchall()
            main_window.comboBox_ciudad_cliente.clear()
            for loc in localidades:
                main_window.comboBox_ciudad_cliente.addItem(loc[0])
            conexion_BD.close()
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al cargar localidades: {e}")
    def __init__(self):
        pass

    def showClientes(self, main_window):
        try:
            main_window.tabla_cliente.setColumnCount(7)
            main_window.tabla_cliente.setHorizontalHeaderLabels(["ID", "Nombre", "CUIT", "DNI", "Tel", "Dirección", "Ciudad"])
            miCrud = CRUD()
            consulta = """
                SELECT c.id_cliente, c.nombre, c.cuit, c.dni, c.tel, c.direccion, l.nombreloc
                FROM cliente c
                LEFT JOIN localidad l ON c.id_loc = l.Id_localidad;
            """
            clientes = miCrud.Read(consulta)
            main_window.tabla_cliente.setRowCount(0)
            for index, cliente1 in enumerate(clientes):
                main_window.tabla_cliente.insertRow(index)
                main_window.tabla_cliente.setItem(index, 0, QTableWidgetItem(str(cliente1[0]))) # id
                main_window.tabla_cliente.setItem(index, 1, QTableWidgetItem(str(cliente1[1]))) # nombre
                main_window.tabla_cliente.setItem(index, 2, QTableWidgetItem(str(cliente1[2]))) # cuit
                main_window.tabla_cliente.setItem(index, 3, QTableWidgetItem(str(cliente1[3]))) # direccion
                main_window.tabla_cliente.setItem(index, 4, QTableWidgetItem(str(cliente1[4]))) # tel
                main_window.tabla_cliente.setItem(index, 5, QTableWidgetItem(str(cliente1[5]))) # dni
                main_window.tabla_cliente.setItem(index, 6, QTableWidgetItem(str(cliente1[6]) if cliente1[6] else "")) # ciudad
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al mostrar clientes: {e}")

    def searchClientes(self, main_window):
        try:
            main_window.tabla_cliente.setColumnCount(6)
            main_window.tabla_cliente.setHorizontalHeaderLabels(["ID", "Nombre", "CUIT", "DNI","Direccion", "Ciudad", "Teléfono"])
            conexion_BD = sqlite3.connect("pedidos.sqlite3")
            cursor = conexion_BD.cursor()
            buscar = main_window.lineEdit_buscar_cliente.text()
            cursor.execute("SELECT * FROM cliente WHERE nombre LIKE ?", ('%' + buscar + '%',))
            clientes = cursor.fetchall()
            main_window.tabla_cliente.setRowCount(0)
            for cliente1 in clientes:
                row_position = main_window.tabla_cliente.rowCount()
                main_window.tabla_cliente.insertRow(row_position)
                main_window.tabla_cliente.setItem(row_position, 0, QTableWidgetItem(str(cliente1[0])))
                main_window.tabla_cliente.setItem(row_position, 1, QTableWidgetItem(cliente1[1]))
                main_window.tabla_cliente.setItem(row_position, 2, QTableWidgetItem(cliente1[2]))
                main_window.tabla_cliente.setItem(row_position, 3, QTableWidgetItem(cliente1[3]))
                main_window.tabla_cliente.setItem(row_position, 4, QTableWidgetItem(cliente1[4]))
                main_window.tabla_cliente.setItem(row_position, 5, QTableWidgetItem(cliente1[5]))
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al buscar clientes: {e}")

    def createClientes(self, main_window):
        try:
            self.cargarLocalidades(main_window)
            main_window.estado = 'AGREGAR'
            main_window.lineEdit_nombre_cliente.clear()
            main_window.lineEdit_nombre_cliente.setEnabled(True)
            main_window.lineEdit_nombre_cliente.setFocus()
            main_window.lineEdit_cuit_cliente.clear()
            main_window.lineEdit_cuit_cliente.setEnabled(True)
            main_window.lineEdit_dni_cliente.clear()
            main_window.lineEdit_dni_cliente.setEnabled(True)
            main_window.comboBox_ciudad_cliente.setCurrentIndex(-1)
            main_window.comboBox_ciudad_cliente.setEnabled(True)
            main_window.lineEdit_telefono_cliente.clear()
            main_window.lineEdit_telefono_cliente.setEnabled(True)
            main_window.lineEdit_direccion_cliente.clear()
            main_window.lineEdit_direccion_cliente.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al preparar alta de cliente: {e}")

    def saveClientes(self, main_window):
        try:
            nombre = main_window.lineEdit_nombre_cliente.text().upper()
            cuit = main_window.lineEdit_cuit_cliente.text().upper()
            dni = main_window.lineEdit_dni_cliente.text().upper()
            tel = main_window.lineEdit_telefono_cliente.text().upper()
            direccion = main_window.lineEdit_direccion_cliente.text().upper()
            ciudad_nombre = main_window.comboBox_ciudad_cliente.currentText()
            # Obtener el id de la ciudad desde la tabla localidad
            conexion_BD = sqlite3.connect("pedidos.sqlite3")
            cursor = conexion_BD.cursor()
            cursor.execute("SELECT Id_localidad FROM localidad WHERE nombreloc = ?", (ciudad_nombre,))
            resultado = cursor.fetchone()
            id_ciudad = resultado[0] if resultado else None
            cursor.close()
            conexion_BD.close()
            miCrud = CRUD()
            if main_window.estado == 'AGREGAR':
                misDatos = (nombre, cuit, direccion, tel, dni, id_ciudad)
                miConsulta = "INSERT INTO cliente (nombre, cuit, direccion, tel, dni, id_loc) VALUES (?,?,?,?,?,?);"
                miCrud.Create(miConsulta, misDatos)
            elif main_window.estado == 'EDITAR':
                misDatos = (nombre, cuit, direccion, tel, dni, id_ciudad, main_window.selectedId)
                miConsulta = "UPDATE cliente SET nombre = ?, cuit = ?, direccion = ?, tel = ?, dni = ?, id_loc = ? WHERE id_cliente = ?;"
                miCrud.Update(miConsulta, (misDatos,))
            elif main_window.estado == 'ELIMINAR':
                miConsulta = f"DELETE from cliente where id={main_window.selectedId};"
                miCrud.Delete(miConsulta)
            self.readClientes(main_window, 0)
            main_window.lineEdit_nombre_cliente.clear()
            main_window.lineEdit_cuit_cliente.clear()
            main_window.lineEdit_dni_cliente.clear()
            main_window.comboBox_ciudad_cliente.setCurrentIndex(-1)
            main_window.lineEdit_telefono_cliente.clear()
            main_window.lineEdit_direccion_cliente.clear()
            main_window.estado = 'CONSULTAR'
            self.showClientes(main_window)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al guardar cliente: {e}")

    def updateClientes(self, main_window):
        self.cargarLocalidades(main_window)
        try:
            fila = main_window.tabla_cliente.currentRow()
            if fila < 0:
                QMessageBox.warning(None, "Advertencia", "Seleccione un cliente para editar.")
                return
            main_window.estado = 'EDITAR'
            main_window.selectedId = main_window.tabla_cliente.item(fila, 0).text()
            main_window.lineEdit_nombre_cliente.setText(main_window.tabla_cliente.item(fila, 1).text())
            main_window.lineEdit_cuit_cliente.setText(main_window.tabla_cliente.item(fila, 2).text())
            main_window.lineEdit_direccion_cliente.setText(main_window.tabla_cliente.item(fila, 3).text())
            main_window.lineEdit_telefono_cliente.setText(main_window.tabla_cliente.item(fila, 4).text())
            main_window.lineEdit_dni_cliente.setText(main_window.tabla_cliente.item(fila, 5).text())
            main_window.comboBox_ciudad_cliente.setCurrentText(main_window.tabla_cliente.item(fila, 6).text())
            main_window.lineEdit_nombre_cliente.setEnabled(True)
            main_window.lineEdit_nombre_cliente.setFocus()
            main_window.lineEdit_cuit_cliente.setEnabled(True)
            main_window.lineEdit_dni_cliente.setEnabled(True)
            main_window.comboBox_ciudad_cliente.setEnabled(True)
            main_window.lineEdit_telefono_cliente.setEnabled(True)
            main_window.lineEdit_direccion_cliente.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al preparar edición de cliente: {e}")

    def deleteClientes(self, main_window):
        try:
            main_window.estado = 'ELIMINAR'
            fila = main_window.tabla_cliente.currentRow()
            if fila < 0:
                QMessageBox.warning(None, "Advertencia", "Seleccione un cliente para eliminar.")
                return
            conn = sqlite3.connect('pedidos.sqlite3')
            cursor = conn.cursor()
            main_window.selectedId = main_window.tabla_cliente.item(fila, 0).text()
            cursor.execute('DELETE FROM cliente WHERE id_cliente = ?', (main_window.selectedId,))
            conn.commit()
            conn.close()
            self.readClientes(main_window, 0)
            self.showClientes(main_window)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al eliminar cliente: {e}")

    def readClientes(self, main_window, Id_Cliente):
        miCrud = CRUD()
        if Id_Cliente > 0:
            miConsulta = "SELECT * FROM cliente WHERE id = " + str(Id_Cliente) + ";"
            index = main_window.tabla_cliente.rowCount()
        else:
            for indice, ancho in enumerate((10, 200, 100, 100, 100, 100), start=0):
                main_window.tabla_cliente.setColumnWidth(indice, ancho)
            miConsulta = "SELECT * FROM cliente;"
            index = 0
        clientes = miCrud.Read(miConsulta)
        return clientes