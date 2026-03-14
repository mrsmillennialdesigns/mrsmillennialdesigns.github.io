// Dynamic review counter — fetches live count from API, updates across all pages
(function(){
  var API='https://mmd-review-counter.mrsmillennial.workers.dev';
  var FALLBACK=778;
  var HIGH_KEY='mmd_review_high';

  // Always use the highest count we've ever seen
  try{var stored=parseInt(localStorage.getItem(HIGH_KEY)||'0');if(stored>FALLBACK)FALLBACK=stored}catch(e){}

  function update(total){
    // Save new high watermark
    if(total>FALLBACK){FALLBACK=total;try{localStorage.setItem(HIGH_KEY,String(total))}catch(e){}}
    document.querySelectorAll('.footer-stats').forEach(function(el){
      el.innerHTML=el.innerHTML.replace(/\d+ reviews/,'<a href="/reviews.html" style="color:rgba(255,255,255,0.5)">'+total+' reviews</a>');
    });
    document.querySelectorAll('.hero-badge').forEach(function(el){
      el.textContent=total+' Five-Star Reviews';
    });
    document.querySelectorAll('.rv-count').forEach(function(el){
      el.textContent=total;
    });
  }

  document.addEventListener('DOMContentLoaded',function(){
    // Show fallback immediately so there's no flash
    update(FALLBACK);
    // Then fetch live count from API
    fetch(API+'/count').then(function(r){return r.json()}).then(function(d){
      if(d.count&&d.count>=FALLBACK)update(d.count);
    }).catch(function(){});
  });

  // Expose increment function for review form
  window.mmdIncrementReview=function(callback){
    fetch(API+'/increment',{method:'POST'}).then(function(r){return r.json()}).then(function(d){
      if(d.count)update(d.count);
      if(callback)callback(d.count);
    }).catch(function(){
      // Fallback: use localStorage if API fails
      var extra=0;
      try{extra=parseInt(localStorage.getItem('mmd_review_extra')||'0')}catch(e){}
      extra++;
      localStorage.setItem('mmd_review_extra',String(extra));
      update(FALLBACK+extra);
      if(callback)callback(FALLBACK+extra);
    });
  };
})();
