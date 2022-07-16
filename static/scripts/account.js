// grab rows in table and feed them into array.
// resort array by user-requested value
// repost data from new array
function sort_alpha_ascending(sortby) {
    // var div_obj = document.getElementById('container_contracts_table').children;
    //
    // if (div_obj.length < 2) {
    //     console.log('less than two contracts...');
    //     return;
    // }
    // for (var i = 0; i < div_obj.length; i++) {
    //     console.log(div_obj[i].innerHTML)
    // }
    //
    //console.log(Object.values(div_obj)[0]);//highlightable in console to dom - each row surrounded by <a>
    console.log('here');
    //console.log($('#container_contracts_table')[0].children);
    //some_obj = $('#container_contracts_table')[0].children.sort();
    table_only = $('#container_contracts_table');


    table_children = $('#container_contracts_table')[0].children;
    some_arr = [];
    for (var i = 0; i < table_children.length; i++) {
        //console.log(table_children.item(i));
        some_arr.push(table_children.item(i));
    }
    console.log('zzzzzzzzzz');
    some_arr.forEach(element => {
        // console.log(element);
        // console.log(element.children[0].children[0].innerHTML);
    });
    some_arr.sort(function (a, b) {
        return ('' + a.children[0].children[0].innerHTML.toString()).localeCompare(b.children[0].children[0].innerHTML.toString());
    })
    for (var i = 0; i < some_arr.length; i++) {
        console.log(some_arr[i]);
    }
    for (var i = 0; i < some_arr.length; i++) {
        table_only.append(some_arr[i]);
    }


    //table_only.prepend("<div>yoyo</div>")



    ///////////////////////////////
    // html_collection = $('#container_contracts_table')[0].children;
    // console.log(html_collection);
    // for (var i = 0; i < html_collection.length; i++) {
    //     //var string1 = html_collection.item(i).children[0].children[0].innerHTML;
    //     //console.log(html_collection.item(i).children[0].children[0].innerHTML);
    //     console.log(string1.toString());
    // }


    var fn;
    fn = function(a, b) {return(a.price - b.price);}
    // if (direction == "down") {
    //     fn = function(a, b) {return(a.price - b.price);}
    // } else {
    //     fn = function(a, b) {return(b.price - a.price);}
    // }
    // html_collection = $('#container_contracts_table')[0].children;
    // for (var i = 0; i < html_collection.length; i++) {
    //     console.log(html_collection.item(i));
    // }

    console.log('here');
    //var arr = [];
    // for (element in div_arr) {
    //     console.log(element);
    // }
}
function sort_alpha_descending(sortby) {
    window.alert('up');
}

//
function sort_alpha(direction, sortby) {

}