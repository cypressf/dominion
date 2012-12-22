// Cypress Library
(function(){
    // object we'll store our functions in
    var library = {};

    library.print = function(s) {
        console.log(s);
    };

    var debug_flag = true;

    library.debug = function(s) {
        if ( debug_flag ) {
            console.debug(s);
        }
    }

    library.set_debug = function(bool) {
        debug_flag = bool;
    }

    library.get_debug = function() {
        return debug_flag;
    }

    // put it in the global namespace
    window._ = library;
})();

var Dominion = 
[{name: "Cellar"},
{name: "Chapel"},
{name: "Moat"},
{name: "Chancellor"},
{name: "Village"},
{name: "Woodcutter"},
{name: "Workshop"},
{name: "Bureaucrat"},
{name: "Feast"},
{name: "Gardens"},
{name: "Militia"},
{name: "Moneylender"},
{name: "Remodel"},
{name: "Smithy"},
{name: "Spy"},
{name: "Thief"},
{name: "Throne Room"},
{name: "Council Room"},
{name: "Festival"},
{name: "Laboratory"},
{name: "Library"},
{name: "Market"},
{name: "Mine"},
{name: "Witch"},
{name: "Adventurer"}];


var Intrigue =
[{name: "Courtyard"},
{name: "Pawn"},
{name: "Secret Chamber"},
{name: "Great Hall"},
{name: "Masquerade"},
{name: "Shanty Town"},
{name: "Steward"},
{name: "Swindler"},
{name: "Wishing Well"},
{name: "Baron"},
{name: "Bridge"},
{name: "Conspirator"},
{name: "Coppersmith"},
{name: "Ironworks"},
{name: "Mining Village"},
{name: "Scout"},
{name: "Duke"},
{name: "Minion"},
{name: "Saboteur"},
{name: "Torturer"},
{name: "Trading Post"},
{name: "Tribute"},
{name: "Upgrade"},
{name: "Harem"},
{name: "Nobles"}];


var Prosperity =
[{name: "Loan"},
{name: "Trade Route"},
{name: "Watchtower"},
{name: "Bishop"},
{name: "Monument"},
{name: "Quarry"},
{name: "Talisman"},
{name: "Worker's Village"},
{name: "City"},
{name: "Contraband"},
{name: "Counting House"},
{name: "Mint"},
{name: "Mountebank"},
{name: "Rabble"},
{name: "Royal Seal"},
{name: "Vault"},
{name: "Venture"},
{name: "Goons"},
{name: "Grand Market"},
{name: "Hoard"},
{name: "Bank"},
{name: "Expand"},
{name: "Forge"},
{name: "King's Court"},
{name: "Peddler"}];


var Seaside =
[{name: "Embargo"},
{name: "Haven"},
{name: "Lighthouse"},
{name: "Native Village"},
{name: "Pearl Diver"},
{name: "Ambassador"},
{name: "Fishing Village"},
{name: "Lookout"},
{name: "Smugglers"},
{name: "Warehouse"},
{name: "Caravan"},
{name: "Cutpurse"},
{name: "Island"},
{name: "Navigator"},
{name: "Pirate Ship"},
{name: "Salvager"},
{name: "Sea Hag"},
{name: "Treasure Map"},
{name: "Bazaar"},
{name: "Explorer"},
{name: "Ghost Ship"},
{name: "Merchant Ship"},
{name: "Outpost"},
{name: "Tactician"},
{name: "Treasury"},
{name: "Wharf"}];


var Cornucopia = 
[{name: "Hamlet"},
{name: "Fortune Teller"},
{name: "Menagerie"},
{name: "Farming Village"},
{name: "Horse Traders"},
{name: "Remake"},
{name: "Tournament"},
{name: "Young Witch"},
{name: "Harvest"},
{name: "Horn of Plenty"},
{name: "Hunting Party"},
{name: "Jester"},
{name: "Fairgrounds"}];


var Alchemy =
[{name: "Transmute"},
{name: "Apothecary"},
{name: "Herbalist"},
{name: "Scrying Pool"},
{name: "University"},
{name: "Alchemist"},
{name: "Familiar"},
{name: "Philosopher's Stone"},
{name: "Golem"},
{name: "Apprentice"},
{name: "Possession"},
{name: "Vineyard"}];


var Hinterlands =
[{name: "Crossroads"},
{name: "Duchess"},
{name: "Fool's Gold"},
{name: "Develop"},
{name: "Oasis"},
{name: "Oracle"},
{name: "Scheme"},
{name: "Tunnel"},
{name: "Jack of All Trades"},
{name: "Noble Brigand"},
{name: "Nomad Camp"},
{name: "Silk Road"},
{name: "Spice Merchant"},
{name: "Trader"},
{name: "Cache"},
{name: "Cartographer"},
{name: "Embassy"},
{name: "Haggler"},
{name: "Highway"},
{name: "Ill-Gotten Gains"},
{name: "Inn"},
{name: "Mandarin"},
{name: "Margrave"},
{name: "Stables"},
{name: "Border Village"},
{name: "Farmland"}];

var cards = {dominion: Dominion,
        hinterlands: Hinterlands,
        alchemy: Alchemy,
        intrigue: Intrigue,
        seaside: Seaside,
        cornucopia: Cornucopia,
        prosperity: Prosperity};


var form = document.querySelector("form");
form.addEventListener("submit", update_page);

function update_page(e){
    /*
    Update the page when the form is submitted.
    */
    e.preventDefault();

    // get the names of expansions that are checked
    var expansions = get_expansions(e.target);
    _.debug(expansions);
    var random_cards = get_random_cards(expansions);
    put_in_dom(random_cards);
}

function put_in_dom(cards) {
    /*
    Put the results of randomization into the DOM
    */
    var i;
    var form = document.querySelector("#form");
    dom_string = "";
    for (expansion in cards) {
        dom_string += "<div id=\"" + expansion + "\" class=\"expansion\">";
        dom_string += "<h1>" + expansion + "</h1>";
        dom_string += "<ul>";
        var i;
        for (i = 0; i < cards[expansion].length; i++) {
            dom_string += "<li>" + cards[expansion][i].name + "</li>";
        }
        dom_string += "</ul>";
        dom_string += "</div>";
    }

    var cards_html = document.querySelector("#cards");
    if (cards_html){
        cards_html.innerHTML = dom_string;
    }
}

function get_expansions(form) {
    /*
    Given the DOM form, returns a list of checked expansion names.
    */
    var checkboxes = form.elements.namedItem("expansion");
    _.debug(checkboxes);
    var expansions = [];
    for(var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            expansions.push(checkboxes[i].value.toLowerCase());
        }
    }
    return expansions;
}

function get_random_cards(expansions){
    /*
    Given a list of expansion names, return a dictionary with those expansion
    names as keys, and lists of cards as the values.

    e.g.
    input{ ["Prosperity", "Intrigue"]
    output{ {
                "Prosperity"{ [card1, card2, card3, card4],
                "Intrigue"{ [card5, card6, card7, card8, card9, card10]
            }
    */

    var expansions = validate_expansions(expansions);
    if (expansions.length < 1){
        return false;
    }

    // get a random number of cards for each expansion
    var ran = constrained_random(expansions.length, 10);
    var random_cards = {};
    var i;
    for (i = 0; i < expansions.length; i++){
        // don't do anything if there are no cards to be delt
        if (!ran[i]){
            continue;
        }

        expansion = expansions[i];

        // shuffle the expansion, then pick the top n cards, where n is the number
        // of cards we randomly selected from this expansion
        cards[expansion].sort( function() { return 0.5 - Math.random() } );
        random_cards[expansion] = cards[expansion].slice(0,ran[i]);

        // if the cards are from prosperity, select 
        // whether or not playing with Colony and Platinum
        if (expansion === "prosperity" && rand_int(1,10) <= ran[i]) {
            random_cards[expansion].push({name:"Platinum"});
            random_cards[expansion].push({name:"Colony"});
        }
    }

    return random_cards
}

function validate_expansions(expansions){
    /*
    Given a list of expansion names, return a list of expansion names
    with all invalid expansion names removed.
    
    e.g.
    input{ ["Prosperity", "Intrigue", "Poop"]
    output{ ["Prosperity", "Intrigue"]

    input{ "alksjdflkajs"
    output{ []
    */
    var i;
    var valid_expansions = [];
    for (i = 0; i < expansions.length; i++) {
        if(expansions[i] in cards) {
            valid_expansions.push(expansions[i]);
        };
    }
    return valid_expansions;
}


function constrained_random(n, total){
    /* Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur. */
    var i;
    var dividers = [0, total];
    for (i = 1; i < n; i++){
        dividers.push(rand_int(0, total));
    }
    dividers.sort(compare_numbers);
    
    _.debug(dividers);

    var intervals = [];

    for (i = 0; i < dividers.length - 1; i++) {
        intervals.push(Math.abs(dividers[i] - dividers[i + 1]));
    }

    return intervals;
}


function rand_int(min, max) {
    // return an int from min to max inclusive
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function compare_numbers(a,b) {
  return a - b;
}