var mongoose = require('mongoose');

var pictureSchema = mongoose.Schema({
	ID: String,
	address: String,
	link: String,
	altText: String,
	tags: [String],
	time: { type: Date, default: Date.now },
});

var Picture = mongoose.model('Picture', pictureSchema);
module.exports = Picture;