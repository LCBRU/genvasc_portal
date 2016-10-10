$(function () {
	if (!Modernizr.inputtypes.date) { 
	  $('input[type="date"]').datetimepicker({ format: 'D/M/YYYY'});
	}
	if (!Modernizr.inputtypes.datetime) { 
	  $('input[type="datetime"]').datetimepicker({ format: 'D/M/YYYY'});
	}
});

