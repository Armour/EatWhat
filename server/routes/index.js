var express = require('express');
var router = express.Router();
var indexController = require('../controller/index.js');

var client = mysql.createConnection(require('../dbConfig.json'));

/* GET home page. */
router.get('/', function(req, res, next) {
    client.query('SELECT * FROM restaurant ORDER BY RAND() LIMIT 20',
        function(err, row, fields) {
            if (err) {
                throw err;
            }
            var restaurant = row;
            client.query('SELECT * FROM user, recommend, recommend_uesr WHERE')
            res.render('index', {
                title: 'Express'
            });
        });
});

router.post('/order', indexController.order);

module.exports = router;
