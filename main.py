# This Python file uses the following encoding: utf-8
import sys
import os
import pandas as pd
import numpy as np
from pyexcelerate import Workbook
import datetime

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject, Slot, Signal, QUrl, QThread, QTimer

file_path = None
class MainWindow(QObject):
    progress_changed = Signal(float, name="progressChanged")
    error_msg = Signal(str, name="errorMsg")

    def __init__(self):
        QObject.__init__(self)
        self.worker = Worker()
        self.worker.progress_changed.connect(self.progress_changed)
        self.worker.error_msg.connect(self.error_msg)
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()

    # Signal name file
    nameFile = Signal(str)

    @Slot()
    def start_worker(self):
        print("Ejecutar!!")
        print(file_path)
        QTimer.singleShot(0, self.worker.run)
        print("Ejecuto?")

    # Open file
    @Slot(str)
    def openFile(self, filePath):
        global file_path
        self.file = file_path = str(QUrl(filePath).toLocalFile())
        name = self.file.split("/")[-1]
        print(name)
        self.nameFile.emit(name)


class Worker(QObject):
    progress_changed = Signal(float)
    error_msg = Signal(str)

    @Slot()
    def run(self):
        """Metodo conectado con la clase principal que esta conectada a la UI, que empieza a correr una vez se da click al boton ejecutar mandando el archivo con ruta completa
        """
        self.progress = 0
        self.update_progress(4)
        self.validateFiles()
        self.update_progress(10)
        self.executeProgram(file_path)

    def update_progress(self, value):
        """Metodo que actualiza la barra de progreso

        Args:
            value ([int]): Valor a aumentar la barra de progreso
        """
        self.progress = value
        print(f"Progreso dentro del metodo de actualizar es de: {self.progress}")
        self.progress_changed.emit(self.progress)

    @Slot(str)
    def validateFiles(self):
        """Funcion que nos manda la señal a la clase conectada con la UI
        """
        self.msg = ""
        self.msg = validationOfFiles()
        if self.msg:
            self.error_msg.emit(str(self.msg))

    def executeProgram(self, filePath):
        csv_path = os.getcwd() + "\csv_data\TC"
        query_path = os.getcwd() + "\csv_data\Query"
        #nombre_ad = input("Digite el nombre del archivo a buscar (adquirencia): ")
        available_files_csv = os.listdir(csv_path)
        available_files_q = os.listdir(query_path)
        meses = {
            1:'ENE',
            2:'FEB',
            3:'MAR',
            4:'ABR',
            5:'MAY',
            6:'JUN',
            7:'JUL',
            8:'AGO',
            9:'SEP',
            10:'OCT',
            11:'NOV',
            12:'DIC'
        }
        self.update_progress(12)
        #* lectura del reporte a extraerle los datos de PayU
        ad_file = pd.ExcelFile(filePath)
        ad_months = []
        for i in range(len(ad_file.sheet_names)):
            ad_months.append(ad_file.parse(sheet_name=ad_file.sheet_names[i], usecols=[4,6,10,16,17,18,19,20,22]))
            ad_months[i].dropna(axis=0, inplace=True)
        self.update_progress(15)
        ad = pd.concat([ad_months[i] for i in range(len(ad_months))], axis=0)
        data_to_read = (ad["F VALE"].dt.month.astype(str) + '_' + ad["F VALE"].dt.year.astype(str)).drop_duplicates().to_list()
        data_to_read_csv = []
        data_to_read_q = []
        for i in range(len(data_to_read)):
            data_to_read_csv.append('TC ' + meses.get(int(data_to_read[i].split("_")[0])) + '_' + data_to_read[i].split("_")[1] + '.csv')
            data_to_read_q.append('QWERYS ' + meses.get(int(data_to_read[i].split("_")[0])) + '_' + data_to_read[i].split("_")[1] + '.xlsx')
        data_to_read_final_csv = []
        for i in data_to_read_csv:
            if i not in available_files_csv:
                self.msg = self.msg + f"\nNo se encontró el archivo {i} para poder hacer la consulta completa"
                print(f"No se encuentra el archivo {i} para poder hacer la consulta completa")
            else:
                data_to_read_final_csv.append(i)
        data_to_read_final_q = []
        for i in data_to_read_q:
            if i not in available_files_q:
                self.msg = self.msg + f"\nNo se encontró el archivo {i} para poder hacer la consulta completa"
                print(f"No se encuentra el archivo {i} para poder hacer la consulta completa")
            else:
                data_to_read_final_q.append(i)
        ad = 0
        self.error_msg.emit(str(self.msg))
        self.update_progress(17)
        #* Lectura de los archivos de PayU y creacion de llaves para la busqueda de cuenta
        cols = [2,3,4,7,8,11,15,16,21,32,48,60]
        datac = [pd.read_csv(csv_path+'\\'+i, sep=";", usecols=cols, low_memory=False) for i in data_to_read_final_csv]
        self.update_progress(19)
        datac = pd.concat([i for i in datac], axis=0)
        datac.reset_index(drop=True, inplace=True)
        self.update_progress(22)
        datac["Creation date"] = pd.to_datetime(datac["Creation date"], format="%Y-%m-%d %H:%M:%S.%f")
        datac['Authorization code'] = datac['Authorization code'].fillna("NA")
        datac['Authorization code'] = datac['Authorization code'].astype('string')
        datac["Processing value"] = datac["Processing value"].fillna(0)
        datac['Processing value'] = datac['Processing value'].astype('int64')
        datac['Extra1'] = datac['Extra1'].astype(str)
        self.update_progress(24)
        datac["Llave_data"] = datac["Creation date"].dt.year.astype(str) + datac["Creation date"].dt.month.astype(str) + datac["Authorization code"].astype(str) + datac["Processing value"].astype(str)
        datac["Llave_data"] = datac["Llave_data"].astype('string')
        datac["Llave_data2"] = datac["Creation date"].dt.year.astype(str) + datac["Creation date"].dt.month.astype(str) + datac["Authorization code"].str[1:].astype(str) + datac["Processing value"].astype(str)
        datac["Llave_data2"] = datac["Llave_data2"].astype('string')
        datac["Llave_data3"] = datac["Creation date"].dt.year.astype(str) + datac["Creation date"].dt.month.astype(str) + datac["Authorization code"].str[2:].astype(str) + datac["Processing value"].astype(str)
        datac["Llave_data3"] = datac["Llave_data3"].astype('string')
        self.update_progress(25)
        #* Lectura de los querys + creacion llaves para busqueda
        dataq = [pd.read_excel(query_path+'\\'+i) for i in data_to_read_final_q]
        self.update_progress(28)
        dataq = pd.concat([i for i in dataq], axis=0)
        dataq.reset_index(drop=True, inplace=True)
        dataq["Llave"] = dataq["FECHA_PAGO"].dt.year.astype(str) + dataq["FECHA_PAGO"].dt.month.astype(str) + dataq["FECHA_PAGO"].dt.day.astype(str) + dataq["CUENTA"].astype(str)
        dataq["Llave"] = dataq["Llave"].astype("string")
        self.update_progress(30)
        def cruce(llave_ad, llave_data, i):
            """Equivalente a un buscarv para las 3 busquedas de cuenta, estado y franquicia de VACIOS

            Args:
                llave_ad ([string]): [llave de adquirencias]
                llave_data ([string]): [llave de los informes de payu]
            """
            ad_months[i].loc[ad_months[i]["Cuenta"].isnull(), 'Cuenta'] = ad_months[i][llave_ad].map(datac.drop_duplicates(llave_data).set_index(llave_data)["Extra1"])
            ad_months[i].loc[ad_months[i]["Estado"].isnull(), 'Estado'] = ad_months[i][llave_ad].map(datac.drop_duplicates(llave_data).set_index(llave_data)["Status"])
            ad_months[i].loc[ad_months[i]["Franquicia"].isnull(), 'Franquicia'] = ad_months[i][llave_ad].map(datac.drop_duplicates(llave_data).set_index(llave_data)["Franchise"])

        wb = Workbook()
        cont = 35
        self.update_progress(cont)
        for i in range(len(ad_months)):
            #* Creacion de index
            ad_months[i].insert(0, "#", ad_months[i].index)
            #* Creacion de llaves para la busqueda
            ad_months[i]["Redondear"] = ad_months[i]["Redondear"].astype("int")
            ad_months[i]["VLR ABONO"] = ad_months[i]["VLR ABONO"].astype("int")
            try:
                ad_months[i]["AUTORIZACION"] = ad_months[i]["AUTORIZACION"].astype("int64")
            except:
                pass
            ad_months[i]["Llave_ad"] = ad_months[i]["F VALE"].dt.year.astype(str) + ad_months[i]["F VALE"].dt.month.astype(str) + ad_months[i]["AUTORIZACION"].astype(str) + ad_months[i]["Redondear"].astype(str)
            ad_months[i]["Llave_ad"] = ad_months[i][["Llave_ad"]].astype('string')
            ad_months[i]["Llave_ad2"] = ad_months[i]["F VALE"].dt.year.astype(str) + ad_months[i]["F VALE"].dt.month.astype(str) + ad_months[i]["AUTORIZACION"].astype(str) + ad_months[i]["VLR ABONO"].astype(str)
            ad_months[i]["Llave_ad2"] = ad_months[i][["Llave_ad2"]].astype('string')
            cont += ((50/len(ad_months))/5)
            self.update_progress(cont)
            #* CRUCE DE DATOS
            ad_months[i]["Cuenta"] = ad_months[i]["Llave_ad"].map(datac.drop_duplicates("Llave_data").set_index("Llave_data")["Extra1"])
            ad_months[i]["Estado"] = ad_months[i]["Llave_ad"].map(datac.drop_duplicates("Llave_data").set_index("Llave_data")["Status"])
            ad_months[i]["Franquicia"] = ad_months[i]["Llave_ad"].map(datac.drop_duplicates("Llave_data").set_index("Llave_data")["Franchise"])
            cont += ((50/len(ad_months))/5)
            self.update_progress(cont)
            cruce("Llave_ad","Llave_data2", i)
            cruce("Llave_ad","Llave_data3", i)
            #* 2 cruce por tema de busqueda con vlr abono
            cruce("Llave_ad2","Llave_data", i)
            cruce("Llave_ad2","Llave_data2", i)
            cruce("Llave_ad2","Llave_data3", i)
            cont += ((50/len(ad_months))/5)
            self.update_progress(cont)
            #* Cambio de tipo de tados para nuevas llaves en queries
            ad_months[i]["Cuenta"] = ad_months[i]["Cuenta"].astype("float")
            ad_months[i]["Cuenta"] = ad_months[i]["Cuenta"].fillna(0)
            ad_months[i]["Cuenta"] = ad_months[i]["Cuenta"].astype("int64")
            ad_months[i]["temp"] = ad_months[i]["Cuenta"].astype("string")
            #* Cruce con Queries
            ad_months[i].drop("Llave_ad", axis=1, inplace=True)
            ad_months[i]["Llave"] = ad_months[i]["F VALE"].dt.year.astype(str) + ad_months[i]["F VALE"].dt.month.astype(str) + ad_months[i]["F VALE"].dt.day.astype(str) + ad_months[i]["temp"].str[-8:].astype(str)
            ad_months[i]["Llave"] = ad_months[i]["Llave"].astype("string")
            #? Con merge buscamos cada registro del quary y lo colocamos a la derecha, si hay 2 se duplica el registro de ad_months
            df = pd.merge(ad_months[i], dataq, on=["Llave"], how="left")
            #? Eliminar registros duplicados de ad_months (Colocar en np.nan)
            df.loc[df.duplicated(["#"]), ('F VALE','F ABONO','AUTORIZACION','VLR COMISION','VLR RETE ICA','VLR RETE FUENTE','VLR ABONO','Redondear','Llave')] = np.nan
            #? Realizar una copia de solo los # para sumar tanto Redondear y VALOR (VALOR de querys)
            c = df[["#","Redondear","VALOR"]].groupby("#").sum()
            cont += ((50/len(ad_months))/5)
            self.update_progress(cont)
            #? Realizar nueva columna con la resta de las 2 columnas, condiciones y nueva columna que nos induca si cruzo o no
            c["Resta"] = c["Redondear"] - c["VALOR"]
            conditions = [
            (c['Resta'] == 0) & (c['VALOR'] != 0),
            (c['Resta'] <= 500) & (c['Resta'] >= -500) & (c['VALOR'] != 0),
            ]
            choices = ['CRUCE','CRUCE CON DIFF']
            c['Res'] = np.select(conditions, choices, default="NO")
            #? Colocar la nueva columna con resultados en el datframe de salida y organizarlas
            ad_months[i] = pd.merge(df, c[["Resta","Res"]], left_on='#', right_index=True, how="left", sort=False)
            cols = ad_months[i].columns.to_list()
            cols = cols[-1:] + cols[:-1]
            ad_months[i] = ad_months[i][cols]
            #* Exportar datos a hoja de excel
            values = [ad_months[i].columns] + list(ad_months[i].values)
            wb.new_sheet(ad_file.sheet_names[i], data=values)
            cont += ((50/len(ad_months))/5)
            self.update_progress(cont)
        #* Guardar el archvios de excel
        name_file = datetime.datetime.now().strftime("%d-%m-%Y")
        wb.save(f"Cruce_Final_Realizado_{name_file}.xlsx")
        self.update_progress(100)
        self.msg = self.msg + f"\n\nPrograma finalizado"
        self.msg = self.msg + f"\nSe ha creado un archivo de Excel en el directorio del programa"
        self.error_msg.emit(str(self.msg))
        print("Archivo de excel creado")

def validationOfFiles():
    """Función que valida que las bases de datos se ecuentren en el deirectorio del programa separados por carpetas

    Returns:
        [str]: Mensaje de error o exito
    """
    print(f"Entro a la funcion de validar files ahora si")
    msg = ""
    currentDirectory = os.listdir(os.getcwd())
    if "csv_data" not in currentDirectory:
        msg = ""
        msg = msg + "\nNo se encuentra la carpeta 'csv_data' en el directorio del programa.\nPorfavor verifique que la carpeta se encuentre en el directorio especificado, y vuelva a ejecutar el programa \ndando click en Acerca de y luego Home"
        return msg
    if "TC" not in os.listdir(os.getcwd() + "\csv_data"):
        msg = ""
        msg = msg + "\nNo se encuentra la carpeta 'TC' dentro de 'csv_data' en el directorio del programa.\nPorfavor verifique que la carpeta se encuentre en el directorio especificado, y vuelva a ejecutar el programa \ndando click en Acerca de y luego Home"
    if "Query" not in os.listdir(os.getcwd() + "\csv_data"):
        msg = ""
        msg = msg + "\nNo se encuentra la carpeta 'Query' dentro de 'csv_data' en el directorio del programa.\nPorfavor verifique que la carpeta se encuentre en el directorio especificado, y vuelva a ejecutar el programa \ndando click en Acerca de y luego Home"
    if msg:
        return msg
    return msg

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Get context
    main = MainWindow()
    engine.rootContext().setContextProperty("backend", main)
    # Load QML file
    engine.load(os.path.join(os.path.dirname(__file__), "qml/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    ret = app.exec_()
    sys.exit(ret)
