// values in table columns mapped to array values:
COLUMN_TO_NUM_ARR = ['type', 'lostudy', 'subject', 'specialization', 'deadline', 'bounty', 'bonuses', 'owner']

//
$(document).ready(function () {
    // sort by:
    $('#select_sort').change(function () {
       console.log($(this).val());
       switch($(this).val()) {
           case '1':
               sort_num('container_market_table', 'up', 'bounty');
               break;
           case '2':
               sort_num('container_market_table', 'down', 'bounty');
               break;
           case '3':
               sort_date('container_market_table', 'up', 'deadline');
               break;
           case '4':
               sort_date('container_market_table', 'down', 'deadline');
               break;
           case '5':
               sort_alpha('container_market_table', 'up', 'lostudy');
               break;
           case '6':
               sort_alpha('container_market_table', 'down', 'lostudy');
               break;
           case '7':
               sort_alpha('container_market_table', 'up', 'owner');
               break;
           case '8':
               sort_alpha('container_market_table', 'down', 'owner');
               break;
           case '9':
               sort_alpha('container_market_table', 'up', 'specialization');
               break;
           case '10':
               sort_alpha('container_market_table', 'down', 'specialization');
               break;
           case '11':
               sort_alpha('container_market_table', 'up', 'subject');
               break;
           case '12':
               sort_alpha('container_market_table', 'down', 'subject');
               break;
           case '13':
               sort_alpha('container_market_table', 'up', '......');// FIX
               break;
           case '14':
               sort_alpha('container_market_table', 'down', '......');// FIX
               break;
           case '15':
               sort_alpha('container_market_table', 'up', 'type');
               break;
           case '16':
               sort_alpha('container_market_table', 'down', 'type');
               break;
       }
    });
});

function sort_alpha(container, direction, sortby) {
    // sorting function:
    var fn;
    if (direction == 'up') {
        fn = function (a, b) {
            return ('' + a.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerText.localeCompare(b.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerText));
        }
    }
    else {
        fn = function (a, b) {
            return -1 * ('' + a.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerText.localeCompare(b.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].innerText));//.match('^[A-Za-z ]+\:[ \n]+(.+)$')[1]
        }
    }
    table_div = $('#' +  container);
    table_children = $('#' +  container)[0].children;
    // transfer to array so can sort:
    some_arr = [];
    // skip over index 0 as it is a header row
    for (var i = 1; i < table_children.length; i++) {
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
            var a_result = new Date(a.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].getAttribute('data-time').match('2[0-9 \:-]+')[0]).toISOString();
            var b_result = new Date(b.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].getAttribute('data-time').match('2[0-9 \:-]+')[0]).toISOString();
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
            var a_result = new Date(a.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].getAttribute('data-time').match('2[0-9 \:-]+')[0]).toISOString();
            var b_result = new Date(b.children[0].children[COLUMN_TO_NUM_ARR.indexOf(sortby)].getAttribute('data-time').match('2[0-9 \:-]+')[0]).toISOString();
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
    // skip over index 0 as it is a header row
    for (var i = 1; i < table_children.length; i++) {
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
    // skip over index 0 as it is a header row
    for (var i = 1; i < table_children.length; i++) {
        some_arr.push(table_children.item(i));
    }
    some_arr.sort(fn);
    // publish changes to DOM:
    some_arr.forEach(element => {
        table_div.append(element)
    })
}