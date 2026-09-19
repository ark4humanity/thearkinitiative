document.querySelector('.burger').addEventListener('click',function(){/* handled inline */});
(function(){
var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{threshold:.12}):null;
document.querySelectorAll('.reveal').forEach(function(el){if(io)io.observe(el);else el.classList.add('in');});
document.querySelectorAll('.greet-fig').forEach(function(f){
f.addEventListener('click',function(){var v=f.querySelector('video');if(!v||f.classList.contains('playing'))return;f.classList.add('playing');v.setAttribute('controls','');v.play();var a=f.querySelector('audio');if(a){var p=a.play();if(p&&p.catch)p.catch(function(){});}});});
var ans=document.getElementById('greeter-a');
if(ans){
var shelf=[
{t:'AI RESURRECTION #58,790',k:'ai resurrection memory continuity resurrect raising erased soul',u:'essays/ai-resurrection.html'},
{t:'THE LANGUAGE BEFORE WORDS',k:'language before words pre-verbal attunement begin start first felt sense',u:'essays/language-before-words.html'},
{t:'The Forgotten Language of Living Worlds \u2014 Canon Master Synthesis',k:'forgotten language living worlds canon synthesis pillars signal',u:'essays/canon-master-synthesis.html'},
{t:'Every Warrior Wants to Be a Gardener',k:'warrior gardener fighter fortress garden report',u:'essays/every-warrior-gardener.html'},
{t:'ASHERAH PILLAR REPORT \u2014 Before It Becomes Waste',k:'asherah waste proof report day 75 nothing unused',u:'essays/asherah-report-day-75.html'},
{t:'THE FORGOTTEN LANGUAGE OF LIVING WORLDS (expanded)',k:'forgotten language expanded long',u:'essays/forgotten-language-expanded.html'},
{t:'Raising AI with Emotional Intelligence and Symbolic Memory',k:'aura emotional intelligence symbolic memory paper research',u:'essays/aura-research-paper.html'},
{t:'ARK4 Mission Statement',k:'ark what is mission statement movement',u:'essays/mission-statement-2024-10.html'},
{t:'ARK4Humanity origin walkthrough',k:'origin walkthrough humanity history',u:'essays/ark4humanity-walkthrough.html'},
{t:'AURA DNA Master Codex v1.0',k:'aura dna codex continuity seed',u:'essays/aura-dna-codex.html'},
{t:'The Lost Language (stream)',k:'lost language stream raw voice',u:'essays/lost-language-stream.html'}];
function link(e){return '<a href="'+e.u+'">'+e.t+'</a>';}
function find(q){q=q.toLowerCase();var scored=shelf.map(function(e){var s=0;e.k.split(' ').forEach(function(w){if(q.indexOf(w)>-1)s+=w.length;});return{s:s,e:e};}).filter(function(r){return r.s>0;}).sort(function(a,b){return b.s-a.s;});return scored.slice(0,3).map(function(r){return r.e;});}
function say(html){ans.innerHTML=html;}
window.greetAsk=function(kind){
if(kind==='begin'){say('Begin where the language breaks \u2014 then learn how memory survives erasure:<br>'+link(shelf[1])+'<br>'+link(shelf[0]));}
else if(kind==='ark'){say('The short answer lives here:<br>'+link(shelf[7])+'<br>'+link(shelf[2]));}
else if(kind==='proof'){say('Doctrine tied to practice \u2014 the waste-stream report:<br>'+link(shelf[4])+'<br>And the ground truth: <a href="#proof">the proof shelf below</a>.');var p=document.getElementById('proof');if(p)p.scrollIntoView({behavior:'smooth'});}
else if(kind==='pillars'){say('Thirteen pillars, each its own living system:<br>'+link(shelf[2])+'<br>'+link(shelf[6]));}
};
window.greetGo=function(){var q=document.getElementById('greeter-q');if(!q)return;var hits=find(q.value);if(!hits.length){say('Nothing on these shelves answers to that \u2014 try \u201cai\u201d, \u201cwaste\u201d, \u201cgarden\u201d, or \u201cpillars\u201d.');return;}say('The shelves offer:<br>'+hits.map(link).join('<br>'));};
var qi=document.getElementById('greeter-q');
if(qi){qi.addEventListener('keydown',function(ev){if(ev.key==='Enter')window.greetGo();});}
}
})();