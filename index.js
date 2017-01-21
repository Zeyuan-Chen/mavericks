var express = require('express');
var mongoose = require('mongoose');
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

var Test = require('./models/test.js');

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
	Test.find(function(err, tests){
		console.log(tests.length);
		var context = {
			tests: tests.map(function(test){
				return {
					name: test.name,
					ID: test.ID
				}
			})
		};
		res.render('about', context);
	});
});

app.get('/json', function(req, res){
	var foo = require('Data/test.json');
	console.log(foo)
	res.render("home");
})

app.use(function(req, res, next) {
	res.status(404);
	res.render('404');
})

app.use(function(err, req, res, next) {
	console.error(err,stack);
	res.status(500);
	res.render(500);
})

Test.find(function(err, tests){
	if(err) return console.error(err);
	if(tests.length) return;

	new Test({
		name: "test1",
		ID: 1,
	}).save();

	new Test({
		name: "test2",
		ID: 2
	}).save();
});

app.listen(app.get('port'), function(){
	console.log( 'Express started on http://localhost:' + app.get('port') + '; press Ctrl - C to terminate')
})