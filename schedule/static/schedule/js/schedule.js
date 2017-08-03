if (typeof DS == 'undefined') { // T = django ticketing
  DS = {};
}

DS = function() {
  // Modal for deleting group
  function sendParametersGroup (title, link) {
    $("#group_title").html(title);
    $('#delete_group_submit').attr('onclick', "window.location.href='"+link+"'");
  }

  return {
    sendParametersGroup: sendParametersGroup,
  };
}();