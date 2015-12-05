function formatDate(date)
{
	var dd = date.getDate();
	var mm = date.getMonth()+1; //January is 0!
	var yyyy = date.getFullYear();
	
	if(dd<10) {
	    dd='0'+dd
	} 
	
	if(mm<10) {
	    mm='0'+mm
	} 
	
	date = dd+'-'+mm+'-'+yyyy;
	return date;
}

function llenarSelect(select, lista) {
    select.find("option").remove();
    $.each(lista, function (key, value) {
        $("<option>").val(value.id).text(value.value).appendTo(select);
    });
}