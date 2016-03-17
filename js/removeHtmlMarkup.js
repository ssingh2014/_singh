
// replace HTML Tags

function removeHtmlMarkup(addr) {
    if (addr != '' && addr != undefined && addr != null) {
        var s = (addr.replace(/<(.|\n)*?>|\\n\s*/gm, ''));
        s = s.replace(/\n\t|\n|\t|\s\s|\"/g, '');
        return s;
    }
}
