const express = require('express');
let router = express();
// middleware function to check for logged-in users
var sessionChecker = (req, res, next) => {
    if (req.session.user && req.cookies.user_sid) {
        res.redirect('/infra');
    } else {
        next();
    }    
};
router.get("/",sessionChecker,(req,res)=>{
    res.render("home");
});

router.post("/",(req,res)=>{
    req.session.user = req.body.name;
    res.redirect("/infra");
});

module.exports = router;