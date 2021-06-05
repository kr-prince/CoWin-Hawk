// Validate data before sending to api
function validateData(data) {
    let errorMsg = '';
    let phonePatt = /^\d{10}$/;
    let pincodePatt = /^\d{6}$/;
    if(!data.contact.match(phonePatt)){
        errorMsg += 'Invaild Phone Number';
    }
    if($('#radio-pincode').prop('checked') && (!data.pincodeDistrictId.match(pincodePatt))) {
        errorMsg += 'Invalid Pincode';
    }
    
    return errorMsg ? {message: errorMsg, status: 'notok'} : {message: errorMsg, status: 'ok'};
}
