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
	var sstats = "";
	collection.findOne({"tvshow":"suits"},{},function(e, docs){
		astats = docs;
		sc = db.get('source_stats');
		sc.find({"tvshow":"suits"},{"sort":[["source_count","desc"]], "limit":10},function(e,docs){
			sstats = docs;
			lc = db.get('lang_stats');
			lc.find({"tvshow":"suits"},{"sort":[["lang_count","desc"]], "limit":10},function(e,docs){
				lstats = docs;
				res.render('suits',{
					"all_stats": astats,
					"source_stats" : sstats,
					"lang_stats": lstats
				})
			});
		});
	});


	
});
module.exports = router;
