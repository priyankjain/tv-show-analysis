var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
	res.render('index', { title: 'Express' });
});



router.get('/suits', function(req, res){
	var db = req.db;
	var collection = db.get('all_stats');
	var astats = "";
	collection.findOne({"tvshow":"suits"},{},function(e, docs){
		astats = docs;
		res.render('suits',{
			"all_stats": astats
		})
	});
});
module.exports = router;
