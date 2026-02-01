from flask import Flask, render_template_string, jsonify, request, session
import random
import time
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "mateubank-secret-key-2026"

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MateuBank - Финансовая игра</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Arial', sans-serif; }
        body { background: #0A0E17; color: #FFFFFF; min-height: 100vh; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        
        /* Шапка */
        .header { 
            background: #1A1F2E; 
            border-radius: 20px; 
            padding: 20px; 
            margin-bottom: 20px;
            display: flex; 
            align-items: center; 
            justify-content: space-between;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        .logo { display: flex; align-items: center; gap: 15px; }
        .logo-icon { font-size: 32px; color: #00D4FF; }
        .logo-text h1 { font-size: 28px; font-weight: bold; color: #00D4FF; }
        .logo-text p { font-size: 14px; color: #8B93B0; margin-top: 5px; }
        .time-display { font-size: 16px; color: #8B93B0; }
        
        /* Карточки баланса */
        .balance-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px;
        }
        .balance-card {
            background: #1A1F2E;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s;
        }
        .balance-card:hover { transform: translateY(-5px); }
        .card-title { 
            font-size: 14px; 
            color: #8B93B0; 
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .card-amount { 
            font-size: 32px; 
            font-weight: bold; 
            margin: 10px 0;
        }
        .card-extra { font-size: 12px; color: #8B93B0; }
        
        /* Общий баланс */
        .total-balance {
            background: linear-gradient(135deg, #1A1F2E 0%, #2A2F3E 100%);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
            border: 2px solid #FFD166;
        }
        .total-label { font-size: 16px; color: #FFD166; margin-bottom: 10px; }
        .total-amount { font-size: 48px; font-weight: bold; color: #FFD166; }
        
        /* Кнопки действий */
        .actions-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .action-btn {
            background: #1A1F2E;
            border: none;
            border-radius: 15px;
            padding: 25px;
            color: white;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        .action-btn:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }
        .action-btn-icon { font-size: 24px; }
        
        /* Цвета кнопок */
        .btn-work { background: linear-gradient(135deg, #007AFF, #5AC8FA); }
        .btn-business { background: linear-gradient(135deg, #34C759, #00FF9D); }
        .btn-casino { background: linear-gradient(135deg, #FF3B30, #FF9500); }
        .btn-mining { background: linear-gradient(135deg, #FF9500, #FFD166); }
        .btn-shop { background: linear-gradient(135deg, #9C27B0, #E040FB); }
        .btn-transfer { background: linear-gradient(135deg, #00BCD4, #00D4FF); }
        
        /* Модальные окна */
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }
        .modal-content {
            background: #1A1F2E;
            border-radius: 20px;
            padding: 30px;
            max-width: 500px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .modal-title {
            font-size: 24px;
            color: #00D4FF;
        }
        .close-btn {
            background: none;
            border: none;
            color: #8B93B0;
            font-size: 24px;
            cursor: pointer;
        }
        
        /* Формы */
        .form-group { margin-bottom: 20px; }
        .form-label { 
            display: block; 
            color: #8B93B0; 
            margin-bottom: 8px; 
            font-size: 14px;
        }
        .form-input {
            width: 100%;
            padding: 12px 15px;
            background: #2A3140;
            border: 2px solid #3A3F50;
            border-radius: 10px;
            color: white;
            font-size: 16px;
        }
        .form-input:focus {
            outline: none;
            border-color: #00D4FF;
        }
        .radio-group {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        .radio-label {
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
        }
        .radio-input { display: none; }
        .radio-custom {
            width: 20px;
            height: 20px;
            border: 2px solid #3A3F50;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .radio-input:checked + .radio-custom {
            border-color: #00D4FF;
        }
        .radio-input:checked + .radio-custom::after {
            content: '';
            width: 10px;
            height: 10px;
            background: #00D4FF;
            border-radius: 50%;
        }
        
        /* Кнопки */
        .btn {
            background: #00D4FF;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            width: 100%;
        }
        .btn:hover { background: #00B8E6; transform: translateY(-2px); }
        .btn-success { background: #00FF9D; }
        .btn-success:hover { background: #00E68C; }
        .btn-danger { background: #FF3860; }
        .btn-danger:hover { background: #FF1A48; }
        .btn-warning { background: #FFD166; color: #333; }
        .btn-warning:hover { background: #FFC233; }
        
        /* Игры */
        .game-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .game-btn {
            background: #2A3140;
            border: 2px solid #3A3F50;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        .game-btn:hover {
            border-color: #00D4FF;
            transform: scale(1.05);
        }
        .game-icon { font-size: 32px; margin-bottom: 10px; }
        .game-title { font-size: 16px; font-weight: bold; margin-bottom: 5px; }
        .game-desc { font-size: 12px; color: #8B93B0; }
        
        /* Уведомления */
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #1A1F2E;
            border-left: 5px solid #00D4FF;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            display: none;
            z-index: 1001;
            max-width: 300px;
        }
        
        /* Адаптивность */
        @media (max-width: 768px) {
            .balance-grid { grid-template-columns: 1fr; }
            .actions-grid { grid-template-columns: 1fr; }
            .total-amount { font-size: 36px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Шапка -->
        <div class="header">
            <div class="logo">
                <div class="logo-icon">⚡</div>
                <div class="logo-text">
                    <h1>MATEUBANK</h1>
                    <p>Финансовая игра</p>
                </div>
            </div>
            <div class="time-display" id="currentTime">🕐 Загрузка...</div>
        </div>

        <!-- Карточки баланса -->
        <div class="balance-grid">
            <div class="balance-card">
                <div class="card-title">💳 Карта</div>
                <div class="card-amount" id="balanceCard">0 M฿</div>
                <div class="card-extra">Основной счет</div>
            </div>
            <div class="balance-card" id="phoneCard">
                <!-- Телефон будет обновляться через JS -->
            </div>
            <div class="balance-card">
                <div class="card-title">🏦 Депозит</div>
                <div class="card-amount" id="balanceDeposit">0 M฿</div>
                <div class="card-extra">Накопительный счет</div>
            </div>
        </div>

        <!-- Общий баланс -->
        <div class="total-balance">
            <div class="total-label">💰 ОБЩИЙ БАЛАНС</div>
            <div class="total-amount" id="totalBalance">0 M฿</div>
        </div>

        <!-- Кнопки действий -->
        <div class="actions-grid">
            <button class="action-btn btn-work" onclick="openModal('workModal')">
                <span class="action-btn-icon">💼</span>
                <span>Работа</span>
            </button>
            <button class="action-btn btn-business" onclick="openModal('businessModal')">
                <span class="action-btn-icon">🏢</span>
                <span>Бизнес</span>
            </button>
            <button class="action-btn btn-casino" onclick="openModal('casinoModal')">
                <span class="action-btn-icon">🎰</span>
                <span>Казино</span>
            </button>
            <button class="action-btn btn-mining" onclick="openModal('miningModal')">
                <span class="action-btn-icon">⛏️</span>
                <span>Майнинг</span>
            </button>
            <button class="action-btn btn-shop" onclick="openModal('shopModal')">
                <span class="action-btn-icon">🛍️</span>
                <span>Магазин</span>
            </button>
            <button class="action-btn btn-transfer" onclick="openModal('transferModal')">
                <span class="action-btn-icon">🔄</span>
                <span>Перевод</span>
            </button>
        </div>

        <!-- Уведомление -->
        <div class="notification" id="notification"></div>

        <!-- Модальные окна -->
        <!-- Модалка работы -->
        <div class="modal" id="workModal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2 class="modal-title">💼 Выбор работы</h2>
                    <button class="close-btn" onclick="closeModal('workModal')">×</button>
                </div>
                <div class="game-grid">
                    <div class="game-btn" onclick="startWork('courier')">
                        <div class="game-icon">🚚</div>
                        <div class="game-title">Курьер</div>
                        <div class="game-desc">100-200 M฿ за доставку</div>
                    </div>
                    <div class="game-btn" onclick="startWork('taxi')">
                        <div class="game-icon">🚕</div>
                        <div class="game-title">Таксист</div>
                        <div class="game-desc">200-400 M฿ за поездку</div>
                    </div>
                    <div class="game-btn" onclick="startWork('seller')">
                        <div class="game-icon">🛒</div>
                        <div class="game-title">Продавец</div>
                        <div class="game-desc">50-150 M฿ за смену</div>
                    </div>
                    <div class="game-btn" onclick="startWork('cleaner')">
                        <div class="game-icon">🧹</div>
                        <div class="game-title">Уборщик</div>
                        <div class="game-desc">80-120 M฿ за уборку</div>
                    </div>
                </div>
                <div id="workCooldown" style="color: #FF3860; text-align: center; margin-top: 15px; display: none;"></div>
            </div>
        </div>

        <!-- Модалка бизнеса -->
        <div class="modal" id="businessModal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2 class="modal-title">🏢 Ваш бизнес</h2>
                    <button class="close-btn" onclick="closeModal('businessModal')">×</button>
                </div>
                <div class="form-group">
                    <div class="form-label">Уровень бизнеса:</div>
                    <div style="font-size: 24px; color: #00D4FF;" id="businessLevel">1</div>
                </div>
                <div class="form-group">
                    <div class="form-label">Доход за клиента:</div>
                    <div style="font-size: 20px; color: #00FF9D;" id="businessIncome">50 M฿</div>
                </div>
                <div class="form-group">
                    <div class="form-label" id="businessStatus">Бизнес не активен</div>
                    <div id="businessCustomers" style="display: none;">Клиентов сегодня: 0</div>
                </div>
                <button class="btn btn-success" onclick="startBusiness()" id="startBusinessBtn">🚀 Начать рабочий день</button>
                <button class="btn" onclick="serveCustomer()" id="serveCustomerBtn" style="display: none; margin-top: 10px;">🤝 Обслужить клиента</button>
                <button class="btn btn-warning" onclick="upgradeBusiness()" style="margin-top: 10px;">📈 Улучшить бизнес</button>
            </div>
        </div>

        <!-- Модалка казино -->
        <div class="modal" id="casinoModal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2 class="modal-title">🎰 Казино удачи</h2>
                    <button class="close-btn" onclick="closeModal('casinoModal')">×</button>
                </div>
                <div style="text-align: center; margin-bottom: 20px;">
                    <p>Угадайте число от 1 до 25</p>
                    <p style="color: #00FF9D;">Выигрыш = число × 100 M฿</p>
                </div>
                <div class="radio-group" id="casinoNumbers" style="justify-content: center;">
                    <!-- Числа будут добавлены через JS -->
                </div>
                <button class="btn btn-danger" onclick="makeBet()" style="margin-top: 20px;">🎲 Сделать ставку</button>
            </div>
        </div>

        <!-- Модалка майнинга -->
        <div class="modal" id="miningModal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2 class="modal-title">⛏️ Крипто-майнинг</h2>
                    <button class="close-btn" onclick="closeModal('miningModal')">×</button>
                </div>
                <div id="miningContent" style="text-align: center; padding: 20px;">
                    <p>Добывайте криптовалюту</p>
                    <p style="color: #FFD166;">Награда: 50-500 M฿</p>
                    <button class="btn btn-warning" onclick="startMining()" style="margin-top: 20px;">⚡ Начать майнинг</button>
                </div>
            </div>
        </div>

        <!-- Модалка магазина -->
        <div class="modal" id="shopModal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2 class="modal-title">🛍️ Магазин улучшений</h2>
                    <button class="close-btn" onclick="closeModal('shopModal')">×</button>
                </div>
                <div style="margin-bottom: 20px; padding: 15px; background: #2A3140; border-radius: 10px;">
                    💳 Баланс на карте: <span id="shopBalance">0 M฿</span>
                </div>
                <div id="shopItems">
                    <!-- Товары будут добавлены через JS -->
                </div>
            </div>
        </div>

        <!-- Модалка перевода -->
        <div class="modal" id="transferModal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2 class="modal-title">🔄 Перевод средств</h2>
                    <button class="close-btn" onclick="closeModal('transferModal')">×</button>
                </div>
                <div class="form-group">
                    <div class="form-label">Откуда:</div>
                    <div class="radio-group" id="transferFrom">
                        <label class="radio-label">
                            <input type="radio" name="from" value="card" checked class="radio-input">
                            <span class="radio-custom"></span>
                            💳 Карта
                        </label>
                    </div>
                </div>
                <div class="form-group">
                    <div class="form-label">Куда:</div>
                    <div class="radio-group" id="transferTo">
                        <label class="radio-label">
                            <input type="radio" name="to" value="deposit" checked class="radio-input">
                            <span class="radio-custom"></span>
                            🏦 Депозит
                        </label>
                    </div>
                </div>
                <div class="form-group">
                    <div class="form-label">Сумма перевода (M฿):</div>
                    <input type="number" class="form-input" id="transferAmount" placeholder="0" min="0" step="1">
                </div>
                <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                    <button class="btn" onclick="setAmount(100)" style="flex: 1;">100</button>
                    <button class="btn" onclick="setAmount(500)" style="flex: 1;">500</button>
                    <button class="btn" onclick="setAmount(1000)" style="flex: 1;">1000</button>
                    <button class="btn" onclick="setAmount(5000)" style="flex: 1;">5000</button>
                    <button class="btn" onclick="setMaxAmount()" style="flex: 1;">MAX</button>
                </div>
                <button class="btn btn-success" onclick="makeTransfer()">✅ Выполнить перевод</button>
            </div>
        </div>
    </div>

    <script>
        let gameData = {};
        let selectedCasinoNumber = 0;
        let miningInterval = null;

        // Обновление времени
        function updateTime() {
            const now = new Date();
            document.getElementById('currentTime').textContent = 
                '🕐 ' + now.toLocaleTimeString('ru-RU');
        }
        setInterval(updateTime, 1000);
        updateTime();

        // Загрузка данных игры
        async function loadGameData() {
            try {
                const response = await fetch('/api/game-data');
                gameData = await response.json();
                updateUI();
            } catch (error) {
                showNotification('Ошибка загрузки данных', 'danger');
            }
        }

        // Обновление интерфейса
        function updateUI() {
            // Балансы
            document.getElementById('balanceCard').textContent = 
                gameData.balance_card.toFixed(1) + ' M฿';
            document.getElementById('balanceDeposit').textContent = 
                gameData.balance_deposit.toFixed(1) + ' M฿';
            
            // Телефон
            const phoneCard = document.getElementById('phoneCard');
            if (gameData.phone_owned) {
                phoneCard.innerHTML = `
                    <div class="card-title">📱 Телефон</div>
                    <div class="card-amount">${gameData.balance_phone.toFixed(1)} M฿</div>
                    <div class="card-extra">Кошелек на телефоне</div>
                `;
            } else {
                phoneCard.innerHTML = `
                    <div class="card-title">📱 Телефон</div>
                    <div class="card-amount" style="color: #FF3860;">🔒</div>
                    <div class="card-extra">Цена: ${gameData.prices.phone} M฿</div>
                `;
            }
            
            // Общий баланс
            const total = gameData.balance_card + gameData.balance_phone + gameData.balance_deposit;
            document.getElementById('totalBalance').textContent = total.toFixed(1) + ' M฿';
            
            // Бизнес
            document.getElementById('businessLevel').textContent = gameData.business_level;
            document.getElementById('businessIncome').textContent = 
                (gameData.business_level * 50) + ' M฿';
            
            if (gameData.business_active) {
                document.getElementById('businessStatus').textContent = '🏢 Рабочий день идет...';
                document.getElementById('businessCustomers').style.display = 'block';
                document.getElementById('businessCustomers').textContent = 
                    `Клиентов сегодня: ${gameData.business_customers}`;
                document.getElementById('startBusinessBtn').style.display = 'none';
                document.getElementById('serveCustomerBtn').style.display = 'block';
            } else {
                document.getElementById('businessStatus').textContent = 'Бизнес не активен';
                document.getElementById('businessCustomers').style.display = 'none';
                document.getElementById('startBusinessBtn').style.display = 'block';
                document.getElementById('serveCustomerBtn').style.display = 'none';
            }
            
            // Магазин
            document.getElementById('shopBalance').textContent = gameData.balance_card.toFixed(1) + ' M฿';
            updateShopItems();
            
            // Перевод
            updateTransferOptions();
        }

        // Работа
        async function startWork(jobType) {
            try {
                const response = await fetch('/api/work', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ job_type: jobType })
                });
                const result = await response.json();
                
                if (result.success) {
                    showNotification(result.message, 'success');
                    loadGameData();
                } else {
                    showNotification(result.message, 'danger');
                    document.getElementById('workCooldown').style.display = 'block';
                    document.getElementById('workCooldown').textContent = 
                        `⏳ Отдохните ${result.wait_time?.toFixed(1) || 3}с`;
                }
            } catch (error) {
                showNotification('Ошибка выполнения работы', 'danger');
            }
        }

        // Бизнес
        async function startBusiness() {
            try {
                const response = await fetch('/api/business/start', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                const result = await response.json();
                showNotification(result.message, result.success ? 'success' : 'danger');
                loadGameData();
            } catch (error) {
                showNotification('Ошибка запуска бизнеса', 'danger');
            }
        }

        async function serveCustomer() {
            try {
                const response = await fetch('/api/business/serve', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                const result = await response.json();
                showNotification(result.message, result.success ? 'success' : 'danger');
                loadGameData();
            } catch (error) {
                showNotification('Ошибка обслуживания клиента', 'danger');
            }
        }

        async function upgradeBusiness() {
            try {
                const response = await fetch('/api/business/upgrade', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                const result = await response.json();
                showNotification(result.message, result.success ? 'success' : 'danger');
                loadGameData();
            } catch (error) {
                showNotification('Ошибка улучшения бизнеса', 'danger');
            }
        }

        // Казино
        function initCasino() {
            const container = document.getElementById('casinoNumbers');
            container.innerHTML = '';
            
            for (let i = 1; i <= 25; i++) {
                const label = document.createElement('label');
                label.className = 'radio-label';
                label.innerHTML = `
                    <input type="radio" name="casino" value="${i}" class="radio-input" 
                           onchange="selectedCasinoNumber = ${i}">
                    <span class="radio-custom"></span>
                    ${i}
                `;
                container.appendChild(label);
            }
        }

        async function makeBet() {
            if (!selectedCasinoNumber) {
                showNotification('Выберите число!', 'danger');
                return;
            }
            
            try {
                const response = await fetch('/api/casino/bet', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ number: selectedCasinoNumber })
                });
                const result = await response.json();
                showNotification(result.message, result.success ? 'success' : 'danger');
                loadGameData();
                if (result.success) {
                    closeModal('casinoModal');
                }
            } catch (error) {
                showNotification('Ошибка ставки', 'danger');
            }
        }

        // Майнинг
        async function startMining() {
            try {
                const response = await fetch('/api/mining/start', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                const result = await response.json();
                
                if (result.success) {
                    document.getElementById('miningContent').innerHTML = `
                        <p>⛏️ Идет майнинг...</p>
                        <div style="width: 100%; height: 20px; background: #2A3140; border-radius: 10px; margin: 20px 0; overflow: hidden;">
                            <div id="miningProgress" style="width: 0%; height: 100%; background: #FFD166; transition: width 0.1s;"></div>
                        </div>
                        <p style="color: #00FF9D;">Ожидаемая награда: ${result.mining_value} M฿</p>
                    `;
                    
                    let progress = 0;
                    miningInterval = setInterval(() => {
                        progress += 1;
                        document.getElementById('miningProgress').style.width = progress + '%';
                        
                        if (progress >= 100) {
                            clearInterval(miningInterval);
                            completeMining(result.mining_value);
                        }
                    }, 100);
                }
            } catch (error) {
                showNotification('Ошибка начала майнинга', 'danger');
            }
        }

        async function completeMining(value) {
            try {
                const response = await fetch('/api/mining/complete', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                const result = await response.json();
                showNotification(result.message, 'success');
                loadGameData();
                setTimeout(() => {
                    document.getElementById('miningContent').innerHTML = `
                        <p>Добывайте криптовалюту</p>
                        <p style="color: #FFD166;">Награда: 50-500 M฿</p>
                        <button class="btn btn-warning" onclick="startMining()" style="margin-top: 20px;">⚡ Начать майнинг</button>
                    `;
                }, 2000);
            } catch (error) {
                showNotification('Ошибка завершения майнинга', 'danger');
            }
        }

        // Магазин
        function updateShopItems() {
            const container = document.getElementById('shopItems');
            const items = [
                { 
                    id: 'phone', 
                    emoji: '📱', 
                    name: 'Смартфон', 
                    price: gameData.prices.phone,
                    owned: gameData.phone_owned,
                    desc: 'Открывает кошелек на телефоне',
                    color: '#FF2D75'
                },
                { 
                    id: 'car', 
                    emoji: '🚗', 
                    name: 'Машина', 
                    price: gameData.prices.car,
                    owned: gameData.car_owned,
                    desc: 'Таксист зарабатывает на 50% больше',
                    color: '#00D4FF'
                },
                { 
                    id: 'house', 
                    emoji: '🏠', 
                    name: 'Дом', 
                    price: gameData.prices.house,
                    owned: gameData.house_owned,
                    desc: '+10% ко всем доходам',
                    color: '#FFD166'
                }
            ];
            
            container.innerHTML = '';
            items.forEach(item => {
                const div = document.createElement('div');
                div.style.cssText = `
                    background: #2A3140;
                    border-radius: 10px;
                    padding: 20px;
                    margin-bottom: 15px;
                    border-left: 5px solid ${item.color};
                `;
                
                if (item.owned) {
                    div.innerHTML = `
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-size: 20px; font-weight: bold;">
                                    ${item.emoji} ${item.name}
                                </div>
                                <div style="color: #8B93B0; font-size: 14px; margin-top: 5px;">
                                    ${item.desc}
                                </div>
                            </div>
                            <div style="color: #00FF9D; font-weight: bold;">✓ Куплено</div>
                        </div>
                    `;
                } else {
                    const canBuy = gameData.balance_card >= item.price;
                    div.innerHTML = `
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-size: 20px; font-weight: bold;">
                                    ${item.emoji} ${item.name}
                                </div>
                                <div style="color: #8B93B0; font-size: 14px; margin-top: 5px;">
                                    ${item.desc}
                                </div>
                            </div>
                            <div>
                                <div style="text-align: right; margin-bottom: 10px;">
                                    <div style="color: ${item.color}; font-weight: bold; font-size: 18px;">
                                        ${item.price} M฿
                                    </div>
                                </div>
                                <button onclick="buyItem('${item.id}')" 
                                        style="background: ${canBuy ? '#00FF9D' : '#FF3860'}; 
                                               color: white; 
                                               border: none; 
                                               padding: 8px 16px; 
                                               border-radius: 5px; 
                                               cursor: ${canBuy ? 'pointer' : 'not-allowed'};">
                                    ${canBuy ? 'Купить' : 'Недостаточно средств'}
                                </button>
                            </div>
                        </div>
                    `;
                }
                
                container.appendChild(div);
            });
        }

        async function buyItem(itemId) {
            try {
                const response = await fetch('/api/shop/buy', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ item_id: itemId })
                });
                const result = await response.json();
                showNotification(result.message, result.success ? 'success' : 'danger');
                loadGameData();
            } catch (error) {
                showNotification('Ошибка покупки', 'danger');
            }
        }

        // Переводы
        function updateTransferOptions() {
            const fromContainer = document.getElementById('transferFrom');
            const toContainer = document.getElementById('transferTo');
            
            const accounts = [
                { id: 'card', emoji: '💳', name: 'Карта', balance: gameData.balance_card },
                { id: 'phone', emoji: '📱', name: 'Телефон', balance: gameData.balance_phone, available: gameData.phone_owned },
                { id: 'deposit', emoji: '🏦', name: 'Депозит', balance: gameData.balance_deposit }
            ];
            
            fromContainer.innerHTML = '';
            toContainer.innerHTML = '';
            
            accounts.forEach(acc => {
                if (acc.id === 'phone' && !acc.available) return;
                
                // From options
                const fromLabel = document.createElement('label');
                fromLabel.className = 'radio-label';
                fromLabel.innerHTML = `
                    <input type="radio" name="from" value="${acc.id}" ${acc.id === 'card' ? 'checked' : ''} class="radio-input">
                    <span class="radio-custom"></span>
                    ${acc.emoji} ${acc.name} (${acc.balance.toFixed(1)} M฿)
                `;
                fromContainer.appendChild(fromLabel);
                
                // To options (кроме текущего выбранного from)
                const toLabel = document.createElement('label');
                toLabel.className = 'radio-label';
                toLabel.innerHTML = `
                    <input type="radio" name="to" value="${acc.id}" ${acc.id === 'deposit' ? 'checked' : ''} class="radio-input">
                    <span class="radio-custom"></span>
                    ${acc.emoji} ${acc.name}
                `;
                toContainer.appendChild(toLabel);
            });
        }

        function setAmount(amount) {
            document.getElementById('transferAmount').value = amount;
        }

        function setMaxAmount() {
            const from = document.querySelector('input[name="from"]:checked').value;
            let maxAmount = 0;
            
            if (from === 'card') maxAmount = gameData.balance_card;
            else if (from === 'phone') maxAmount = gameData.balance_phone;
            else if (from === 'deposit') maxAmount = gameData.balance_deposit;
            
            document.getElementById('transferAmount').value = Math.floor(maxAmount);
        }

        async function makeTransfer() {
            const from = document.querySelector('input[name="from"]:checked').value;
            const to = document.querySelector('input[name="to"]:checked').value;
            const amount = parseFloat(document.getElementById('transferAmount').value);
            
            if (!amount || amount <= 0) {
                showNotification('Введите корректную сумму!', 'danger');
                return;
            }
            
            if (from === to) {
                showNotification('Нельзя переводить на тот же счет!', 'danger');
                return;
            }
            
            try {
                const response = await fetch('/api/transfer', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        from_account: from,
                        to_account: to,
                        amount: amount
                    })
                });
                const result = await response.json();
                showNotification(result.message, result.success ? 'success' : 'danger');
                if (result.success) {
                    loadGameData();
                    closeModal('transferModal');
                }
            } catch (error) {
                showNotification('Ошибка перевода', 'danger');
            }
        }

        // Уведомления
        function showNotification(message, type) {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.style.borderLeftColor = 
                type === 'success' ? '#00FF9D' : 
                type === 'danger' ? '#FF3860' : '#00D4FF';
            notification.style.display = 'block';
            
            setTimeout(() => {
                notification.style.display = 'none';
            }, 3000);
        }

        // Модальные окна
        function openModal(modalId) {
            document.getElementById(modalId).style.display = 'flex';
            if (modalId === 'casinoModal') initCasino();
        }

        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
            if (miningInterval) {
                clearInterval(miningInterval);
                miningInterval = null;
            }
        }

        // Закрытие модалок при клике вне их
        window.onclick = function(event) {
            if (event.target.className === 'modal') {
                event.target.style.display = 'none';
                if (miningInterval) {
                    clearInterval(miningInterval);
                    miningInterval = null;
                }
            }
        }

        // Инициализация
        document.addEventListener('DOMContentLoaded', () => {
            loadGameData();
        });
    </script>
</body>
</html>
'''

# API эндпоинты
@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/api/game-data', methods=['GET'])
def get_game_data():
    if 'game_data' not in session:
        session['game_data'] = {
            'currency': "M฿",
            'balance_card': 1000.0,
            'balance_phone': 0.0,
            'balance_deposit': 0.0,
            'phone_owned': False,
            'car_owned': False,
            'house_owned': False,
            'prices': {'phone': 5000, 'car': 25000, 'house': 100000},
            'last_work_time': 0,
            'work_cooldown': 3,
            'business_level': 1,
            'business_active': False,
            'business_customers': 0,
            'mining_active': False,
            'mining_start_time': 0,
            'mining_value': 0
        }
    return jsonify(session['game_data'])

@app.route('/api/work', methods=['POST'])
def work():
    data = request.json
    job_type = data.get('job_type', 'courier')
    game_data = session['game_data']
    
    current_time = time.time()
    if current_time - game_data['last_work_time'] < game_data['work_cooldown']:
        wait = game_data['work_cooldown'] - (current_time - game_data['last_work_time'])
        return jsonify({
            'success': False,
            'message': f'Отдохните еще {wait:.1f} секунд!',
            'wait_time': wait
        })
    
    earnings_map = {
        'courier': random.randint(100, 200),
        'taxi': random.randint(200, 400),
        'seller': random.randint(50, 150),
        'cleaner': random.randint(80, 120)
    }
    
    earnings = earnings_map.get(job_type, 100)
    if game_data['house_owned']:
        earnings = int(earnings * 1.1)
    if job_type == 'taxi' and game_data['car_owned']:
        earnings = int(earnings * 1.5)
    
    game_data['balance_card'] += earnings
    game_data['last_work_time'] = current_time
    session['game_data'] = game_data
    
    return jsonify({
        'success': True,
        'earnings': earnings,
        'message': f'Работа выполнена! +{earnings}{game_data["currency"]}',
        'balance_card': game_data['balance_card']
    })

@app.route('/api/business/start', methods=['POST'])
def start_business():
    game_data = session['game_data']
    game_data['business_active'] = True
    game_data['business_customers'] = 0
    session['game_data'] = game_data
    return jsonify({'success': True, 'message': 'Рабочий день начался!'})

@app.route('/api/business/serve', methods=['POST'])
def serve_customer():
    game_data = session['game_data']
    if not game_data['business_active']:
        return jsonify({'success': False, 'message': 'Сначала начните рабочий день!'})
    
    income = game_data['business_level'] * 50
    if game_data['house_owned']:
        income = int(income * 1.1)
    
    game_data['balance_card'] += income
    game_data['business_customers'] += 1
    session['game_data'] = game_data
    
    return jsonify({
        'success': True,
        'income': income,
        'message': f'Клиент обслужен! +{income}{game_data["currency"]}',
        'customers': game_data['business_customers']
    })

@app.route('/api/business/upgrade', methods=['POST'])
def upgrade_business():
    game_data = session['game_data']
    cost = game_data['business_level'] * 1000
    
    if game_data['balance_card'] >= cost:
        game_data['balance_card'] -= cost
        game_data['business_level'] += 1
        session['game_data'] = game_data
        return jsonify({
            'success': True,
            'message': f'Бизнес улучшен до уровня {game_data["business_level"]}!',
            'business_level': game_data['business_level']
        })
    else:
        return jsonify({
            'success': False,
            'message': f'Недостаточно средств! Нужно {cost}{game_data["currency"]}'
        })

@app.route('/api/casino/bet', methods=['POST'])
def casino_bet():
    data = request.json
    selected = data.get('number', 0)
    game_data = session['game_data']
    
    if selected == 0:
        return jsonify({'success': False, 'message': 'Выберите число!'})
    
    number = random.randint(1, 25)
    
    if selected == number:
        winnings = number * 100
        if game_data['house_owned']:
            winnings = int(winnings * 1.1)
        game_data['balance_card'] += winnings
        session['game_data'] = game_data
        return jsonify({
            'success': True,
            'message': f'🎉 Вы угадали число {number}! Выигрыш: {winnings}{game_data["currency"]}'
        })
    else:
        return jsonify({
            'success': False,
            'message': f'😞 Загадано число {number}, а вы выбрали {selected}'
        })

@app.route('/api/mining/start', methods=['POST'])
def start_mining():
    game_data = session['game_data']
    game_data['mining_active'] = True
    game_data['mining_start_time'] = time.time()
    game_data['mining_value'] = random.randint(50, 500)
    session['game_data'] = game_data
    
    return jsonify({
        'success': True,
        'mining_value': game_data['mining_value'],
        'message': 'Майнинг начался!'
    })

@app.route('/api/mining/complete', methods=['POST'])
def complete_mining():
    game_data = session['game_data']
    
    if not game_data['mining_active']:
        return jsonify({'success': False, 'message': 'Майнинг не активен!'})
    
    earnings = game_data['mining_value']
    if game_data['house_owned']:
        earnings = int(earnings * 1.1)
    
    game_data['balance_card'] += earnings
    game_data['mining_active'] = False
    session['game_data'] = game_data
    
    return jsonify({
        'success': True,
        'message': f'Майнинг завершен! Добыто: {earnings}{game_data["currency"]}'
    })

@app.route('/api/shop/buy', methods=['POST'])
def shop_buy():
    data = request.json
    item_id = data.get('item_id')
    game_data = session['game_data']
    
    if item_id not in ['phone', 'car', 'house']:
        return jsonify({'success': False, 'message': 'Неверный товар!'})
    
    price = game_data['prices'][item_id]
    
    if game_data['balance_card'] < price:
        return jsonify({'success': False, 'message': f'Недостаточно средств! Нужно {price}{game_data["currency"]}'})
    
    if item_id == 'phone' and not game_data['phone_owned']:
        game_data['balance_card'] -= price
        game_data['phone_owned'] = True
        game_data['balance_phone'] = 100  # Бонус
        message = f'📱 Смартфон куплен! Кошелек на телефоне активирован. +100{game_data["currency"]} бонус!'
    elif item_id == 'car' and not game_data['car_owned']:
        game_data['balance_card'] -= price
        game_data['car_owned'] = True
        message = '🚗 Машина куплена! Таксист теперь работает быстрее.'
    elif item_id == 'house' and not game_data['house_owned']:
        game_data['balance_card'] -= price
        game_data['house_owned'] = True
        message = '🏠 Дом куплен! Все доходы увеличены на 10%.'
    else:
        return jsonify({'success': False, 'message': 'Этот товар уже куплен!'})
    
    session['game_data'] = game_data
    return jsonify({'success': True, 'message': message})

@app.route('/api/transfer', methods=['POST'])
def transfer():
    data = request.json
    from_account = data.get('from_account')
    to_account = data.get('to_account')
    amount = float(data.get('amount', 0))
    game_data = session['game_data']
    
    if amount <= 0:
        return jsonify({'success': False, 'message': 'Сумма должна быть больше нуля!'})
    
    if from_account == to_account:
        return jsonify({'success': False, 'message': 'Нельзя переводить на тот же счет!'})
    
    # Проверка баланса
    if from_account == 'card':
        if amount > game_data['balance_card']:
            return jsonify({'success': False, 'message': 'Недостаточно средств на карте!'})
        game_data['balance_card'] -= amount
    elif from_account == 'phone':
        if not game_data['phone_owned']:
            return jsonify({'success': False, 'message': 'Телефон не куплен!'})
        if amount > game_data['balance_phone']:
            return jsonify({'success': False, 'message': 'Недостаточно средств на телефоне!'})
        game_data['balance_phone'] -= amount
    elif from_account == 'deposit':
        if amount > game_data['balance_deposit']:
            return jsonify({'success': False, 'message': 'Недостаточно средств на депозите!'})
        game_data['balance_deposit'] -= amount
    
    # Зачисление
    if to_account == 'card':
        game_data['balance_card'] += amount
    elif to_account == 'phone':
        if not game_data['phone_owned']:
            return jsonify({'success': False, 'message': 'Телефон не куплен!'})
        game_data['balance_phone'] += amount
    elif to_account == 'deposit':
        game_data['balance_deposit'] += amount
    
    session['game_data'] = game_data
    return jsonify({
        'success': True,
        'message': f'Перевод выполнен! {amount}{game_data["currency"]}'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
