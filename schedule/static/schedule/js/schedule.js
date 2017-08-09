if (typeof DS == 'undefined') { // T = django ticketing
  DS = {};
}

DS = function() {
  // Modal for deleting group
  function sendDeletionParameters (title, link, message) {
    $("#modal_title").html(title);
    $("#modal_message").html(message);
    $('#delete_submit').attr('onclick', "window.location.href='"+link+"'");
  }

  function createEvent(start, end) {
	  starttime = $.fullCalendar.formatDate(start,'HH:mm:ss');
	  endtime = $.fullCalendar.formatDate(end,'HH:mm:ss');
	  // get day which is clicked
	  day = $.fullCalendar.formatDate(start,'d');
	  // create hidden input (from)
	  $('<input>').attr({
	      type: 'hidden',
	      id: 'day'+day+'_from_id',
	      name: 'day'+day+'_from',
	      value: starttime
	  }).appendTo('form');

	  // create hidden input (until)
	  $('<input>').attr({
	      type: 'hidden',
	      id: 'day'+day+'_until_id',
	      name: 'day'+day+'_until',
	      value: endtime
	  }).appendTo('form');

	  $("#calendar").fullCalendar('renderEvent',
	    {
	      id: day,
	      title: $.fullCalendar.formatDate(start,'dddd'),
	      start: start,
	      end: end,
	    },true);
  }

  function updateEvent(event) {
  	$('#day'+event.id+'_from_id').val($.fullCalendar.formatDate(event.start,'HH:mm:ss'));
    $('#day'+event.id+'_until_id').val($.fullCalendar.formatDate(event.end,'HH:mm:ss'));
  }

  function deleteEvent(event_id) {
	 	$('#day'+event_id+'_from_id').remove();	
    $('#day'+event_id+'_until_id').remove();
    $('#calendar').fullCalendar('removeEvents', event_id);
  }

  // calendar_id is a string
  function showCalendar(calendar_id) {
  	$('#'+calendar_id).show();

  	// This is needed in order to show only one calendar at the time
  	if (calendar_id == 'calendar1') {
    	$('#calendar2').hide();
  	} else {
  		$('#calendar1').hide();
  	}
  }

  function chooseSwapShift(shift_event, calendar_id) {
  	var start = $.fullCalendar.formatDate(shift_event.start,'HH:mm');
    var end = $.fullCalendar.formatDate(shift_event.end,'HH:mm');
    var date = shift_event._start.format('DD-MM-YYYY');
    var title = shift_event.title + " " + date + " <br>" + start + "-" + end ;

    var btn_id = calendar_id+'_btn'

  	$(btn_id).val(shift_event._id);
  	$(btn_id).html(title);
  	$(btn_id).css('background-color', shift_event.color);
  }

  return {
    sendDeletionParameters: sendDeletionParameters,
    createEvent: createEvent,
    updateEvent: updateEvent,
    deleteEvent: deleteEvent,
    showCalendar: showCalendar,
    chooseSwapShift: chooseSwapShift,
  };
}();