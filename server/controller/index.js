var express = require('express');
var mysql = require('mysql');

var client = mysql.createConnection(require('../dbConfig.json'));

exports.order = function(req, res) {
    if (req.body.restaurant_id) {
        for (var i = 0; i < req.body.restaurant_id.length; i++) {
            client.query('INSERT INTO evaluate(user_id, restaurant_id, score) ', [req.body.user_id, req.body.restaurant_id[i], req.body.score[i]],
                function(err) {
                    if (err) {
                        throw err;
                    }
                });
        }
        /*return res.json({
            code: 0,
            message: "Score Success"
        });*/
    }
}
