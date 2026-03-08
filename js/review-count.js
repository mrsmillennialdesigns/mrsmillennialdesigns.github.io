// Dynamic review counter — updates 777 across all pages
(function(){
  var BASE=777;
  var extra=0;
  try{extra=parseInt(localStorage.getItem('mmd_review_extra')||'0')}catch(e){}
  var total=BASE+extra;
  document.addEventListener('DOMContentLoaded',function(){
    // Update footer stats
    document.querySelectorAll('.footer-stats').forEach(function(el){
      el.innerHTML=el.innerHTML.replace(/\d+ reviews/,'<a href="/reviews.html" style="color:rgba(255,255,255,0.5)">'+total+' reviews</a>');
    });
    // Update hero badge
    document.querySelectorAll('.hero-badge').forEach(function(el){
      el.textContent=total+' Five-Star Reviews';
    });
    // Update any .rv-count elements
    document.querySelectorAll('.rv-count').forEach(function(el){
      el.textContent=total;
    });
  });
})();
