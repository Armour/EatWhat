var express = require('express');
var router = express.Router();
var userController = require('../controller/user.js');

router.get('/register', function (req, res) {
    res.render('register', {
        title: 'Register'
    })
})

router.post('/login', userController.login);
router.post('/register', userController.register);
router.get('/logout', userController.logout);

module.exports = router;
