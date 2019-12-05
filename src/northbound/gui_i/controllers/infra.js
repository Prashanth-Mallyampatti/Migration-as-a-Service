const express = require('express');
let router = express();
const yaml = require('./saveYaml');

// middleware function to check for logged-in users
var sessionChecker = (req, res, next) => {
    if (!req.session.user || !req.cookies.user_sid) {
        res.redirect('/');
    } else {
        next();
    }    
};

router.get("/",sessionChecker,(req,res)=>{
    res.render("infra",{
        heading: `Infrastructure for ${req.session.user}`,
        name: req.session.user
    });
});

router.post("/",(req,res)=>{
    let submission = req.body["input"];
    yaml.save(submission,req.session.user,"infra/"+req.session.user);
    res.send();
});
module.exports = router;
