// run at page load:
window.onload = function () {
    const tz_offset = new Date().getTimezoneOffset()
console.log(tz_offset);
document.getElementById('r_f_timezone').value = tz_offset;
}