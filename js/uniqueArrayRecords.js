
function get_UniqueArrayRecords(arrayVal) {
    if (arrayVal != undefined && arrayVal != null && arrayVal.length > 0) {
        {
            var n = {};
            var r = [];

            for (var i = 0; i < arrayVal.length; i++) {
                if (!n[arrayVal[i]]) {
                    n[arrayVal[i]] = true;
                    r.push(arrayVal[i]);
                }
            }
            return r;
        }
    }
}
