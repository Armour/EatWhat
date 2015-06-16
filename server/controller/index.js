var express = require('express');
var mysql = require('mysql');

var client = mysql.createConnection(require('../dbConfig.json'));

exports.order = function(req, res) {
    if (req.body.restaurant_id) {
        var values = [];
        var sql = "INSERT INTO evaluate (user_id, restaurant_id, score) VALUES ?";
        for (var i = 0; i < req.body.restaurant_id.length; i++) {
            console.log(req.body.restaurant_id[i]);
            var tmpArr = [req.body.user_id, req.body.restaurant_id[i], '4'];
            values.push(tmpArr);
        }
        client.query(sql, [values],
            function(err, rows, fields) {
                if (err) {
                    throw err;
                }
                return res.json({
                    code: 0,
                    message: "Score Success"
                });
            })
    }
}
