// values in table columns mapped to array values:
COLUMN_TO_NUM_ARR = ['position', 'phase', 'type', 'lostudy', 'subject', 'specialization', 'deadline1', 'deadline2', 'bounty', 'efbonus', 'egbonus', 'newchatmsg']
// grab rows in table and feed them into array.
// resort array by user-requested value
// repost data from new array
function sort_alpha(direction, sortby) {
    // sorting function:
    var fn;
    if (direction == 'up') {
        fn = function (a, b) {
            console.log(('' + a.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerHTML.toString()).localeCompare(b.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerHTML.toString()));
            return ('' + a.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerHTML.toString()).localeCompare(b.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerHTML.toString());
        }
    }
    else {
        fn = function (a, b) {
            console.log(a.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerHTML.toString());
            console.log(-1 * ('' + a.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerHTML.toString()).localeCompare(b.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerHTML.toString()));
            return -1 * ('' + a.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerHTML.toString()).localeCompare(b.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerHTML.toString());
        }
    }
    table_div = $('#container_contracts_table');
    table_children = $('#container_contracts_table')[0].children;
    // transfer to array so can sort:
    some_arr = [];
    for (var i = 0; i < table_children.length; i++) {
        some_arr.push(table_children.item(i));
    }
    // sort the array alphabetically:
    some_arr.sort(fn);
    // publish changes to DOM:
    some_arr.forEach(element => {
        table_div.append(element)
    })
}

function sort_date(direction, sortby) {
    // sorting function:
    var fn;
    if (direction == 'up') {
        fn = function (a, b) {
            var a_result = new Date(a.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerHTML).toISOString();
            var b_result = new Date(b.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerHTML).toISOString();
            if (a_result > b_result) {
                return 1;
            }
            else {
                return -1;
            }
        }
    }
    else {
        fn = function (a, b) {
            var a_result = new Date(a.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerHTML).toISOString();
            var b_result = new Date(b.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerHTML).toISOString();
            if (a_result > b_result) {
                return -1;
            }
            else {
                return 1;
            }
        }
    }
    table_div = $('#container_contracts_table');
    table_children = $('#container_contracts_table')[0].children;
    // transfer to array so can sort:
    some_arr = [];
    for (var i = 0; i < table_children.length; i++) {
        some_arr.push(table_children.item(i));
    }
    some_arr.sort(fn);
    // publish changes to DOM:
    some_arr.forEach(element => {
        table_div.append(element)
    })
}

function sort_num(direction, sortby) {
    // sorting function:
    var fn;
    if (direction == 'up') {
        fn = function (a, b) {
            return parseFloat(a.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerHTML) - parseFloat(b.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerHTML);
        }
    }
    else {
        fn = function (a, b) {
            return parseFloat(b.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerHTML) - parseFloat(a.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerHTML);
        }
    }
    table_div = $('#container_contracts_table');
    table_children = $('#container_contracts_table')[0].children;
    // transfer to array so can sort:
    some_arr = [];
    for (var i = 0; i < table_children.length; i++) {
        some_arr.push(table_children.item(i));
    }
    some_arr.sort(fn);
    // publish changes to DOM:
    some_arr.forEach(element => {
        table_div.append(element)
    })
}