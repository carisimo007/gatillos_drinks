import sqlite3
import os


class Conexion:

    def __init__(self):
        os.makedirs("database", exist_ok=True)

        self.conexion = sqlite3.connect("database/gatillos.db")
        self.cursor = self.conexion.cursor()

    def ejecutar(self, sql, parametros=()):
        self.cursor.execute(sql, parametros)
        self.conexion.commit()

    def consultar(self, sql, parametros=()):
        self.cursor.execute(sql, parametros)
        return self.cursor.fetchall()

    def consultar_uno(self, sql, parametros=()):
        self.cursor.execute(sql, parametros)
        return self.cursor.fetchone()

    def cerrar(self):
        self.conexion.close()