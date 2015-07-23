
$(document).ready(function() {
$('.date').datepicker();
});
var formErrors = {% if form_errors %}true{% else %}false{% endif %};

