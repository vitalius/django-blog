$(document).ready(function() {
   // &#9818; - &#9823;
   //$(".home_link").html('&#'+ (9818+Math.floor(Math.random()*5)) +';');
   //$(".home_link").html('[0, ..., &#8734;]');
   //$(".home_link").html('@');
   //$(".home_link").html('&#8734');

   //top_colors = ['#3f5f5f', '#cc0000', '#003366', '#097054', '#003264'];
   //$("#top_bar").css("background", pick_rand(top_colors));
 
   $(".title_link").hover(
          function() { $(this).stop().animate({color:'#777777'}, 100) },
          function() { $(this).stop().animate({color:'#000000'}, 300) }
   );


   function callback() { 
     setTimeout(function() {
       $( ".home_link" ).removeAttr( "style" ).hide().fadeIn();
     }, 1000 );
   };

   $(".home_link").hover(
          function() { $(this).stop().animate({color:'#FFFFBE', fontSize: "1.5em", lineHeight: "1.5em"}, 100)},
          function() { $(this).stop().animate({color:'#FFFFBE', fontSize: "1em",   lineHeight: "2.5em"}, 200)}
          //function() { $(this).effect('shake', 200) }
          //function() { $(this).stop() } 
   );

 
   var top_string = $("#top_bar_title").text()
   var rand_num = Math.floor(Math.random()*10000000);
   $("#rand_num").html(top_string+rand_num);

   $("#copyleft_notice").html('&copy; 2011');
   $("#comment_title").html(pick_rand(com_titles));
   $("#comment_title").gradientText();

   var r_bs_verb  = pick_rand(bs_verb);
   var r_bs_adj1  = pick_rand(bs_adj);
   var r_bs_adj2  = pick_rand(bs_adj);
   var r_bs_noun1 = pick_rand(bs_noun_sing);
   var r_bs_noun2 = pick_rand(bs_noun);

   var r_bs_job_one   = pick_rand(bs_job_one);
   var r_bs_job_two   = pick_rand(bs_job_two); 
   var r_bs_job_three = pick_rand(bs_job_three);


   $("#about_string").html("The " +
   r_bs_adj1 + " " + r_bs_noun1 + " described in this blog, attempts to " + r_bs_verb + " " +
   r_bs_adj2 + " " + r_bs_noun2 + ". This technology is pioneered by " +
   r_bs_job_one + " " + r_bs_job_two + " " + r_bs_job_three + ", " +
   "<a href='http://www.facebook.com/vital.pavlenko'>Vitaliy&nbsp;Pavlenko</a>");

});

var addthis_config = {
     ui_click: true,
     services_compact: 'facebook,livejournal,twitter,email,more'
};
  
var addthis_localize = {
    share_caption: "Tell friends",
    email: "Email",
    favorites: "Favorites",
    more: "More..."
};
