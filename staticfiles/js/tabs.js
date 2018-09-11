if(window.location.pathname === "/teacher") {
	// Buttons
    var $home_button = $('#home-button');
    var $old_button = $('#old-button');
    var $outgoing_button = $('#outgoing-button');
    var $incoming_button = $('#incoming-button');
    var $unapproved_button = $('#unapproved-button');

    // Fragments
    var $home_fragment = $('#home-fragment');
    var $old_fragment = $('#old-fragment');
    var $outgoing_fragment = $('#outgoing-fragment');
    var $incoming_fragment = $('#incoming-fragment');
    var $unapproved_fragment = $('#unapproved-fragment');

    // Callbacks for buttons
    $home_button.click(switch_teacher_home());
	$old_button.click(switch_teacher_old());
	$outgoing_button.click(switch_teacher_outgoing());
	$incoming_button.click(switch_teacher_incoming());
	$unapproved_button.click(switch_teacher_unapproved());
}
else if(window.location.pathname === "/student") {
	// Buttons
    var $active_button = $('#active-button');
    var $pending_button = $('#pending-button');
    var $old_button = $('#old-button');

	// Fragments
	var $active_fragment = $('#active-fragment');
    var $pending_fragment = $('#pending-fragment');
    var $old_fragment = $('#old-fragment');

	// Callbacks for buttons
	$active_button.click(switch_student_active());
	$pending_button.click(switch_student_pending());
	$old_button.click(switch_student_old());
}

function activate(elem, frag) {
    frag.show();
    elem.removeClass('btn-secondary');
    elem.addClass('btn-primary');
}
function deactivate(elem, frag) {
    frag.hide();
    elem.addClass('btn-secondary');
    elem.removeClass('btn-primary');
}
// Teacher functions
function switch_teacher_home(){
	activate($home_button, $home_fragment);
    deactivate($old_button, $old_fragment);
    deactivate($outgoing_button, $outgoing_fragment);
    deactivate($incoming_button, $incoming_fragment);
    deactivate($unapproved_button, $unapproved_fragment);
}
function switch_teacher_unapproved(){
	deactivate($home_button, $home_fragment);
    deactivate($old_button, $old_fragment);
    deactivate($outgoing_button, $outgoing_fragment);
    deactivate($incoming_button, $incoming_fragment);
    activate($unapproved_button, $unapproved_fragment);
}
function switch_teacher_incoming(){
	deactivate($home_button, $home_fragment);
    deactivate($old_button, $old_fragment);
    deactivate($outgoing_button, $outgoing_fragment);
    activate($incoming_button, $incoming_fragment);
    deactivate($unapproved_button, $unapproved_fragment);
}
function switch_teacher_outgoing(){
	deactivate($home_button, $home_fragment);
    deactivate($old_button, $old_fragment);
    activate($outgoing_button, $outgoing_fragment);
    deactivate($incoming_button, $incoming_fragment);
    deactivate($unapproved_button, $unapproved_fragment);
}
function switch_teacher_old(){
	deactivate($home_button, $home_fragment);
    activate($old_button, $old_fragment);
    deactivate($outgoing_button, $outgoing_fragment);
    deactivate($incoming_button, $incoming_fragment);
    deactivate($unapproved_button, $unapproved_fragment);
}
// Student functions
function switch_student_home(){
    deactivate($active_button, $active_fragment);
    deactivate($pending_button, $pending_fragment);
    deactivate($old_button, $old_fragment);
    activate($home_button, $home_fragment);
}
function switch_student_active(){
    activate($active_button, $active_fragment);
    deactivate($pending_button, $pending_fragment);
    deactivate($old_button, $old_fragment);
	deactivate($home_button, $home_fragment);
}
function switch_student_pending(){
	deactivate($active_button, $active_fragment);
	activate($pending_button, $pending_fragment);
	deactivate($old_button, $old_fragment);
	deactivate($home_button, $home_fragment);
}
function switch_student_old(){
	deactivate($active_button, $active_fragment);
	deactivate($pending_button, $pending_fragment);
	activate($old_button, $old_fragment);
	deactivate($home_button, $home_fragment);
}


if(window.location.pathname === "/teacher"){
    if(window.location.hash === "unapproved"){
		switch_teacher_unapproved();
    }
    else if(window.location.hash === "incoming"){
		switch_teacher_incoming();
    }
    else if(window.location.hash === "outgoing"){
		switch_teacher_outgoing();
    }
    else if(window.location.hash === "old"){
		switch_teacher_old();
    }
    else if(window.location.hash === "home"){
    	switch_teacher_home();
    }
}
else if(window.location.pathname === "/student"){
    if(window.location.hash === "active"){
		switch_student_active();
    }
    else if(window.location.hash === "pending"){
		switch_student_pending();
    }
    else if(window.location.hash === "old"){
		switch_student_old();
    }
    else if(window.location.hash === "home"){
    	switch_student_home();
    }
}