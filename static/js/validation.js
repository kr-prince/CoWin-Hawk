// Validate data before sending to api
function validateData(data) {
    console.log(data);  
    let errorMsg = '';
    let phonePatt = /^\d{10}$/;
    let pincodePatt = /^\d{6}$/;
    console.log(data);
    if(!data.contact.match(phonePatt)){
        errorMsg += '<p> Invaild Phone Number </p>'
    }
    if(data.pincode && (!data.pincode.match(pincodePatt))) {
        errorMsg += '<p> Invalid Pincode </p>'
    }
    
    return errorMsg ? {msg: errorMsg, status: 'notok'} : {msg: errorMsg, status: 'ok'};
}
