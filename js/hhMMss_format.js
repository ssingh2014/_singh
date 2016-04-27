
function getFormatedDurationInMinSec(val) {
    if (val != undefined && val != null && val != "") {

        var s = val.toUpperCase();

        if (s.indexOf('M') != -1) {

            s = s.split('M');
            var min = s[0].replace(/PT/g, '');
            var sec = s[1].replace(/S/g, '');
            s = Number(min) * 60 + Number(sec);

            var hours = Math.floor(s / 3600) < 10 ? ("00" + Math.floor(s / 3600)).slice(-2) : Math.floor(s / 3600);
            var minutes = ("00" + Math.floor((s % 3600) / 60)).slice(-2);
            var seconds = ("00" + (s % 3600) % 60).slice(-2);
            s = hours + ":" + minutes + ":" + seconds;

            var checkHH = s.split(':')[0];
            checkHH = Number(checkHH);

            if (checkHH != 00) {
                s = hours + ":" + minutes + ":" + seconds;
            }
            else if (checkHH == 00) {
                s = minutes + ":" + seconds;
            }
        }
        return s;
    }
}
