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
                let newOption = $('<option>');
                newOption.attr('value',state.state_id).text(state.state_name);
                $('#states').append(newOption)
            });
        });

        // onChange Event of Dropdown
        $("select.state-select  ").change(async function(){
            var selectedStateId = $(this).children("option:selected").val();
            if(selectedStateId !== "None") {
                var allDistricts = await populateDistricts(selectedStateId);
                allDistricts.map(district => {
                    let newOption = $('<option>');
                    newOption.attr('value',district.district_id).text(district.district_name);
                    $('#districts').append(newOption)
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
            data.state_id = $('.state-select:selected').val();
            data.district_id = $('.district-select:selected').val();
        } else {
            data.pincode = $('#pincode').val();
        }
        return data;    
    }
    
    // Submit Handler
    function submitDetails() {
        $('#formId').hide();
        $('.spinner-border').show();
        let data = makeData();
        let retVal = validateData(data);
        if(retVal.status === 'ok') {
            setTimeout(async ()=>{
                $('#formId').show();
                const result = await sendPostReq('reqres.in',data);
                console.log(result);
                $('.spinner-border').hide();
            },5000);
        } else {
            $('.spinner-border').hide();
            // add danger class to this
            $('.alert-dismissible').addClass(notificationClasses.danger);
            $('#notification-content').append(`${retVal.msg}`);
            $('.notification-container').show();
        } 
    }

});