const express = require('express');
const app = express();
const port = process.env.PORT || 8080;

app.get('/', (req, res) => {
  res.send(`
    <h1>Hello, World!</h1>
    <img src="https://placehold.co/600x400" alt="placeholder image">
  `);
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});