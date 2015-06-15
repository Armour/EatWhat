var express = require('express');
var router = express.Router();
var mysql = require('mysql');
var indexController = require('../controller/index.js');

var client = mysql.createConnection(require('../dbConfig.json'));

/* GET home page. */
router.get('/', function(req, res, next) {
    client.query('SELECT * FROM restaurant ORDER BY RAND() LIMIT 20',
        function(err, rows) {
            if (err) {
                throw err;
            }
            var restaurant = [];
            if (rows) {
                console.log('hello');
                rows.foreach(function(e) {
                    console.log('!' + e);
                    restaurant.push({
                        id: e.id,
                        name: e.name,
                        score: e.score,
                        total: e.total,
                        picture: e.picture
                    })
                })
            }
            //client.query('SELECT * FROM user, recommend, recommend_uesr WHERE')
            res.render('index', {
                title: 'Express',
                restaurant: restaurant
            });
        });
});

router.post('/order', indexController.order);

module.exports = router;
