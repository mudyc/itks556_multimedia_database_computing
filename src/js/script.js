var glovar = glovar || {}
glovar.api_key = "6fbadc88ba164f7970effd4c4f6d2658";
glovar.ctx = $('meta[name="context"]').attr('content');

// image loader http://desandro.github.com/imagesloaded/
(function(c,n){var l="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==";c.fn.imagesLoaded=function(f){function m(){var b=c(i),a=c(h);d&&(h.length?d.reject(e,b,a):d.resolve(e));c.isFunction(f)&&f.call(g,e,b,a)}function j(b,a){b.src===l||-1!==c.inArray(b,k)||(k.push(b),a?h.push(b):i.push(b),c.data(b,"imagesLoaded",{isBroken:a,src:b.src}),o&&d.notifyWith(c(b),[a,e,c(i),c(h)]),e.length===k.length&&(setTimeout(m),e.unbind(".imagesLoaded")))}var g=this,d=c.isFunction(c.Deferred)?c.Deferred():
0,o=c.isFunction(d.notify),e=g.find("img").add(g.filter("img")),k=[],i=[],h=[];c.isPlainObject(f)&&c.each(f,function(b,a){if("callback"===b)f=a;else if(d)d[b](a)});e.length?e.bind("load.imagesLoaded error.imagesLoaded",function(b){j(b.target,"error"===b.type)}).each(function(b,a){var d=a.src,e=c.data(a,"imagesLoaded");if(e&&e.src===d)j(a,e.isBroken);else if(a.complete&&a.naturalWidth!==n)j(a,0===a.naturalWidth||0===a.naturalHeight);else if(a.readyState||a.complete)a.src=l,a.src=d}):m();return d?d.promise(g):
g}})(jQuery);


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

$(document).ready(function(){

    $('h1,p').hide();
    $('h1').fadeIn(2000).fadeOut(4000);
    $('p').delay(1000).fadeIn(2000).fadeOut(3000);

    $('h1,p').promise().done(function(){
	console.log("asfd");
	$.getJSON(urlInteresting(), function(data){
	    if (data.stat == 'ok') {
		glovar.photos = data.photos;
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
    var p = glovar.photos.photo[glovar.index];

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

	var p = glovar.photos.photo[glovar.index];

	$.post( glovar.ctx + '/rest/impression/'+$(this).text(), JSON.stringify(p), {contentType: 'application/json'} );
    });
    $('#next').click(function(){
	event.preventDefault();
	nextPhoto();
    });
}