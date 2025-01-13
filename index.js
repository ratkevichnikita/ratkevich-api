const express = require('express');
const app = express();
const port = 3005;

app.get('/', (req, res) => {
  res.send('Все настроено!');
});

app.listen(port, () => {
  console.log(`Сервер запущен на http://localhost:${port}`);
});