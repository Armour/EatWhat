var express = require('express');
var router = express.Router();
var sys = require('sys')
var exec = require('child_process').exec;
var mysql = require('mysql');
var indexController = require('../controller/index.js');

var client = mysql.createConnection(require('../dbConfig.json'));
var child;

/* GET home page. */
router.get('/', function(req, res, next) {
    var user = [];
    var restaurant = [];

    child = exec("bash update_recommend.sh", function(error, stdout, stderr) {
        console.log("recommend update!");
        if (error !== null) {
            console.log('exec error: ' + error);
        }
    });
    var recommend = require('../../db\ \&\ algorithm/recommend.json');
    console.log(recommend);

    client.query('SELECT * FROM user WHERE username=?', [req.query.username],
        function(err, rows) {
            if (err) {
                throw err;
            }
            if (rows) {
                user = rows[0];
            }
        });

    client.query('SELECT * FROM restaurant ORDER BY id',
        function(err, rows) {
            if (err) {
                throw err;
            }
            if (rows) {
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
