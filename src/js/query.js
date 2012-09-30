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


$(document).ready(function(){

    $('#continue').click(function(){
	$('h1,p,a').fadeOut('fast');
	$('h1,p,a').promise().done(function(){
	    
	    $.getJSON(urlInteresting(), function(data){
		if (data.stat == 'ok') {
		    glovar.photos = getRandomSubarray(data.photos.photo, 5);
		    glovar.index = 0;
		    nextPhoto();
		}
	    });
	});
    });

});


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

function photo(img){
    return 'http://farm'+ img.farm +'.staticflickr.com/'
	+ img.server+'/'+ img.id+'_'+ img.secret+'_z.jpg';
}

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
	//doImpressions();
    });
    $.post( glovar.ctx + '/rest/top/impression', JSON.stringify(p), {contentType: 'application/json'}).complete(function(data){

	$('#content img').promise().done(function(){
	    var query = $(
		'<div id="query" style="display:hidden; position:absolute;">'
		+ '<p><b>'+data.responseText+'</b>'
		+ ' - is that correct impression of the image?</p>'
		+ '<a id="yes" href="#">yes</a>'
		+ '<a id="no" href="#">no</a>'
		+ '</div>'
	    );
	    $('#content').append(query);
	    query.css('top', (window.innerHeight - query.height()) / 2);
	    query.css('left', (window.innerWidth - query.width()) / 2);

	    $('#query').hide().delay(1500).fadeIn('slow');

	    $('#query a').click(function(event){
		event.preventDefault();
		
		$.post( glovar.ctx + '/rest/match/'+$(this).text(), JSON.stringify(p), {contentType: 'application/json'}).complete(function(data){
		    nextPhoto();
		});
	    });
	});
    });
}

function allDone(){
    window.location = glovar.ctx + '/thanks.html'
}
