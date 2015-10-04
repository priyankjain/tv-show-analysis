var express = require('express');
var router = express.Router();
var fs = require("fs");
var path = require('path');
/* GET home page. */
router.get('/', function(req, res, next) {
	res.render('index', { title: 'TV Show Analysis' });
});



router.get('/suits', function(req, res){
	var db = req.db;
	var lang_map = req.lang_map;
	var collection = db.get('all_stats');
	var astats = "";
	var sstats = "";
	collection.findOne({"tvshow":"suits"},{},function(e, docs){
		astats = docs;
		sc = db.get('source_stats');
		sc.find({"tvshow":"suits"},{"sort":[["source_count","desc"]], "limit":10},function(e,docs){
			sstats = docs;
			lc = db.get('lang_stats');
			lc.find({"tvshow":"suits", "lang":{$ne: "und"}},{"sort":[["lang_count","desc"]], "limit":10},function(e,docs){
				lstats = docs;
				for(i=0; i<lstats.length; i++){
					lstats[i]['lang'] = lang_map[lstats[i]['lang']];
				}
				res.render('tvshow',{
					"all_stats": astats,
					"source_stats" : sstats,
					"lang_stats": lstats,
					"title": "Suits - USA - TV Show Analysis",
					"heading": "Suits - USA",
					"image": "Suits.jpg"
				})
			});
		});
	});


	
});

router.get('/game-of-thrones', function(req, res){
	var db = req.db;
	var lang_map = req.lang_map;
	var collection = db.get('all_stats');
	var astats = "";
	var sstats = "";
	collection.findOne({"tvshow":"got"},{},function(e, docs){
		astats = docs;
		sc = db.get('source_stats');
		sc.find({"tvshow":"got"},{"sort":[["source_count","desc"]], "limit":10},function(e,docs){
			sstats = docs;
			lc = db.get('lang_stats');
			lc.find({"tvshow":"got", "lang":{$ne: "und"}},{"sort":[["lang_count","desc"]], "limit":10},function(e,docs){
				lstats = docs;
				for(i=0; i<lstats.length; i++){
					lstats[i]['lang'] = lang_map[lstats[i]['lang']];
				}
				res.render('tvshow',{
					"all_stats": astats,
					"source_stats" : sstats,
					"lang_stats": lstats,
					"title": "Game Of Thrones - HBO - TV Show Analysis",
					"heading": "Game Of Thrones - HBO",
					"image": "GOT.jpg"
				})
			});
		});
	});


	
});
module.exports = router;
