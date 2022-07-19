// values in table columns mapped to array values:
COLUMN_TO_NUM_ARR = ['type', 'lostudy', 'subject', 'specialization', 'deadline2', 'deadline1', 'bounty', 'egbonus', 'efbonus']

function sort_alpha(container, direction, sortby) {
    // sorting function:
    var fn;
    if (direction == 'up') {
        fn = function (a, b) {
            return ('' + a.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerText.match('^[A-Za-z ]+\:[ \n]+(.+)$')[1].localeCompare(b.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerText.match('^[A-Za-z ]+\:[ \n]+(.+)$')[1]));
        }
    }
    else {
        fn = function (a, b) {
            return -1 * ('' + a.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerText.match('^[A-Za-z ]+\:[ \n]+(.+)$')[1].localeCompare(b.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerText.match('^[A-Za-z ]+\:[ \n]+(.+)$')[1]));
        }
    }
    table_div = $('#' +  container);
    table_children = $('#' +  container)[0].children;
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

function sort_date(container, direction, sortby) {
    // sorting function:
    var fn;
    if (direction == 'up') {
        fn = function (a, b) {
            var a_result = new Date(a.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerText.match('2[0-9 \:-]+')[0]).toISOString();
            var b_result = new Date(b.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerText.match('2[0-9 \:-]+')[0]).toISOString();
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
            var a_result = new Date(a.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerText.match('2[0-9 \:-]+')[0]).toISOString();
            var b_result = new Date(b.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerText.match('2[0-9 \:-]+')[0]).toISOString();
            if (a_result > b_result) {
                return -1;
            }
            else {
                return 1;
            }
        }
    }
    table_div = $('#' +  container);
    table_children = $('#' +  container)[0].children;
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

function sort_num(container, direction, sortby) {
    // sorting function:
    var fn;
    if (direction == 'up') {
        fn = function (a, b) {
            return parseFloat(a.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerText.match('[0-9]+\.[0-9]+')[0]) - parseFloat(b.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerText.match('[0-9]+\.[0-9]+')[0]);
        }
    }
    else {
        fn = function (a, b) {
            return parseFloat(b.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerText.match('[0-9]+\.[0-9]+')[0]) - parseFloat(a.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerText.match('[0-9]+\.[0-9]+')[0]);
        }
    }
    table_div = $('#' +  container);
    table_children = $('#' +  container)[0].children;
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