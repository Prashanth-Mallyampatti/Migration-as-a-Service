const express = require('express');
const app = express();
const fs = require('fs');
var path = require('path');
const routes = require('./routes/routes');
const https = require('https');
cookieParser = require('cookie-parser');
var session = require('express-session');
const port = 4000;
app.set('port',port);
const bodyParser = require('body-parser');	
app.use(bodyParser.urlencoded({ extended: false }));	
app.use(bodyParser.json());
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname + '/views'));
app.use(express.static(__dirname + '/assets'));

app.use(cookieParser());

// initialize express-session to allow us track the logged-in user across sessions.
app.use(session({
    key: 'user_sid',
    secret: 'somerandonstuffs',
    resave: false,
    saveUninitialized: false,
    cookie: {
        expires: 600000
    }
}));

app.use((req, res, next) => {
    if (req.cookies.user_sid && !req.session.user) {
        res.clearCookie('user_sid');        
    }
    next();
});
app.use(routes);

app.listen(port, () => {
    console.log(`Server running on port: ${port}`);
});