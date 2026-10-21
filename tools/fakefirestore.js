/* A stand-in for the Firebase compat SDK, used only by tools/check_shared.py.
   It keeps one shared collection in localStorage, so several tabs in one browser act like several
   people at a table, and it refuses writes that firestore.rules would refuse. Never served to the public. */
(function(){
  var KEY='fakefs';
  function all(){try{return JSON.parse(localStorage.getItem(KEY)||'{}');}catch(e){return {};}}
  function put(x){localStorage.setItem(KEY,JSON.stringify(x));fire();}
  var subs=[];
  function fire(){subs.forEach(function(f){setTimeout(f,0);});}
  window.addEventListener('storage',function(e){if(e.key===KEY)fire();});
  var DEL={__del:1};
  var KEYS=['room','dir','layer','t','k','name','pid','at','st','gone'];
  function ok(d){
    var ks=Object.keys(d);
    return ks.length===KEYS.length&&KEYS.every(function(k){return ks.indexOf(k)>=0;})
      &&Number.isInteger(d.room)&&d.room>=1&&d.room<=26&&['dn','up'].indexOf(d.dir)>=0&&['surface','under','core'].indexOf(d.layer)>=0
      &&typeof d.t==='string'&&d.t.length>=1&&d.t.length<=400&&typeof d.k==='string'&&d.k.length<=40
      &&typeof d.name==='string'&&d.name.length>=1&&d.name.length<=40&&typeof d.pid==='string'&&d.pid.length>=1&&d.pid.length<=40
      &&Number.isInteger(d.at)&&d.st&&typeof d.st==='object'&&Object.keys(d.st).length<=60&&typeof d.gone==='boolean';
  }
  var BOARDS=['ice-s6','ice-s7'];
  function deny(){return Promise.reject(new Error('PERMISSION_DENIED (fake rules)'));}
  function coll(name){
    return {
      doc:function(id){
        id=id||('d'+Math.random().toString(36).slice(2,14));
        var path=name+'/'+id;
        return {id:id,
          set:function(d){if(BOARDS.indexOf(name)<0||!ok(d)||Object.keys(d.st).length||d.gone!==false)return deny();var x=all();x[path]=JSON.parse(JSON.stringify(d));put(x);return Promise.resolve();},
          update:function(u){var x=all(),old=x[path];if(!old)return deny();var nd=JSON.parse(JSON.stringify(old));
            Object.keys(u).forEach(function(k){var v=u[k];if(k.indexOf('st.')===0){var p=k.slice(3);if(v===DEL)delete nd.st[p];else nd.st[p]=v;}else nd[k]=v;});
            if(!ok(nd)||['room','dir','layer','pid','at'].some(function(k){return nd[k]!==old[k];}))return deny();
            x[path]=nd;put(x);return Promise.resolve();}};
      },
      where:function(f,op,v){
        return {onSnapshot:function(cb,err){
          if(BOARDS.indexOf(name)<0){setTimeout(function(){err(new Error('PERMISSION_DENIED'));},0);return function(){};}
          var go=function(){var x=all(),docs=[];Object.keys(x).forEach(function(p){var s=p.split('/');if(s[0]===name&&x[p][f]===v)docs.push({id:s[1],data:function(){return JSON.parse(JSON.stringify(x[p]));}});});
            cb({forEach:function(fn){docs.forEach(fn);}});};
          subs.push(go);setTimeout(go,0);
          return function(){var i=subs.indexOf(go);if(i>=0)subs.splice(i,1);};
        }};
      }
    };
  }
  var fs={settings:function(){},collection:coll};
  window.firebase={apps:[],initializeApp:function(){this.apps.push(1);},firestore:Object.assign(function(){return fs;},{FieldValue:{delete:function(){return DEL;}}})};
})();
