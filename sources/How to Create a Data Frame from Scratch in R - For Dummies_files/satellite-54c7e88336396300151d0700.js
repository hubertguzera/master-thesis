_satellite.pushAsyncScript(function(event, target, $variables){
  /*
 * Percent Page Viewed
 * 
 * This Adobe DTM snippet will allow you to capture when a visitor has scrolled a certain % of a page.
 * To use, you will add the below code as a 3rd party script to a page load rule at either page top,
 * page bottom, or DOM ready.  It will not work if added as an onload rule.
 *
 * The code is configurable so you can capture any % complete milestones as a user scrolls.  The
 * milestones are in the "milestones" array in the _satellite.ppv object.  The defaults are 25, 50, 75
 * and 100, but they can be configured to capture any milestone.  When a visitor scrolls past the 
 * milestone, it will fire a direct call rule named "Percent Page Viewed X", where X is the milestone.
 * 
 * 
 * If using this for Adobe and you'd prefer to call this on the subsequent pageview (rather than in a direct 
 * call rule, use the setCookie code below and create a data element that uses readCookie
 */
_satellite.ppv = {
  milestones: [25,50,75,100],
  tracked: [],
  calculate: function(){
    var d = document, b = document.body, w = window, m=_satellite.ppv.milestones.sort(function(a,b){return a-b});
    var dh = Math.max(Math.max(b.scrollHeight,d.documentElement.scrollHeight),Math.max(b.offsetHeight,d.documentElement.offsetHeight),Math.max(b.clientHeight,d.documentElement.clientHeight)),
      vph = w.innerHeight||(d.documentElement.clientHeight||b.clientHeight),
      st = w.pageYOffset||(d.documentElement.scrollTop||b.scrollTop),
      vh = st + vph,
      pv = Math.round(vh/dh*100);
    for(var i=0; i<m.length; i++){
      if((m[i] && m[i+1]) || m[i]==m[m.length-1]){
        if((m[i]<=pv && m[i+1]>pv) || (m[i]<=pv && m[i] == m[m.length-1] && pv <= 100)){
          if(_satellite.indexOf(_satellite.ppv.tracked,m[i])==-1){
            //_satellite.track('Percent Page Viewed '+m[i]);
			_satellite.setCookie("ppvPlugin",c[e]);
            _satellite.ppv.tracked.push(m[i]);
          }
        }
      }
    }
  },
  scroll: function(){
    _satellite.addEventHandler(window,'scroll',_satellite.ppv.calculate,false);
    _satellite.addEventHandler(window,'resize',_satellite.ppv.calculate,false);
  }
};
_satellite.addEventHandler(window,'load',_satellite.ppv.scroll,false);

/* Minified Code */
_satellite.ppv={
milestones:[25,50,75,100],
tracked:[],calculate:function(){var g=document,j=document.body,k=window,c=_satellite.ppv.milestones.sort(function(i,d){return i-d});var h=Math.max(Math.max(j.scrollHeight,g.documentElement.scrollHeight),Math.max(j.offsetHeight,g.documentElement.offsetHeight),Math.max(j.clientHeight,g.documentElement.clientHeight)),a=k.innerHeight||(g.documentElement.clientHeight||j.clientHeight),n=k.pageYOffset||(g.documentElement.scrollTop||j.scrollTop),f=n+a,l=Math.round(f/h*100);for(var e=0;e<c.length;e++){if((c[e]&&c[e+1])||c[e]==c[c.length-1]){if((c[e]<=l&&c[e+1]>l)||(c[e]<=l&&c[e]==c[c.length-1]&&l<=100)){if(_satellite.indexOf(_satellite.ppv.tracked,c[e])==-1){_satellite.setCookie("ppvPlugin",c[e]);_satellite.ppv.tracked.push(c[e])}}}}},scroll:function(){_satellite.addEventHandler(window,"scroll",_satellite.ppv.calculate,false);_satellite.addEventHandler(window,"resize",_satellite.ppv.calculate,false)}};_satellite.addEventHandler(window,"load",_satellite.ppv.scroll,false);
});
