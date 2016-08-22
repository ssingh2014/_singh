// indexOf -- regEx

function findIndexOfRegEx(val) {
    if (val != undefined && val != null && val != "") {
        var s = val.replace(/\s/gi, '');
        s = s.search(/canada|croatia|ericwood|TorontoScarborough|unitedkingdom|israel|thailand|puertorico|thailand|italy|newzealand|vancouver|ireland|indonesia|gb|[a-z]\d[a-z]\d[a-z]\d/gi);
        if (s == -1) {
            return s;
        }
    }
}


// -----------------------------------------

var str = "this is ABCD string";
var s = str.search(/ABCD/gi);  // ABCD index number is --> 8 
