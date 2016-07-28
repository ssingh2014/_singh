function filterOutNonEnglishCharacter(val) {
    if (val != "" && val != undefined && val != null) {
        var regEx = /([^a-z0-9\w\s`~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/])/gi;
        var s = val.search(regEx);
        
        if (s == -1) {
            return val;
        }
    }
}
