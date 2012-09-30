var glovar = glovar || {}
glovar.api_key = "6fbadc88ba164f7970effd4c4f6d2658";
glovar.ctx = $('meta[name="context"]').attr('content');



function urlInteresting(){
    return "http://api.flickr.com/services/rest/"
	+ "?method=flickr.interestingness.getList"
	+ "&api_key="+glovar.api_key
	+ "&format=json"
	+ "&jsoncallback=?";
}

function photo(img){
    return 'http://farm'+ img.farm +'.staticflickr.com/'
	+ img.server+'/'+ img.id+'_'+ img.secret+'_z.jpg';
}

function getRandomSubarray(arr, size) {
    var shuffled = arr.slice(0), i = arr.length, min = i - size, temp, index;
    while (i-- > min) {
        index = Math.floor(i * Math.random());
        temp = shuffled[index];
        shuffled[index] = shuffled[i];
        shuffled[i] = temp;
    }
    return shuffled.slice(min);
}


$(document).ready(function(){

    $('h1,p').hide();
    $('h1').fadeIn(2000).fadeOut(4000);
    $('p').delay(1000).fadeIn(2000).fadeOut(3000);

    $('h1,p').promise().done(function(){
	console.log("asfd");
	$.getJSON(urlInteresting(), function(data){
	    if (data.stat == 'ok') {
		glovar.photos = getRandomSubarray(data.photos.photo, 20);
		glovar.index = 0;
		nextPhoto();
	    }
	});
    });
});

/*
var impressions =
    'showy,sober,natural,artificial,warm,cold,bright,dark,'
    + 'intellectual,emotional,soft,hard,light,grave,'
    + 'strong,feeble,favorite,disliked,static,dynamic,cheerful,gloomy,'
    + 'beautiful,ugly,manly,womanly,vivid,vague,clear,blurred,'
    + 'simple,complicated,graceful,vulgar,new,old,excited,melancholy';
*/
//http://simple.wikipedia.org/wiki/List_of_simple_adjectives
//http://edutechwiki.unige.ch/en/Semantic_differential_scale
var impressions = 'bright,dim;warm,cold;hard,soft;'
    +'heavy,light;clean,dirty;emotional,logical;empty,full;happy,sad;'
    +'strong,weak;calm,excited;new,old;feminine,masculine';

function nextPhoto(){
    $('#content').children().remove();
    glovar.index += 1;
    if (glovar.index >= glovar.photos.length)
	return allDone();
    var p = glovar.photos[glovar.index];

    $('#content').append($('<img style="position:absolute;left:'+0+'px;top:'+0+'px;" src="'+photo(p)+'" />'));
    $('#content img').hide().fadeIn('slow');
    $('#content img').imagesLoaded(function(){
	var imgtop = (window.innerHeight - parseInt($(this).height())) / 2;
	var imgleft = (window.innerWidth - parseInt($(this).width())) / 2;
	$(this).css('left', imgleft);
	$(this).css('top', imgtop);
	doImpressions();
    });
}
function doImpressions() {
    $('#content').append($('<a id="next" style="display:none;position:absolute;" href="#" >next image</a>'));
    $('#next').css('top', (window.innerHeight - $('#next').height()) / 2);
    $('#next').css('left', (window.innerWidth - $('#next').width()) / 2);

    var imp_arr = impressions.split(';');
    var angle = 0;
    var angleDelta = 2*Math.PI / (imp_arr.length );
    for (idx in imp_arr) {
	var i = imp_arr[idx];
	var x = window.innerWidth/2;
	x = x-50 + Math.sin(angle)*(x-100);
	var y = window.innerHeight/2;
	y = y-25 + Math.cos(angle)*(y-50);

	var iElem = 
	    '<div style="position:absolute;left:'+x+'px;top:'+y+'px" >'
	    + '<a href="#">'+i.split(',')[0]+'</a> '
	    + '<a href="#">'+i.split(',')[1]+'</a>'
	    + '</div>';
	
	$('#content').append($(iElem));
	angle += angleDelta;
    }

    $('#content div a').click(function(event){
	event.preventDefault();
	$(this).next().fadeOut('fast');
	$(this).prev().fadeOut('fast');
	$(this).parent().animate({
	    top:  window.innerHeight/2,
	    left: window.innerWidth/2}).fadeOut('slow');

	$('#next').fadeIn('slow');

	var p = glovar.photos[glovar.index];

	$.post( glovar.ctx + '/rest/impression/'+$(this).text(), JSON.stringify(p), {contentType: 'application/json'} );
    });
    $('#next').click(function(){
	event.preventDefault();
	nextPhoto();
    });
}


function allDone(){
    window.location = glovar.ctx + '/query.html'
}
