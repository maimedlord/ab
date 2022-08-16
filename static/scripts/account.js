// values in table columns mapped to array values:
COLUMN_TO_NUM_ARR = ['position', 'type', 'phase', 'lostudy', 'subject', 'specialization', 'deadline', 'deadline2', 'bounty', 'efbonus', 'egbonus', 'newchatmsg']

// on load
window.onload = function () {
    sort_date('container_contracts_table', 'up', 'deadline');
};

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