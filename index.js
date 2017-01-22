var express = require('express');
var mongoose = require('mongoose');
var probe = require('probe-image-size');
var opts = {
	server: {
		socketOptions: {keepAlive: 1}
	}
};
//var credentials = require('./credentials.js');

var app = express();

switch(app.get('env')){
	case 'development':
		mongoose.connect("mongodb://admin:abcdef@ds117819.mlab.com:17819/mavericks", opts);
		break;
	case 'production':
		mongoose.connect("mongodb://admin:abcdef@ds117819.mlab.com:17819/mavericks", opts);
		break;
	default: 
		throw new Error('Unknown execution environment: ' + app.get('env'));
}

var Picture = require('./models/picture.js');

app.use(express.static('public'));
app.set('port', process.env.PORT || 3000);

var handlebars = require('express-handlebars')
			.create({defaultLayout:'main'});
app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');

app.get('/', function(req, res) {
	res.render('home');
})

app.get('/about', function(req, res) {
	Picture.find(function(err, pics){
		console.log(pics.length);
		var context = {
			pics: pics.map(function(picture){
				return {
					address: picture.address,
					link: picture.link,
					altText: picture.altText,
					tags: picture.tags					
				}
			})
		};
		res.render('about', context);
	});
});

/*
app.get('/json', function(req, res){
	var foo = require('Data/picture.json');
	console.log(foo)
	res.render("home");
})
*/
app.use(function(req, res, next) {
	res.status(404);
	res.render('404');
})

app.use(function(err, req, res, next) {
	console.error(err,stack);
	res.status(500);
	res.render(500);
})

Picture.find(function(err, pics){
	if(err) return console.error(err);
	if(pics.length) return;

	new Picture({
		name: "test",
		ID: "000",
		link: "src/pic1.jpg",
		altText: "Error displaying picture"
		//tags: ["None"]
	}).save();
});

app.listen(app.get('port'), function(){
	console.log( 'Express started on http://localhost:' + app.get('port') + '; press Ctrl - C to terminate')
})