var _NUMBER_PARAMS = [
                "cost_treasure",
                "cost_potions",
                "plus_actions",
                "plus_cards",
                "plus_treasure",
                "plus_buys",
                "trashes",
                "treasure",
                "victory_points"]
var _OTHER_PARAMS = ["name", "is_attack", "is_reaction", "description"]

function post_form(url, data, callback, form){
    var req = _.http_request();
    req.onreadystatechange = function(){
        callback(req, form);
    };
    req.open('POST', url);
    req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    req.send(data);
}

var card; 

function successfully_saved(req, form) {
    if (req.readyState === 4) {
        _.debug("received: " + req.status + req.responseText);
        card = JSON.parse(req.responseText);
        if (req.status === 200) {
            glow_green(form);
        }
    }
}

function display_all_cards() {
    var expansions = randomizer.expansions();
    var cards;
    var e;
    for (e in expansions) {
        _.debug(expansions[e]);
        make_header(e);
        cards = expansions[e];
        var c;
        for(c in cards) {
            populate_card(cards[c]);
        }
    }
}

function attach_listeners() {
    var forms = document.querySelectorAll("form");
    var i;
    for(i = 0; i < forms.length; i++) {
        forms[i].addEventListener("submit", form_submitted);
        forms[i].addEventListener("change", form_submitted);
    }
}

function form_submitted(e) {
    _.debug(this);
    e.preventDefault();
    save_card(this);
}

function glow_green(form) {
    form.classList.add("green");
    setTimeout(function(){form.classList.remove("green");}, 1000);
}

function save_card(form) {
    var inputs = form.elements;
    var i;
    var node;
    var str = "";
    for (i = 0; i < inputs.length; i++){
        node = inputs[i];
        if (node.type === "radio") {
            if (node.checked) {
                str += node.name + "=" + node.value + "&";
            }
        }
        if (node.value && (node.type === "number" || node.type === "textarea" || node.type === "text")) {
            str += encodeURIComponent(node.name) + "=" + encodeURIComponent(node.value) + "&";
        }
        _.debug("name " + inputs[i].name + " value " + inputs[i].value);
    }
    _.debug(str);
    post_form('/api/cards/'+inputs["id"].value, str, successfully_saved, form);
}

function make_header(expansion_name) {
    var h1 = document.createElement("h1");
    h1.innerText = expansion_name;
    document.body.appendChild(h1);
}

function populate_card(card) {
    var form = document.createElement("form");
    dom_string = "";
    dom_string +="<input type='hidden' name='id' value='" + _.escape_html(card.id) +"'>";
    dom_string += "<input type='text' name='name' placeholder='name' value='"+_.escape_html(card.name)+"'>";
    dom_string += "<textarea name='description' placeholder='description'>"+ _.escape_html(card.description)+ "</textarea>";
    var i;
    for (i = 0; i < _NUMBER_PARAMS.length; i++) {
        dom_string += "<label>" + _.escape_html(_NUMBER_PARAMS[i]);
        dom_string += "<input type='number' name='"+_.escape_html(_NUMBER_PARAMS[i])+"' value='"+_.escape_html(card[_NUMBER_PARAMS[i]])+"'>";
        dom_string += "</label>";
    }
    dom_string +="<fieldset><legend>attack</legend>";
    dom_string +="<label>F";
    dom_string += "<input type='radio' name='is_attack' value='false'";
    if (!card.is_attack) {
        dom_string += " checked";
    }
    dom_string += ">";
    dom_string +="</label><label>T";

    dom_string += "<input type='radio' name='is_attack' value='true'";
    if (card.is_attack) {
        dom_string += " checked";
    }
    dom_string += "></label></fieldset>";

    dom_string +="<fieldset><legend>reaction</legend>";
    dom_string +="<label>F";
    dom_string += "<input type='radio' name='is_reaction' value='false'";
    if (!card.is_reaction) {
        dom_string += " checked";
    }
    dom_string += ">";
    dom_string +="</label><label>T";

    dom_string += "<input type='radio' name='is_reaction' value='true'";
    if (card.is_reaction) {
        dom_string += " checked";
    }
    dom_string += "></label></fieldset>";


    form.innerHTML = dom_string;
    document.body.appendChild(form);
}

function init(){
    display_all_cards();
    attach_listeners();
}

randomizer.sync_db(init());
