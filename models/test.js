var mongoose = require('mongoose');

var testSchema = mongoose.Schema({
	name: String,
	ID: Number,
});

testSchema.methods.getDisplayID = function(){
	return this.ID;
};

var Test = mongoose.model('Test', testSchema);
module.exports = Test;