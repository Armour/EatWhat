var express = require('express');
var router = express.Router();
var userController = require('../controller/user.js');

/* GET users listing. */
router.post('/login', userController.login);
router.post('/register', userController.register);

module.exports = router;
