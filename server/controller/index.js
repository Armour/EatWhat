var express = require('express');
var mysql = require('mysql');

var client = mysql.createConnection(require('../dbConfig.json'));

exports.order = function(req, res) {
    client.query('INSERT INTO evaluate(user_id, restaurant_id, score) ', [req.body.user_id, req.body.restaurant_id, req.body.score],
        function(err) {
            if (err) {
                throw err;
            }
            return res.json({
                code: 0,
                message: "Score Success"
            });
        });
}
