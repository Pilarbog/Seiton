from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget
# from sqlshot import sqlqueryselecttbl,sqlquerytitlesearch
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QIcon
import qdarkstyle
import os


import sys
from system.localidad.localidad import Localidad
from system.producto.producto import Producto
from system.chofer.chofer import Chofer
from system.vehiculo.vehiculo import Vehiculo
from system.cliente.cliente import Cliente



class Main(QMainWindow):
    def __init__(self, parent=None):

        super(Main, self).__init__(parent)
        loadUi('pantallas.ui', self)
        # defino las variables que voy a utilizar
        self.lastId=0
        self.selectedId=0
        self.filaTabla=0
        self.estado='CONSULTAR'  


        #-------Menu lateral--------
        self.btn_menu = self.findChild(QtWidgets.QToolButton, "btn_menu")
        self.btn_menu.clicked.connect(self.toggle_dock)

        # crear dock
        self.menu_dock = QtWidgets.QDockWidget("Menú", self)
        self.menu_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)

        # cargar el contenido del ui dentro de un widget y setearlo en el dock
        menu_widget = QtWidgets.QWidget()
        uic.loadUi("menu_principal.ui", menu_widget)
        self.menu_dock.setWidget(menu_widget)
        menu_widget.setMinimumWidth(420)
        menu_widget.setMinimumHeight(300)

        self.menu_dock.setMinimumWidth(500)
        self.menu_dock.setMaximumWidth(500)   # opcional, para que no se achique/agrande


        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.menu_dock)
        self.menu_dock.hide()  # empezar oculto

                #--------Estilos y temas ---------
        self.tabWidget.setStyleSheet("""
            QTabWidget::pane {
                background-color: #bdd4ff;
            }

            QTabBar::tab {
                background: #bdd4ff;
                color: black;           /* ← texto visible en fondo claro */
                padding: 6px;
                border: 1px solid #999;
            }

            QTabBar::tab:selected {
                background: #bdd4ff;
                font-weight: bold;
                color: black;           /* ← texto visible */
            }

            /* Solo las páginas internas del tab */
            QTabWidget QWidget {
                background-color: #bdd4ff;
                color: black;           /* ← texto negro interno */
            }
                /* Botones dentro del TabWidget */
            QTabWidget QPushButton {
                background-color: #e6eeff;   /* un tono claro para resaltar */
                color: black;
                border: 1px solid #6783b5;   /* ← vuelve a aparecer el borde */
                border-radius: 4px;
                padding: 4px 8px;
            }

            QTabWidget QPushButton:hover {
                background-color: #d0e0ff;
            }

            QTabWidget QPushButton:pressed {
                background-color: #b7cdfa;
            }

        """)


        #----------------Boton configuracion de estilo
        # Aplicar estilo personalizado al frame de configuración y ocultarlo inicialmente
        if hasattr(self, 'frameConfiguracion') and self.frameConfiguracion is not None:
            # fondo solicitado #636ae8 y texto en blanco para legibilidad
            # Añadimos radio de borde y padding para un look más estético
            self.frameConfiguracion.setStyleSheet(
                "background-color: #636ae8; color: white; border-radius: 10px; padding: 12px;"
            )
            # Guardar geometría original para la animación
            try:
                self._config_orig_geom = self.frameConfiguracion.geometry()
                # posición fuera de la pantalla/izquierda (oculto)
                self._config_hidden_geom = QtCore.QRect(-self._config_orig_geom.width(),
                                                        self._config_orig_geom.y(),
                                                        self._config_orig_geom.width(),
                                                        self._config_orig_geom.height())
                # Empezar oculto y posicionado fuera
                self.frameConfiguracion.setGeometry(self._config_hidden_geom)
                self.frameConfiguracion.hide()
            except Exception:
                # Si algo falla, simplemente ocultamos
                self.frameConfiguracion.hide()

        # Mejora estética de las etiquetas dentro del frame de configuración
        # Ajustamos título y estilos solo si existen los widgets en la UI.
        try:
            # Determinar ancho útil para las etiquetas según la geometría original del frame
            try:
                label_width = self._config_orig_geom.width() - 24
                if label_width < 240:
                    label_width = 240
            except Exception:
                label_width = 260

            if hasattr(self, 'label_51') and self.label_51 is not None:
                # Corregir texto y estilo del título
                try:
                    self.label_51.setText('Configuración')
                except Exception:
                    pass
                f = self.label_51.font()
                f.setPointSize(12)
                f.setBold(True)
                self.label_51.setFont(f)
                self.label_51.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                self.label_51.setStyleSheet('color: white;')
                # Evitar que el texto se corte: permitir wrap y expandir
                try:
                    self.label_51.setWordWrap(True)
                    self.label_51.setMinimumWidth(label_width)
                    self.label_51.setMaximumHeight(60)  # permitir más alto si es necesario para wrap
                    self.label_51.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
                except Exception:
                    pass
                # Aplicar la misma fuente del título a las labels secundarias (sin cambiar posición)
                try:
                    f_title = self.label_51.font()
                    if hasattr(self, 'label_52') and self.label_52 is not None:
                        self.label_52.setFont(f_title)
                    if hasattr(self, 'label_53') and self.label_53 is not None:
                        self.label_53.setFont(f_title)
                except Exception:
                    pass
        except Exception:
            pass

        # Estilizar botones dentro de frameConfiguracion para mejor contraste y legibilidad
        try:
            btn_style = (
                "QPushButton{background-color: white; color: #636ae8; border-radius:8px; padding:6px 10px;}"
                "QPushButton:hover{background-color: #f0f0f5;}"
                "QPushButton:pressed{background-color: #e6e6eb;}"
            )
            if hasattr(self, 'btnModo') and self.btnModo is not None:
                self.btnModo.setStyleSheet(btn_style)
                self.btnModo.setMinimumWidth(90)
            if hasattr(self, 'btnIdioma') and self.btnIdioma is not None:
                self.btnIdioma.setStyleSheet(btn_style)
                self.btnIdioma.setMinimumWidth(90)
            # Si existe el botón que abre el panel de configuración, dejarlo como está
        except Exception:
            pass

        # ---------- Idiomas (español/inglés) ----------
        # Mapa de traducciones (es -> en) para etiquetas y botones.
        # Rextos a utilizar para la traducciom.
        self.translations_map = {
            'Configuración': 'Configuration',
            'Tema': 'Theme',
            'Idioma': 'Language',
            'Agregar': 'Add',
            'Editar': 'Edit',
            'Guardar': 'Save',
            'Buscar': 'Search',
            'Eliminar': 'Delete',
            'Localidad': 'Location',
            'Codigo Postal': 'Postal Code',
            'Código Postal': 'Postal Code',
            'Vehiculo': 'Vehicle',
            'Vehículo': 'Vehicle',
            'Cliente': 'Client',
            'Configuracion': 'Configuration',
            'Chofer': 'Driver',
            'Conductor': 'Driver',
            'Producto': 'Product',
            # plurals / tab names
            'Choferes': 'Drivers',
            'Productos': 'Products',
            'Localidad': 'Location',
            'Localidades': 'Locations',
            'Registro  de Localidades': 'Location registration',
            'Registro Vehiculos': 'Vehicle registration',
            'Vehiculos': 'Vehicles',
            'Clientes': 'Clients',
            # Client form labels
            'Registro clientes': 'Client registration',
            'Nombre/Razón social': 'Name/Company',
            'Cuil/Cuit': 'Tax ID',
            'Dni': 'ID',
            'DNI': 'ID',
            'Dirección': 'Address',
            'Telefono': 'Phone',
            'Ciudad': 'City',
            # Chofer form labels
            'Registro choferes': 'Driver registration',
            'Registro choferes': 'Driver registration',
            'Agregar Chofer': 'Add Driver',
            # Producto form labels
            'Registro Productos': 'Product registration',
            'Lista de productos': 'Product list',
            'Tabla productos': 'Products table',
            'Codigo del producto': 'Product code',
            'Codigo producto': 'Product code',
            # Campos comunes y variantes (Productos / Vehículos / Formularios)
            'Nombre completo': 'Full name',
            'Direccion': 'Address',
            'Fecha de Nacimiento': 'Date of Birth',
            'Fecha de Nacimmiento': 'Date of Birth',
            'Descripcion': 'Description',
            'Descripción': 'Description',
            'Precio': 'Price',
            'Precio Unitario': 'Unit Price',
            'Stock': 'Stock',
            'Cantidad': 'Quantity',
            'Categoria': 'Category',
            'Categoría': 'Category',
            'Codigo': 'Code',
            'Código': 'Code',
            # Vehículo
            'Registro Vehículos': 'Vehicle registration',
            'Marca': 'Brand',
            'Modelo': 'Model',
            'Matricula': 'License plate',
            'Disponibilidad': 'Availability',
            #Pllanillas
            'Agregar Cliente': 'Add Client',
            'Agregar Vehículo': 'Add Vehicle',
            'Agregar Producto': 'Add Product',
            'Agregar Localidad': 'Add Location',
            'Agregar Chofer': 'Add Driver',
            'Agregar a Planilla': 'Add to Form',
            'Continuar': 'Continue',
            'Inspeccionar': 'Inspect',
            'Agregar': 'Add',
            'Registro Planillas': 'Form Registration',
    
        }
        # reverse map (en -> es)
        self.reverse_translations = {v: k for k, v in self.translations_map.items()}

        # Estado de idioma actual (predeterminado español)
        self.current_lang = 'es'

        # Conectar el botón de idioma para alternar idioma si existe
        try:
            if hasattr(self, 'btnIdioma') and self.btnIdioma is not None:
                # Mostrar código de idioma actual
                try:
                    self.btnIdioma.setText('ES')
                except Exception:
                    pass
                self.btnIdioma.clicked.connect(self.toggle_language)
        except Exception:
            pass

        # Conectar el botón de configuración sólo si existe en la UI
        if hasattr(self, 'btnConfiguracion') and self.btnConfiguracion is not None:
            self.btnConfiguracion.clicked.connect(self.toggleConfiguracion)

        # ---------- MODO (toggle) ----------
        # Variable de estado local que indica si la aplicación está en modo oscuro.
        # La inicializamos como True para que la app arranque en modo oscuro.
        self.is_dark = True

        # Rutas a los iconos que usamos (opcional). Usamos os.path.join para construir
        # rutas portables en diferentes sistemas operativos.
        self.icono_sol = os.path.join('imagenes', 'modoclaro.png')  # icono para modo claro
        self.icono_luna = os.path.join('imagenes', 'modooscuro.png')  # icono para modo oscuro

        try:
            # Si el botón existe en la UI, configuramos su icono inicial y lo conectamos
            # a la función que alterna el tema (toggle_theme).
            if hasattr(self, 'btnModo'):
                # Si el archivo del icono de luna existe y estamos en modo oscuro,
                # lo asignamos al botón para que refleje el estado actual.
                if os.path.exists(self.icono_luna) and self.is_dark:
                    self.btnModo.setIcon(QIcon(self.icono_luna))
                # Si el icono del sol existe y estuvieramos en modo claro lo usaríamos.
                elif os.path.exists(self.icono_sol) and not self.is_dark:
                    self.btnModo.setIcon(QIcon(self.icono_sol))

                # Conectamos el evento click del botón `btnModo` al método toggle_theme.
                # Al pulsar el botón se ejecutará toggle_theme y alternará el tema.
                self.btnModo.clicked.connect(self.toggle_theme)
        except Exception:
            # Capturamos excepciones para evitar que la falta de botón o iconos rompa la app.
            pass

        # Aplicar el tema oscuro por defecto al inicio de la aplicación.
        # Usamos QApplication.instance().setStyleSheet(...) para aplicar el stylesheet
        # globalmente a todos los widgets de la aplicación.
        try:
            if qdarkstyle is not None:
                # Si la librería qdarkstyle está instalada, preferimos su stylesheet
                # porque es más completo y consistente.
                QApplication.instance().setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
            else:
                # Si qdarkstyle no está disponible, aplicamos un stylesheet mínimo
                # como fallback (esto colorea background y texto de widgets básicos).
                dark = """
                QWidget{background-color:#2b2b2b;color:#e6e6e6}
                QPushButton{background-color:#3c3f41;color:#e6e6e6}
                """
                QApplication.instance().setStyleSheet(dark)
        except Exception:
            # Ignoramos errores para que la app siga funcionando si algo falla
            # al aplicar estilos (por ejemplo, si QApplication no está inicializada).
            pass
            



        #------------- LOCALIDADES
        Localidad.showLocalidades(self) #primero muestro contenidos en la pantalla
        Localidad.readLocalidades(self,self.lastId)
        # defino botones con su función asociada que son metodos del objeto categoria
        self.btnGuardarLocalidad.clicked.connect(lambda: Localidad.saveLocalidades(self))

        self.btnAgregarLocalidad.clicked.connect(lambda: Localidad.createLocalidades(self))
        self.btnEditarLocalidad.clicked.connect(lambda: Localidad.updateLocalidades(self))
        self.btnEliminarLocalidad.clicked.connect(lambda: Localidad.deleteLocalidades(self))
        self.btnBuscarLocalidad.clicked.connect(lambda: Localidad.searchLocalidades(self))

        self.tablalocalidad.doubleClicked.connect(lambda: Localidad.doubleClicked_tabla(self))    
        self.tablalocalidad.clicked.connect(lambda: Localidad.clicked_tabla(self))

        #------------- PRODUCTOS
        Producto.showProductos(self) #primero muestro contenidos en la pantalla
        Producto.readProductos(self,self.lastId)
        # defino botones con su función asociada que son metodos del objeto categoria
        self.btnGuardarProducto.clicked.connect(lambda: Producto.saveProductos(self))

        self.btnAgregarProducto.clicked.connect(lambda: Producto.createProductos(self))
        self.btnEditarProducto.clicked.connect(lambda: Producto.updateProductos(self))
        self.btnEliminarLocalidad.clicked.connect(lambda: Localidad.deleteLocalidades(self))
        self.btnBuscarProducto.clicked.connect(lambda: Producto.searchProductos(self))

        self.tablaproductos.doubleClicked.connect(lambda: Producto.doubleClicked_tabla(self))    
        self.tablaproductos.clicked.connect(lambda: Producto.clicked_tabla(self))

        #------------- CHOFERES
        Chofer.showChoferes(self) #primero muestro contenidos en la pantalla  
        Chofer.readChoferes(self,self.lastId)
        # defino botones con su función asociada que son metodos del objeto categoria
        self.btnGuardarChofer.clicked.connect(lambda: Chofer.saveChoferes(self))

        self.btnAgregarChofer.clicked.connect(lambda: Chofer.createChoferes(self))
        self.btnEditarChofer.clicked.connect(lambda: Chofer.updateChoferes(self))
        self.btnEliminarChofer.clicked.connect(lambda: Chofer.deleteChoferes(self))
        self.btnBuscarChofer.clicked.connect(lambda: Chofer.searchChoferes(self))
        self.tablachoferes.doubleClicked.connect(lambda: Chofer.doubleClicked_tabla(self))    
        self.tablachoferes.clicked.connect(lambda: Chofer.clicked_tabla(self))

        #------------- VEHICULOS
        self.vehiculo = Vehiculo()
        self.vehiculo.showVehiculos(self)
        self.btn_guardar_vehiculo.clicked.connect(lambda: self.vehiculo.saveVehiculos(self))
        self.btn_agregar_vehiculo.clicked.connect(lambda: self.vehiculo.createVehiculos(self))
        self.btn_editar_vehiculo.clicked.connect(lambda: self.vehiculo.updateVehiculos(self))
        self.btn_eliminar_vehiculo.clicked.connect(lambda: self.vehiculo.deleteVehiculos(self))
        self.btn_buscar_vehiculo.clicked.connect(lambda: self.vehiculo.searchVehiculos(self))
        self.tablavehiculo.doubleClicked.connect(lambda: self.vehiculo.doubleClicked_tabla(self))
        self.tablavehiculo.clicked.connect(lambda: self.vehiculo.clicked_tabla(self))
        # El lineEdit_buscar_2 se usa para escribir el texto a filtrar en la búsqueda de vehículos.

        #------------- CLIENTES
        self.cliente = Cliente()
        self.cliente.showClientes(self)
        self.btn_guardar_cliente.clicked.connect(lambda: self.cliente.saveClientes(self))
        self.btn_agregar_cliente.clicked.connect(lambda: self.cliente.createClientes(self))
        if hasattr(self, 'btn_agregar_cliente_3'):
            self.btn_agregar_cliente_3.clicked.connect(lambda: self.cliente.createClientes(self))
        self.btn_editar_cliente.clicked.connect(lambda: self.cliente.updateClientes(self))
        self.btn_eliminar_cliente.clicked.connect(lambda: self.cliente.deleteClientes(self))
        self.btn_buscar_cliente.clicked.connect(lambda: self.cliente.searchClientes(self))
        self.tabla_cliente.doubleClicked.connect(lambda: self.cliente.doubleClicked_tabla(self) if hasattr(self.cliente, 'doubleClicked_tabla') else None)
        self.tabla_cliente.clicked.connect(lambda: self.cliente.clicked_tabla(self) if hasattr(self.cliente, 'clicked_tabla') else None)
        # El lineEdit_buscar_cliente se usa para escribir el texto a filtrar en la búsqueda de clientes.
 
    def toggle_theme(self):
        """Alterna entre tema oscuro y claro para toda la aplicación.

        Comentarios línea por línea:
        - if self.is_dark: comprobamos el estado actual.
        - QApplication.instance().setStyleSheet(""): limpiar stylesheet vuelve al tema nativo/claro.
        - self.btnModo.setIcon(...): cambiar icono visual del botón (opcional).
        - self.is_dark = False: actualizar la variable de estado local.
        - else: aplicamos el stylesheet oscuro (qdarkstyle si existe, si no fallback).
        - finalmente se actualiza self.is_dark a True.
        """
        try:
            if self.is_dark:
                # Estábamos en oscuro -> cambiar a claro.
                # Limpiar el stylesheet global devuelve el tema por defecto del sistema.
                QApplication.instance().setStyleSheet("")

                # Si el icono del sol existe, lo ponemos para indicar que ahora está en claro.
                try:
                    if os.path.exists(self.icono_sol):
                        self.btnModo.setIcon(QIcon(self.icono_sol))
                except Exception:
                    # No crítico: si cambiar el icono falla, no interrumpimos.
                    pass

                # Marcamos que ahora no estamos en modo oscuro.
                self.is_dark = False
            else:
                # Estábamos en claro -> cambiar a oscuro.
                # Preferimos qdarkstyle cuando está instalado (mejor apariencia).
                if qdarkstyle is not None:
                    QApplication.instance().setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
                else:
                    # Fallback: stylesheet mínimo para modo oscuro.
                    dark = """
                    QWidget{background-color:#2b2b2b;color:#e6e6e6}
                    QPushButton{background-color:#3c3f41;color:#e6e6e6}
                    """
                    QApplication.instance().setStyleSheet(dark)

                # Intentamos cambiar el icono a la luna (no es crítico si falla).
                try:
                    if os.path.exists(self.icono_luna):
                        self.btnModo.setIcon(QIcon(self.icono_luna))
                except Exception:
                    pass

                # Marcamos que ahora estamos en modo oscuro.
                self.is_dark = True
        except Exception:
            # Capturamos cualquier excepción inesperada para no romper la app.
            pass
    def toggle_dock(self):
        visible = self.menu_dock.isVisible()
        self.menu_dock.setVisible(not visible)

    def toggle_language(self):
        """Alterna entre español e inglés para las etiquetas y botones.

        Sólo se traducen textos que estén explícitamente definidos en
        `self.translations_map` (clave en español -> valor en inglés).
        """
        try:
            if self.current_lang == 'es':
                self.current_lang = 'en'
                self.apply_language('en')
                # marcar botón con el código opuesto
                try:
                    if hasattr(self, 'btnIdioma') and self.btnIdioma is not None:
                        self.btnIdioma.setText('EN')
                except Exception:
                    pass
            else:
                self.current_lang = 'es'
                self.apply_language('es')
                try:
                    if hasattr(self, 'btnIdioma') and self.btnIdioma is not None:
                        self.btnIdioma.setText('ES')
                except Exception:
                    pass
        except Exception:
            pass

    def apply_language(self, lang):
        """Aplica el idioma `lang` ('es' o 'en') a QLabel y QPushButton.

        Sólo se traducen textos exactamente iguales a las claves del mapa.
        """
        if lang not in ('es', 'en'):
            return

        try:
            # Traducir QLabels
            for lbl in self.findChildren(QtWidgets.QLabel):
                try:
                    t = lbl.text().strip()
                    if not t:
                        continue
                    if lang == 'en' and t in self.translations_map:
                        lbl.setText(self.translations_map[t])
                    elif lang == 'es' and t in self.reverse_translations:
                        lbl.setText(self.reverse_translations[t])
                except Exception:
                    pass

            # Traducir títulos de QGroupBox si los hubiera
            for g in self.findChildren(QtWidgets.QGroupBox):
                try:
                    t = g.title().strip()
                    if not t:
                        continue
                    if lang == 'en' and t in self.translations_map:
                        g.setTitle(self.translations_map[t])
                    elif lang == 'es' and t in self.reverse_translations:
                        g.setTitle(self.reverse_translations[t])
                except Exception:
                    pass

            # Traducir textos de pestañas en QTabWidget
            for tw in self.findChildren(QtWidgets.QTabWidget):
                try:
                    for i in range(tw.count()):
                        t = tw.tabText(i).strip()
                        if not t:
                            continue
                        if lang == 'en' and t in self.translations_map:
                            tw.setTabText(i, self.translations_map[t])
                        elif lang == 'es' and t in self.reverse_translations:
                            tw.setTabText(i, self.reverse_translations[t])
                except Exception:
                    pass

            # Traducir QPushButtons
            for btn in self.findChildren(QtWidgets.QPushButton):
                try:
                    t = btn.text().strip()
                    if not t:
                        continue
                    if lang == 'en' and t in self.translations_map:
                        btn.setText(self.translations_map[t])
                    elif lang == 'es' and t in self.reverse_translations:
                        btn.setText(self.reverse_translations[t])
                except Exception:
                    pass

            # Traducir QCheckBox (por ejemplo: Disponibilidad)
            for cb in self.findChildren(QtWidgets.QCheckBox):
                try:
                    t = cb.text().strip()
                    if not t:
                        continue
                    if lang == 'en' and t in self.translations_map:
                        cb.setText(self.translations_map[t])
                    elif lang == 'es' and t in self.reverse_translations:
                        cb.setText(self.reverse_translations[t])
                except Exception:
                    pass
        except Exception:
            pass

    def toggleConfiguracion(self):
        # Animación de deslizado para `frameConfiguracion` (entrada/salida horizontal)
        if not hasattr(self, 'frameConfiguracion') or self.frameConfiguracion is None:
            return

        # Asegurarse de tener geometrías calculadas
        try:
            orig = self._config_orig_geom
            hidden = self._config_hidden_geom
        except Exception:
            orig = self.frameConfiguracion.geometry()
            hidden = QtCore.QRect(-orig.width(), orig.y(), orig.width(), orig.height())

        visible = self.frameConfiguracion.isVisible()

        # Preparar la animación sobre la propiedad 'geometry'
        anim = QtCore.QPropertyAnimation(self.frameConfiguracion, b"geometry")
        anim.setDuration(250)
        anim.setEasingCurve(QtCore.QEasingCurve.InOutQuad)

        if not visible:
            # Mostrar: colocar inicialmente en hidden, luego animar hacia orig
            self.frameConfiguracion.setGeometry(hidden)
            self.frameConfiguracion.show()
            anim.setStartValue(hidden)
            anim.setEndValue(orig)
            self._config_anim = anim
            self._config_anim.start()
        else:
            # Ocultar: animar hacia hidden y ocultar al terminar
            anim.setStartValue(self.frameConfiguracion.geometry())
            anim.setEndValue(hidden)

            def on_finished():
                try:
                    self.frameConfiguracion.hide()
                except Exception:
                    pass

            anim.finished.connect(on_finished)
            self._config_anim = anim
            self._config_anim.start()
# ------ main -------------
if __name__ == "__main__":
    mi_aplicacion = QApplication(sys.argv)
    mi_app = Main()
    mi_app.show()


    sys.exit(mi_aplicacion.exec_())

