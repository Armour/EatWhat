var express = require('express');
var router = express.Router();
var mysql = require('mysql');
var indexController = require('../controller/index.js');
var recommend = require('../../db\ \&\ algorithm/recommend.json');

var client = mysql.createConnection(require('../dbConfig.json'));

/* GET home page. */
router.get('/', function(req, res, next) {
    var user = [];
    var restaurant = [];

    client.query('SELECT * FROM user WHERE username=?', [req.query.username],
        function(err, rows) {
            if (err) {
                throw err;
            }
            if (rows) {
                user = rows[0];
            }
        });

    client.query('SELECT * FROM restaurant ORDER BY RAND() LIMIT 20',
        function(err, rows) {
            if (err) {
                throw err;
            }
            if (rows) {
                console.log('hello');
                console.log(rows);
                rows.forEach(function(e) {
                    restaurant.push({
                        id: e.id,
                        name: e.name,
                        score: e.score,
                        total: e.total,
                        picture: e.picture
                    })
                })
            }
            res.render('index', {
                title: 'Express',
                user: user,
                restaurant: restaurant,
                recommend: recommend
            });
        });
});

router.post('/order', indexController.order);

module.exports = router;
