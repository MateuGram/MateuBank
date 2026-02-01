import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import math
from datetime import datetime
import os
import sys

class MobileMateuBankApp:
    def __init__(self):
        self.root = tk.Tk()
        
        # Определяем размер экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Настройки для мобильных устройств
        if screen_width < 768:  # Мобильный телефон
            self.is_mobile = True
            app_width = min(400, screen_width - 20)
            app_height = min(700, screen_height - 100)
        else:  # ПК
            self.is_mobile = False
            app_width = 400
            app_height = 700
        
        self.root.title("MateuBank Mobile")
        self.root.geometry(f"{app_width}x{app_height}")
        self.root.configure(bg='#0A0E17')
        
        # Центрирование окна
        self.center_window(app_width, app_height)
        
        # Валюта
        self.currency = " M฿"
        
        # Начальный баланс
        self.balance_card = 1000.0
        self.balance_phone = 0.0
        self.balance_deposit = 0.0
        
        # Магазин
        self.phone_owned = False
        self.car_owned = False
        self.house_owned = False
        
        # Цены
        self.prices = {
            'phone': 5000,
            'car': 25000,
            'house': 100000
        }
        
        # Время
        self.last_work_time = 0
        self.work_cooldown = 3
        
        # Бизнес
        self.business_level = 1
        self.business_active = False
        self.business_customers = 0
        
        # Игровые переменные
        self.current_game = None
        self.mining_active = False
        self.mining_start_time = 0
        self.mining_value = 0
        
        #
