const express = require('express');
const homeController = require('../controllers/home');
const infraController = require('../controllers/infra');
const migrateController = require('../controllers/migrate');
let router = express();
router.use("/",homeController);
router.use("/infra",infraController);
router.use("/migrate",migrateController);
module.exports = router;