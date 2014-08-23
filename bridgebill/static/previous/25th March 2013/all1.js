// Start - Highlight current menu item
$(document).ready(function(){
    loc = $(location).attr('href');
    $('li a').each(function(){
        var menu_url = "^" + this.href;
        if (loc.match(menu_url)) {
            $(this).parent().addClass('currentLink');
        };
    });
});
// End - Highlight current menu item

// Start - Validation on User Signup page 
$(document).ready(function(){
    $('#user_signup_form_minjs').validate({
        errorClass: 'error',
        success: function(label) {
            label.html('&nbsp;').addClass('valid')
        },
        rules: {
            firstname: {
                required: true,
                minlength: 2,
            },
            username: {
                required: true,
                minlength: 7,
                email: true, 
            },
            password1: {
                required: true,
            },
            password2: {
                required: true,
                equalTo: '#id_password1',
            },
        },
        messages: {
            firstname: {
                required: '&nbsp;',
                minlength: '&nbsp;',
            },
            username: {
                required: '&nbsp;',
                minlength: '&nbsp;',
                email: '&nbsp;',
            },
            password1: {
                required: '&nbsp;',
            },
            password2: {
                required: '&nbsp;',
                equalTo: '&nbsp;',
            },
        },
    });
});
// End - Validation on User Signup page 

// Start - To stop the submission of any errors or blank fields on User Signup page 
$(document).ready(function(){
    $('form#user_signup_form_minjs li.last button#save').click(function(){
        if ($('form#user_signup_form_minjs').validate().form() === false) {
            event.preventDefault();
        };
    });
});
// End - To stop the submission of any errors or blank fields on User Signup page 

// Start - Table sorting functionality
var MonthNumber = {};

MonthNumber["Jan "] = "01";
MonthNumber["Feb "] = "02";
MonthNumber["Mar "] = "03";
MonthNumber["Apr "] = "04";
MonthNumber["May "] = "05";
MonthNumber["Jun "] = "06";
MonthNumber["Jul "] = "07";
MonthNumber["Aug "] = "08";
MonthNumber["Sep "] = "09";
MonthNumber["Oct "] = "10";
MonthNumber["Nov "] = "11";
MonthNumber["Dec "] = "12";

$.tablesorter.addParser({
    id: 'dateDjango',
    is: function(s) {
        return false;
    },
    format: function(s) {
        if (s.length > 0) {
            var date = s.match(/^(\d{1,2}[sndrth]{2} )?(\w{3} )?(\d{4})$/);
            var d = '01';
            if (date[1]) {
                d = '' + parseInt(String(date[1]));
                if (d.length == 1) {
                    d = "0" + d;
                }
            }

            var m = '01';
            if (date[2]) {
                m = MonthNumber[date[2]];
            }

            var y = date[3];
            return '' + y + m + d;
        }
        else {
            return '';
        }
    },
    type: 'numeric'
});

$.tablesorter.addParser({
    id: 'amountDjango',
    is: function(s) {
        return false;
    },
    format: function(s) {
        if (s.length > 0) {
            var amount = s.slice(3);
            amount = amount.replace(/\,/g,'');
            return '' + amount;
        }
        else {
            return '';
        }
    },
    type: 'numeric'
});

$(document).ready(function(){
    $('table#who_owes_me_table').tablesorter({
        headers: { 0: { sorter: "dateDjango" }, 3: { sorter: "amountDjango" } }
    });
    $('table#who_i_owe_table').tablesorter({
        headers: { 0: { sorter: "dateDjango" }, 3: { sorter: "amountDjango" } }
    });
    $('table#transaction_history_table').tablesorter({
        headers: { 2: { sorter: "dateDjango" }, 4: { sorter: "amountDjango" } }
    });
    $('table#record_payment_table').tablesorter({
        headers: { 0: { sorter: false }, 1: { sorter: "dateDjango" }, 3: { sorter: "amountDjango" } }
    });
    $('table#payment_success_table').tablesorter({
        headers: { 0: { sorter: "dateDjango" }, 2: { sorter: "amountDjango" }, 4: { sorter: false } }
    });
});
// End - Table sorting functionality

// Start - Form validation for Equal Split page 
$(document).ready(function(){
    $('form#equal_split').validate({
        errorClass: 'error',
        errorElement: 'span',
        validClass: 'valid',
        rules: {
            date: {
                required: true,
                //date: true,
            },
            description: {
                required: true,
                minlength: 2,
            },
            amount: {
                required: true,
                minlength: 1,
                number: true,
            },
        },
        messages: {
            date: {
                required: '&nbsp',
                //date: '&nbsp',
            },
            description: {
                required: '&nbsp;',
                minlength: '&nbsp;',
            },
            amount: {
                required: '&nbsp;',
                minlength: '&nbsp;',
                number: '&nbsp',
            },
        },
    });
});
// End - Form validation for Equal Split page 

// Start - Add more friends or people on Equal Split page 
var i=0;
$(document).ready(function(){
    $('form#equal_split button.add_friend').click(function(){
        var html_fragment_1 = '<li><input type="checkbox" checked="checked"' + 'name="people_new" class="people_new" value="people_new_' + i + '" />';
        var html_fragment_2 = '<input class="dynamic_add_in name_new" type="text" id="id_name_' + i + '" name="name_' + i + '" placeholder="Friend\'s Name" />';
        var html_fragment_3 = '<input class="dynamic_add_in email_new" type="text" id="id_email_'+ i + '" name="email_' + i + '" placeholder="Friend\'s Email Address" />';
        var html_fragment_4 = '<input class="remove_friend" type="submit" value="&#10006;" /></li>';
        var html_fragment = html_fragment_1 + html_fragment_2 + html_fragment_3 + html_fragment_4;
        //var html_fragment = html_fragment_1 + html_fragment_2 + html_fragment_3;
        $('form#equal_split ul.people li:last').after(html_fragment);
        i++;
        return false;
    });
});

$(document).ready(function(){
    $('form#equal_split ul.people').on('click', 'input.remove_friend', function(){
        $(this).parent().remove();
        return false;
    });
});
// End - Add more friends or people on Equal Split page 

// Start - To validate new name fields added on Equal Split page 
$(document).ready(function(){
    $('form#equal_split').on({
        change: validate_name_equal_split,
    },('input[id*=id_name_]')
    );
});

function validate_name_equal_split(){
    $('form#equal_split input[id*=id_name_]').each(function() {
        $(this).rules("add", {
            required: true,
            minlength: 2,
            messages: {
                required: '&nbsp',
                minlength: '&nbsp',
            },
        });
    });
};
// End - To validate new name fields added on Equal Split page 

// Start - To validate new email fields added on Equal Split page 
$(document).ready(function(){
    $('form#equal_split').on({
        change: validate_email_equal_split,
    },('input[id*=id_email_]')
    );
});

function validate_email_equal_split(){
    $('form#equal_split input[id*=id_email_]').each(function() {
        $(this).rules("add", {
            required: true,
            email: true,
            minlength: 7,
            messages: {
                email: '&nbsp',
                required: '&nbsp',
                minlength: '&nbsp',
            },
        });
    });
};
// End - To validate new email fields added on Equal Split page 

// Start - To stop the submission of any unchecked new friend name and email fields added on Equal Split page 
$(document).ready(function(){
    $('form#equal_split').on('click', ('li.last button#save'), validate_equal_split_save);
});

function validate_equal_split_save(event){
    var input_checked_counter = 0;
    $('form#equal_split input[name*=people]').each(function(){
        if ($(this).is(":checked")) {
            input_checked_counter++;
        };
    });
    if (input_checked_counter === 0) {
        $('span.friend_checked').css("visibility", "visible");
        event.preventDefault();
    }
    else {
        $('span.friend_checked').css("visibility", "hidden");
    };

    $('form#equal_split input[class="people_new"]').each(function(){
        if ($(this).is(":checked")) {
            if ($(this).nextAll('input[id*=id_name_]').val().length === 0) {
                $(this).nextAll('input[id*=id_name_]').addClass('error_2');
                event.preventDefault();
            };
            if ($(this).nextAll('input[id*=id_email_]').val().length === 0) {
                $(this).nextAll('input[id*=id_email_]').addClass('error_2');
                event.preventDefault();
            };
        };
    });

    if ($('form#equal_split').validate().form() === false) {
        event.preventDefault();
    };
};
// End - To stop the submission of any unchecked new friend name and email fields added on Equal Split page 

// Start - Form validation for Un-Equal Split page 
$(document).ready(function(){
    $('form#unequal_split').validate({
        errorClass: 'error',
        errorElement: 'span',
        validClass: 'valid',
        rules: {
            date: {
                required: true,
                //date: true,
            },
            description: {
                required: true,
                minlength: 2,
            },
            amount: {
                required: true,
                minlength: 1,
                number: true,
            },
            total_people: {
                required: true,
                digits: true,
            },
        },
        messages: {
            date: {
                required: '&nbsp',
                //date: '&nbsp',
            },
            description: {
                required: '&nbsp;',
                minlength: '&nbsp;',
            },
            amount: {
                required: '&nbsp;',
                minlength: '&nbsp;',
                number: '&nbsp',
            },
            total_people: {
                required: '&nbsp;',
                digits: '&nbsp;',
            },
        },
    });
});
// End - Form validation for Un-Equal Split page 

// Start - To calculate amount depending on user input
// For Firefox
/*$(document).ready(function(){*/
    //$('form#unequal_split').on('click', 'select[id*=id_number_of_people] option', function(event){
        //var total_amount = Number($('form#unequal_split input#id_amount').val()) 
        //var total_people = Number($('form#unequal_split input#id_total_people').val());
        //if (($(this).val() !== 'Other') && (total_amount !== 0) && (total_people !== 0)) {
            //var borrower_amount = total_amount/total_people * Number($(this).val());
            //borrower_amount = Math.round(borrower_amount*100)/100;
            //$(this).parent().parent().parent().find('input[id*=id_borrower_amount]').val(borrower_amount);
        //}
        //else {
            //$(this).parent().parent().parent().find('input[id*=id_borrower_amount]').val('');
        //};
    //});
/*});*/

// For Chrome 
$(document).ready(function(){
    $('form#unequal_split').on('change', 'select[id*=id_number_of_people]', function(event){
        var total_amount = Number($('form#unequal_split input#id_amount').val()) 
        var total_people = Number($('form#unequal_split input#id_total_people').val());
        if (($(this).val() !== 'Other') && (total_amount !== 0) && (total_people !== 0)) {
            var borrower_amount = total_amount/total_people * Number($(this).val());
            borrower_amount = Math.round(borrower_amount*100)/100;
            $(this).parent().parent().find('input[id*=id_borrower_amount]').val(borrower_amount);
        }
        else {
            $(this).parent().parent().find('input[id*=id_borrower_amount]').val('');
        };
    });
});
// End - To calculate amount depending on user input

// Start - Add more friends or people on Un-Equal Split page 
var i=0;
$(document).ready(function(){
    $('form#unequal_split button.add_friend').click(function(){
        var html_fragment_1 = '<tr><td class="name"><input type="hidden" name="people_new" class="people_new" value="x_people_new_' + i + '" />';
        var html_fragment_2 = '<input class="dynamic_add_in" type="text" id="x_id_name_' + i + '" name="x_name_' + i + '" placeholder="Friend\'s Name" />';
        var html_fragment_3 = '<input class="dynamic_add_in" type="text" id="x_id_email_'+ i + '" name="x_email_' + i + '" placeholder="Friend\'s Email Address" /></td>';
        var html_fragment_4 = '<td class="number"><select id="x_id_number_of_people_' + i + '" name="x_number_of_people_' + i + '"><option value="" selected="selected"></option><option value="1">1 person</option><option value="2">2 people</option><option value="3">3 people</option><option value="4">4 people</option><option value="5">5 people</option><option value="Other">Other</option></select></td>'
        var html_fragment_5 = '<td class="amount"><input type="text" id="x_id_borrower_amount_' + i + '" name="x_borrower_amount_' + i + '" /></td>';
        var html_fragment_6 = '<td class="remove_table_row"><input class="remove_friend" type="submit" value="&#10006;" /></td></tr>';
        var html_fragment = html_fragment_1 + html_fragment_2 + html_fragment_3 + html_fragment_4 + html_fragment_5 + html_fragment_6;
        $('form#unequal_split table#unequal_split_people_table tbody tr:last').after(html_fragment);
        i++;
        return false;
    });
});

$(document).ready(function(){
    $('form#unequal_split table#unequal_split_people_table').on('click', 'input.remove_friend', function(){
        $(this).parent().parent().remove();
        return false;
    });
});
// End - Add more friends or people on Un-Equal Split page 

// Start - To validate amount fields for existing friends on Un-Equal Split page 
$(document).ready(function(){
    $('form#unequal_split').on({
        change: validate_amount_existing_unequal_split,
    },('input[id^=id_borrower_amount_]')
    );
});

function validate_amount_existing_unequal_split(){
    $('form#unequal_split input[id^=id_borrower_amount_]').each(function() {
        $(this).rules("add", {
            required: false,
            minlength: 1,
            number: true,
            messages: {
                required: '&nbsp',
                minlength: '&nbsp',
                number: '&nbsp',
            },
        });
    });
};
// End - To validate amount fields for existing friends on Un-Equal Split page 

// Start - To validate new name, email and amount fields added on Un-Equal Split page 
$(document).ready(function(){
    $('form#unequal_split').on({
        change: validate_unequal_split_new,
    },('input[id^=x_id_name_]')
    );
});

$(document).ready(function(){
    $('form#unequal_split').on({
        change: validate_unequal_split_new,
    },('input[id^=x_id_email_]')
    );
});

$(document).ready(function(){
    $('form#unequal_split').on({
        change: validate_unequal_split_new,
    },('input[id^=x_id_borrower_amount_]')
    );
});

function validate_unequal_split_new(){
    $('form#unequal_split input[id^=x_id_name_]').each(function() {
        $(this).rules("add", {
            required: true,
            minlength: 2,
            messages: {
                required: '&nbsp',
                minlength: '&nbsp',
            },
        });
    });
    $('form#unequal_split input[id^=x_id_email_]').each(function() {
        $(this).rules("add", {
            required: true,
            email: true,
            minlength: 7,
            messages: {
                email: '&nbsp',
                required: '&nbsp',
                minlength: '&nbsp',
            },
        });
    });
    $('form#unequal_split input[id^=x_id_borrower_amount_]').each(function() {
        $(this).rules("add", {
            required: true,
            minlength: 1,
            number: true,
            messages: {
                required: '&nbsp',
                minlength: '&nbsp',
                number: '&nbsp',
            },
        });
    });
};
// End - To validate new name, email and amount fields added on Un-Equal Split page 

// Start - To stop the submission of any unchecked new friend name and email fields added on Un-Equal Split page 
$(document).ready(function(){
    $('form#unequal_split').on('click', ('li.last button#save'), validate_unequal_split_save);
});

function validate_unequal_split_save(event){
    var input_checked_counter = 0;
    $('form#unequal_split input[class=people]').each(function(){
        if ($(this).nextAll('select[id^=id_borrower]').val().length !== 0) {
            input_checked_counter++;
        };
    });
    $('form#unequal_split input[class=people_new]').each(function(){
        if ($(this).nextAll('input[id^=x_id_name]').val().length !== 0) {
            input_checked_counter++;
        };
    });
    if (input_checked_counter === 0) {
        $('span.friend_checked').css("visibility", "visible");
        event.preventDefault();
    }
    else {
        $('span.friend_checked').css("visibility", "hidden");
    };


    if ($('form#unequal_split').validate().form() === false) {
        event.preventDefault();
        return false;
    }
    else {
        var value = true;
        $('form#unequal_split input[class=people]').each(function(){
            if (($(this).nextAll('select[id^=id_borrower]').val().length === 0) && ($(this).parent().parent().find('select[id^=id_number_of_people]').val() === '') && ($(this).parent().parent().find('input[id^=id_borrower_amount]').val().length !== 0)) {
                event.preventDefault();
                $(this).nextAll('select[id^=id_borrower]').addClass('error_2');
                $(this).parent().parent().find('select[id^=id_number_of_people]').addClass('error_2');
                value = false;
            };
            if (($(this).nextAll('select[id^=id_borrower]').val().length === 0) && ($(this).parent().parent().find('select[id^=id_number_of_people]').val() !== '') && ($(this).parent().parent().find('input[id^=id_borrower_amount]').val().length === 0)) {
                event.preventDefault();
                $(this).nextAll('select[id^=id_borrower]').addClass('error_2');
                $(this).parent().parent().find('input[id^=id_borrower_amount]').addClass('error_2');
                value = false;
            };
            if (($(this).nextAll('select[id^=id_borrower]').val().length === 0) && ($(this).parent().parent().find('select[id^=id_number_of_people]').val() !== '') && ($(this).parent().parent().find('input[id^=id_borrower_amount]').val().length !== 0)) {
                event.preventDefault();
                $(this).nextAll('select[id^=id_borrower]').addClass('error_2');
                value = false;
            };
            if (($(this).nextAll('select[id^=id_borrower]').val().length !== 0) && ($(this).parent().parent().find('select[id^=id_number_of_people]').val() === '') && ($(this).parent().parent().find('input[id^=id_borrower_amount]').val().length === 0)) {
                event.preventDefault();
                $(this).parent().parent().find('select[id^=id_number_of_people]').addClass('error_2');
                $(this).parent().parent().find('input[id^=id_borrower_amount]').addClass('error_2');
                value = false;
            };
            if (($(this).nextAll('select[id^=id_borrower]').val().length !== 0) && ($(this).parent().parent().find('select[id^=id_number_of_people]').val() === '') && ($(this).parent().parent().find('input[id^=id_borrower_amount]').val().length !== 0)) {
                event.preventDefault();
                $(this).parent().parent().find('select[id^=id_number_of_people]').addClass('error_2');
                value = false;
            };
            if (($(this).nextAll('select[id^=id_borrower]').val().length !== 0) && ($(this).parent().parent().find('select[id^=id_number_of_people]').val() !== '') && ($(this).parent().parent().find('input[id^=id_borrower_amount]').val().length === 0)) {
                event.preventDefault();
                $(this).parent().parent().find('input[id^=id_borrower_amount]').addClass('error_2');
                value = false;
            };
        });

        $('form#unequal_split input[class=people_new]').each(function(){
            if (($(this).nextAll('input[id^=x_id_name]').val().length === 0) && ($(this).nextAll('input[id^=x_id_email]').val().length === 0) && ($(this).parent().parent().find('select[id^=x_id_number_of_people]').val() === '') && ($(this).parent().parent().find('input[id^=x_id_borrower_amount]').val().length !== 0)) {
                event.preventDefault();
                $(this).nextAll('input[id^=x_id_name]').addClass('error_2');
                $(this).nextAll('input[id^=x_id_email]').addClass('error_2');
                $(this).parent().parent().find('select[id^=x_id_number_of_people]').addClass('error_2');
                value = false;
            };
            if (($(this).nextAll('input[id^=x_id_name]').val().length === 0) && ($(this).nextAll('input[id^=x_id_email]').val().length === 0) && ($(this).parent().parent().find('select[id^=x_id_number_of_people]').val() !== '') && ($(this).parent().parent().find('input[id^=x_id_borrower_amount]').val().length === 0)) {
                event.preventDefault();
                $(this).nextAll('input[id^=x_id_name]').addClass('error_2');
                $(this).nextAll('input[id^=x_id_email]').addClass('error_2');
                $(this).parent().parent().find('input[id^=x_id_borrower_amount]').addClass('error_2');
                value = false;
            };
            if (($(this).nextAll('input[id^=x_id_name]').val().length === 0) && ($(this).nextAll('input[id^=x_id_email]').val().length === 0) && ($(this).parent().parent().find('select[id^=x_id_number_of_people]').val() !== '') && ($(this).parent().parent().find('input[id^=x_id_borrower_amount]').val().length !== 0)) {
                event.preventDefault();
                $(this).nextAll('input[id^=x_id_name]').addClass('error_2');
                $(this).nextAll('input[id^=x_id_email]').addClass('error_2');
                value = false;
            };
            if (($(this).nextAll('input[id^=x_id_name]').val().length === 0) && ($(this).nextAll('input[id^=x_id_email]').val().length !== 0) && ($(this).parent().parent().find('select[id^=x_id_number_of_people]').val() === '') && ($(this).parent().parent().find('input[id^=x_id_borrower_amount]').val().length === 0)) {
                event.preventDefault();
                $(this).nextAll('input[id^=x_id_name]').addClass('error_2');
                $(this).parent().parent().find('select[id^=x_id_number_of_people]').addClass('error_2');
                $(this).parent().parent().find('input[id^=x_id_borrower_amount]').addClass('error_2');
                value = false;
            };
            if (($(this).nextAll('input[id^=x_id_name]').val().length === 0) && ($(this).nextAll('input[id^=x_id_email]').val().length !== 0) && ($(this).parent().parent().find('select[id^=x_id_number_of_people]').val() === '') && ($(this).parent().parent().find('input[id^=x_id_borrower_amount]').val().length !== 0)) {
                event.preventDefault();
                $(this).nextAll('input[id^=x_id_name]').addClass('error_2');
                $(this).parent().parent().find('select[id^=x_id_number_of_people]').addClass('error_2');
                value = false;
            };
            if (($(this).nextAll('input[id^=x_id_name]').val().length === 0) && ($(this).nextAll('input[id^=x_id_email]').val().length !== 0) && ($(this).parent().parent().find('select[id^=x_id_number_of_people]').val() !== '') && ($(this).parent().parent().find('input[id^=x_id_borrower_amount]').val().length === 0)) {
                event.preventDefault();
                $(this).nextAll('input[id^=x_id_name]').addClass('error_2');
                $(this).parent().parent().find('input[id^=x_id_borrower_amount]').addClass('error_2');
                value = false;
            };
            if (($(this).nextAll('input[id^=x_id_name]').val().length === 0) && ($(this).nextAll('input[id^=x_id_email]').val().length !== 0) && ($(this).parent().parent().find('select[id^=x_id_number_of_people]').val() !== '') && ($(this).parent().parent().find('input[id^=x_id_borrower_amount]').val().length !== 0)) {
                event.preventDefault();
                $(this).nextAll('input[id^=x_id_name]').addClass('error_2');
                value = false;
            };
            if (($(this).nextAll('input[id^=x_id_name]').val().length !== 0) && ($(this).nextAll('input[id^=x_id_email]').val().length === 0) && ($(this).parent().parent().find('select[id^=x_id_number_of_people]').val() === '') && ($(this).parent().parent().find('input[id^=x_id_borrower_amount]').val().length === 0)) {
                event.preventDefault();
                $(this).nextAll('input[id^=x_id_email]').addClass('error_2');
                $(this).parent().parent().find('select[id^=x_id_number_of_people]').addClass('error_2');
                $(this).parent().parent().find('input[id^=x_id_borrower_amount]').addClass('error_2');
                value = false;
            };
            if (($(this).nextAll('input[id^=x_id_name]').val().length !== 0) && ($(this).nextAll('input[id^=x_id_email]').val().length === 0) && ($(this).parent().parent().find('select[id^=x_id_number_of_people]').val() === '') && ($(this).parent().parent().find('input[id^=x_id_borrower_amount]').val().length !== 0)) {
                event.preventDefault();
                $(this).nextAll('input[id^=x_id_email]').addClass('error_2');
                $(this).parent().parent().find('select[id^=x_id_number_of_people]').addClass('error_2');
                value = false;
            };
            if (($(this).nextAll('input[id^=x_id_name]').val().length !== 0) && ($(this).nextAll('input[id^=x_id_email]').val().length === 0) && ($(this).parent().parent().find('select[id^=x_id_number_of_people]').val() !== '') && ($(this).parent().parent().find('input[id^=x_id_borrower_amount]').val().length === 0)) {
                event.preventDefault();
                $(this).nextAll('input[id^=x_id_email]').addClass('error_2');
                $(this).parent().parent().find('input[id^=x_id_borrower_amount]').addClass('error_2');
                value = false;
            };
            if (($(this).nextAll('input[id^=x_id_name]').val().length !== 0) && ($(this).nextAll('input[id^=x_id_email]').val().length === 0) && ($(this).parent().parent().find('select[id^=x_id_number_of_people]').val() !== '') && ($(this).parent().parent().find('input[id^=x_id_borrower_amount]').val().length !== 0)) {
                event.preventDefault();
                $(this).nextAll('input[id^=x_id_email]').addClass('error_2');
                value = false;
            };
            if (($(this).nextAll('input[id^=x_id_name]').val().length !== 0) && ($(this).nextAll('input[id^=x_id_email]').val().length !== 0) && ($(this).parent().parent().find('select[id^=x_id_number_of_people]').val() === '') && ($(this).parent().parent().find('input[id^=x_id_borrower_amount]').val().length === 0)) {
                event.preventDefault();
                $(this).parent().parent().find('select[id^=x_id_number_of_people]').addClass('error_2');
                $(this).parent().parent().find('input[id^=x_id_borrower_amount]').addClass('error_2');
                value = false;
            };
            if (($(this).nextAll('input[id^=x_id_name]').val().length !== 0) && ($(this).nextAll('input[id^=x_id_email]').val().length !== 0) && ($(this).parent().parent().find('select[id^=x_id_number_of_people]').val() === '') && ($(this).parent().parent().find('input[id^=x_id_borrower_amount]').val().length !== 0)) {
                event.preventDefault();
                $(this).parent().parent().find('select[id^=x_id_number_of_people]').addClass('error_2');
                value = false;
            };
            if (($(this).nextAll('input[id^=x_id_name]').val().length !== 0) && ($(this).nextAll('input[id^=x_id_email]').val().length !== 0) && ($(this).parent().parent().find('select[id^=x_id_number_of_people]').val() !== '') && ($(this).parent().parent().find('input[id^=x_id_borrower_amount]').val().length === 0)) {
                event.preventDefault();
                $(this).parent().parent().find('input[id^=x_id_borrower_amount]').addClass('error_2');
                value = false;
            };
         });
         return value;
    };
};
// End - To stop the submission of any unchecked new friend name and email fields added on Un-Equal Split page 

// Start - Date Plugin
$(document).ready(function(){
    $('li input#id_date').datepicker({ dateFormat: "dd/mm/yy", altField: "#id_xdate", altFormat: "dd-mm-yy" });
});
// End - Date Plugin

// Start - Validation on Settle Payment page
$(document).ready(function(){
    $('#record_payment').validate({
        errorClass: 'error',
        errorElement: 'span',
        validClass: 'valid',
        rules: {
            date: {
                required: true,
                //date: true,
            },
        },
        messages: {
            date: {
                required: '&nbsp;',
                //date: '&nbsp;',
            },
        },
    });
});
// End - Validation on Settle Payment page

// Start - Table row select on Record Payment page
$(document).ready(function(){
    $('table#record_payment_table tbody tr')
    .filter(':has(:checkbox:checked)')
    .addClass('highlight')
    .end()
    .click(function(event){
        $(this).toggleClass('highlight');
        if (event.target.type !== 'checkbox') {
            if ($(':checkbox', this).is(':checked')) {
                $(':checkbox', this).attr('checked', false);
            }
            else {
                $(':checkbox', this).attr('checked', true);
            };
        };
    });
});

$(document).ready(function(){
    $('table#record_payment_table thead tr th.check_bill input:checkbox').click(function(){
        if ($(this).is(':checked')) {
            $('table#record_payment_table tbody tr input:checkbox').attr('checked', true);
            $('table#record_payment_table tbody tr').addClass('highlight');
        }
        else {
            $('table#record_payment_table tbody tr input:checkbox').attr('checked', false);
            $('table#record_payment_table tbody tr').removeClass('highlight');
        };
    });
});
// End - Table row select on Record Payment page

// Start - Settle Payment - Stop submit if no rows are selected
$(document).ready(function(){
    $('form#record_payment li.last button#save').click(function(event){
        var temp = 'false';
        $('form#record_payment tbody tr input:checkbox').each(function(){
            if ($(this).is(':checked')) {
                temp = 'true';
            };
        });
        if (temp === 'false') {
            event.preventDefault();
            $('span.bills_checked').css("visibility", "visible");
        };
    });
});
// End - Settle Payment - Stop submit if no rows are selected

// Start - Validation on My Profile page 
$(document).ready(function(){
    $('#my_profile').validate({
        errorClass: 'error',
        rules: {
            first_name: {
                required: true,
                minlength: 2,
            },
            email: {
                required: true,
                minlength: 7,
                email: true, 
            },
        },
        messages: {
            first_name: {
                required: '&nbsp;',
                minlength: '&nbsp;',
            },
            email: {
                required: '&nbsp;',
                minlength: '&nbsp;',
                email: '&nbsp;',
            },
        },
    });
});
// End - Validation on My Profile page 

// Start - To stop the submission of any errors or blank fields on My Profile page 
$(document).ready(function(){
    $('form#my_profile li.last button#save').click(function(){
        if ($('form#my_profile').validate().form() === false) {
            event.preventDefault();
        };
    });
});
// End - To stop the submission of any errors or blank fields on My Profile page 

// Start - For getting Django CSRF variable in AJAX requests
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
// End - For getting Django CSRF variable in AJAX requests

// Start - Show Edit button only on hover on My Friends page
$(document).ready(function(){
    $('ul#my_friends').on({
        mouseenter: function(){
            $(this).children('span.last').show();
        },
        mouseleave: function(){
            $(this).children('span.last').hide();
        }
    }, 'li');
});
// End - Show Edit button only on hover on My Friends page

// Start - Edit friend details on My Friends page
var j = 0
$(document).ready(function(){
    $('ul#my_friends').on({
        click: function(){
            var html_fragment_1 = '<span class="mock_border"><input class="dynamic_add_in name_new" type="text" id="id_name_' + i + '" name="name_' + j + '" placeholder="Friend\'s Name" value="' + $(this).parent().prevAll('span.mock_border').children('span.name').text() + '" />';
            var html_fragment_2 = '<input class="dynamic_add_in email_new" type="text" id="id_email_'+ j + '" name="email_' + j + '" placeholder="Friend\'s Email Address" value="' + $(this).parent().prevAll('span.mock_border').children('span.email').text() + '" /></span>';
            var html_fragment_3 = '<span class="dynamic_add_in last_new save"><button class="save_friend_1"' + ' value="' + $(this).val() + '">Save</button></span>';
            var html_fragment_4 = '<span class="dynamic_add_in last_new cancel"><button class="cancel_friend_1"' + ' value="' + $(this).val() + '">Cancel</button></span>';
            var html_fragment_5 = '<span class="ajax_loading"><img src="/static/images/ajax-loader.gif" alt="Processing" /></span>';
            var html_fragment = '\n' + html_fragment_1 + '\n' + html_fragment_2 + '\n' + html_fragment_3 + '\n' + html_fragment_4 + '\n' + html_fragment_5 + '\n';
            $(this).parent().parent().html(html_fragment);
            j++;
        }
    },'li button.edit_friend');
});
// End - Edit friend details on My Friends page

// Start - Add friend on My Friends page
var k = 0;
$(document).ready(function(){
    $('ul.my_friends.add_remove_button button.add_friend').click(function(){
        var html_fragment_1 = '<li><span class="mock_border"><input class="dynamic_add_in name_new" type="text" id="id_name_' + k + '" name="name_' + k + '" placeholder="Friend\'s Name" />';
        var html_fragment_2 = '<input class="dynamic_add_in email_new" type="text" id="id_email_'+ k + '" name="email_' + k + '" placeholder="Friend\'s Email Address" /></span>';
        var html_fragment_3 = '<span class="dynamic_add_in last_new save"><button class="save_friend_2">Save</button></span>';
        var html_fragment_4 = '<span class="dynamic_add_in last_new cancel"><button class="cancel_friend_2">Cancel</button></span>';
        var html_fragment_5 = '<span class="ajax_loading"><img src="/static/images/ajax-loader.gif" alt="Processing" /></span></li>';
        var html_fragment = '\n' + html_fragment_1 + '\n' + html_fragment_2 + '\n' + html_fragment_3 + '\n' + html_fragment_4 + '\n' + html_fragment_5 + '\n';
        $('ul#my_friends li:last').after(html_fragment);
        k++;
        return false;
    });
});
// End - Add friend on My Friends page

// Start - Save a friend after having clicked on Edit on My Friends page
$(document).ready(function(){
    $('ul#my_friends').on('click', 'button.save_friend_1', function(){
        $(this).parent().hide();
        $(this).parent().nextAll('span.last_new').hide();
        $(this).parent().nextAll('span.error_django').hide();
        $(this).parent().nextAll('span.ajax_loading').show();
        $.ajax({
            type: 'POST',
            url: '/my-profile/my-friends/edit-friend/' + $(this).val()+ '/', 
            context: this,
            data: { 'friend_name': $(this).parent().prevAll('span.mock_border').children('input[id*=id_name]').val(), 'friend_email': $(this).parent().prevAll('span.mock_border').children('input[id*=id_email]').val() },
            datatype: 'json',
            success: function(result) {
                if (result.error_message) {
                    if ($(this).parent().nextAll('span.error_django')) {
                        $(this).parent().nextAll('span.error_django').remove();
                    }
                    $(this).parent().show();
                    $(this).parent().nextAll('span.last_new').show();
                    $(this).parent().nextAll('span.ajax_loading').hide();
                    var html_fragment = '<span class="error_django">' + result.error_message + '</span>';
                    $(this).parent().parent().append(html_fragment);
                }
                else {
                    var html_fragment_1 = '<span class="mock_border"><span class="name">' + result.friend_name + '</span>';
                    var html_fragment_2 = '<span class="email">' + result.friend_email + '</span></span>';
                    var html_fragment_3 = '<span style="display: none;" class="last edit"><button class="edit_friend" value="' + result.userfriend_id + '">Edit</button></span>';
                    var html_fragment_4 = '<span style="display: none;" class="last delete"><button class="delete_friend" value="' + result.userfriend_id + '">Delete</button></span>';
                    var html_fragment_5 = '<span class="ajax_loading"><img src="/static/images/ajax-loader.gif" alt="Processing" /></span>';
                    var html_fragment = '\n' + html_fragment_1 + '\n' + html_fragment_2 + '\n' + html_fragment_3 + '\n' + html_fragment_4 + '\n' + html_fragment_5 + '\n';
                    $(this).parent().parent().html(html_fragment);
                }
            },
            error: function() {
                alert("Oops..something went wrong!");
            }
        });
        return false;
    });
});
// End - Save a friend after having clicked on Edit on My Friends page

// Start - Cancel a friend after having clicked on Edit on My Friends page
$(document).ready(function(){
    $('ul#my_friends').on('click', 'button.cancel_friend_1', function(){
        $(this).parent().hide();
        $(this).parent().prevAll('span.last_new').hide();
        $(this).parent().nextAll('span.error_django').hide();
        $(this).parent().nextAll('span.ajax_loading').show();
        $.ajax({
            type: 'GET',
            url: '/my-profile/my-friends/edit-friend/' + $(this).val() + '/',
            context: this,
            datatype: 'json',
            success: function(result) {
                var html_fragment_1 = '<span class="mock_border"><span class="name">' + result.friend_name + '</span>';
                var html_fragment_2 = '<span class="email">' + result.friend_email + '</span></span>';
                var html_fragment_3 = '<span style="display: none;" class="last"><button class="edit_friend" value="' + result.userfriend_id + '">Edit</button></span>';
                var html_fragment_4 = '<span style="display: none;" class="last delete"><button class="delete_friend" value="' + result.userfriend_id + '">Delete</button></span>';
                var html_fragment_5 = '<span class="ajax_loading"><img src="/static/images/ajax-loader.gif" alt="Processing" /></span>';
                var html_fragment = '\n' + html_fragment_1 + '\n' + html_fragment_2 + '\n' + html_fragment_3 + '\n' + html_fragment_4 + '\n' + html_fragment_5 + '\n';
                $(this).parent().parent().html(html_fragment);
            },
            error: function() {
                alert("Oops..something went wrong!");
            }
        });
        return false;
    });
});
// End - Cancel a friend after having clicked on Edit on My Friends page

// Start - If user presses escape or enter on My Friends page
$(document).ready(function(){
    $('ul#my_friends').on('keyup', 'input', function(event){
        if (event.keyCode == 27) { // For Escape
            $(this).parent().nextAll().children('button[class*=cancel_friend]').click();
        }
        if (event.keyCode == 13) { // For Enter
            $(this).parent().nextAll().children('button[class*=save_friend]').click();
        }
        
    });
});
// End - If user presses escape or enter on My Friends page

// Start - Save a friend after having clicked on Add on My Friends page
$(document).ready(function(){
    $('ul#my_friends').on('click', 'button.save_friend_2', function(){
        $(this).parent().hide();
        $(this).parent().nextAll('span.last_new').hide();
        $(this).parent().nextAll('span.error_django').hide();
        $(this).parent().nextAll('span.ajax_loading').show();
        $.ajax({
            type: 'POST',
            url: '/my-profile/my-friends/add-friend/', 
            context: this,
            data: { 'friend_name': $(this).parent().prevAll('span.mock_border').children('input[id*=id_name]').val(), 'friend_email': $(this).parent().prevAll('span.mock_border').children('input[id*=id_email]').val() },
            datatype: 'json',
            success: function(result) {
                if (result.error_message) {
                    if ($(this).parent().nextAll('span.error_django')) {
                        $(this).parent().nextAll('span.error_django').remove();
                    }
                    $(this).parent().show();
                    $(this).parent().nextAll('span.last_new').show();
                    $(this).parent().nextAll('span.ajax_loading').hide();
                    var html_fragment = '<span class="error_django">' + result.error_message + '</span>';
                    $(this).parent().parent().append(html_fragment);
                }
                else {
                    var html_fragment_1 = '<span class="mock_border"><span class="name">' + result.friend_name + '</span>';
                    var html_fragment_2 = '<span class="email">' + result.friend_email + '</span></span>';
                    var html_fragment_3 = '<span style="display: none;" class="last"><button class="edit_friend" value="' + result.userfriend_id + '">Edit</button></span>';
                    var html_fragment_4 = '<span style="display: none;" class="last delete"><button class="delete_friend" value="' + result.userfriend_id + '">Delete</button></span>';
                    var html_fragment_5 = '<span class="ajax_loading"><img src="/static/images/ajax-loader.gif" alt="Processing" /></span>';
                    var html_fragment = '\n' + html_fragment_1 + '\n' + html_fragment_2 + '\n' + html_fragment_3 + '\n' + html_fragment_4 + '\n' + html_fragment_5 + '\n';
                    $(this).parent().parent().html(html_fragment);

                    if ($('ul#my_friends li').length > 1) {
                        $('ul#my_friends').prevAll('p.my_friends.default_message').hide();
                    }
                }
            },
            error: function() {
                alert("Oops..something went wrong!");
            }
        });
        return false;
    });
});
// End - Save a friend after having clicked on Add on My Friends page

// Start - Cancel a friend after having clicked on Add on My Friends page
$(document).ready(function(){
    $('ul#my_friends').on('click', 'button.cancel_friend_2', function(){
        $(this).parent().parent().remove();
        return false;
    });
});
// End - Cancel a friend after having clicked on Add on My Friends page

// Start - Delete user friend / mark user friend as deleted in UserFriend table
$(document).ready(function(){
    $('ul#my_friends').on('click', 'button.delete_friend', function(){
        $(this).parent().hide();
        $(this).parent().prevAll('span.last').hide();
        $(this).parent().nextAll('span.ajax_loading').show();
        $.ajax({
            type: 'POST',
            url: '/my-profile/my-friends/delete-friend/' + $(this).val() + '/', 
            context: this,
            data: { 'friend_email': $(this).val() },
            datatype: 'json',
            success: function(result) {
                $(this).parent().parent().remove();
                if ($('ul#my_friends li').length <= 1) {
                    $('ul#my_friends').prevAll('p.page_header').after('<p class="my_friends default_message">None yet. Click the button below to add your contacts.</p>');
                }
            },
            error: function() {
                alert("Oops..something went wrong!");
            }
        });
        return false;
    });
});
// End - Delete user friend / mark user friend as deleted in UserFriend table
