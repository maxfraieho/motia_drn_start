# 🚀 TRANSFER BRIEF - Перенос проекту MOTIA DRN на новий сервер

**Дата**: 2025-10-18
**Проект**: DRAKON Viewer + Testing Framework
**Поточний сервер**: Raspberry Pi (обмежені ресурси)
**Цільовий сервер**: Потужніший Linux сервер

---

## 📋 Зміст

1. [Системні вимоги](#системні-вимоги)
2. [Підготовка нового сервера](#підготовка-нового-сервера)
3. [Встановлення залежностей](#встановлення-залежностей)
4. [Клонування проекту](#клонування-проекту)
5. [Налаштування Docker](#налаштування-docker)
6. [Налаштування nginx](#налаштування-nginx)
7. [Налаштування GitHub](#налаштування-github)
8. [Система тестування](#система-тестування)
9. [Claude Code налаштування](#claude-code-налаштування)
10. [Deployment процес](#deployment-процес)
11. [Перевірка роботи](#перевірка-роботи)
12. [Troubleshooting](#troubleshooting)

---

## 🖥️ Системні вимоги

### Мінімальні вимоги:
- **OS**: Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- **CPU**: 4+ cores (для Playwright тестів)
- **RAM**: 8GB+ (Playwright вимагає мінімум 4GB)
- **Disk**: 50GB+ SSD
- **Network**: Стабільне з'єднання (для GitHub та Docker Registry)

### Рекомендовані вимоги:
- **CPU**: 8+ cores
- **RAM**: 16GB+
- **Disk**: 100GB+ NVMe SSD

---

## 🛠️ Підготовка нового сервера

### 1. Оновлення системи
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Встановлення базових утиліт
```bash
sudo apt install -y \
  git \
  curl \
  wget \
  vim \
  htop \
  build-essential \
  ca-certificates \
  gnupg \
  lsb-release
```

### 3. Налаштування firewall (якщо потрібно)
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

---

## 📦 Встановлення залежностей

### 1. Docker
```bash
# Додати Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Додати Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Встановити Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Додати користувача в групу docker
sudo usermod -aG docker $USER
newgrp docker

# Перевірити встановлення
docker --version
```

### 2. Node.js (для тестування)
```bash
# Встановити Node.js 20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Перевірити версії
node --version  # v20.x.x
npm --version   # 10.x.x
```

### 3. Playwright (для браузерного тестування)
```bash
# Встановити Playwright dependencies
sudo npx playwright install-deps

# Перевірити
npx playwright --version
```

---

## 📂 Клонування проекту

### 1. Налаштування SSH ключів для GitHub
```bash
# Генерація SSH ключа (якщо потрібно)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Додати ключ в ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Показати публічний ключ (скопіювати в GitHub Settings → SSH Keys)
cat ~/.ssh/id_ed25519.pub
```

### 2. Клонування репозиторію
```bash
cd ~
git clone git@github.com:maxfraieho/motia_drn_start.git motia-drn

cd motia-drn
git status
```

### 3. Структура проекту
```
motia-drn/
├── tools/
│   └── drakon-viewer/         # DRAKON Editor веб-застосунок
│       ├── public/            # Статичні файли (HTML, CSS, JS)
│       │   ├── index.html
│       │   ├── js/
│       │   │   ├── app.js           # Основна логіка + Testing API
│       │   │   ├── state-manager.js # Управління станом
│       │   │   └── drakonwidget.js  # DRAKON рендеринг
│       │   └── css/
│       ├── Dockerfile         # Налаштування Docker контейнера
│       ├── nginx.conf         # Налаштування nginx
│       └── deploy.sh          # Скрипт автоматичного деплою
├── test/                      # Система тестування
│   ├── test.js               # Playwright тести (7 тестів)
│   ├── package.json          # Залежності тестів
│   └── test/                 # Результати тестів
│       ├── AI_browser_test_report.md
│       └── AI_Test_Diagram.json
├── promt/                    # Документація та промпти
└── TRANSFER-BRIEF.md         # Цей документ
```

---

## 🐳 Налаштування Docker

### 1. Перевірка Dockerfile
```bash
cat tools/drakon-viewer/Dockerfile
```

Має містити:
```dockerfile
FROM nginx:alpine
COPY public /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 2. Побудова образу
```bash
cd tools/drakon-viewer
docker build -t drakon-viewer .
```

### 3. Запуск контейнера
```bash
docker run -d \
  --name motia_drakon_viewer \
  --restart unless-stopped \
  -p 8080:80 \
  drakon-viewer
```

### 4. Перевірка статусу
```bash
docker ps | grep motia_drakon_viewer
docker logs motia_drakon_viewer
```

---

## 🌐 Налаштування nginx

### Варіант 1: Прямий доступ через Docker (порт 8080)
```bash
# Доступ: http://your-server-ip:8080
```

### Варіант 2: Reverse Proxy через nginx на хості

#### Встановлення nginx на хості
```bash
sudo apt install -y nginx
```

#### Створення конфігурації
```bash
sudo vim /etc/nginx/sites-available/drakon-viewer
```

Вміст файлу:
```nginx
server {
    listen 80;
    server_name drakon.yourdomain.com;  # Змінити на ваш домен

    location / {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Cache control для статичних файлів
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            proxy_pass http://localhost:8080;
            expires 7d;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

#### Активація конфігурації
```bash
sudo ln -s /etc/nginx/sites-available/drakon-viewer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Варіант 3: HTTPS через Let's Encrypt (рекомендовано)
```bash
# Встановити certbot
sudo apt install -y certbot python3-certbot-nginx

# Отримати SSL сертифікат
sudo certbot --nginx -d drakon.yourdomain.com

# Auto-renewal вже налаштований через systemd timer
sudo systemctl status certbot.timer
```

---

## 🔐 Налаштування GitHub

### 1. Налаштування Git користувача
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 2. Тестування доступу
```bash
ssh -T git@github.com
# Очікуваний вивід: Hi username! You've successfully authenticated...
```

### 3. Налаштування deployment webhook (опціонально)
Для автоматичного деплою при push в GitHub.

---

## 🧪 Система тестування

### 1. Встановлення залежностей тестів
```bash
cd ~/motia-drn/test
npm install
```

Файл `package.json`:
```json
{
  "name": "drakon-playwright-tests",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "test": "node test.js"
  },
  "dependencies": {
    "playwright": "^1.56.0"
  }
}
```

### 2. Встановлення браузерів Playwright
```bash
npx playwright install chromium
```

### 3. Запуск тестів
```bash
npm test
```

### 4. Структура тестів

**7 тестів через Testing API:**
1. ✅ Create New Diagram via API
2. ⚠️  Insert Action Node via API (має проблему з drakonwidget)
3. ✅ Verify Diagram Data
4. ✅ Save Diagram
5. ✅ Undo/Redo via Keyboard
6. ✅ Canvas Zoom
7. ✅ Load from LocalStorage

**Результати:**
- Звіт: `test/AI_browser_test_report.md`
- Приклад JSON: `test/AI_Test_Diagram.json`

### 5. Testing API в браузері

Testing API доступне глобально через `window.DrakonTestAPI`:

```javascript
// Створити діаграму
const diagram = window.DrakonTestAPI.createDiagram('Test Diagram');

// Отримати діаграму
const currentDiagram = window.DrakonTestAPI.getDiagram();

// Кількість нод
const nodeCount = window.DrakonTestAPI.getNodeCount();

// Додати ноду (action, question, branch, end)
window.DrakonTestAPI.addNode('action');

// Зберегти діаграму
window.DrakonTestAPI.saveDiagram();

// Перевірити режим редагування
const isEditMode = window.DrakonTestAPI.isEditMode();
```

---

## 🤖 Claude Code налаштування

### 1. Встановлення Claude Code (якщо потрібно)
Завантажити з: https://claude.ai/download

### 2. Налаштування проекту для Claude Code

#### Файл `.claudeproject` (в корені проекту)
```json
{
  "name": "MOTIA DRN - DRAKON Editor",
  "description": "DRAKON visual programming editor with testing framework",
  "include": [
    "tools/drakon-viewer/**/*",
    "test/**/*",
    "promt/**/*"
  ],
  "exclude": [
    "node_modules/**",
    "**/node_modules/**",
    "test/test/*.png",
    "**/.git/**"
  ]
}
```

#### Файл `Claude.md` (документація для Claude)
Використовується Claude Code для розуміння проекту.

### 3. Налаштування SSH для Claude Code
```bash
# Claude Code використовує системні SSH ключі
# Переконатися що ключі налаштовані (див. розділ GitHub)
```

### 4. Дозволи для автоматичних команд

У Claude Code можна налаштувати automatic approvals для:
```bash
# Git операції
git add
git commit
git push

# Docker операції
docker exec
docker restart
docker ps

# Deployment
./deploy.sh

# Testing
npm test
npx playwright
```

Налаштувати в: `Settings → Permissions → Automatic Approvals`

### 5. Корисні команди для Claude

```bash
# Перевірити статус проекту
git status
docker ps

# Запустити тести
cd /path/to/motia-drn/test && npm test

# Деплой
cd /path/to/motia-drn/tools/drakon-viewer && ./deploy.sh "Deploy message"

# Перевірити логи контейнера
docker logs motia_drakon_viewer --tail 50
```

---

## 🚢 Deployment процес

### Автоматичний деплой через deploy.sh

Скрипт `tools/drakon-viewer/deploy.sh`:

```bash
#!/bin/bash

echo "🚀 DRAKON Viewer Deployment Script"
echo "=================================="

# 1. Перевірити чи контейнер запущений
if ! docker ps | grep -q motia_drakon_viewer; then
    echo "❌ Container not running"
    exit 1
fi
echo "✅ Container motia_drakon_viewer is running"

# 2. Commit changes
if git diff --quiet && git diff --cached --quiet; then
    echo "⚠️  No changes to commit"
else
    echo "📝 Changes detected. Committing..."
    git add .
    git commit -m "$1"
    echo "✅ Changes committed"
fi

# 3. Push to GitHub
echo "📤 Pushing to remote..."
git push
echo "✅ Pushed to remote"

# 4. Restart container (nginx picks up new files)
echo "🔄 Restarting nginx container..."
docker restart motia_drakon_viewer
echo "✅ Container restarted successfully"

echo ""
echo "🎉 Deployment completed!"
echo ""
echo "🌐 Your site is live at: https://your-domain.com/"
echo ""
echo "📋 Next steps:"
echo "   - Test the changes in browser"
echo "   - Check browser console for errors"
echo "   - Clear browser cache if needed (Ctrl+Shift+R)"
```

### Використання:
```bash
cd ~/motia-drn/tools/drakon-viewer
./deploy.sh "Update feature X"
```

### Ручний деплой:
```bash
# 1. Commit та push змін
git add .
git commit -m "Update message"
git push

# 2. Перебудувати образ (якщо змінено Dockerfile або nginx.conf)
docker build -t drakon-viewer .

# 3. Зупинити старий контейнер
docker stop motia_drakon_viewer
docker rm motia_drakon_viewer

# 4. Запустити новий контейнер
docker run -d \
  --name motia_drakon_viewer \
  --restart unless-stopped \
  -p 8080:80 \
  drakon-viewer

# 5. Перевірити
docker logs motia_drakon_viewer
```

---

## ✅ Перевірка роботи

### 1. Перевірка Docker
```bash
# Статус контейнера
docker ps | grep motia_drakon_viewer

# Логи
docker logs motia_drakon_viewer --tail 50

# Зайти в контейнер
docker exec -it motia_drakon_viewer sh
ls -la /usr/share/nginx/html/
exit
```

### 2. Перевірка веб-сайту
```bash
# Локально
curl -I http://localhost:8080

# Через домен (якщо налаштовано)
curl -I https://your-domain.com
```

### 3. Перевірка Testing API
Відкрити в браузері Developer Tools (F12) → Console:
```javascript
// Перевірити наявність API
console.log(typeof window.DrakonTestAPI);  // должно быть "object"

// Створити тестову діаграму
const diagram = window.DrakonTestAPI.createDiagram('Test');
console.log(diagram);

// Перевірити кількість нод
console.log(window.DrakonTestAPI.getNodeCount());  // повинно бути 3
```

### 4. Запуск повних тестів
```bash
cd ~/motia-drn/test
npm test

# Переглянути звіт
cat test/AI_browser_test_report.md
```

### 5. Перевірка performance
```bash
# Використання ресурсів контейнером
docker stats motia_drakon_viewer

# Системні ресурси
htop
```

---

## 🔧 Troubleshooting

### Проблема: Docker контейнер не запускається
```bash
# Перевірити логи
docker logs motia_drakon_viewer

# Перевірити чи порт вільний
sudo netstat -tulpn | grep 8080

# Якщо порт зайнятий, змінити на інший
docker run -d --name motia_drakon_viewer -p 9090:80 drakon-viewer
```

### Проблема: Зміни не відображаються після deploy
```bash
# Перевірити версію файлів в контейнері
docker exec motia_drakon_viewer cat /usr/share/nginx/html/js/app.js | head -n 1

# Hard restart контейнера
docker stop motia_drakon_viewer
docker rm motia_drakon_viewer
docker build --no-cache -t drakon-viewer .
docker run -d --name motia_drakon_viewer -p 8080:80 drakon-viewer

# Очистити browser cache (Ctrl+Shift+R в браузері)
```

### Проблема: Playwright тести падають
```bash
# Перевстановити браузери
npx playwright install --force chromium

# Встановити system dependencies
sudo npx playwright install-deps

# Запустити тести з debug output
DEBUG=pw:api npm test
```

### Проблема: Git push не працює
```bash
# Перевірити SSH ключі
ssh -T git@github.com

# Переконатися що remote правильний
git remote -v

# Якщо потрібно, змінити на SSH
git remote set-url origin git@github.com:maxfraieho/motia_drn_start.git
```

### Проблема: Недостатньо пам'яті для тестів
```bash
# Перевірити вільну пам'ять
free -h

# Збільшити swap (якщо потрібно)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Додати в /etc/fstab для постійного використання
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Проблема: Повільна робота
```bash
# Перевірити системні ресурси
htop
iotop

# Перевірити Docker ресурси
docker stats

# Очистити Docker системи
docker system prune -a
```

---

## 📊 Поточний статус тестів

**Останній запуск: 2025-10-18**

```
🚀 DRAKON Editor v3.2 Browser Tests (Testing API)

==================================================
📊 TEST SUMMARY
==================================================
✅ Passed: 5/7 (71%)
❌ Failed: 1/7
⚠️  Warnings: 1/7
==================================================
```

**Працюючі тести:**
- ✅ Test 3: Verify Diagram Data
- ✅ Test 4: Save Diagram
- ✅ Test 5: Undo/Redo
- ✅ Test 6: Canvas Zoom
- ✅ Test 7: Load from LocalStorage

**Проблемні тести:**
- ❌ Test 1: Create New Diagram (помилка рендерингу в drakonwidget.js)
- ⚠️  Test 2: Insert Action Node (помилка з config в drakonwidget.js)

**Примітка:** Діаграми створюються коректно (JSON валідний), проблема в рендерингу drakonwidget.js.

---

## 📝 Checklist для переносу

### Перед переносом:
- [ ] Створити бекап поточної бази даних (якщо є)
- [ ] Експортувати всі діаграми з localStorage
- [ ] Задокументувати поточні налаштування nginx
- [ ] Зберегти SSH ключі

### На новому сервері:
- [ ] Встановити всі залежності (Docker, Node.js, etc.)
- [ ] Налаштувати SSH ключі для GitHub
- [ ] Клонувати репозиторій
- [ ] Налаштувати Docker контейнер
- [ ] Налаштувати nginx (reverse proxy або SSL)
- [ ] Встановити Playwright для тестів
- [ ] Запустити тести для перевірки
- [ ] Налаштувати Claude Code
- [ ] Протестувати deployment процес

### Після переносу:
- [ ] Оновити DNS записи (якщо змінюється домен)
- [ ] Перенести діаграми користувачів
- [ ] Запустити повний набір тестів
- [ ] Налаштувати моніторинг (опціонально)
- [ ] Налаштувати бекапи (опціонально)

---

## 🔗 Корисні посилання

- **GitHub репозиторій**: https://github.com/maxfraieho/motia_drn_start
- **Playwright документація**: https://playwright.dev/
- **Docker документація**: https://docs.docker.com/
- **nginx документація**: https://nginx.org/en/docs/
- **Claude Code**: https://claude.ai/code

---

## 📞 Контакти та підтримка

При виникненні проблем:
1. Перевірити розділ [Troubleshooting](#troubleshooting)
2. Переглянути логи Docker: `docker logs motia_drakon_viewer`
3. Запустити тести: `cd ~/motia-drn/test && npm test`
4. Перевірити GitHub Issues у репозиторії

---

**Останнє оновлення**: 2025-10-18
**Версія документа**: 1.0
**Автор**: Generated with Claude Code

