var express = require('express');
var mysql = require('mysql');

var client = mysql.createConnection(require('../dbConfig.json'));

exports.register = function (req, res) {
    if (req.body.username.length === 0) {
        return res.json({
            code: 1,
            message: "No Username Inputed"
        })
    }
    if (req.body.password.length === 0) {
        return res.json({
            code: 2,
            message: "No Password Inputed"
        })
    }
    if (req.body.repassword.length === 0) {
        return res.json({
            code: 3,
            message: "You Need Reinput Your Password"
        })
    }
    if (req.body.password !== req.body.repassword) {
        return res.json({
            code: 4,
            message: "Password Not Match"
        })
    }
    client.query('INSERT INTO user (username, password) VALUES(?,?)',[req.body.username, req.body.password],
            function(err) {
                if (err) {
                    throw err;
                } else {
                    return res.json({
                        code: 0,
                        message: "Insert Success"
                    })
                }
            }
    )
}


exports.login = function (req, res) {
    if (req.body.username.length === 0) {
        return res.json({
            code: 1,
            message: "Empty username"
        })
    }
    client.query('SELECT * FROM user WHERE username=?', [req.body.username],
        function(err, row, fields) {
            if (err) {
                throw err;
            }
            if (row[0]) {
                if (row[0].password != req.body.password) {
                    return res.json({
                        code: 5,
                        message: "Wrong Password"
                    })
                } else {
                    req.session.username = req.body.username;
                    return res.json({
                        code: 0,
                        message: "Login Success"
                    })
                }
            } else {
                return res.json({
                    code : 6,
                    message: "Username Does Not Exist"
                })
            }
        });
};

express.logout = function (req, res) {
    req.session.destory(err) {
        if (!err) {
            return res.json({
                code: 0,
                message: "Logout Success"
            })
        }
    }
}
