// grab rows in table and feed them into array.
// resort array by user-requested value
// repost data from new array
function sort_alpha_ascending(sortby) {
    var div_obj = document.getElementById('container_contracts_table').children;
    console.log(div_obj[0].innerHTML);
    console.log(Object.keys(div_obj)[0]);
    console.log(Object.values(div_obj)[0]);
    var newvar = Object.values(div_obj)[1];
    console.log(newvar)
    var arr = [];
    // for (element in div_arr) {
    //     console.log(element);
    // }
}
function sort_alpha_descending(sortby) {
    window.alert('up');
}