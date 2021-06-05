$(document).ready(function(){

    // notification classes
    const notificationClasses = {
        "success" : "alert-success",
        "warning" : "alert-warning",
        "danger"  : "alert-danger"
    }

    function initializeApp() {
        // Hide spinner intially ..
        $('.spinner-border').hide();

        // Hide notification alert
        $('.notification-container').hide();

        // Intial Setup for dropdown
        if($('#radio-pincode').prop('checked', true)) {
            $('.pincode-details').show();
            $('.district-details').hide();
        } else {
            $('.pincode-details').hide();
            $('.district-details').show();
        }

        // onClick Listener for radioButtons
        $('#radio-pincode').click(function(){
            $('#radio-district').prop('checked', false);
            $('#radio-pincode').prop('checked', true);
            $('.pincode-details').show();
            $('.district-details').hide();
        });

        $('#radio-district').click(async function()     {
            $('#radio-pincode').prop('checked', false);
            $('#radio-district').prop('checked', true);
            $('.pincode-details').hide();
            $('.district-details').show();

            // fetch all the data from api and populate states dropdown
            var allStates = await populateStates();
            allStates.map(state => {
                let newOption = $('<option></option>');
                newOption.val(state.state_id).text(state.state_name);
                $('#states').append(newOption);
            });
        });

        // onChange Event of Dropdown
        $("select.state-select").change(async function(){
            var selectedStateId = $(this).children("option:selected").val();
            if(selectedStateId !== "None") {
                $('#districts').empty();
                var allDistricts = await populateDistricts(selectedStateId);
                allDistricts.map(district => {
                    let newOption = $('<option></option>');
                    newOption.val(district.district_id).text(district.district_name);
                    $('#districts').append(newOption);
                });
            }
        });

        // onClick Event for Submit
        $('#submitButton').click(function(){
            submitDetails();
        });
    }

    // Intialize the app
    initializeApp();
    
    // request data to submit
    function makeData() {
        let data = {};
        data.name = $('#name').val();
        data.contact = $('#phone').val();

        if($('#radio-district').prop('checked')) {
            // Send District Id and Name
            data.pincodeDistrictId = $('#districts').val();
            data.districtName = $('#districts option:selected').text();
        } else {
            // Only Pincode
            data.pincodeDistrictId = $('#pincode').val();
        }
        return data;    
    }
    
    // Submit Handler
    function submitDetails() {
        $('.spinner-border').show();
        let data = makeData();
        let retVal = validateData(data);
        if(retVal.status === 'ok') {
            setTimeout(async ()=>{
                $('#formId').show();
                const result = await sendPostReq('reqres.in',data);
                $('.spinner-border').hide();
                custom_notify("success", result.message);
            },1000);
        } else {
            $('.spinner-border').hide();
            custom_notify("danger", retVal.message);
        } 
    }

    function custom_notify(severity, message) {
        // console.log(severity, message);
        $('.notification-container').html("");
        $('.notification-container').html('<div class="alert alert-dismissible fade show" role="alert"> \
           <div id="notification-content"> '+message+' </div>\
           <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
           </div>');
        $('.alert-dismissible').addClass(notificationClasses[severity]);
        $('.notification-container').show();
    }

    $('[data-toggle="popover"]').popover({
    	trigger: 'focus'
    }); 
    $('.popover-dismiss').popover({
    	trigger: 'focus'
    });

});