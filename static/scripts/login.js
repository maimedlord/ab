// run at page load:
window.onload = function () {
    const tz_offset = new Date().getTimezoneOffset()
console.log(tz_offset);
document.getElementById('tz_offset').value = tz_offset;
}