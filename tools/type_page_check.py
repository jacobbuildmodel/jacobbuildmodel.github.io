"""tools/type_page_check.py -- the page check for a change of typeface or of
the heading hook (pull request 64, 12 November 2026). Needs tools/type_tools.py.

    python tools/type_page_check.py compare <build of main> <build of the branch>
        every HTML file in both builds: heading words, ids, "#" anchors, the
        table of contents and the whole visible text must be identical; the
        XML files (RSS feeds, sitemap) byte-identical. Lists the headings the
        hook split into label and finding, and the H2s with a colon left whole.
    python tools/type_page_check.py harness <build of the branch>
        writes _type_check.html into the build. Serve the build and open that
        page in a browser: it loads ten page types in frames 390 and 1280 px
        wide, light and dark, and reports for each: horizontal scroll, fonts
        that failed, the first font family and size of each kind of text, the
        size ladder, digit widths, the lowest text contrast, faces used in
        the first screen that are not preloaded, and how far the page moves
        when every font is replaced by its fallback. The result is JSON in
        the page (window.R, and the element with id "out").
"""
import glob, html, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import type_tools as T


# ------------------------------------------------------------------ compare
def strip(t):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"(?s)<[^>]+>", "", t))).strip()


def stage_compare(a, b):
    def files(d):
        return {os.path.relpath(p, d).replace("\\", "/") for p in glob.glob(os.path.join(d, "**", "*"), recursive=True)
                if os.path.isfile(p)}
    fa, fb = files(a), files(b)
    print("files: main %d, branch %d" % (len(fa), len(fb)))
    print("only in main:", sorted(fa - fb))
    print("only in branch:", sorted(fb - fa))
    pages = sorted(p for p in fa & fb if p.endswith(".html"))
    xml = sorted(p for p in fa & fb if p.endswith(".xml"))
    same_xml = [p for p in xml if open(os.path.join(a, p), "rb").read() == open(os.path.join(b, p), "rb").read()]
    print("xml files (RSS feeds, sitemap): %d, byte-identical: %d; differing: %s"
          % (len(xml), len(same_xml), sorted(set(xml) - set(same_xml))))
    heads = split = 0
    bad = []
    colon_unsplit = []
    for p in pages:
        ta = open(os.path.join(a, p), encoding="utf-8").read()
        tb = open(os.path.join(b, p), encoding="utf-8").read()

        def hs(t):
            out = []
            for m in re.finditer(r"(?s)<h([1-6])([^>]*)>(.*?)</h\1>", t):
                i = re.search(r'\bid="?([^"\s>]+)', m.group(2))
                anchors = re.findall(r'<a hidden class="?anchor"?[^>]*href="?([^"\s>]+)', m.group(3))
                inner = re.sub(r"(?s)<a hidden.*?</a>", "", m.group(3))
                out.append((m.group(1), i.group(1) if i else "", strip(inner), tuple(anchors)))
            return out

        def toc(t):
            m = re.search(r'(?s)<div class="?toc"?>.*?</details>', t)
            return m.group(0) if m else ""

        def body(t):
            return strip(re.sub(r"(?is)<(script|style|head)\b.*?</\1>", "", t))
        ha, hb = hs(ta), hs(tb)
        heads += len(hb)
        if ha != hb:
            bad.append((p, "headings", [x for x in zip(ha, hb) if x[0] != x[1]][:2]))
        if toc(ta) != toc(tb):
            bad.append((p, "toc", ""))
        if body(ta) != body(tb):
            x, y = body(ta), body(tb)
            i = next((k for k in range(min(len(x), len(y))) if x[k] != y[k]), min(len(x), len(y)))
            bad.append((p, "text", (x[max(0, i - 60):i + 60], y[max(0, i - 60):i + 60])))
        for m in re.finditer(r'(?s)<h2 id="?([^"\s>]+)"? class="?[^>]*h2-split[^>]*>(.*?)</h2>', tb):
            split += 1
            lab = re.search(r'(?s)<span class="?h2-label"?>(.*?)<span class="?h2-colon', m.group(2))
            print("  split  %-34s %s | %s" % (p[:34], strip(lab.group(1)) if lab else "?",
                                              strip(re.sub(r"(?s)<a hidden.*?</a>", "", m.group(2).split("h2-text")[-1][1:]))[:70]))
        for m in re.finditer(r"(?s)<h2((?![^>]*h2-split)[^>]*)>(.*?)</h2>", tb):
            s = strip(re.sub(r"(?s)<a hidden.*?</a>", "", m.group(2)))
            if ":" in s:
                colon_unsplit.append((p, s[:90]))
    print("pages compared: %d; headings: %d; split: %d" % (len(pages), heads, split))
    print("H2 with a colon left whole:", colon_unsplit)
    print("DIFFERENCES:", bad if bad else "none (heading words, ids, anchors, table of contents and visible text identical)")


# ------------------------------------------------------------------ harness
HARNESS = r"""<!doctype html><meta charset="utf-8"><title>running</title>
<body style="margin:0"><div id="host"></div><pre id="out"></pre>
<script>
var PAGES = __PAGES__;
var FILES = {"Newsreader|400|normal":"newsreader-latin-400-normal.woff2","Newsreader|400|italic":"newsreader-latin-400-italic.woff2","Newsreader|600|normal":"newsreader-latin-600-normal.woff2","Inter|400|normal":"inter-latin-400-normal.woff2","Inter|600|normal":"inter-latin-600-normal.woff2","JetBrains Mono Digits|400|normal":"jetbrains-mono-digits-400.woff2","JetBrains Mono Digits|700|normal":"jetbrains-mono-digits-700.woff2"};
var R = [], first = {};
function sleep(ms){return new Promise(function(r){setTimeout(r,ms);});}
function rgb(c){var m=/rgba?\(([^)]+)\)/.exec(c); if(!m) return null; var p=m[1].split(/[\s,\/]+/).filter(function(x){return x!=="";}).map(parseFloat); return [p[0],p[1],p[2],p.length>3?p[3]:1];}
function lin(v){v/=255; return v<=0.04045? v/12.92 : Math.pow((v+0.055)/1.055,2.4);}
function L(c){return 0.2126*lin(c[0])+0.7152*lin(c[1])+0.0722*lin(c[2]);}
function over(f,b){var a=f[3]; return [f[0]*a+b[0]*(1-a), f[1]*a+b[1]*(1-a), f[2]*a+b[2]*(1-a), 1];}
function hex(c){return "#"+[0,1,2].map(function(i){return ("0"+Math.round(c[i]).toString(16)).slice(-2);}).join("");}
function bgOf(el,w){var layers=[]; for(var e=el;e&&e.nodeType===1;e=e.parentElement){var c=rgb(w.getComputedStyle(e).backgroundColor); if(c&&c[3]>0){layers.push(c); if(c[3]>=1) break;}} var base=[255,255,255,1]; for(var i=layers.length-1;i>=0;i--) base=over(layers[i],base); return base;}
function direct(el){var s=""; for(var n=el.firstChild;n;n=n.nextSibling) if(n.nodeType===3) s+=n.nodeValue; return s.trim();}
function faceKeys(cs,txt){var fam=cs.fontFamily.split(",").map(function(x){return x.trim().replace(/^["']|["']$/g,"");}); var w=parseInt(cs.fontWeight,10), it=cs.fontStyle==="italic", out=[];
  function tx(f){ if(f==="Newsreader") return it? "Newsreader|400|italic" : f+"|"+(w>500?600:400)+"|normal"; if(f==="Inter") return f+"|"+(w>500?600:400)+"|normal"; return null; }
  if(fam[0]==="JetBrains Mono Digits"){ if(/[0-9]/.test(txt)) out.push(fam[0]+"|"+(w>500?700:400)+"|normal"); if(/[^0-9\s]/.test(txt)){var k=tx(fam[1]); if(k) out.push(k);} }
  else {var k2=tx(fam[0]); out.push(k2||("OTHER:"+fam[0]));}
  return out;}
async function one(name,path,width,theme){
  try{localStorage.setItem("pref-theme",theme);}catch(e){}
  var f=document.createElement("iframe"); f.style.cssText="display:block;border:0;width:"+width+"px;height:"+(width<600?844:800)+"px";
  document.getElementById("host").appendChild(f);
  await new Promise(function(r){f.onload=r; f.src=path;});
  var d=f.contentDocument, w=f.contentWindow;
  await d.fonts.ready; await sleep(350); await d.fonts.ready;
  var o={p:name,w:width,t:theme};
  o.theme=d.documentElement.getAttribute("data-theme"); o.bg=hex(bgOf(d.body,w));
  o.ovf=d.documentElement.scrollWidth-w.innerWidth;
  var st={}; d.fonts.forEach(function(x){st[x.status]=(st[x.status]||0)+1; if(x.status==="error"){(o.fontErr=o.fontErr||[]).push(x.family+" "+x.weight+" "+x.style);}}); o.fonts=st;
  function q(s){return d.querySelector(s);}
  function fz(s){var e=q(s); if(!e) return null; var c=w.getComputedStyle(e); return c.fontFamily.split(",")[0].replace(/["']/g,"")+" "+(+parseFloat(c.fontSize).toFixed(1))+"/"+c.fontWeight+(c.fontStyle==="italic"?"i":"");}
  function px(s){var e=q(s); return e?+parseFloat(w.getComputedStyle(e).fontSize).toFixed(1):null;}
  var sel={title:".post-title, .page-header h1",lead:".entry-lead",h2:".post-content h2",label:".post-content h2 .h2-label",h3:".post-content h3",body:".post-content > p",td:".post-content td",th:".post-content th",strip:".method-strip-item",dstrip:".decision-strip",count:".track-band-counts dd",cal:".track-band-cal",nav:"header nav a, .header a",h1:"h1",meta:".post-meta",foot:"footer"};
  var fam={}; for(var k in sel){var v=fz(sel[k]); if(v) fam[k]=v;}
  var fj=JSON.stringify(fam), key=name+"|"+width; if(first[key]===fj) o.fam="="; else {o.fam=fam; if(!first[key]) first[key]=fj;}
  var lad=[px(sel.title),px(sel.h2),px(sel.h3),px(".post-content > p")||px(".post-content")]; o.lad=lad;
  var seq=lad.filter(function(x){return x!=null;}); o.ladOk=seq.every(function(x,i){return i===0||x<seq[i-1];});
  function dig(s){var e=q(s); if(!e) return null; var a=d.createElement("span"),b=d.createElement("span"); a.textContent="1111111111"; b.textContent="0000000000"; [a,b].forEach(function(x){x.style.cssText="position:absolute;visibility:hidden;white-space:nowrap"; e.appendChild(x);}); var r=[+a.getBoundingClientRect().width.toFixed(2),+b.getBoundingClientRect().width.toFixed(2)]; a.remove(); b.remove(); return r;}
  o.dig={}; ["td","th","strip","dstrip","count","cal"].forEach(function(k){var r=dig(sel[k]); if(r) o.dig[k]=r;});
  var par={}; d.querySelectorAll(".post-content h2").forEach(function(h){var p=h.parentElement; if(!p.classList.contains("post-content")){var kk=p.tagName.toLowerCase()+"."+p.className; par[kk]=(par[kk]||0)+1;}});
  var inC=d.querySelectorAll(".post-content h2").length, spC=d.querySelectorAll(".post-content h2.h2-split").length;
  o.h2=[inC,spC,d.querySelectorAll("h2.h2-split").length-spC]; if(Object.keys(par).length) o.h2par=par;
  var minr=99,bad={},fold={},other={},n=0,all=d.body.querySelectorAll("*");
  for(var i=0;i<all.length;i++){var e=all[i]; if(e.closest("svg,script,style,noscript,math")) continue; var txt=direct(e); if(!txt) continue; var r=e.getBoundingClientRect(); if(r.width<1||r.height<1) continue; var cs=w.getComputedStyle(e); if(cs.visibility!=="visible"||cs.clipPath!=="none"||cs.clip!=="auto") continue;
    var fg=rgb(cs.color); if(!fg) continue; var op=1; for(var a=e;a&&a.nodeType===1;a=a.parentElement) op*=parseFloat(w.getComputedStyle(a).opacity);
    var bg=bgOf(e,w), c=over([fg[0],fg[1],fg[2],fg[3]*op],bg), l1=L(c), l2=L(bg), ratio=(Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05); n++;
    if(ratio<minr) minr=ratio; if(ratio<4.5){var kk=e.tagName.toLowerCase()+"."+String(e.className).split(" ")[0]+" "+hex(c)+" on "+hex(bg); if(!bad[kk]) bad[kk]=+ratio.toFixed(2);}
    faceKeys(cs,txt).forEach(function(k){ if(k.indexOf("OTHER:")===0) other[k.slice(6)]=(other[k.slice(6)]||0)+1; else if(r.top<w.innerHeight&&r.bottom>0&&r.left<w.innerWidth) fold[k]=1; });}
  o.con=[+minr.toFixed(2),n]; if(Object.keys(bad).length) o.bad=bad;
  var pre=[].map.call(d.querySelectorAll('link[rel="preload"][as="font"]'),function(l){return l.getAttribute("href").split("/").pop();});
  var need=Object.keys(fold).map(function(k){return FILES[k]||k;});
  o.notPre=need.filter(function(x){return pre.indexOf(x)<0;}); o.preUnused=pre.filter(function(x){return need.indexOf(x)<0;});
  if(theme==="light"&&width===390&&Object.keys(other).length) o.other=other;
  if(name==="article"&&theme==="light"){var cx=d.createElement("canvas").getContext("2d"), s1=(q(".post-content > p")||d.body).textContent.replace(/\s+/g," ").slice(0,600);
    var mw=function(font,s){cx.font=font; return +cx.measureText(s).width.toFixed(1);};
    o.canvas={serif:[mw('400 20px "Newsreader"',s1),mw('400 20px "Newsreader Fallback"',s1),mw('400 20px Georgia',s1)],sans:[mw('400 20px "Inter"',s1),mw('400 20px "Inter Fallback"',s1),mw('400 20px Arial',s1)],digits:[mw('400 20px "JetBrains Mono Digits"',"0123456789"),mw('700 20px "JetBrains Mono Digits"',"0123456789"),mw('400 20px "Inter"',"0123456789")]};}
  var blocks=[].slice.call(d.querySelectorAll(".post-content p, .post-content li, .post-content h2, .post-content h3, .post-title, .page-header h1, .entry-lead, .entry-content, .entry-header h2"));
  var hb=blocks.map(function(x){return x.getBoundingClientRect().height;}), h0=d.documentElement.scrollHeight, rs=d.documentElement.style;
  rs.setProperty("--font-serif",'"Newsreader Fallback", Georgia, serif'); rs.setProperty("--font-sans",'"Inter Fallback", Arial, sans-serif'); rs.setProperty("--font-figures",'"Inter Fallback", Arial, sans-serif');
  void d.body.offsetHeight;
  var ch=0; blocks.forEach(function(x,i){if(Math.abs(x.getBoundingClientRect().height-hb[i])>0.5) ch++;});
  o.swap=[h0,d.documentElement.scrollHeight,ch,blocks.length];
  f.remove(); return o;
}
(async function(){
  for(var i=0;i<PAGES.length;i++) for(var wi=0;wi<2;wi++) for(var ti=0;ti<2;ti++){
    try{R.push(await one(PAGES[i][0],PAGES[i][1],[390,1280][wi],["light","dark"][ti]));}catch(e){R.push({p:PAGES[i][0],err:String(e)});}
    document.title="running "+R.length;
  }
  try{localStorage.removeItem("pref-theme");}catch(e){}
  window.DONE=true; document.title="done"; document.getElementById("out").textContent=JSON.stringify(R);
})();
</script>"""


def stage_harness(pub):
    pages = [[n, p or T.open_page(pub)] for n, p in T.PAGES]
    out = os.path.join(pub, "_type_check.html")
    text = HARNESS.replace("__PAGES__", json.dumps(pages))
    text.encode("ascii")
    open(out, "w", encoding="ascii", newline="\n").write(text)
    print("wrote", out)


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 3 and a[0] == "compare":
        stage_compare(a[1], a[2])
    elif len(a) == 2 and a[0] == "harness":
        stage_harness(a[1])
    else:
        sys.exit(__doc__)
