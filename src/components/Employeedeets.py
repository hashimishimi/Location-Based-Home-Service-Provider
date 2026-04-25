from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
import mysql.connector

import mysql.connector
import sys

DB_CONFIG ={
            "host": "localhost",
            "user": "root",
            "password": "pashu",
            "database": "home_service"
            }


@dataclass
class employeemodif:
    def AddEmp(name, email, phone_num, service, lat, lng):
        try:
            con = mysql.connector.connect(**DB_CONFIG)

            cursor = con.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                emp_ID INT AUTO_INCREMENT PRIMARY KEY,
                Name varchar(18),
                email varchar(35),
                phone_num varchar(13),
                service varchar(15),
                lat DECIMAL(10,8),
                lng DECIMAL(11,8)
                )                   
            """)

            cursor.execute("INSERT INTO employees (Name, email, phone_num, service, lat, lng) VALUES (%s, %s, %s, %s, %s, %s)",(name, email, phone_num, service, lat, lng))

            con.commit()

            cursor.close()
            con.close()

        except Exception as e:
            raise CustomException(e,sys)