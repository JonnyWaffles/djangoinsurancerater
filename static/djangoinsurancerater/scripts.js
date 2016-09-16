// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

function setGlobals(target, val) {
  
  var anyNonEmpty = false;
  target.each(function() {
    if($(this).val()){
      anyNonEmpty = true;         
    }
  });

  if (anyNonEmpty === true) {
    answer = confirm("Over write current limits or deductibles?");
    if (answer) {
      target.val(val).change();
    }      
  } 
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function fader(selectedquery) {
  selectedquery.each( function () {
    var $row = $(this).closest(".row");
    if ( $(this).val() === "0") {
      $row.fadeTo("fast", 0.2);
     } else {
       $row.fadeTo("fast", 1);
     }
    })
  }

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$( document ).ready(function () {
  
  $("#global-limit").change(function() { 
    setGlobals($(".limit input"), $(this).val());
    var prevalue = $(this).val()
    $(this).val(numberWithCommas(prevalue));
  });
  
  $("#global-deductible").change(function() { 
    setGlobals($(".deductible input"), $(this).val());
    var prevalue = $(this).val()
    $(this).val(numberWithCommas(prevalue))
  });
  
  $(".limit input, .deductible input").change(function() {
    var prevalue = $(this).val();
    $(this).val(numberWithCommas(prevalue));
    fader($(this));
    var $form = $(this).closest(".insuring-agreement-form");
    $.post($form.attr('action'), $form.serialize(), function(response) {
      var $currentpremiumdiv = $form.find(".premium")
      // Need to find the same form as $form in the response and then find the premium
      $currentpremiumdiv.html(response.premium)
    });
    //no post data error....
  });
  
  fader($(".limit input"));
  
  $(".glyphicon-remove").click( function() {
    var $form = $(this).closest(".insuring-agreement-form");
    $form.find(".limit input, .deductible input").val('0').change();
  });
                            
});
