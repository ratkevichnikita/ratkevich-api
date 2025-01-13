const express = require('express');
const cors = require('cors');
const app = express();

// Разрешаем запросы с http://localhost:3000
app.use(cors({
  origin: ['http://localhost:3000', 'https://localhost:3000']
}));

app.get('/', (req, res) => {
  res.send('Все настроено! Проверка автодеплоя');
});

app.listen(3000, () => {
  console.log('Сервер запущен на https://localhost:3000');
});